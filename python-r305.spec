# Created by pyp2rpm-3.1.3
%global pypi_name R305


Name:           python-%{pypi_name}
Version:        1.0.0
Release:        1%{?dist}
Summary:        python API for R305 finger print module

License:        GPLv3+
URL:            https://github.com/girish946/pthon-R305
Source0:        https://files.pythonhosted.org/packages/source/R/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch


%description
python API for R305 finger print module over UART. Each module contains getHeader() and parse() methods. getHeader() generates the frame for the command for the specific instruction. The parse() for theat module parses the response of the command and shows the result.

%package -n     python2-%{pypi_name}
Summary:        python API for R305 finger print module.
%{?python_provide:%python_provide python2-%{pypi_name}}

BuildRequires:  python-setuptools
BuildRequires:  python2-devel
 
Requires:       pyserial
%description -n python2-%{pypi_name}
python API for R305 finger print module over UART.


%prep
%autosetup -n %{pypi_name}-%{version}
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info
sed -i -e '/^#!\//, 1d' r305/*.py


%build
%py2_build


%install
# Must do the subpackages' install first because the scripts in /usr/bin are
# overwritten with every setup.py install.

%py2_install


%files -n python2-%{pypi_name}
%license LICENSE
%doc 
%{_bindir}/Verify.py
%{python2_sitelib}/r305/
%{python2_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info/


%changelog
* Sat Nov 5 2016 girish joshi <girish946@gmail.com> - 1.0.0
- initial package is created.
- basic functionality of r305 added.
