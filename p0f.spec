Name:		p0f
Summary:	passive OS fingerprinting tool
Version:	1.8
Release:	1
License:	GPL
Group:		Applications/Networking
Source0:	http://www.stearns.org/p0f/%{name}-%{version}.tgz
Source1:	%{name}.init
Requires(post,preun):/sbin/chkconfig
Vendor:		Michal Zalewski <lcamtuf@coredump.cx>
URL:		http://www.stearns.org/p0f/
BuildRequires:	libpcap-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
p0f performs passive OS fingerprinting technique bases on information
coming from remote host when it establishes connection to our system.
Captured packets contains enough information to determine OS - and,
unlike active scanners (nmap, queSO) - it is done without sending
anything to this host.

%prep
%setup -q

%build
%{__make} all

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{%{_sysconfdir},/etc/rc.d/init.d,%{_sbindir},%{_mandir},%{_mandir}/man1,/var/log}

install p0f.fp $RPM_BUILD_ROOT%{_sysconfdir}
install p0f $RPM_BUILD_ROOT%{_sbindir}
install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/p0f
install p0f.1 $RPM_BUILD_ROOT%{_mandir}/man1

touch $RPM_BUILD_ROOT/var/log/p0f

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add %{name}
if [ -f /var/lock/subsys/%{name} ]; then
        /etc/rc.d/init.d/%{name} restart 1>&2
else
        echo "Run \"/etc/rc.d/init.d/%{name} start\" to start %{name} daemon."
fi

%preun
if [ "$1" = "0" ]; then
        if [ -f /var/lock/subsys/%{name} ]; then
                /etc/rc.d/init.d/%{name} stop 1>&2
        fi
        /sbin/chkconfig --del %{name}
fi

%files
%defattr(644,root,root,755)
%doc README COPYING
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/p0f.fp
%attr(754,root,root) /etc/rc.d/init.d/p0f
%attr(755,root,root) %{_sbindir}/p0f
%attr(644,root,root) %{_mandir}/man1/p0f.1*
%attr(600,root,root) %ghost /var/log/p0f
