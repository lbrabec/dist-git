%global bootstrap 1

%if %{bootstrap}
%global bootstrap_dist ~bootstrap
%else
%global bootstrap_dist %{nil}
%endif

Name:           ghc
Version:        9.6.7
Release:        1%{?dist}%{bootstrap_dist}
Summary:        The Glasgow Haskell Compiler

License:        BSD-3-Clause
URL:            https://www.haskell.org/ghc/
BuildArch:      x86_64 aarch64 ppc64le s390x

Source0:        https://downloads.haskell.org/~ghc/%{version}/ghc-%{version}-src.tar.xz
Source1:        hadrian-bootstrap-sources.tar.gz
Source2:        prepare-hadrian-bootstrap.py

BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  ncurses-devel
BuildRequires:  gmp
BuildRequires:  gmp-devel
BuildRequires:  libffi
BuildRequires:  zlib-devel
BuildRequires:  xz-devel
BuildRequires:  libffi-devel
BuildRequires:  perl
BuildRequires:  python3
BuildRequires:  tar
BuildRequires:  gzip
BuildRequires:  bzip2
BuildRequires:  patch
BuildRequires:  pkgconfig
BuildRequires:  findutils
BuildRequires:  diffutils
BuildRequires:  which
%if %{bootstrap}
# Initial bootstrap is from EPEL, where GHC 9.6 is shipped as ghc9.6
BuildRequires:  ghc9.6
BuildRequires:  ghc9.6-compiler-default
%else
# Later we self-bootstrap, our RPM is just ghc 
BuildRequires:  ghc
%endif

%global ghclibdir %{_libdir}/ghc-%{version}

%description
GHC is a state-of-the-art programming suite for Haskell.  This package
is built from upstream source.
%if %{bootstrap}
Bootstrapped with the installed GHC 9.6 compiler from the bootstrap mirror.
%else
Bootstrapped with the installed ghc package.
%endif

%prep
%setup -q -c -T -n ghc-%{version}

# Upstream GHC source (creates ./ghc-%{version}/).
tar -xJf %{SOURCE0}

# Hadrian bootstrap deps are vendored (built offline by download-sources.sh).
cp %{SOURCE1} hadrian-bootstrap-sources.tar.gz
# Match Hadrian's builtin package versions to the compiler available in this
# build environment (the download host may not have the bootstrap package DB).
if [ -n "${GHC_PACKAGE_DB:-}" ]; then
    python3 %{SOURCE2} \
        --ghc-pkg "${GHC_PKG:-$(command -v ghc-pkg)}" \
        --ghc-package-db "${GHC_PACKAGE_DB}" \
        --patch-archive hadrian-bootstrap-sources.tar.gz
else
    python3 %{SOURCE2} \
        --ghc-pkg "${GHC_PKG:-$(command -v ghc-pkg)}" \
        --patch-archive hadrian-bootstrap-sources.tar.gz
fi

%build
export LANG=C.UTF-8

cd ghc-%{version}

python3 hadrian/bootstrap/bootstrap.py \
    -w "$(command -v ghc)" \
    -s "../hadrian-bootstrap-sources.tar.gz"

./configure --prefix=%{_prefix} --libdir=%{_libdir}

_build/bin/hadrian \
    -j%{?__smp_build_ncpus:1} \
    --flavour=perf \
    binary-dist-dir \
    --docs=no-sphinx \
    --docs=no-haddocks

%install
export LANG=C.UTF-8
cd ghc-%{version}/_build/bindist/ghc-%{version}-*

./configure --prefix=%{buildroot}%{ghclibdir} \
    --bindir=%{buildroot}%{_bindir} \
    --libdir=%{buildroot}%{_libdir}
make install

# GHC bindist wrappers embed configure paths; strip $RPM_BUILD_ROOT.
sed -i -e "s|%{buildroot}||g" %{buildroot}%{_bindir}/*

%files
%{_bindir}/ghc
%{_bindir}/ghc-*
%{_bindir}/ghci
%{_bindir}/ghci-*
%{_bindir}/ghc-pkg
%{_bindir}/ghc-pkg-*
%{_bindir}/runghc
%{_bindir}/runghc-*
%{_bindir}/runhaskell
%{_bindir}/runhaskell-*
%{_bindir}/haddock
%{_bindir}/haddock-*
%{_bindir}/hp2ps
%{_bindir}/hp2ps-*
%{_bindir}/hpc
%{_bindir}/hpc-*
%{_bindir}/hsc2hs
%{_bindir}/hsc2hs-*
%{ghclibdir}/

%changelog
* Fri Sep 25 2026 Builder <builder@localhost> - 9.6.7-1
- Bootstrap from the GHC 9.6 mirror packages

