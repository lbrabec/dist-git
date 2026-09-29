#!/usr/bin/env python3
"""Create hadrian-bootstrap-sources.tar.gz from a GHC source tree.

Run from download-sources.sh when preparing SRPM sources (network allowed).
The generated archive keeps Hadrian's upstream plan by default; the RPM spec
patches builtin versions against the compiler package database in the build
environment. The RPM build does not download Hackage dependencies.

Patches builtin package versions in the bootstrap plan to match the
bootstrap compiler's package DB (needed when bootstrapping from EPEL).
"""

from __future__ import annotations

import argparse
import io
import json
import os
import re
import subprocess
import tarfile
import tempfile
import time
from http.client import HTTPException
from typing import Optional
from urllib.error import URLError
from urllib.request import urlretrieve

HACKAGE_PACKAGE_URL = "https://hackage.haskell.org/package"


def download_file(url: str, dest: str) -> None:
    attempts = 3
    temp_dest = f"{dest}.part"

    for attempt in range(1, attempts + 1):
        try:
            urlretrieve(url, temp_dest)
        except (HTTPException, OSError, URLError) as error:
            try:
                os.unlink(temp_dest)
            except FileNotFoundError:
                pass

            if attempt == attempts:
                raise

            delay = 2 ** (attempt - 1)
            print(
                f"  Download failed ({error}); retrying in {delay}s "
                f"(attempt {attempt}/{attempts})",
                flush=True,
            )
            time.sleep(delay)
        else:
            os.replace(temp_dest, dest)
            return


def get_installed_versions(
    ghc_pkg: str, ghc_package_db: Optional[str] = None
) -> dict[str, str]:
    command = [ghc_pkg]
    if ghc_package_db:
        command.extend(["--global-package-db", ghc_package_db])
    command.extend(["list", "--simple-output"])
    output = subprocess.check_output(command, text=True)
    versions: dict[str, str] = {}
    for entry in output.split():
        match = re.match(r"^(.+)-(\d[\d.]*)$", entry)
        if match:
            versions[match.group(1)] = match.group(2)
    return versions


def patch_plan(plan: dict, ghc_pkg: str, ghc_package_db: Optional[str]) -> int:
    installed = get_installed_versions(ghc_pkg, ghc_package_db)
    patched = 0
    missing: list[str] = []
    for entry in plan.get("builtin", []):
        pkg = entry["package"]
        plan_ver = entry["version"]
        actual_ver = installed.get(pkg)
        if actual_ver is None:
            missing.append(pkg)
        elif actual_ver != plan_ver:
            print(f"  Patching builtin {pkg}: {plan_ver} -> {actual_ver}")
            entry["version"] = actual_ver
            patched += 1

    if missing:
        raise SystemExit(
            "Selected compiler package database is missing Hadrian builtin "
            "package(s): "
            + ", ".join(missing)
            + ". Check that GHC_PKG and GHC_PACKAGE_DB select the compiler "
            "package database used for the build."
        )

    return patched


def patch_builtin_versions(
    plan_path: str, ghc_pkg: str, ghc_package_db: Optional[str] = None
) -> int:
    with open(plan_path) as f:
        plan = json.load(f)

    patched = patch_plan(plan, ghc_pkg, ghc_package_db)

    with open(plan_path, "w") as f:
        json.dump(plan, f, indent=2)

    return patched


def patch_bootstrap_archive(
    archive_path: str, ghc_pkg: str, ghc_package_db: Optional[str] = None
) -> int:
    archive_dir = os.path.dirname(os.path.abspath(archive_path))
    archive_mode = os.stat(archive_path).st_mode & 0o7777
    fd, tmp_archive = tempfile.mkstemp(
        prefix=".hadrian-bootstrap-", suffix=".tar.gz", dir=archive_dir
    )
    os.close(fd)

    try:
        with tarfile.open(archive_path, "r:gz") as src:
            members = src.getmembers()
            plan_member = next(
                (member for member in members if member.name.rsplit("/", 1)[-1] == "plan-bootstrap.json"),
                None,
            )
            if plan_member is None:
                raise SystemExit(
                    f"Hadrian bootstrap archive has no plan-bootstrap.json: {archive_path}"
                )

            plan_stream = src.extractfile(plan_member)
            if plan_stream is None:
                raise SystemExit("Cannot read plan-bootstrap.json from archive")
            with plan_stream:
                plan = json.load(plan_stream)

            patched = patch_plan(plan, ghc_pkg, ghc_package_db)
            plan_data = (json.dumps(plan, indent=2) + "\n").encode()
            with tarfile.open(tmp_archive, "w:gz") as dst:
                for member in members:
                    if member.name == plan_member.name:
                        member.size = len(plan_data)
                        dst.addfile(member, io.BytesIO(plan_data))
                    else:
                        dst.addfile(
                            member,
                            src.extractfile(member) if member.isfile() else None,
                        )

        os.chmod(tmp_archive, archive_mode)
        os.replace(tmp_archive, archive_path)
        print(f"Patched {patched} builtin version(s) in {archive_path}")
        return patched
    finally:
        if os.path.exists(tmp_archive):
            os.unlink(tmp_archive)


def download_hackage_deps(plan_path: str, output_dir: str) -> None:
    with open(plan_path) as f:
        data = json.load(f)

    os.makedirs(output_dir, exist_ok=True)

    for dep in data.get("dependencies", []):
        name = dep["package"]
        version = dep["version"]

        if name == "hadrian":
            continue

        tarball = f"{name}-{version}.tar.gz"
        url = f"{HACKAGE_PACKAGE_URL}/{name}-{version}/{tarball}"
        dest = os.path.join(output_dir, tarball)

        if os.path.exists(dest):
            print(f"  Skipping {tarball}")
            continue

        print(f"  Downloading {tarball}")
        download_file(url, dest)

        revision = dep.get("revision")
        if revision is not None:
            cabal_url = (
                f"{HACKAGE_PACKAGE_URL}/{name}-{version}/revision/{revision}.cabal"
            )
            cabal_dest = os.path.join(output_dir, f"{name}.cabal")
            print(f"  Downloading {name}.cabal (revision {revision})")
            download_file(cabal_url, cabal_dest)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ghc-src-dir")
    parser.add_argument(
        "--ghc-pkg",
        help="patch builtin versions using this bootstrap compiler's ghc-pkg",
    )
    parser.add_argument("--ghc-package-db")
    parser.add_argument("--plan", default="hadrian/bootstrap/plan-bootstrap-9_6_6.json")
    parser.add_argument("--output")
    parser.add_argument(
        "--patch-archive",
        help="retarget an existing Hadrian source archive to this GHC package database",
    )
    args = parser.parse_args()

    if args.patch_archive:
        if args.ghc_src_dir or args.output:
            parser.error("--patch-archive cannot be combined with source generation")
        if not args.ghc_pkg:
            parser.error("--patch-archive requires --ghc-pkg")
        patch_bootstrap_archive(
            args.patch_archive, args.ghc_pkg, args.ghc_package_db
        )
        return

    if not args.ghc_src_dir or not args.output:
        parser.error("--ghc-src-dir and --output are required for source generation")

    plan_path = os.path.join(args.ghc_src_dir, args.plan)
    if not os.path.isfile(plan_path):
        raise SystemExit(f"Hadrian plan not found: {plan_path}")

    with tempfile.TemporaryDirectory() as tmpdir:
        deps_dir = os.path.join(tmpdir, "bootstrap-sources")
        plan_copy = os.path.join(deps_dir, "plan-bootstrap.json")
        os.makedirs(deps_dir, exist_ok=True)
        with open(plan_path) as src, open(plan_copy, "w") as dst:
            dst.write(src.read())

        if args.ghc_pkg:
            print("Patching hadrian bootstrap plan for bootstrap GHC")
            patched = patch_builtin_versions(
                plan_copy, args.ghc_pkg, args.ghc_package_db
            )
            print(f"Patched {patched} builtin version(s)")
        else:
            print("Using upstream Hadrian bootstrap plan")

        download_hackage_deps(plan_path, deps_dir)

        with tarfile.open(args.output, "w:gz") as tar:
            for item in os.listdir(deps_dir):
                tar.add(os.path.join(deps_dir, item), arcname=item)

    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
