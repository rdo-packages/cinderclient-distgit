%{!?sources_gpg: %{!?dlrn:%global sources_gpg 1} }
%global sources_gpg_sign 0x2426b928085a020d8a90d0d879ab7008d0896c8a
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
# we are excluding some BRs from automatic generator
%global excluded_brs doc8 bandit pre-commit hacking flake8-import-order

%global sname cinderclient

%global with_doc 1

%global common_desc \
Client library (cinderclient python module) and command line utility \
(cinder) for interacting with OpenStack Cinder (Block Storage) API.

Name:             python-cinderclient
Version:          XXX
Release:          XXX
Summary:          Python API and CLI for OpenStack Cinder

License:          Apache-2.0
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

BuildRequires:    python3-devel
BuildRequires:    pyproject-rpm-macros
%description -n python3-%{sname}
%{common_desc}

%if 0%{?with_doc}
%package doc
Summary:          Documentation for OpenStack Cinder API Client
Group:            Documentation

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


sed -i /.*-c{env:TOX_CONSTRAINTS_FILE.*/d tox.ini
sed -i /^minversion.*/d tox.ini
sed -i /^requires.*virtualenv.*/d tox.ini

# Exclude some bad-knwon BRs
for pkg in %{excluded_brs};do
sed -i /^${pkg}.*/d doc/requirements.txt
sed -i /^${pkg}.*/d test-requirements.txt
done
# Automatic BR generation
%generate_buildrequires
%if 0%{?with_doc}
  %pyproject_buildrequires -t -e %{default_toxenv},docs
%else
  %pyproject_buildrequires -t -e %{default_toxenv}
%endif

%build
%pyproject_wheel

%if 0%{?with_doc}
export PYTHONPATH=.
%tox -e docs
sphinx-build-3 -W -b man doc/source doc/build/man

# Fix hidden-file-or-dir warnings
rm -fr doc/build/html/.doctrees doc/build/html/.buildinfo
%endif

%install
%pyproject_install
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
%{python3_sitelib}/*.dist-info
%{_sysconfdir}/bash_completion.d/cinder.bash_completion
%if 0%{?with_doc}
%{_mandir}/man1/cinder.1*
%endif

%if 0%{?with_doc}
%files doc
%doc doc/build/html
%endif

%changelog
