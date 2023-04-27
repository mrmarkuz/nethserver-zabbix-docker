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
%define composeVersion 2.5.0
Source1: https://github.com/docker/compose/releases/download/v%{composeVersion}/docker-compose-linux-x86_64
Source2: https://github.com/zabbix/zabbix-docker/archive/refs/tags/6.0.4.tar.gz
Source3: https://github.com/mikefarah/yq/releases/download/v4.25.1/yq_linux_amd64
Requires: nethserver-docker,nethserver-zabbix-agent
Conflicts: nethserver-zabbix
BuildRequires: nethserver-devtools
BuildArch: x86_64

%description
NethServer Zabbix configuration

%changelog
* Thu Apr 21 2022 Markus Neuberger <info@markusneuberger.at> - 0.0.1-1
- Init

%prep
%setup

%build
perl createlinks
mkdir -p root/var/lib/nethserver/zabbix-docker/backup

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

mkdir -p %{buildroot}/opt/zabbix-docker
mv %SOURCE1 %{buildroot}/opt/zabbix-docker/docker-compose

tar -xzf %SOURCE2 --strip-components=1 -C %{buildroot}/opt/zabbix-docker/
rm %SOURCE2

mv %SOURCE3 %{buildroot}/opt/zabbix-docker/yq

%{genfilelist} $RPM_BUILD_ROOT \
> %{name}-%{version}-%{release}-filelist

%post
%postun

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}-%{version}-%{release}-filelist
%defattr(-,root,root)
%dir %{_nseventsdir}/%{name}-update
%attr(0755,root,root) /opt/zabbix-docker/docker-compose
%attr(0755,root,root) /opt/zabbix-docker/yq
%doc COPYING
