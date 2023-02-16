%{!?sources_gpg: %{!?dlrn:%global sources_gpg 1} }
%global sources_gpg_sign 0x2426b928085a020d8a90d0d879ab7008d0896c8a
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global sname cinderclient

%global with_doc 1

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
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
Source101:        https://tarballs.openstack.org/%{name}/%{name}-%{upstream_version}.tar.gz.asc
Source102:        https://releases.openstack.org/_static/%{sources_gpg_sign}.txt
%endif

BuildArch:        noarch

# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
BuildRequires:  /usr/bin/gpgv2
BuildRequires:  openstack-macros
%endif

BuildRequires:    git-core

%description
%{common_desc}

%package -n python3-%{sname}
Summary:          Python API and CLI for OpenStack Cinder
%{?python_provide:%python_provide python3-%{sname}}

BuildRequires:    python3-devel
BuildRequires:    python3-setuptools
BuildRequires:    python3-pbr

Requires:         python3-pbr >= 5.5.0
Requires:         python3-prettytable >= 0.7.2
Requires:         python3-requests
Requires:         python3-keystoneauth1 >= 5.0.0
Requires:         python3-oslo-i18n >= 5.0.1
Requires:         python3-oslo-utils >= 4.8.0
Requires:         python3-stevedore >= 3.3.0

%description -n python3-%{sname}
%{common_desc}

%if 0%{?with_doc}
%package doc
Summary:          Documentation for OpenStack Cinder API Client
Group:            Documentation

BuildRequires:    python3-reno
BuildRequires:    python3-sphinx
BuildRequires:    python3-openstackdocstheme
BuildRequires:    python3-keystoneauth1
BuildRequires:    python3-oslo-utils
BuildRequires:    python3-prettytable

%description      doc
%{common_desc}

This package contains auto-generated documentation.
%endif

%prep
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
%{gpgverify}  --keyring=%{SOURCE102} --signature=%{SOURCE101} --data=%{SOURCE0}
%endif
%autosetup -n %{name}-%{upstream_version} -S git

# Remove bundled egg-info
rm -rf python_cinderclient.egg-info

# Let RPM handle the requirements
rm -f {,test-}requirements.txt

%build
%{py3_build}

%if 0%{?with_doc}
export PYTHONPATH=.
sphinx-build-3 -W -b html doc/source doc/build/html
sphinx-build-3 -W -b man doc/source doc/build/man

# Fix hidden-file-or-dir warnings
rm -fr doc/build/html/.doctrees doc/build/html/.buildinfo
%endif

%install
%{py3_install}
# Create a versioned binary for backwards compatibility until everything is pure py3
ln -s cinder %{buildroot}%{_bindir}/cinder-3

# Delete tests
rm -fr %{buildroot}%{python3_sitelib}/cinderclient/tests

install -p -D -m 644 tools/cinder.bash_completion %{buildroot}%{_sysconfdir}/bash_completion.d/cinder.bash_completion

%if 0%{?with_doc}
install -p -D -m 644 doc/build/man/cinder.1 %{buildroot}%{_mandir}/man1/cinder.1
%endif

%files -n python3-%{sname}
%doc README.rst
%license LICENSE
%{_bindir}/cinder
%{_bindir}/cinder-3
%{python3_sitelib}/cinderclient
%{python3_sitelib}/*.egg-info
%{_sysconfdir}/bash_completion.d/cinder.bash_completion
%if 0%{?with_doc}
%{_mandir}/man1/cinder.1*
%endif

%if 0%{?with_doc}
%files doc
%doc doc/build/html
%endif

%changelog
