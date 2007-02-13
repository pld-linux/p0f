Summary:	Passive OS fingerprinting tool
Summary(pl.UTF-8):	Narzędzie do pasywnej daktyloskopii systemów operacyjnych
Name:		p0f
Version:	2.0.8
Release:	2
License:	LGPL v2.1
Group:		Applications/Networking
# Official releases:
Source0:	http://lcamtuf.coredump.cx/p0f/%{name}-%{version}.tgz
# Source0-md5:	1ccbcd8d4c95ef6dae841120d23c56a5
# Devel:
#Source0:	http://lcamtuf.coredump.cx/p0f/%{name}-devel.tgz
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Source3:	%{name}.logrotate
Patch0:		%{name}-DESTDIR.patch
URL:		http://lcamtuf.coredump.cx/p0f.shtml
BuildRequires:	libpcap-devel
BuildRequires:	rpmbuild(macros) >= 1.268
Requires(post):	fileutils
Requires(post,preun):	/sbin/chkconfig
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Requires(pre):	/bin/id
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Requires:	rc-scripts
Provides:	group(p0f)
Provides:	user(p0f)
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
p0f performs passive OS fingerprinting technique based on information
coming from remote host when it establishes connection to our system.
Captured packets contains enough information to determine OS - and,
unlike active scanners (nmap, queSO) - it is done without sending
anything to this host.

%description -l pl.UTF-8
p0f przeprowadza pasywną daktyloskopię systemu operacyjnego bazując na
informacjach, które wysyła zdalny system kiedy ustanawia połączenie z
naszym. Wyłapane pakiety zawierają wystarczająco dużo informacji by
określić system operacyjny - i, w przeciwieństwie do aktywnych
skanerów (nmap, queSO) - jest to robione bez wysyłania czegokolwiek do
tego hosta.

%prep
%setup -q -n %{name}
%patch0 -p1

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
install -d $RPM_BUILD_ROOT{/etc/rc.d/init.d,/etc/sysconfig,/etc/logrotate.d,%{_sbindir},%{_mandir}/man1}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/p0f
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/p0f
install %{SOURCE3} $RPM_BUILD_ROOT/etc/logrotate.d/p0f
cd test
install p0fq p0f-* $RPM_BUILD_ROOT%{_sbindir}

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%groupadd -g 164 p0f
%useradd -u 164 -c "p0f user" -g p0f p0f

%post
if [ ! -f /var/log/p0f ]; then
	touch /var/log/p0f
	chown root:root /var/log/p0f
	chmod 600 /var/log/p0f
fi
/sbin/chkconfig --add p0f
%service p0f restart "p0f daemon"

%preun
if [ "$1" = "0" ]; then
	%service p0f stop
	/sbin/chkconfig --del p0f
fi

%postun
if [ "$1" = "0" ]; then
	%userremove p0f
	%groupremove p0f
fi

%files
%defattr(644,root,root,755)
%doc doc/{CREDITS,KNOWN_BUGS,README,TODO,ChangeLog}
%dir %{_sysconfdir}/p0f
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/p0f/*
%attr(754,root,root) /etc/rc.d/init.d/p0f
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/p0f
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/logrotate.d/p0f
%attr(755,root,root) %{_sbindir}/p0f*
%{_mandir}/man1/p0f.1*
