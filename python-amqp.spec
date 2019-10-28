#
# Conditional build:
%bcond_with	doc	# build doc (broken)
%bcond_with	tests	# do not perform "make test"
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

%define 	module		amqp
%define		pypi_name	amqp
Summary:	AMQP 0.9.1 client library
Summary(pl.UTF-8):	Biblioteka kliencka AMQP 0.9.1
Name:		python-%{module}
Version:	2.3.2
Release:	2
License:	LGPL v2.1
Group:		Libraries/Python
Source0:	https://files.pythonhosted.org/packages/source/a/amqp/%{module}-%{version}.tar.gz
# Source0-md5:	11fce0d01f4ee6886a02415c20cece80
URL:		http://amqp.readthedocs.org/
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.710
%if %{with python2}
BuildRequires:	python-setuptools
%if %{with tests}
BuildRequires:	python-coverage >= 3.0
BuildRequires:	python-mock
BuildRequires:	python-nose
BuildRequires:	python-nose-cover3
BuildRequires:	python-unittest2>=0.4.0
%endif
%if %{with doc}
BuildRequires:	python-sphinxcontrib-issuetracker
BuildRequires:	sphinx-pdg-2
%endif
%endif
%if %{with python3}
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-coverage >= 3.0
BuildRequires:	python3-mock
BuildRequires:	python3-nose
BuildRequires:	python3-nose-cover3
%endif
%if %{with doc}
BuildRequires:	python3-sphinxcontrib-issuetracker
BuildRequires:	sphinx-pdg-3
%endif
%endif
Requires:	python-modules
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is a fork of amqplib which was originally written by Barry
Pederson. It is maintained by the Celery project, and used by kombu as
a pure python alternative when librabbitmq is not available.

This library should be API compatible with librabbitmq.

%package -n python3-%{module}
Summary:	AMQP 0.9.1 client library
Summary(pl.UTF-8):	Biblioteka kliencka AMQP 0.9.1
Group:		Libraries/Python
Requires:	python3-modules

%description -n python3-%{module}
This is a fork of amqplib which was originally written by Barry
Pederson. It is maintained by the Celery project, and used by kombu as
a pure python alternative when librabbitmq is not available.

This library should be API compatible with librabbitmq.

%package apidocs
Summary:	%{module} API documentation
Summary(pl.UTF-8):	Dokumentacja API %{module}
Group:		Documentation

%description apidocs
API documentation for %{module}.

%description apidocs -l pl.UTF-8
Dokumentacja API %{module}.

%package -n python3-%{module}-apidocs
Summary:	%{module} API documentation
Summary(pl.UTF-8):	Dokumentacja API %{module}
Group:		Documentation

%description -n python3-%{module}-apidocs
API documentation for %{module}.

%description -n python3-%{module}-apidocs -l pl.UTF-8
Dokumentacja API %{module}.

%prep
%setup -q -n %{module}-%{version}

%build
%if %{with python2}
%py_build %{?with_tests:test}

%if %{with doc}
cd docs
PYTHONPATH=../build-2/lib %{__make} -j1 html SPHINXBUILD=sphinx-build-2
rm -rf .build/html/_sources
mv .build .build2
cd ..
%endif

%endif

%if %{with python3}
%py3_build %{?with_tests:test}

%if %{with doc}
cd docs
PYTHONPATH=../build-3/lib %{__make} -j1 html SPHINXBUILD=sphinx-build-3
rm -rf .build/html/_sources
mv .build .build3
cd ..
%endif
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
%doc Changelog README.rst
%dir %{py_sitescriptdir}/%{module}
%{py_sitescriptdir}/%{module}/*.py[co]
%{py_sitescriptdir}/%{module}-%{version}-py*.egg-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/.build2/html/*
%endif
%endif

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%doc Changelog README.rst
%{py3_sitescriptdir}/%{module}
%{py3_sitescriptdir}/%{module}-%{version}-py*.egg-info

%if %{with doc}
%files -n python3-%{module}-apidocs
%defattr(644,root,root,755)
%doc docs/.build3/html/*
%endif
%endif
