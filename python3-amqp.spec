#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit tests

%define 	module		amqp
%define		pypi_name	amqp
Summary:	AMQP 0.9.1 client library
Summary(pl.UTF-8):	Biblioteka kliencka AMQP 0.9.1
Name:		python3-%{module}
Version:	5.0.5
Release:	4
License:	BSD
Group:		Libraries/Python
Source0:	https://files.pythonhosted.org/packages/source/a/amqp/%{module}-%{version}.tar.gz
# Source0-md5:	4b46b380d33d3fb8faccba415a1beaff
URL:		https://amqp.readthedocs.io/
BuildRequires:	python3-modules >= 1:3.6
BuildRequires:	python3-setuptools >= 1:20.6.7
%if %{with tests}
BuildRequires:	python3-case >= 1.3.1
BuildRequires:	python3-pytest >= 3.0
BuildRequires:	python3-pytest-rerunfailures >= 6.0
BuildRequires:	python3-vine >= 5.0.0
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	python3-sphinx_celery >= 1.4.8
BuildRequires:	sphinx-pdg-3
%endif
Requires:	python3-modules >= 1:3.6
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is a fork of amqplib which was originally written by Barry
Pederson. It is maintained by the Celery project, and used by kombu as
a pure python alternative when librabbitmq is not available.

This library should be API compatible with librabbitmq.

%description -l pl.UTF-8
Ten projekt to odgałęzienie amqplib, pierwotnie napisane przez
Barry'ego Pedersona. Jest utrzymywane przez projekt Celery i używane
przez kombu jako czysto pythonowa alternatywa dla librabbitmq, jeśli
ta nie jest dostępna.

Biblioteka powinna być zgodna co do API z librabbitmq.

%package apidocs
Summary:	API documentation for amqp module
Summary(pl.UTF-8):	Dokumentacja API modułu amqp
Group:		Documentation

%description apidocs
API documentation for amqp module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu amqp.

%prep
%setup -q -n %{module}-%{version}

%build
%py3_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS="case.pytest" \
%{__python3} -m pytest t/unit
%endif

%if %{with doc}
%{__make} -C docs html \
	SPHINXBUILD=sphinx-build-3
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc Changelog LICENSE README.rst
%{py3_sitescriptdir}/%{module}
%{py3_sitescriptdir}/%{module}-%{version}-py*.egg-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_modules,_static,reference,*.html,*.js}
%endif
