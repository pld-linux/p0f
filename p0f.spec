Name:		p0f
Summary:	passive OS fingerprinting tool
Summary(pl):	Narzêdzie do pasywnej daktyloskopii systemów operacyjnych
Version:	1.8
Release:	1
License:	GPL
Group:		Applications/Networking
Group(de):	Applikationen/Netzwerkwesen
Group(pl):	Aplikacje/Sieciowe
Source0:	http://www.stearns.org/p0f/%{name}-%{version}.tgz
Source1:	%{name}.init
Prereq:		/sbin/chkconfig
BuildRequires:  libpcap-devel
Vendor:		Michal Zalewski <lcamtuf@coredump.cx>
URL:		http://www.stearns.org/p0f/
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
install -d $RPM_BUILD_ROOT%{_sysconfdir}
	install -d $RPM_BUILD_ROOT/etc/rc.d/init.d
install -d $RPM_BUILD_ROOT%{_sbindir}
	install -d $RPM_BUILD_ROOT%{_mandir}/man1
cp -p p0f.fp $RPM_BUILD_ROOT%{_sysconfdir}
cp -p p0f $RPM_BUILD_ROOT%{_sbindir}
	cp -p p0f.init $RPM_BUILD_ROOT/etc/rc.d/init.d/p0f
        cp -p p0f.1 p0f.1.orig
	rm -f p0f.1.gz
	gzip -9 p0f.1
	mv p0f.1.orig p0f.1
	mv p0f.1.gz $RPM_BUILD_ROOT%{_mandir}/man1

						
%clean
	rm -rf $RPM_BUILD_ROOT


%files
%defattr(644,root,root,755)
					%doc	README COPYING
%attr(644,root,root) %{_sysconfdir}/p0f.fp
%attr(755,root,root)				/etc/rc.d/init.d/p0f
%attr(755,root,root) %{_sbindir}/p0f
%attr(644,root,root)				%{_mandir}/man1/p0f.1.gz


%post
if [ ! -f /var/log/p0f ]; then
	touch /var/log/p0f
	chown root.root /var/log/p0f
	chmod 600 /var/log/p0f
fi
if [ "$1" = "1" ]; then         #This package is being installed for the first time
	/sbin/chkconfig --add p0f
fi


%preun
if [ "$1" = "0" ]; then		#This is being completely erased, not upgraded
	/sbin/chkconfig --del p0f
fi
