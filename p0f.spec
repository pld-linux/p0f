# TODO: use ip instead of ifconfig in .init
Summary:	Passive OS fingerprinting tool
Summary(pl):	Narzêdzie do pasywnej daktyloskopii systemów operacyjnych
Name:		p0f
Version:	2.0.3
Release:	1
License:	LGPL v2.1
Vendor:		Michal Zalewski <lcamtuf@coredump.cx>
Group:		Applications/Networking
# Official releases:
Source0:	http://lcamtuf.coredump.cx/p0f/%{name}-%{version}.tgz
# Source0-md5:	583688a4c5718eec0bb34102b3ac457b
# Devel:
#Source0:	http://lcamtuf.coredump.cx/p0f/%{name}-devel.tgz
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Patch0:		%{name}-DESTDIR.patch
URL:		http://lcamtuf.coredump.cx/p0f.shtml
BuildRequires:	libpcap-devel
PreReq:		rc-scripts
Requires(post,preun):	/sbin/chkconfig
Requires(post):	fileutils
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
%setup -q -n %{name}
%patch0 -p0

%build
%{__make} %{name} -f mk/Linux \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags} -fomit-frame-pointer -Wall"

cd test
%{__cc} %{rpmldflags} %{rpmcflags} -o p0fq p0fq.c
%{__cc} %{rpmldflags} %{rpmcflags} -o p0f-sendack  sendack.c
%{__cc} %{rpmldflags} %{rpmcflags} -o p0f-sendack2 sendack2.c
%{__cc} %{rpmldflags} %{rpmcflags} -o p0f-sendsyn  sendsyn.c

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/rc.d/init.d,/etc/sysconfig,%{_sbindir},%{_mandir}/man1}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/p0f
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/p0f
cd test
install p0fq p0f-* $RPM_BUILD_ROOT%{_sbindir}

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ ! -f /var/log/p0f ]; then
	touch /var/log/p0f
	chown root:root /var/log/p0f
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
%doc doc/{CREDITS,KNOWN_BUGS,README,TODO,ChangeLog}
%dir %{_sysconfdir}/p0f
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/p0f/*
%attr(754,root,root) /etc/rc.d/init.d/p0f
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) /etc/sysconfig/p0f
%attr(755,root,root) %{_sbindir}/p0f*
%{_mandir}/man1/p0f.1*
