%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global sname cinderclient
%if 0%{?fedora}
%global with_python3 1
%endif

Name:             python-cinderclient
Version:          XXX
Release:          XXX
Summary:          Python API and CLI for OpenStack Cinder

License:          ASL 2.0
URL:              http://github.com/openstack/python-cinderclient
Source0:          https://pypi.io/packages/source/p/%{name}/%{name}-%{version}.tar.gz

BuildArch:        noarch

BuildRequires:    git

%description
Client library (cinderclient python module) and command line utility
(cinder) for interacting with OpenStack Cinder (Block Storage) API.

%package -n python2-%{sname}
Summary:          Python API and CLI for OpenStack Cinder
%{?python_provide:%python_provide python2-%{sname}}

BuildRequires:    python2-devel
BuildRequires:    python-setuptools
BuildRequires:    python-pbr
BuildRequires:    python-d2to1

Requires:         python-babel
Requires:         python-keystoneclient
Requires:         python-pbr
Requires:         python-prettytable
Requires:         python-requests
Requires:         python-setuptools
Requires:         python-simplejson
Requires:         python-six
Requires:         python-keystoneauth1 >= 2.12.0
Requires:         python-oslo-i18n >= 3.9.0
Requires:         python-oslo-utils >= 3.16.0

%description -n python2-%{sname}
Client library (cinderclient python module) and command line utility
(cinder) for interacting with OpenStack Cinder (Block Storage) API.


%if 0%{?with_python3}
%package -n python3-%{sname}
Summary:          Python API and CLI for OpenStack Cinder
%{?python_provide:%python_provide python3-%{sname}}

BuildRequires:    python3-devel
BuildRequires:    python3-setuptools
BuildRequires:    python3-pbr
BuildRequires:    python3-d2to1

Requires:         python3-babel
Requires:         python3-keystoneclient
Requires:         python3-pbr
Requires:         python3-prettytable
Requires:         python3-requests
Requires:         python3-setuptools
Requires:         python3-simplejson
Requires:         python3-six
Requires:         python3-keystoneauth1 >= 2.12.0
Requires:         python3-oslo-i18n >= 3.9.0
Requires:         python3-oslo-utils >= 3.16.0

%description -n python3-%{sname}
Client library (cinderclient python module) and command line utility
(cinder) for interacting with OpenStack Cinder (Block Storage) API.
%endif


%package doc
Summary:          Documentation for OpenStack Cinder API Client
Group:            Documentation

BuildRequires:    python-reno
BuildRequires:    python-sphinx
BuildRequires:    python-oslo-sphinx

%description      doc
Client library (cinderclient python module) and command line utility
(cinder) for interacting with OpenStack Cinder (Block Storage) API.

This package contains auto-generated documentation.


%prep
%autosetup -n %{name}-%{upstream_version} -S git

# Remove bundled egg-info
rm -rf python_cinderclient.egg-info

# Let RPM handle the requirements
rm -f {,test-}requirements.txt

%build
%py2_build
%if 0%{?with_python3}
%py3_build
%endif

export PYTHONPATH="$( pwd ):$PYTHONPATH"
sphinx-build -b html doc/source html
sphinx-build -b man doc/source man

# Fix hidden-file-or-dir warnings
rm -fr html/.doctrees html/.buildinfo

%install
%if 0%{?with_python3}
%py3_install
mv %{buildroot}%{_bindir}/cinder %{buildroot}%{_bindir}/cinder-%{python3_version}
ln -s ./cinder-%{python3_version} %{buildroot}%{_bindir}/cinder-3
# Delete tests
rm -fr %{buildroot}%{python3_sitelib}/cinderclient/tests
%endif

%py2_install
mv %{buildroot}%{_bindir}/cinder %{buildroot}%{_bindir}/cinder-%{python2_version}
ln -s ./cinder-%{python2_version} %{buildroot}%{_bindir}/cinder-2
# Delete tests
rm -fr %{buildroot}%{python2_sitelib}/cinderclient/tests

ln -s ./cinder-2 %{buildroot}%{_bindir}/cinder

install -p -D -m 644 tools/cinder.bash_completion %{buildroot}%{_sysconfdir}/bash_completion.d/cinder.bash_completion

install -p -D -m 644 man/cinder.1 %{buildroot}%{_mandir}/man1/cinder.1

%files -n python2-%{sname}
%doc README.rst
%license LICENSE
%{_bindir}/cinder
%{_bindir}/cinder-2*
%{python2_sitelib}/cinderclient
%{python2_sitelib}/*.egg-info
%{_sysconfdir}/bash_completion.d/cinder.bash_completion
%{_mandir}/man1/cinder.1*

%if 0%{?with_python3}
%files -n python3-%{sname}
%doc README.rst
%license LICENSE
%{_bindir}/cinder-3*
%{python3_sitelib}/cinderclient
%{python3_sitelib}/*.egg-info
%endif

%files doc
%doc html

%changelog
# REMOVEME: error caused by commit http://git.openstack.org/cgit/openstack/python-cinderclient/commit/?id=ebcfedaec2365ff5da160b5c37045afa964d4d69
