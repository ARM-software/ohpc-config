#
# Copyright (c) 2013 SUSE LINUX Products GmbH, Nuernberg, Germany.
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

%define texlive_version 2012
%define texlive_release 20120611
%define texlive_noarch  60

%define __perl_requires		%{nil}
%define __os_install_post	/usr/lib/rpm/brp-compress \\\
  %(ls /usr/lib/rpm/brp-suse.d/* 2> /dev/null | grep -vE 'check-la|boot-scripts|rpath|symlink|desktop|strip-debug|gcc-output|debuginfo|libtool|kernel-log') %{nil}

Name: texlive-everypage
Version: %{texlive_version}.%{texlive_noarch}.1.1svn15878
Release: %{?rlobs:%{rlobs}}%{!?rlobs:0}
License: LPPL-1.0
Summary: Provide hooks to be run on every page of a document
Group: Productivity/Publishing/TeX/Base
Url: http://www.tug.org/texlive/
Requires: texlive >= %{texlive_version}
Requires: coreutils
BuildRequires: ed
%if 0%{?suse_version}
BuildRequires: texlive-filesystem
%else
BuildRequires: texlive-base
%endif
BuildRequires: xz
Provides: tex(everypage.sty)
# Download at ftp://ftp.ctan.org/pub/tex/systems/texlive/tlnet/archive/
# from 20120611
Source0: everypage.tar.xz
Source1: everypage.doc.tar.xz
BuildArch: noarch

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
The package provides hooks to perform actions on every page, or
on the current page. Specifically, actions are performed after
the page is composed, but before it is shipped, so they can be
used to prepare the output page in tasks like putting
watermarks in the background, or in setting the next page
layout, etc.

date: 2008-02-19 18:31:19 +0000


%package doc
Summary: Documentation for texlive-everypage
Version: %{texlive_version}.%{texlive_noarch}.1.1svn15878
Release: %{?rlobs:%{rlobs}}%{!?rlobs:0}

%description doc
This package includes the documentation for texlive-everypage

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
    ln -sf %{_texmfmaindir}/texconfig/zypper.py \
	%{buildroot}/var/adm/update-scripts/%{name}-%{version}-%{release}-zypper
    tar --use-compress-program=xz -xf %{S:0} -C %{buildroot}%{_datadir}/texlive/texmf-dist
    tar --use-compress-program=xz -xf %{S:1} -C %{buildroot}%{_datadir}/texlive/texmf-dist
    rm -v  %{buildroot}%{_datadir}/texlive/texmf
    rm -v  %{buildroot}%{_datadir}/texlive/texmf-dist
    rm -vr %{buildroot}%{_datadir}/texlive
    # Remove this
    rm -vrf %{buildroot}%{_texmfdistdir}/tlpkg/tlpobj
    rm -vrf %{buildroot}%{_texmfmaindir}/tlpkg/tlpobj
    rm -vrf %{buildroot}%{_texmfdistdir}/source

%clean
rm -rf %{buildroot}

%post
mkdir -p /var/run/texlive
> /var/run/texlive/run-mktexlsr

%postun
if test $1 = 0; then
    %{_bindir}/mktexlsr 2> /dev/null || :
    exit 0
fi
mkdir -p /var/run/texlive
> /var/run/texlive/run-mktexlsr

%posttrans
test -z "$ZYPP_IS_RUNNING" || exit 0
VERBOSE=false %{_texmfmaindir}/texconfig/update || :

%files doc
%defattr(-,root,root,755)
%{_texmfdistdir}/doc/latex/everypage/README
%{_texmfdistdir}/doc/latex/everypage/everypage.pdf

%files
%defattr(-,root,root,755)
%{_texmfdistdir}/tex/latex/everypage/everypage.sty
/var/adm/update-scripts/%{name}-%{version}-%{release}-zypper

%changelog
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
