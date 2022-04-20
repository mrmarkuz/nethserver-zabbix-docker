Summary: nethserver-zabbix-docker sets up the monitoring system in docker
%define name nethserver-zabbix-docker
Name: %{name}
%define version 0.0.1
%define release 1
Version: %{version}
Release: %{release}%{?dist}
License: GPL
Group: Networking/Daemons
Source: %{name}-%{version}.tar.gz
BuildRoot: /var/tmp/%{name}-%{version}-%{release}-buildroot
Requires: nethserver-zabbix-agent,nethserver-postgresql,zabbix-server-pgsql,zabbix-web,net-snmp-utils,nethserver-net-snmp,php-pgsql,nethserver-rh-php73-php-fpm
Conflicts: nethserver-zabbix
BuildRequires: nethserver-devtools
BuildArch: noarch

%description
NethServer Zabbix configuration

%changelog
* Thu Apr 21 2022 Markus Neuberger <info@markusneuberger.at> - 0.0.1-1
- Init

%prep
%setup

%build
perl createlinks
mkdir -p root/var/lib/nethserver/zabbix/backup

%install
rm -rf $RPM_BUILD_ROOT
(cd root; find . -depth -print | cpio -dump $RPM_BUILD_ROOT)
rm -f %{name}-%{version}-%{release}-filelist

mkdir -p %{buildroot}/usr/share/cockpit/nethserver/applications/
mkdir -p %{buildroot}/usr/libexec/nethserver/api/%{name}/
mkdir -p %{buildroot}/usr/share/cockpit/%{name}/

cp -a %{name}.json %{buildroot}/usr/share/cockpit/nethserver/applications/
cp -a api/* %{buildroot}/usr/libexec/nethserver/api/%{name}/
cp -a ui/* %{buildroot}/usr/share/cockpit/%{name}/

%{genfilelist} $RPM_BUILD_ROOT \
  --file /etc/sudoers.d/50_nsapi_nethserver_zabbix 'attr(0440,root,root)' \
  --file /usr/libexec/nethserver/api/%{name}/read 'attr(775,root,root)' \
  --dir /var/lib/nethserver/zabbix/backup 'attr(755,postgres,postgres)' \
> %{name}-%{version}-%{release}-filelist
exit 0

%post
%postun

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}-%{version}-%{release}-filelist
%defattr(-,root,root)
%dir %{_nseventsdir}/%{name}-update
%doc COPYING
