#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit tests
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

%define 	module		amqp
%define		pypi_name	amqp
Summary:	AMQP 0.9.1 client library
Summary(pl.UTF-8):	Biblioteka kliencka AMQP 0.9.1
Name:		python-%{module}
# keep 2.x here for python2 support
Version:	2.6.1
Release:	1
License:	BSD
Group:		Libraries/Python
Source0:	https://files.pythonhosted.org/packages/source/a/amqp/%{module}-%{version}.tar.gz
# Source0-md5:	c8cf9c75d7cd2e747fa49f3e3c47b3b1
URL:		https://amqp.readthedocs.io/
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with python2}
BuildRequires:	python-modules >= 1:2.7
BuildRequires:	python-setuptools >= 20.6.7
%if %{with tests}
BuildRequires:	python-case >= 1.3.1
BuildRequires:	python-pytest >= 3.0
BuildRequires:	python-pytest-rerunfailures >= 6.0
BuildRequires:	python-vine >= 1.1.3
%endif
%endif
%if %{with python3}
BuildRequires:	python3-modules >= 1:3.5
BuildRequires:	python3-setuptools >= 20.6.7
%if %{with tests}
BuildRequires:	python3-case >= 1.3.1
BuildRequires:	python3-pytest >= 3.0
BuildRequires:	python3-pytest-rerunfailures >= 6.0
BuildRequires:	python3-vine >= 1.1.3
BuildRequires:	python3-vine < 5
%endif
%endif
%if %{with doc}
BuildRequires:	python-sphinx_celery >= 1.4.6
BuildRequires:	sphinx-pdg-2
%endif
Requires:	python-modules >= 1:2.7
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

%package -n python3-%{module}
Summary:	AMQP 0.9.1 client library
Summary(pl.UTF-8):	Biblioteka kliencka AMQP 0.9.1
Group:		Libraries/Python
Requires:	python3-modules >= 1:3.5

%description -n python3-%{module}
This is a fork of amqplib which was originally written by Barry
Pederson. It is maintained by the Celery project, and used by kombu as
a pure python alternative when librabbitmq is not available.

This library should be API compatible with librabbitmq.

%description -n python3-%{module} -l pl.UTF-8
Ten projekt to odgałęzienie amqplib, pierwotnie napisane przez
Barry'ego Pedersona. Jest utrzymywane przez projekt Celery i używane
przez kombu jako czysto pythonowa alternatywa dla librabbitmq, jeśli
ta nie jest dostępna.

Biblioteka powinna być zgodna co do API z librabbitmq.

%package apidocs
Summary:	API documentation for amqp module
Summary(pl.UTF-8):	Dokumentacja API modułu amqp
Group:		Documentation
Obsoletes:	python3-amqp-apidocs < 2.6.1

%description apidocs
API documentation for amqp module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu amqp.

%prep
%setup -q -n %{module}-%{version}

%build
%if %{with python2}
%py_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS="case.pytest" \
%{__python} -m pytest t/unit
%endif
%endif

%if %{with python3}
%py3_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS="case.pytest" \
%{__python3} -m pytest t/unit
%endif
%endif

%if %{with doc}
%{__make} -C docs html \
	SPHINXBUILD=sphinx-build-2
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%py_postclean
%endif

%if %{with python3}
%py3_install
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc Changelog LICENSE README.rst
%{py_sitescriptdir}/%{module}
%{py_sitescriptdir}/%{module}-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%doc Changelog LICENSE README.rst
%{py3_sitescriptdir}/%{module}
%{py3_sitescriptdir}/%{module}-%{version}-py*.egg-info
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_modules,_static,reference,*.html,*.js}
%endif
