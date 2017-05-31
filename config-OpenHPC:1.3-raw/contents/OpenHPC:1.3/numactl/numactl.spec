#
# spec file for package numactl
#
# Copyright (c) 2016 SUSE LINUX GmbH, Nuernberg, Germany.
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


Url:            http://oss.sgi.com/projects/libnuma/

Name:           numactl
Summary:        NUMA Policy Control
License:        GPL-2.0+
Group:          System/Management
Version:        2.0.9
Release:        0
# bug437293
%ifarch ppc64
Obsoletes:      numactl-64bit
%endif
#
Source:         ftp://oss.sgi.com/www/projects/libnuma/download/numactl-%{version}.tar.gz
Source2:        baselibs.conf
Patch0:         revert_date_in_numastat.patch
Patch1:         0001-Fixed-segfault-when-no-node-could-be-found-in-sysfs-.patch
Patch2:         check_for_return_val_of_numa_node_to_cpus.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
ExcludeArch:    s390 s390x
Requires:       perl

%description
Control NUMA policy for individual processes. Offer libnuma for
individual NUMA policy in applications.

%package -n libnuma1
Summary:        NUMA Policy Control
License:        LGPL-2.1+
Group:          Development/Languages/C and C++

%description -n libnuma1
Control NUMA policy for individual processes. Offer libnuma for
individual NUMA policy in applications.

%package -n libnuma-devel
Summary:        NUMA Policy Control
License:        GPL-2.0+
Group:          Development/Languages/C and C++
Requires:       libnuma1 = %{version}

%description -n libnuma-devel
Control NUMA policy for individual processes. Offer libnuma for
individual NUMA policy in applications.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
# looks like a numactl mainline bug, will propably be fixed
# until next update and the rm line can get removed again.
# Remove the empty file, so that numstat gets build:
rm numastat

make %{?_smp_mflags} CFLAGS="${RPM_OPT_FLAGS}"

%install
install -d -m 755 $RPM_BUILD_ROOT/usr/bin
install -d -m 755 $RPM_BUILD_ROOT%{_mandir}/man3
install -d -m 755 $RPM_BUILD_ROOT%{_mandir}/man5
install -d -m 755 $RPM_BUILD_ROOT%{_libdir}
install -d -m 755 $RPM_BUILD_ROOT/usr/include
make prefix="%buildroot/%_prefix" libdir="%buildroot/%_libdir" install
rm -f $RPM_BUILD_ROOT/%{_libdir}/lib*a

%clean
rm -rf $RPM_BUILD_ROOT

%post -n libnuma1 -p /sbin/ldconfig

%postun -n libnuma1 -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_bindir}/*
%{_mandir}/man8/*
%doc CHANGES

%files -n libnuma1
%defattr(-,root,root)
%{_libdir}/lib*so.*

%files -n libnuma-devel
%defattr(-,root,root)
%doc %{_mandir}/man3/*
%{_includedir}/*
%{_libdir}/lib*so

%changelog
