#!/usr/bin/env bash
# Download the GHC and Hadrian bootstrap sources used by ghc-mirror.spec.
# Pass --patch-existing to retarget the current Hadrian source archive without
# downloading source files again.
#
# Source collection does not require a local GHC package database. The RPM
# spec patches the Hadrian plan using the compiler package database in its
# build environment. To patch the archive manually, use --patch-existing.

set -euo pipefail

GHC_VERSION="9.6.7"
GHC_SOURCE_URL="https://downloads.haskell.org/~ghc/${GHC_VERSION}/ghc-${GHC_VERSION}-src.tar.xz"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
GHC_SRC_TARBALL="${SCRIPT_DIR}/ghc-${GHC_VERSION}-src.tar.xz"
HADRIAN_BOOTSTRAP_TARBALL="${SCRIPT_DIR}/hadrian-bootstrap-sources.tar.gz"
GHCPKG_COMMAND="${GHC_PKG:-ghc-pkg}"

if [[ "${1:-}" == "--patch-existing" ]]; then
    if ! GHCPKG_PATH="$(command -v "${GHCPKG_COMMAND}")"; then
        echo "Cannot find ghc-pkg executable: ${GHCPKG_COMMAND}" >&2
        echo "Set GHC_PKG to the bootstrap compiler's ghc-pkg executable." >&2
        exit 1
    fi
    if [[ ! -f "${HADRIAN_BOOTSTRAP_TARBALL}" ]]; then
        echo "Missing ${HADRIAN_BOOTSTRAP_TARBALL}; run download-sources.sh first." >&2
        exit 1
    fi
    patch_args=(
        --ghc-pkg "${GHCPKG_PATH}"
        --patch-archive "${HADRIAN_BOOTSTRAP_TARBALL}"
    )
    if [[ -n "${GHC_PACKAGE_DB:-}" ]]; then
        patch_args+=(--ghc-package-db "${GHC_PACKAGE_DB}")
    fi
    python3 "${SCRIPT_DIR}/prepare-hadrian-bootstrap.py" "${patch_args[@]}"
    exit 0
elif [[ $# -gt 0 ]]; then
    echo "Usage: $0 [--patch-existing]" >&2
    exit 2
fi

WORK_DIR="$(mktemp -d)"
trap 'rm -rf "${WORK_DIR}"' EXIT

if [[ -f "${GHC_SRC_TARBALL}" ]]; then
    echo "  skip  $(basename "${GHC_SRC_TARBALL}")"
else
    echo "  get   $(basename "${GHC_SRC_TARBALL}")"
    curl -fsSL --retry 3 --retry-delay 2 \
        -o "${WORK_DIR}/ghc-${GHC_VERSION}-src.tar.xz" \
        "${GHC_SOURCE_URL}"
    mv "${WORK_DIR}/ghc-${GHC_VERSION}-src.tar.xz" "${GHC_SRC_TARBALL}"
fi

echo "  unpacking GHC source"
tar -xJf "${GHC_SRC_TARBALL}" -C "${WORK_DIR}"

echo "  preparing Hadrian bootstrap sources"
prepare_args=(
    --ghc-src-dir "${WORK_DIR}/ghc-${GHC_VERSION}"
)
prepare_args+=(--output "${WORK_DIR}/hadrian-bootstrap-sources.tar.gz")
python3 "${SCRIPT_DIR}/prepare-hadrian-bootstrap.py" "${prepare_args[@]}"
mv "${WORK_DIR}/hadrian-bootstrap-sources.tar.gz" \
    "${HADRIAN_BOOTSTRAP_TARBALL}"

echo "Done. Sources for ghc-mirror.spec:"
printf '  %s\n' "${GHC_SRC_TARBALL}" "${HADRIAN_BOOTSTRAP_TARBALL}"
printf '  %s\n' "${SCRIPT_DIR}/prepare-hadrian-bootstrap.py"
