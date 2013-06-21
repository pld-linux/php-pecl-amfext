%define		php_name	php%{?php_suffix}
%define		modname	amfext
%define		status		beta
Summary:	%{modname} - ActionScript Message Format extension
Summary(pl.UTF-8):	%{modname} - rozszerzenie ActionScript Message Format
Name:		%{php_name}-pecl-%{modname}
Version:	0.9.2
Release:	1
License:	PHP 2.02
Group:		Development/Languages/PHP
Source0:	http://pecl.php.net/get/%{modname}-%{version}.tgz
# Source0-md5:	c5899ca580f19ef7f057b6ea41c2d236
URL:		http://pecl.php.net/package/amfext/
BuildRequires:	%{php_name}-devel >= 3:5.0.0
BuildRequires:	rpmbuild(macros) >= 1.650
%{?requires_php_extension}
Requires:	php(core) >= 5.0.4
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Allows to encode and decode PHP data in ActionScript Message Format
(AMF) version 0 and 3.

In PECL status of this extension is: %{status}.

%description -l pl.UTF-8
Rozszerzenie to pozwala (de)kodowanie danych PHP do formatu
ActionScript Message Format (AMF) w wersji 0 i 3.

To rozszerzenie ma w PECL status: %{status}.

%prep
%setup -qc
mv %{modname}-%{version}/* .

%build
phpize
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d
%{__make} install \
	INSTALL_ROOT=$RPM_BUILD_ROOT \
	EXTENSION_DIR=%{php_extensiondir}
cat <<'EOF' > $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d/%{modname}.ini
; Enable %{modname} extension module
extension=%{modname}.so
EOF

mv -f $RPM_BUILD_ROOT%{php_extensiondir}/{amf,%{modname}}.so

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
%doc CREDITS README
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/%{modname}.ini
%attr(755,root,root) %{php_extensiondir}/%{modname}.so
