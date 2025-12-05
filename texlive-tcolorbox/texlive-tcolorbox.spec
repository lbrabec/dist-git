%global tl_version 2023

%{!?_texdir: %global _texdir %{_datadir}/texlive}

Name:           texlive-tcolorbox
Version:        6.8.0
Release:        1%{?dist}
Summary:        Coloured boxes, for LaTeX examples and theorems, etc.
License:        LPPL-1.3c
URL:            https://ctan.org/pkg/tcolorbox
BuildArch:      noarch

Source0:        http://ctan.math.illinois.edu/systems/texlive/tlnet/archive/tcolorbox.tar.xz
Source1:        http://ctan.math.illinois.edu/systems/texlive/tlnet/archive/tcolorbox.doc.tar.xz
Source2:        lppl1.3.txt

BuildRequires:  texlive-base
BuildRequires:  texlive-kpathsea

Requires:       texlive-base
Requires:       texlive-kpathsea
Requires:       tex(environ.sty)
Requires:       tex(pgf.sty)
Requires:       tex(tools.sty)

Provides:       tex(tcbbreakable.code.tex) = %{tl_version}
Provides:       tex(tcbdocumentation.code.tex) = %{tl_version}
Provides:       tex(tcbexternal.code.tex) = %{tl_version}
Provides:       tex(tcbfitting.code.tex) = %{tl_version}
Provides:       tex(tcbhooks.code.tex) = %{tl_version}
Provides:       tex(tcblistings.code.tex) = %{tl_version}
Provides:       tex(tcblistingscore.code.tex) = %{tl_version}
Provides:       tex(tcblistingsutf8.code.tex) = %{tl_version}
Provides:       tex(tcbmagazine.code.tex) = %{tl_version}
Provides:       tex(tcbminted.code.tex) = %{tl_version}
Provides:       tex(tcbposter.code.tex) = %{tl_version}
Provides:       tex(tcbprocessing.code.tex) = %{tl_version}
Provides:       tex(tcbraster.code.tex) = %{tl_version}
Provides:       tex(tcbskins.code.tex) = %{tl_version}
Provides:       tex(tcbskinsjigsaw.code.tex) = %{tl_version}
Provides:       tex(tcbtheorems.code.tex) = %{tl_version}
Provides:       tex(tcbvignette.code.tex) = %{tl_version}
Provides:       tex(tcbxparse.code.tex) = %{tl_version}
Provides:       tex(tcolorbox.sty) = %{tl_version}

%description
This package provides an environment for coloured and framed text boxes
with a heading line. Optionally, such a box may be split in an upper and
a lower part; thus the package may be used for the setting of LaTeX
examples where one part of the box displays the source code and the other
part shows the output. Another common use case is the setting of theorems.
The package supports saving and reuse of source code and text parts. The
package depends on the pgf, verbatim, environ, and etoolbox packages.

%prep
%setup -q -c -T
xz -dc %{SOURCE0} | tar x
xz -dc %{SOURCE1} | tar x
cp %{SOURCE2} .

%build
# Nothing to build

%install
mkdir -p %{buildroot}%{_texdir}/texmf-dist
cp -a tex %{buildroot}%{_texdir}/texmf-dist/
cp -a doc %{buildroot}%{_texdir}/texmf-dist/

%files
%license lppl1.3.txt
%{_texdir}/texmf-dist/tex/latex/tcolorbox
%doc %{_texdir}/texmf-dist/doc/latex/tcolorbox

%changelog
* Fri Dec 05 2025 Lukas Brabec <lbrabec@redhat.com> - 6.8.0-1
- Initial package for RHEL
