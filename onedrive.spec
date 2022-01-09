Summary:	OneDrive Free Client written in D
Name:		onedrive
Version:	2.4.13
Release:	3
License:	GPL v3
Source0:	https://github.com/abraunegg/onedrive/archive/v%{version}/%{name}-v%{version}.tar.gz
# Source0-md5:	18d5f1af56f7e3118e2dd00ad75bc8fa
URL:		https://github.com/abraunegg/onedrive
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	curl-devel
BuildRequires:	ldc
BuildRequires:	libnotify-devel
BuildRequires:	sqlite-devel
BuildRequires:	systemd-devel
BuildRequires:	rpmbuild(macros) >= 2.011
Requires(post,preun):	systemd-units >= 1:250.1
Requires:	systemd-units >= 1:250.1
ExclusiveArch:	%{x8664}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Free CLI client for Microsoft OneDrive written in D.

%prep
%setup -q
sed -i 's/-o root -g users//g' Makefile.in
sed -i 's/-o root -g root//g' Makefile.in
# sed -i '/git/d' Makefile
sed -i "s|std\.c\.|core\.stdc\.|" src/sqlite.d
echo %{version} > version

%build
%{__aclocal}
%{__autoconf}
bash %configure
export DFLAGS="%{_d_optflags}"
export PREFIX="%{_prefix}"
%{__make} DC=ldmd2

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
    PREFIX="%{_prefix}" \
	DESTDIR=$RPM_BUILD_ROOT

chmod a-x $RPM_BUILD_ROOT%{_mandir}/man1/%{name}*

%clean
rm -rf $RPM_BUILD_ROOT

%post
%systemd_user_post %{name}.service

%preun
%systemd_user_preun %{name}.service

%files
%defattr(644,root,root,755)
%doc README.md LICENSE CHANGELOG.md
%config(noreplace) %verify(not md5 mtime size) /etc/logrotate.d/onedrive
%attr(755,root,root) %{_bindir}/%{name}
%{systemduserunitdir}/%{name}.service
%{systemdunitdir}/%{name}@.service
%{_mandir}/man1/%{name}.1*
%{_docdir}/%{name}
