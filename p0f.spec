Summary:	Passive OS fingerprinting tool
Summary(pl.UTF-8):	Narzędzie do pasywnej daktyloskopii systemów operacyjnych
Name:		p0f
Version:	3.03b
Release:	1
License:	LGPL v2.1
Group:		Networking/Utilities
# Official releases:
Source0:	http://lcamtuf.coredump.cx/p0f3/releases/%{name}-%{version}.tgz
# Source0-md5:	034d068deb68badfbede6dcc89cc80cf
# Devel:
#Source0:	http://lcamtuf.coredump.cx/p0f/%{name}-devel.tgz
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Source3:	%{name}.logrotate
URL:		http://lcamtuf.coredump.cx/p0f3/
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
%setup -q

%build
%{__make} \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags} -DFP_FILE=\"/usr/share/p0f/p0f.fp\"" \
	LDFLAGS="%{rpmldflags}"

%{__make} -C tools \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags}" \
	LDFLAGS="%{rpmldflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/rc.d/init.d,/etc/sysconfig,/etc/logrotate.d,%{_sbindir},%{_datadir}/p0f}
install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/p0f
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/p0f
install %{SOURCE3} $RPM_BUILD_ROOT/etc/logrotate.d/p0f
install p0f tools/p0f-{client,sendsyn,sendsyn6} $RPM_BUILD_ROOT%{_sbindir}
install p0f.fp $RPM_BUILD_ROOT%{_datadir}/p0f

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
%doc docs/{ChangeLog,existential-notes.txt,extra-sigs.txt,README,TODO} tools/README-TOOLS
%attr(754,root,root) /etc/rc.d/init.d/p0f
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/p0f
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/logrotate.d/p0f
%attr(755,root,root) %{_sbindir}/p0f*
%{_datadir}/p0f
