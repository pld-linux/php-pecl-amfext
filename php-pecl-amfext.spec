%define		_modname	amfext
%define		_status		beta
Summary:	%{_modname} - ActionScript Message Format extension
Summary(pl.UTF-8):	%{_modname} - rozszerzenie ActionScript Message Format
Name:		php-pecl-%{_modname}
Version:	0.9.2
Release:	1
License:	PHP 2.02
Group:		Development/Languages/PHP
Source0:	http://pecl.php.net/get/%{_modname}-%{version}.tgz
# Source0-md5:	c5899ca580f19ef7f057b6ea41c2d236
URL:		http://pecl.php.net/package/amfext/
BuildRequires:	php-devel >= 3:5.0.0
BuildRequires:	rpmbuild(macros) >= 1.344
%{?requires_php_extension}
Requires:	php-common >= 4:5.0.4
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Allows to encode and decode PHP data in ActionScript Message Format
(AMF) version 0 and 3.

In PECL status of this extension is: %{_status}.

%description -l pl.UTF-8
Rozszerzenie to pozwala (de)kodowanie danych PHP do formatu
ActionScript Message Format (AMF) w wersji 0 i 3.

To rozszerzenie ma w PECL status: %{_status}.

%prep
%setup -q -c

%build
cd %{_modname}-%{version}
phpize
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d

%{__make} install \
	-C %{_modname}-%{version} \
	INSTALL_ROOT=$RPM_BUILD_ROOT \
	EXTENSION_DIR=%{php_extensiondir}
cat <<'EOF' > $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d/%{_modname}.ini
; Enable %{_modname} extension module
extension=%{_modname}.so
EOF

mv -f $RPM_BUILD_ROOT%{php_extensiondir}/{amf,%{_modname}}.so

%clean
rm -rf $RPM_BUILD_ROOT

%post
%php_webserver_restart

%postun
if [ "$1" = 0 ]; then
	%php_webserver_restart
fi

%files
%defattr(644,root,root,755)
%doc %{_modname}-%{version}/{CREDITS,README}
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/%{_modname}.ini
%attr(755,root,root) %{php_extensiondir}/%{_modname}.so
