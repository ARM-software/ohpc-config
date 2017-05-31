#
# spec file for package 
#
# Copyright (c) 2014 SUSE LINUX Products GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.opensuse.org/
#


%define texlive_version 3.72

%define __perl_requires		%{nil}
%define __os_install_post	/usr/lib/rpm/brp-compress \\\
  %(ls /usr/lib/rpm/brp-suse.d/* 2> /dev/null | grep -vE 'check-la|boot-scripts|rpath|symlink|desktop|strip-debug|gcc-output|debuginfo|libtool|kernel-log') %{nil}

Name: texlive-tcolorbox
Version: %{texlive_version}
Release: %{?rlobs:%{rlobs}}%{!?rlobs:0}
License: LPPL-1.0
Summary: Coloured boxes, for LaTeX examples and theorems, etcetera
Group: Productivity/Publishing/TeX/Base
Url: http://www.tug.org/texlive/
Requires(pre): texlive >= %{texlive_version}
Requires(post): coreutils
Requires(postun): coreutils
Requires(postun): texlive >= %{texlive_version}
Requires(posttrans): texlive >= %{texlive_version}
#Recommends: texlive-tcolorbox-doc >= %{texlive_version}
BuildRequires: ed
#BuildRequires: texlive-filesystem
BuildRequires: xz
Provides: tex(tcbbreakable.code.tex)
Provides: tex(tcbdocumentation.code.tex)
Provides: tex(tcbhooks.code.tex)
Provides: tex(tcblistings.code.tex)
Provides: tex(tcblistingsutf8.code.tex)
Provides: tex(tcbskins.code.tex)
Provides: tex(tcbtheorems.code.tex)
Provides: tex(tcolorbox.sty)
Requires: tex(pgf.sty)
Requires: tex(verbatim.sty)
# Download at ftp://ftp.ctan.org/pub/tex/systems/texlive/tlnet/archive/
# from 20130620
Source0: tcolorbox.tar.xz
Source1: tcolorbox.doc.tar.xz
BuildArch: noarch
# skip-check-libtool-deps

%global _varlib		%{_localstatedir}/lib
%global _libexecdir	%{_prefix}/lib

%define _texmfdistdir	%{_datadir}/texmf
%define _texmfmaindir	%{_libexecdir}/texmf
%define _texmfdirs	\{%{_texmfdistdir},%{_texmfmaindir}\}

%define _texmfconfdir	%{_sysconfdir}/texmf
%define _texmfvardir	%{_varlib}/texmf
%define _texmfcache	%{_localstatedir}/cache/texmf
%define _fontcache	%{_texmfcache}/fonts
#
%define _x11bin		%{_prefix}/bin
%define _x11lib		%{_libdir}
%define _x11data	%{_datadir}/X11
%define _x11inc		%{_includedir}
%define _appdefdir	%{_x11data}/app-defaults


%description
The package provides an environment for coloured and framed
text boxes with a heading line. Optionally, such a box can be
split in an upper and a lower part; thus the package may be
used for the setting of LaTeX examples where one part of the
box displays the source code and the other part shows the
output. Another common use case is the setting of theorems. The
package supports saving and reuse of source code and text
parts.

date: 2013-05-16 17:39:08 +0000


%package doc
Summary: Documentation for texlive-tcolorbox
Version: %{texlive_version}
Release: %{?rlobs:%{rlobs}}%{!?rlobs:0}
Provides: locale(texlive-tcolorbox-doc:en)

%description doc
This package includes the documentation for texlive-tcolorbox

%prep
%setup -q -c -T

%build

%install
    rm -rf %{buildroot}
    mkdir -p %{buildroot}%{_texmfdistdir}
    mkdir -p %{buildroot}%{_texmfmaindir}
    mkdir -p %{buildroot}%{_datadir}/texlive
    mkdir -p %{buildroot}/var/adm/update-scripts
    ln -sf ../../share/texmf %{buildroot}%{_datadir}/texlive/texmf-dist
    ln -sf ../../lib/texmf   %{buildroot}%{_datadir}/texlive/texmf
    ln -sf %{_texmfdistdir}/texconfig/zypper.py \
	%{buildroot}/var/adm/update-scripts/%{name}-%{version}-%{release}-zypper
    tar --use-compress-program=xz -xf %{S:0} -C %{buildroot}%{_datadir}/texlive/texmf-dist
    tar --use-compress-program=xz -xf %{S:1} -C %{buildroot}%{_datadir}/texlive/texmf-dist
    rm -v  %{buildroot}%{_datadir}/texlive/texmf
    rm -v  %{buildroot}%{_datadir}/texlive/texmf-dist
    rm -vr %{buildroot}%{_datadir}/texlive
    # Remove this
    rm -vrf %{buildroot}%{_texmfdistdir}/tlpkg/tlpobj
    rm -vrf %{buildroot}%{_texmfmaindir}/tlpkg/tlpobj

%clean
rm -rf %{buildroot}

%post
mkdir -p /var/run/texlive
> /var/run/texlive/run-mktexlsr
> /var/run/texlive/run-update

%postun
if test $1 = 0; then
    %{_bindir}/mktexlsr 2> /dev/null || :
    exit 0
fi
mkdir -p /var/run/texlive
> /var/run/texlive/run-mktexlsr
> /var/run/texlive/run-update

%posttrans
test -f /var/run/texlive/run-update || exit 0
test -z "$ZYPP_IS_RUNNING" || exit 0
VERBOSE=false %{_texmfdistdir}/texconfig/update || :
rm -f /var/run/texlive/run-update

%files doc
%defattr(-,root,root,755)
%{_texmfdistdir}/doc/latex/tcolorbox/Basilica_5.png
%{_texmfdistdir}/doc/latex/tcolorbox/CHANGES
%{_texmfdistdir}/doc/latex/tcolorbox/README
%{_texmfdistdir}/doc/latex/tcolorbox/tcolorbox-example.pdf
%{_texmfdistdir}/doc/latex/tcolorbox/tcolorbox-example.tex
%{_texmfdistdir}/doc/latex/tcolorbox/tcolorbox.doc.abstract.tex
%{_texmfdistdir}/doc/latex/tcolorbox/tcolorbox.doc.bib
%{_texmfdistdir}/doc/latex/tcolorbox/tcolorbox.doc.breakable.tex
%{_texmfdistdir}/doc/latex/tcolorbox/tcolorbox.doc.coremacros.tex
%{_texmfdistdir}/doc/latex/tcolorbox/tcolorbox.doc.coreoptions.tex
%{_texmfdistdir}/doc/latex/tcolorbox/tcolorbox.doc.documentation.tex
%{_texmfdistdir}/doc/latex/tcolorbox/tcolorbox.doc.hooks.tex
%{_texmfdistdir}/doc/latex/tcolorbox/tcolorbox.doc.index.tex
%{_texmfdistdir}/doc/latex/tcolorbox/tcolorbox.doc.intro.tex
%{_texmfdistdir}/doc/latex/tcolorbox/tcolorbox.doc.listings.tex
%{_texmfdistdir}/doc/latex/tcolorbox/tcolorbox.doc.references.tex
%{_texmfdistdir}/doc/latex/tcolorbox/tcolorbox.doc.skins.tex
%{_texmfdistdir}/doc/latex/tcolorbox/tcolorbox.doc.theorems.tex
%{_texmfdistdir}/doc/latex/tcolorbox/tcolorbox.doc.verbatim.tex
%{_texmfdistdir}/doc/latex/tcolorbox/tcolorbox.pdf
%{_texmfdistdir}/doc/latex/tcolorbox/tcolorbox.tex
%{_texmfdistdir}/doc/latex/tcolorbox/lichtspiel.jpg
%{_texmfdistdir}/doc/latex/tcolorbox/tcolorbox.doc.external.tex
%{_texmfdistdir}/doc/latex/tcolorbox/tcolorbox.doc.filling.tex
%{_texmfdistdir}/doc/latex/tcolorbox/tcolorbox.doc.fitting.tex
%{_texmfdistdir}/doc/latex/tcolorbox/tcolorbox.doc.graphics.tex
%{_texmfdistdir}/doc/latex/tcolorbox/tcolorbox.doc.initoptions.tex
%{_texmfdistdir}/doc/latex/tcolorbox/tcolorbox.doc.magazine.tex
%{_texmfdistdir}/doc/latex/tcolorbox/tcolorbox.doc.picturecredits.tex
%{_texmfdistdir}/doc/latex/tcolorbox/tcolorbox.doc.quickref.tex
%{_texmfdistdir}/doc/latex/tcolorbox/tcolorbox.doc.raster.tex
%{_texmfdistdir}/doc/latex/tcolorbox/tcolorbox.doc.recording.tex
%{_texmfdistdir}/doc/latex/tcolorbox/tcolorbox.doc.s_main.sty
%{_texmfdistdir}/doc/latex/tcolorbox/tcolorbox.doc.s_snippet.sty
%{_texmfdistdir}/doc/latex/tcolorbox/tcolorbox.doc.technical.tex
%{_texmfdistdir}/doc/latex/tcolorbox/tcolorbox.doc.xparse.tex

%files
%defattr(-,root,root,755)
%{_texmfdistdir}/tex/latex/tcolorbox/tcbbreakable.code.tex
%{_texmfdistdir}/tex/latex/tcolorbox/tcbdocumentation.code.tex
%{_texmfdistdir}/tex/latex/tcolorbox/tcbhooks.code.tex
%{_texmfdistdir}/tex/latex/tcolorbox/tcblistings.code.tex
%{_texmfdistdir}/tex/latex/tcolorbox/tcblistingsutf8.code.tex
%{_texmfdistdir}/tex/latex/tcolorbox/tcbskins.code.tex
%{_texmfdistdir}/tex/latex/tcolorbox/tcbtheorems.code.tex
%{_texmfdistdir}/tex/latex/tcolorbox/tcolorbox.sty
%{_texmfdistdir}/tex/latex/tcolorbox/blueshade.png
%{_texmfdistdir}/tex/latex/tcolorbox/crinklepaper.png
%{_texmfdistdir}/tex/latex/tcolorbox/goldshade.png
%{_texmfdistdir}/tex/latex/tcolorbox/pink_marble.png
%{_texmfdistdir}/tex/latex/tcolorbox/tcbexternal.code.tex
%{_texmfdistdir}/tex/latex/tcolorbox/tcbfitting.code.tex
%{_texmfdistdir}/tex/latex/tcolorbox/tcblistingscore.code.tex
%{_texmfdistdir}/tex/latex/tcolorbox/tcbmagazine.code.tex
%{_texmfdistdir}/tex/latex/tcolorbox/tcbminted.code.tex
%{_texmfdistdir}/tex/latex/tcolorbox/tcbraster.code.tex
%{_texmfdistdir}/tex/latex/tcolorbox/tcbskinsjigsaw.code.tex
%{_texmfdistdir}/tex/latex/tcolorbox/tcbxparse.code.tex
/var/adm/update-scripts/%{name}-%{version}-%{release}-zypper

%changelog
* Tue May 20 2014 schwab@suse.de
- Make sure texconfig/update is run only once per transaction

* Wed Apr 09 2014 werner@suse.de
- Be aware that blanks may occure around RequirePackage (bnc#872559) 

* Fri Mar 21 2014 werner@suse.de
- Remove superfluous xfs dependcies

* Mon Oct 28 2013 werner@suse.de
- Make Lua(La)TeX knowing about varfonts from mktex.cnf (bnc#847102) 

* Wed Sep 25 2013 werner@suse.de
- Be aware that texlive scripts are now in the packages them self 

* Tue Sep 10 2013 werner@suse.de
- Change /bin/env to /usr/bin/env in latexdiff tool below doc 

* Fri Aug 09 2013 werner@suse.de
- Be aware that the package texlive-ascii-font is the former
  texlive-ascii

* Thu Aug 08 2013 werner@suse.de
- Do not override TEXMFLOCAL with TEXMFMAIN as this is now TEXMFDIST 

* Wed Aug 07 2013 werner@suse.de
- Drop dependency freeglut-devel of texlive-asymptote (bnc#833498)

* Mon Aug 05 2013 werner@suse.de
- Make sure that TEXMFMAIN is /usr/share/texmf now 
- Replace texmf.cnf if really required that is do not install
  as .rpmnew but move the old to .rpmold

* Fri Aug 02 2013 werner@suse.de
- Move leipzig.tex from doc/latex/leipzig/leipzig.tex to 
  tex/latex/leipzig/leipzig.tex

* Tue Jul 30 2013 werner@suse.de
- Update to TeXLive 2013 (timestamp 20130620)
  + Distribution layout: the top-level texmf/ directory has been
    merged into texmf-dist/, for simplicity. Both the TEXMFMAIN
    and TEXMFDIST Kpathsea variables now point to texmf-dist.
  + Many small language collections have been merged together,
    to simplify installation.
  + MetaPost: native support for PNG output and floating-point
    (IEEE double) has been added.
  + LuaTEX: updated to Lua 5.2, and includes a new library
    (pdfscanner) to process external PDF page content, among
    much else (see its web pages).
  + XeTEX (also see its web pages for more):
    The HarfBuzz library now used for font layout instead of ICU.
    Graphite2 and HarfBuzz are used instead of SilGraphite for Graphite layout.
    On Macs, Core Text is used instead of the (deprecated) ATSUI.
    Prefer TrueType/OpenType fonts to Type1 when the names are the same.
    Fix occasional mismatch in font finding between XeTEX and xdvipdfmx.
    Support OpenType math cut-ins.
  + xdvi: now uses FreeType instead of t1lib for rendering.
  + microtype.sty: some support for XeTEX (protrusion) and LuaTEX
    (protrusion, font expansion, tracking), among other enhancements. 
- Update biblatex-biber to 1.7
- Udpate biblatex of TeXLive 2013 to 2.7a

* Tue Jul 16 2013 werner@suse.de
- Let texlive-arev require tex(mdacmr.fd) (bnc#819867) 
- Avoid line break in patch pgf_plain.dif (bnc#823273)

* Tue May 07 2013 werner@suse.de
- As lcdf-typetools does not support kpathsea nor search below
  texmf tree build the texlive-lcdftypetools(-bin) packages again
  and let them conflict with the lcdf-typetools package.

* Mon May 06 2013 werner@suse.de
- Asymptote binaries may have the same version as the format files
  of the asymptote package it self (bnc#813032)

* Wed Mar 27 2013 werner@suse.de
- Change Obsoletes from < 2012+subversion to <= 2011 (bnc#811162)
- Let mathdesign require tex(texnansi.enc) (bnc#808731)
- Let biber-bin require perl(Text::BibTeX) (bnc#811258)
- Do not require xfs as we do not use xfs at all, otherwise we
  have to add some more lua code in the %post scriptlet.

* Tue Feb 26 2013 werner@suse.de
- Avoid doubling mktex.opt content with excessive patch which had
  lead that the original content overrides the new one (bnc#801727)

* Tue Feb 05 2013 werner@suse.de
- Work around missing support of %posttrans scriptlets in libzypp
  due missing rpm option for not to execute those scriptlets (bnc#773575)

* Tue Oct 09 2012 werner@suse.de
- Add require texlive-metapost for texlive-dvips
- Add some more requires for latex-bin
- Add require pdftex.def for texlive-pdftex
- Do not reqiure package pgfmath in pgffor.sty (bnc#783252)

* Wed Sep 12 2012 werner@suse.de
- Use disturl for rpmbuild runs
- Aggregate licenses for meta spec file automatically

* Wed Aug 29 2012 cfarrell@suse.com
- license update: GPL-2.0+ and LPPL-1.3c and GPL-3.0+ and MPL-1.1 and
  LPPL-1.0 and OFL-1.1 and Apache-2.0 
  Aggregate licenses for spec file without subpackages

* Thu Aug 02 2012 werner@suse.de
- Change font config semantic as the font directories below
  /usr/share/fonts will be always found by freetype

* Fri Jul 20 2012 werner@suse.de
- Source validator does not like not applied patches 

* Thu Jul 19 2012 werner@suse.de
- Correct path in pgf patch 

* Thu Jul 19 2012 werner@suse.de
- Make the sub packagers texlive-spec-{a..z} valid for source
  validator

* Thu Jul 12 2012 werner@suse.de
- Add patch to make pgf work with plain TeX (bnc#746719) 

* Thu Jun 28 2012 werner@suse.de
- Make jadetex format build in posttrans scriptlet 

* Wed Jun 27 2012 werner@suse.de
- Add some missed files
- Break cycle between latex and latex-bin 

* Tue Jun 26 2012 werner@suse.de
- move lgrenc.dfu from doc to tex tree

* Tue Jun 26 2012 werner@suse.de
- Avoid dependency loops between kpathsea, tetex, and texconfig
  with the main package texlive as otherwise the three packages
  will be isntalled before texlive

* Fri Jun 22 2012 werner@suse.de
- Make sure that posttrans scriptlets will execute update script 

* Fri Jun 22 2012 werner@suse.de
- Re-run generator script to add missed docfiles 

* Thu Jun 21 2012 werner@suse.de
- Avoid failing scriptlets due slice split 

* Thu Jun 21 2012 werner@suse.de
- Modify the runtime Makefile to allow to build slices from the
  2236 spec files may help to speed up the serial checks and
  serial rpmlint run

* Thu Jun 21 2012 werner@suse.de
- Do not forget requirements of texlive-latex-bin

* Wed Jun 20 2012 werner@suse.de
- Add some minimal requirements for texlive-tex, texlive-latex,
  texlive-luatex, and texlive-texinfo 

* Mon Jun 18 2012 werner@suse.de
- Fix wrong placement of tex files
- Xecyr has only win executables

* Mon Jun 18 2012 werner@suse.de
- Simplify dependency chain(s)
- Allow pure source packages (knuth, latex-tds, ...)
- Allow empty packages (hyphen, bibtexu, ...) for dependencies

* Thu Jun 14 2012 werner@suse.de
- Make RPMlint happy 

* Thu Jun 14 2012 werner@suse.de
- Make main spec file run several rpmbuild processes in parallel 

* Wed Jun 13 2012 werner@suse.de
- Update to frozen/final 2012 (timestamp 20120611) 

* Mon Jun 04 2012 werner@suse.de
- Avoid source url for all tar balls as our checkin script can not
  handle snapshots nor is knowing about the infrastructure of the
  upstream TeXLive server

* Thu May 31 2012 werner@suse.de
- Do not forget the sub package like doc and fonts 

* Thu May 31 2012 werner@suse.de
- Suppress leading dot in build release number 

* Thu May 31 2012 werner@suse.de
- Change version/release scheme 
- Avoid to list optional loaded but not existing files as required

* Thu May 24 2012 werner@suse.de
- Add fix for latex2man insecure tmp file handling (bnc#758046) 

* Mon May 21 2012 werner@suse.de
- Avoid making delcmdchanges.bash to be a text file 

* Mon May 14 2012 werner@suse.de
- If MT_FEATURES includes varfonts and system default is not
  writable choose $HOME/.cache/texmf/fonts 

* Wed May 09 2012 werner@suse.de
- Make rpm lint happy

* Fri Apr 13 2012 werner@suse.de
- Initial packaging of TeXLive using package database texlive.tlpdb
  that is we have now a lot small packages around
