# Macros for py2/py3 compatibility
%if 0%{?fedora} || 0%{?rhel} > 7
%global pyver %{python3_pkgversion}
%else
%global pyver 2
%endif
%global pyver_bin python%{pyver}
%global pyver_sitelib %python%{pyver}_sitelib
%global pyver_install %py%{pyver}_install
%global pyver_build %py%{pyver}_build
# End of macros for py2/py3 compatibility
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global sname cinderclient

%global common_desc \
Client library (cinderclient python module) and command line utility \
(cinder) for interacting with OpenStack Cinder (Block Storage) API.

Name:             python-cinderclient
Version:          XXX
Release:          XXX
Summary:          Python API and CLI for OpenStack Cinder

License:          ASL 2.0
URL:              http://github.com/openstack/python-cinderclient
Source0:          https://tarballs.openstack.org/%{name}/%{name}-%{upstream_version}.tar.gz

BuildArch:        noarch

BuildRequires:    git

%description
%{common_desc}

%package -n python%{pyver}-%{sname}
Summary:          Python API and CLI for OpenStack Cinder
%{?python_provide:%python_provide python%{pyver}-%{sname}}

BuildRequires:    python%{pyver}-devel
BuildRequires:    python%{pyver}-setuptools
BuildRequires:    python%{pyver}-pbr
# Handle python2 exception
%if %{pyver} == 2
BuildRequires:    python-d2to1
%else
BuildRequires:    python%{pyver}-d2to1
%endif
Requires:         python%{pyver}-babel
Requires:         python%{pyver}-pbr
Requires:         python%{pyver}-prettytable
Requires:         python%{pyver}-requests
Requires:         python%{pyver}-six
Requires:         python%{pyver}-keystoneauth1 >= 3.4.0
Requires:         python%{pyver}-oslo-i18n >= 3.15.3
Requires:         python%{pyver}-oslo-utils >= 3.33.0
Requires:         python%{pyver}-simplejson

%description -n python%{pyver}-%{sname}
%{common_desc}

%package doc
Summary:          Documentation for OpenStack Cinder API Client
Group:            Documentation

BuildRequires:    python%{pyver}-reno
BuildRequires:    python%{pyver}-sphinx
BuildRequires:    python%{pyver}-openstackdocstheme

%description      doc
%{common_desc}

This package contains auto-generated documentation.


%prep
%autosetup -n %{name}-%{upstream_version} -S git

# Remove bundled egg-info
rm -rf python_cinderclient.egg-info

# Let RPM handle the requirements
rm -f {,test-}requirements.txt

%build
%{pyver_build}

sphinx-build-%{pyver} -W -b html doc/source doc/build/html
sphinx-build-%{pyver} -W -b man doc/source doc/build/man

# Fix hidden-file-or-dir warnings
rm -fr doc/build/html/.doctrees doc/build/html/.buildinfo

%install
%{pyver_install}
# Create a versioned binary for backwards compatibility until everything is pure py3
ln -s cinder %{buildroot}%{_bindir}/cinder-%{pyver}

# Delete tests
rm -fr %{buildroot}%{pyver_sitelib}/cinderclient/tests

install -p -D -m 644 tools/cinder.bash_completion %{buildroot}%{_sysconfdir}/bash_completion.d/cinder.bash_completion

install -p -D -m 644 doc/build/man/cinder.1 %{buildroot}%{_mandir}/man1/cinder.1

%files -n python%{pyver}-%{sname}
%doc README.rst
%license LICENSE
%{_bindir}/cinder
%{_bindir}/cinder-%{pyver}
%{pyver_sitelib}/cinderclient
%{pyver_sitelib}/*.egg-info
%{_sysconfdir}/bash_completion.d/cinder.bash_completion
%{_mandir}/man1/cinder.1*

%files doc
%doc doc/build/html

%changelog
