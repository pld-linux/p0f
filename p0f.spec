Summary:	passive OS fingerprinting tool
Summary(pl):	Narzêdzie do pasywnej daktyloskopii systemów operacyjnych
Name:		p0f
Version:	1.8.3
Release:	1
License:	GPL
Vendor:		Michal Zalewski <lcamtuf@coredump.cx>
Group:		Applications/Networking
Source0:	http://www.stearns.org/p0f/%{name}-%{version}.tgz
Source1:	%{name}.init
Source2:	%{name}.sysconfig
URL:		http://www.stearns.org/p0f/
Prereq:		/sbin/chkconfig
BuildRequires:	libpcap-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
p0f performs passive OS fingerprinting technique based on information
coming from remote host when it establishes connection to our system.
Captured packets contains enough information to determine OS - and,
unlike active scanners (nmap, queSO) - it is done without sending
anything to this host.

%description -l pl
p0f przeprowadza pasywn± daktyloskopiê systemu operacyjnego bazuj±c na
informacjach, które wysy³a zdalny system kiedy ustanawia po³±czenie z
naszym. Wy³apane pakiety zawieraj± wystarczaj±co du¿o informacji by
okre¶liæ system operacyjny - i, w przeciwieñstwie do aktywnych
skanerów (nmap, queSO) - jest to robione bez wysy³ania czegokolwiek do
tego hosta.

%prep
%setup -q

%build
%{__make} all

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/rc.d/init.d,/etc/sysconfig,%{_sbindir},%{_mandir}/man1,%{_bindir}}

install p0f.fp $RPM_BUILD_ROOT%{_sysconfdir}
install p0f $RPM_BUILD_ROOT%{_sbindir}
install p0frep $RPM_BUILD_ROOT%{_bindir}

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/p0f
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/p0f
install p0f.1 $RPM_BUILD_ROOT%{_mandir}/man1

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ ! -f /var/log/p0f ]; then
	touch /var/log/p0f
	chown root.root /var/log/p0f
	chmod 600 /var/log/p0f
fi
/sbin/chkconfig --add p0f
if [ -f /var/lock/subsys/p0f ]; then
	/etc/rc.d/init.d/p0f restart >&2
else
	echo "Run \"/etc/rc.d/init.d/p0f start\" to start p0f daemon."
fi

%preun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/p0f ]; then
		/etc/rc.d/init.d/p0f stop >&2
	fi
	/sbin/chkconfig --del p0f
fi

%files
%defattr(644,root,root,755)
%doc README CREDITS ChangeLog
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/p0f.fp
%attr(754,root,root) /etc/rc.d/init.d/p0f
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) /etc/sysconfig/p0f
%attr(755,root,root) %{_sbindir}/p0f
%attr(755,root,root) %{_bindir}/p0frep
%{_mandir}/man1/p0f.1*
