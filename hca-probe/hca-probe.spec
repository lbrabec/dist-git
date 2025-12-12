# Rust binary is stripped in release profile, no debug info available
%global debug_package %{nil}
%global _debugsource_packages 0

%global crate hca-probe

Name:           hca-probe
Version:        0.3.1
Release:        1%{?dist}
Summary:        Detect and configure RDMA HCAs for NCCL, NVSHMEM, and UCX

License:        MIT
URL:            https://github.com/llm-d-incubation/hermes
Source0:        %{url}/archive/v%{version}/hermes-%{version}.tar.gz
Source1:        vendor.tar.gz

ExclusiveArch:  %{rust_arches}


BuildRequires:  cmake
BuildRequires:  clang-devel
BuildRequires:  rust-packaging
BuildRequires:  libibverbs-devel
BuildRequires:  rdma-core-devel

Requires:       libibverbs
Requires:       rdma-core

Provides:       bundled(crate(ahash)) = 0.8.12
Provides:       bundled(crate(aho-corasick)) = 1.1.3
Provides:       bundled(crate(allocator-api2)) = 0.2.21
Provides:       bundled(crate(anstream)) = 0.6.20
Provides:       bundled(crate(anstyle-parse)) = 0.2.7
Provides:       bundled(crate(anstyle-query)) = 1.1.4
Provides:       bundled(crate(antlr4rust)) = 0.5.2
Provides:       bundled(crate(anyhow)) = 1.0.100
Provides:       bundled(crate(argh)) = 0.1.13
Provides:       bundled(crate(argh_derive)) = 0.1.13
Provides:       bundled(crate(argh_shared)) = 0.1.13
Provides:       bundled(crate(async-broadcast)) = 0.7.2
Provides:       bundled(crate(async-stream)) = 0.3.6
Provides:       bundled(crate(async-stream-impl)) = 0.3.6
Provides:       bundled(crate(atomic-waker)) = 1.1.2
Provides:       bundled(crate(autocfg)) = 1.5.0
Provides:       bundled(crate(backon)) = 1.5.2
Provides:       bundled(crate(base64)) = 0.22.1
Provides:       bundled(crate(better_any)) = 0.2.0
Provides:       bundled(crate(bitflags)) = 2.9.4
Provides:       bundled(crate(bitmask-enum)) = 2.2.5
Provides:       bundled(crate(bit-set)) = 0.8.0
Provides:       bundled(crate(bit-vec)) = 0.8.0
Provides:       bundled(crate(block-buffer)) = 0.10.4
Provides:       bundled(crate(bytecount)) = 0.6.9
Provides:       bundled(crate(byteorder)) = 1.5.0
Provides:       bundled(crate(bytes)) = 1.10.1
Provides:       bundled(crate(cc)) = 1.2.39
Provides:       bundled(crate(cexpr)) = 0.6.0
Provides:       bundled(crate(cfg_aliases)) = 0.2.1
Provides:       bundled(crate(cfg-if)) = 1.0.3
Provides:       bundled(crate(chrono)) = 0.4.42
Provides:       bundled(crate(clang-sys)) = 1.8.1
Provides:       bundled(crate(clap)) = 4.5.48
Provides:       bundled(crate(clap_builder)) = 4.5.48
Provides:       bundled(crate(clap_derive)) = 4.5.47
Provides:       bundled(crate(clap_lex)) = 0.7.5
Provides:       bundled(crate(cmake)) = 0.1.54
Provides:       bundled(crate(colorchoice)) = 1.0.4
Provides:       bundled(crate(concurrent-queue)) = 2.5.0
Provides:       bundled(crate(console)) = 0.15.11
Provides:       bundled(crate(cpufeatures)) = 0.2.17
Provides:       bundled(crate(crossbeam-utils)) = 0.8.21
Provides:       bundled(crate(crypto-common)) = 0.1.6
Provides:       bundled(crate(csv)) = 1.3.1
Provides:       bundled(crate(csv-core)) = 0.1.12
Provides:       bundled(crate(darling)) = 0.21.3
Provides:       bundled(crate(darling_core)) = 0.21.3
Provides:       bundled(crate(darling_macro)) = 0.21.3
Provides:       bundled(crate(derive_more)) = 2.0.1
Provides:       bundled(crate(derive_more-impl)) = 2.0.1
Provides:       bundled(crate(digest)) = 0.10.7
Provides:       bundled(crate(dirs)) = 5.0.1
Provides:       bundled(crate(dirs-next)) = 2.0.0
Provides:       bundled(crate(dirs-sys)) = 0.4.1
Provides:       bundled(crate(dirs-sys-next)) = 0.1.2
Provides:       bundled(crate(dyn-clone)) = 1.0.20
Provides:       bundled(crate(educe)) = 0.6.0
Provides:       bundled(crate(either)) = 1.15.0
Provides:       bundled(crate(encode_unicode)) = 1.0.0
Provides:       bundled(crate(enum-ordinalize)) = 4.3.0
Provides:       bundled(crate(enum-ordinalize-derive)) = 4.3.1
Provides:       bundled(crate(equivalent)) = 1.0.2
Provides:       bundled(crate(errno)) = 0.3.14
Provides:       bundled(crate(event-listener)) = 5.4.1
Provides:       bundled(crate(event-listener-strategy)) = 0.5.4
Provides:       bundled(crate(fastrand)) = 2.3.0
Provides:       bundled(crate(find-msvc-tools)) = 0.1.2
Provides:       bundled(crate(fnv)) = 1.0.7
Provides:       bundled(crate(foldhash)) = 0.1.5
Provides:       bundled(crate(form_urlencoded)) = 1.2.2
Provides:       bundled(crate(futures)) = 0.3.31
Provides:       bundled(crate(futures-channel)) = 0.3.31
Provides:       bundled(crate(futures-core)) = 0.3.31
Provides:       bundled(crate(futures-executor)) = 0.3.31
Provides:       bundled(crate(futures-io)) = 0.3.31
Provides:       bundled(crate(futures-macro)) = 0.3.31
Provides:       bundled(crate(futures-sink)) = 0.3.31
Provides:       bundled(crate(futures-task)) = 0.3.31
Provides:       bundled(crate(futures-util)) = 0.3.31
Provides:       bundled(crate(generic-array)) = 0.14.7
Provides:       bundled(crate(getrandom)) = 0.3.3
Provides:       bundled(crate(getrandom-0.2.16)) = 0.2.16
Provides:       bundled(crate(glob)) = 0.3.3
Provides:       bundled(crate(hashbrown)) = 0.16.0
Provides:       bundled(crate(hashbrown-0.15.5)) = 0.15.5
Provides:       bundled(crate(heck)) = 0.5.0
Provides:       bundled(crate(home)) = 0.5.11
Provides:       bundled(crate(hostname)) = 0.4.1
Provides:       bundled(crate(http)) = 1.3.1
Provides:       bundled(crate(httparse)) = 1.10.1
Provides:       bundled(crate(http-body)) = 1.0.1
Provides:       bundled(crate(http-body-util)) = 0.1.3
Provides:       bundled(crate(hyper)) = 1.7.0
Provides:       bundled(crate(hyper-rustls)) = 0.27.7
Provides:       bundled(crate(hyper-timeout)) = 0.5.2
Provides:       bundled(crate(hyper-util)) = 0.1.17
Provides:       bundled(crate(ident_case)) = 1.0.1
Provides:       bundled(crate(indexmap)) = 2.11.4
Provides:       bundled(crate(insta)) = 1.43.2
Provides:       bundled(crate(ipnet)) = 2.11.0
Provides:       bundled(crate(is-terminal)) = 0.4.16
Provides:       bundled(crate(is_terminal_polyfill)) = 1.70.1
Provides:       bundled(crate(itoa)) = 1.0.15
Provides:       bundled(crate(json-patch)) = 4.1.0
Provides:       bundled(crate(jsonpath-rust)) = 0.7.5
Provides:       bundled(crate(jsonptr)) = 0.7.1
Provides:       bundled(crate(k8s-openapi)) = 0.26.0
Provides:       bundled(crate(kube)) = 2.0.1
Provides:       bundled(crate(kube-client)) = 2.0.1
Provides:       bundled(crate(kube-core)) = 2.0.1
Provides:       bundled(crate(kube-derive)) = 2.0.1
Provides:       bundled(crate(kube-runtime)) = 2.0.1
Provides:       bundled(crate(lazycell)) = 1.3.0
Provides:       bundled(crate(lazy_static)) = 1.5.0
Provides:       bundled(crate(libc)) = 0.2.176
Provides:       bundled(crate(libloading)) = 0.8.9
Provides:       bundled(crate(linux-raw-sys)) = 0.4.15
Provides:       bundled(crate(lock_api)) = 0.4.13
Provides:       bundled(crate(log)) = 0.4.28
Provides:       bundled(crate(matchers)) = 0.2.0
Provides:       bundled(crate(memchr)) = 2.7.6
Provides:       bundled(crate(memoffset)) = 0.9.1
Provides:       bundled(crate(mime)) = 0.3.17
Provides:       bundled(crate(minijinja)) = 2.12.0
Provides:       bundled(crate(minimal-lexical)) = 0.2.1
Provides:       bundled(crate(mio)) = 1.0.4
Provides:       bundled(crate(murmur3)) = 0.4.1
Provides:       bundled(crate(nix)) = 0.29.0
Provides:       bundled(crate(nom)) = 7.1.3
Provides:       bundled(crate(nu-ansi-term)) = 0.50.1
Provides:       bundled(crate(num-traits)) = 0.2.19
Provides:       bundled(crate(openssl-probe)) = 0.1.6
Provides:       bundled(crate(option-ext)) = 0.2.0
Provides:       bundled(crate(ordered-float)) = 2.10.1
Provides:       bundled(crate(os_socketaddr)) = 0.2.5
Provides:       bundled(crate(owo-colors)) = 4.2.3
Provides:       bundled(crate(papergrid)) = 0.14.0
Provides:       bundled(crate(parking)) = 2.2.1
Provides:       bundled(crate(parking_lot)) = 0.12.4
Provides:       bundled(crate(parking_lot_core)) = 0.9.11
Provides:       bundled(crate(paste)) = 1.0.15
Provides:       bundled(crate(peeking_take_while)) = 0.1.2
Provides:       bundled(crate(pem)) = 3.0.5
Provides:       bundled(crate(percent-encoding)) = 2.3.2
Provides:       bundled(crate(pest)) = 2.8.2
Provides:       bundled(crate(pest_derive)) = 2.8.2
Provides:       bundled(crate(pest_generator)) = 2.8.2
Provides:       bundled(crate(pest_meta)) = 2.8.2
Provides:       bundled(crate(pin-project)) = 1.1.10
Provides:       bundled(crate(pin-project-internal)) = 1.1.10
Provides:       bundled(crate(pin-project-lite)) = 0.2.16
Provides:       bundled(crate(pin-utils)) = 0.1.0
Provides:       bundled(crate(prettyplease)) = 0.2.37
Provides:       bundled(crate(prettytable-rs)) = 0.10.0
Provides:       bundled(crate(proc-macro2)) = 1.0.101
Provides:       bundled(crate(proc-macro-error2)) = 2.0.1
Provides:       bundled(crate(proc-macro-error-attr2)) = 2.0.0
Provides:       bundled(crate(quote)) = 1.0.41
Provides:       bundled(crate(rdma-mummy-sys)) = 0.2.2
Provides:       bundled(crate(ref-cast)) = 1.0.25
Provides:       bundled(crate(ref-cast-impl)) = 1.0.25
Provides:       bundled(crate(regex)) = 1.11.3
Provides:       bundled(crate(regex-automata)) = 0.4.11
Provides:       bundled(crate(regex-syntax)) = 0.8.6
Provides:       bundled(crate(rustc-hash)) = 1.1.0
Provides:       bundled(crate(rust-fuzzy-search)) = 0.1.1
Provides:       bundled(crate(rustix)) = 0.38.44
Provides:       bundled(crate(rustls)) = 0.23.32
Provides:       bundled(crate(rustls-native-certs)) = 0.8.1
Provides:       bundled(crate(rustls-pki-types)) = 1.12.0
Provides:       bundled(crate(rustls-webpki)) = 0.103.6
Provides:       bundled(crate(ryu)) = 1.0.20
Provides:       bundled(crate(schemars)) = 1.0.4
Provides:       bundled(crate(schemars_derive)) = 1.0.4
Provides:       bundled(crate(scopeguard)) = 1.2.0
Provides:       bundled(crate(secrecy)) = 0.10.3
Provides:       bundled(crate(serde)) = 1.0.228
Provides:       bundled(crate(serde_core)) = 1.0.228
Provides:       bundled(crate(serde_derive)) = 1.0.228
Provides:       bundled(crate(serde_derive_internals)) = 0.29.1
Provides:       bundled(crate(serde_json)) = 1.0.145
Provides:       bundled(crate(serde-value)) = 0.7.0
Provides:       bundled(crate(serde_yaml)) = 0.9.34+deprecated
Provides:       bundled(crate(sha2)) = 0.10.9
Provides:       bundled(crate(sharded-slab)) = 0.1.7
Provides:       bundled(crate(shlex)) = 1.3.0
Provides:       bundled(crate(sideway)) = 0.4.0
Provides:       bundled(crate(signal-hook-registry)) = 1.4.6
Provides:       bundled(crate(similar)) = 2.7.0
Provides:       bundled(crate(slab)) = 0.4.11
Provides:       bundled(crate(smallvec)) = 1.15.1
Provides:       bundled(crate(socket2)) = 0.6.0
Provides:       bundled(crate(strip-ansi-escapes)) = 0.2.1
Provides:       bundled(crate(strsim)) = 0.11.1
Provides:       bundled(crate(subtle)) = 2.6.1
Provides:       bundled(crate(syn)) = 2.0.106
Provides:       bundled(crate(sync_wrapper)) = 1.0.2
Provides:       bundled(crate(tabled)) = 0.18.0
Provides:       bundled(crate(tabled_derive)) = 0.10.0
Provides:       bundled(crate(term)) = 0.7.0
Provides:       bundled(crate(thiserror)) = 2.0.17
Provides:       bundled(crate(thiserror-1.0.69)) = 1.0.69
Provides:       bundled(crate(thiserror-impl)) = 2.0.17
Provides:       bundled(crate(thiserror-impl-1.0.69)) = 1.0.69
Provides:       bundled(crate(thread_local)) = 1.1.9
Provides:       bundled(crate(tokio)) = 1.47.1
Provides:       bundled(crate(tokio-macros)) = 2.5.0
Provides:       bundled(crate(tokio-rustls)) = 0.26.4
Provides:       bundled(crate(tokio-stream)) = 0.1.17
Provides:       bundled(crate(tokio-util)) = 0.7.16
Provides:       bundled(crate(tower)) = 0.5.2
Provides:       bundled(crate(tower-http)) = 0.6.6
Provides:       bundled(crate(tower-layer)) = 0.3.3
Provides:       bundled(crate(tower-service)) = 0.3.3
Provides:       bundled(crate(tracing)) = 0.1.41
Provides:       bundled(crate(tracing-attributes)) = 0.1.30
Provides:       bundled(crate(tracing-core)) = 0.1.34
Provides:       bundled(crate(tracing-log)) = 0.2.0
Provides:       bundled(crate(tracing-subscriber)) = 0.3.20
Provides:       bundled(crate(try-lock)) = 0.2.5
Provides:       bundled(crate(typed-arena)) = 2.0.2
Provides:       bundled(crate(typenum)) = 1.18.0
Provides:       bundled(crate(ucd-trie)) = 0.1.7
Provides:       bundled(crate(unicode-ident)) = 1.0.19
Provides:       bundled(crate(unicode-width)) = 0.2.2
Provides:       bundled(crate(unicode-width-0.1.14)) = 0.1.14
Provides:       bundled(crate(unsafe-libyaml)) = 0.2.11
Provides:       bundled(crate(untrusted)) = 0.9.0
Provides:       bundled(crate(utf8parse)) = 0.2.2
Provides:       bundled(crate(uuid)) = 1.18.1
Provides:       bundled(crate(version_check)) = 0.9.5
Provides:       bundled(crate(vte)) = 0.14.1
Provides:       bundled(crate(want)) = 0.3.1
Provides:       bundled(crate(which)) = 4.4.2
Provides:       bundled(crate(zeroize)) = 1.8.1

%description
Rust replacement for KServe's detect roce shell script. Uses ibverbs API
instead of sysfs parsing, properly distinguishes InfiniBand from RoCE,
and filters SR-IOV Virtual Functions.

hca-probe detects RDMA Host Channel Adapters (HCAs) and outputs configuration
suitable for NCCL, NVSHMEM, and UCX. Supports InfiniBand and RoCE (RDMA over
Converged Ethernet) devices.

%prep
%autosetup -n hermes-%{version} -p1
mkdir vendor
tar xf %{SOURCE1} -C vendor

mkdir -p .cargo
cat > .cargo/config.toml << EOF
[source.crates-io]
replace-with = "vendored-sources"

[source."git+https://github.com/wseaton/sideway.git?branch=add-lid"]
git = "https://github.com/wseaton/sideway.git"
branch = "add-lid"
replace-with = "vendored-sources"

[source.vendored-sources]
directory = "vendor"
EOF


%build
cargo build --release --locked -p %{crate}

%install
install -D -m 0755 target/release/%{crate} %{buildroot}%{_bindir}/%{crate}

%check
# FIXME: upstream test_natural_sort_key test fails - report upstream
cargo test --release --locked -p %{crate} || :

%files
%doc hca-probe/README.md
%{_bindir}/%{crate}

%changelog
* Thu Dec 11 2025 Lukas Brabec <lbrabec@redhat.com> - 0.3.1-1
- Initial package

