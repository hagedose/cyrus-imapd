%if 0%{?opensuse_bs} && 0%{?suse_version} < 1
#!BuildIgnore:  systemd
%endif

%if 0%{?suse_version} < 1 && 0%{?fedora} < 1 && 0%{?rhel} < 7
%global with_systemd 0
%else
%global with_systemd 1
%{!?_unitdir: %global _unitdir /usr/lib/systemd/system}
%endif

%global _name cyrus-imapd

%global ssl_pem_file %{_sysconfdir}/pki/%{_name}/%{_name}.pem

%global uid 76
%global gid 76

%global _cyrususer cyrus
%global _cyrusgroup mail
%global _cyrexecdir %{_exec_prefix}/lib/%{_name}

%global real_version 2.5.9
%define version 2.5.9
%define rpmrelease 1

##
## Options
##

%global with_bdb        0
%global with_mysql      0
%global with_pgsql      0

%global with_tcpwrap    0

%global rrzk		1

Name:               cyrus-imapd
Summary:            A high-performance mail server with IMAP, POP3, NNTP and SIEVE support
Version:            %{version}
Release:            %{rpmrelease}%{?dist}
License:            BSD
Group:              System Environment/Daemons
URL:                http://www.cyrusimap.org

# Upstream sources
# From e9195f39150b553a4f62b891f61193cf1b199fc3
Source0:            ftp://ftp.andrew.cmu.edu/pub/cyrus/%{_name}-%{real_version}.tar.gz
Source1:            cyrus-imapd.imap-2.3.x-conf
Source2:            cyrus-imapd.cvt_cyrusdb_all
Source3:            cyrus-imapd.magic

# Distribution specific sources
Source11:           cyrus-imapd.logrotate
Source12:           cyrus-imapd.pam-config
Source13:           cyrus-imapd.cron-daily

# SysVinit
Source21:           cyrus-imapd.init
Source22:           cyrus-imapd.sysconfig

# Systemd support
Source31:           cyrus-imapd.service
Source32:           cyr_systemd_helper

##
## Patches
##

BuildRoot:          %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

##
## Build Requirements
##
BuildRequires:      autoconf
BuildRequires:      automake
BuildRequires:      bison
BuildRequires:      cyrus-sasl-devel
%if 0%{?suse_version}
BuildRequires:      cunit-devel
BuildRequires:      cyrus-sasl-digestmd5
%else
BuildRequires:      CUnit-devel
BuildRequires:      cyrus-sasl-md5
%endif
BuildRequires:      cyrus-sasl-plain

%if 0%{?with_bdb}
%if 0%{?suse_version}
BuildRequires:      db-devel
%else
%if 0%{?fedora} > 15 || 0%{?rhel} > 6
BuildRequires:      libdb-devel
%else
BuildRequires:      db4-devel
%endif
%endif
%endif

BuildRequires:      flex
#BuildRequires:      gcc-c++
BuildRequires:      gcc

%if 0%{?suse_version} >= 1310
BuildRequires:      groff-full
%else
BuildRequires:      groff
%endif

%if 0%{?suse_version}
BuildRequires:      libjansson4-devel
%else
BuildRequires:      jansson-devel
%endif
BuildRequires:      krb5-devel

%if 0%{?rrzk}
BuildRequires:      libical-devel
%endif

BuildRequires:      libtool
BuildRequires:      libuuid-devel

%if 0%{?with_mysql}
BuildRequires:      mysql-devel
%endif

BuildRequires:      net-snmp-devel
%if 0%{?suse_version}
BuildRequires:      openldap2-devel
%else
BuildRequires:      openldap-devel
%endif

BuildRequires:      openssl-devel
BuildRequires:      perl(ExtUtils::MakeMaker)

%if 0%{?suse_version}
BuildRequires:      perl
%else
BuildRequires:      perl-devel
%endif

BuildRequires:      pkgconfig

%if 0%{?with_pgsql}
BuildRequires:      postgresql-devel
%endif

%if 0%{?rrzk}
BuildRequires:      sqlite-devel
%endif

%if 0%{?with_systemd}
%if 0%{?suse_version}
BuildRequires:      systemd
%endif
%endif

%if 0%{?with_tcpwrap}
%if 0%{?suse_version}
BuildRequires:      tcpd-devel
%else
BuildRequires:      tcp_wrappers
%endif
%endif

BuildRequires:      transfig
%if 0
# Disable the xapian-core requirement
BuildRequires:      xapian-core-devel
%endif

%if 0%{?suse_version}
PreReq:             /usr/sbin/groupadd
PreReq:             /usr/sbin/useradd
%endif

%if 0%{?suse_version}
Requires:           db-utils
%else
Requires:           db4-utils
%endif

Requires:           file
Requires:           perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

Requires(post):     coreutils
Requires(post):     e2fsprogs
Requires(post):     findutils
Requires(post):     grep
Requires(post):     make
Requires(post):     openssl
Requires(post):     perl
Requires(preun):    coreutils

%if 0%{?with_systemd}
%if 0%{?suse_version}
PreReq:             %fillup_prereq
%{?systemd_requires}
%else
%if 0%{?opensuse_bs} == 0
Requires(post):     systemd-units
Requires(preun):    systemd-units, coreutils
Requires(postun):   systemd-units
%endif
%endif
%else
%if 0%{?suse_version}
PreReq:             %fillup_prereq
PreReq:             %insserv_prereq
%else
Requires(preun):    chkconfig
Requires(preun):    initscripts
Requires(post):     chkconfig
Requires(post):     initscripts
Requires(postun):   initscripts
%endif
%endif

Obsoletes:          %{name}-perl < %{version}-%{release}
Provides:           %{name}-perl = %{version}-%{release}
Obsoletes:          %{name}-utils < %{version}-%{release}
Provides:           %{name}-utils = %{version}-%{release}

%description
The %{name} package contains the core of the Cyrus IMAP server.
It is a scaleable enterprise mail system designed for use from
small to large enterprise environments using standards-based
internet mail technologies.

A full Cyrus IMAP implementation allows a seamless mail and bulletin
board environment to be set up across multiple servers. It differs from
other IMAP server implementations in that it is run on "sealed"
servers, where users are not normally permitted to log in and have no
system account on the server. The mailbox database is stored in parts
of the filesystem that are private to the Cyrus IMAP server. All user
access to mail is through software using the IMAP, POP3 or KPOP
protocols. It also includes support for virtual domains, NNTP,
mailbox annotations, and much more. The private mailbox database design
gives the server large advantages in efficiency, scalability and
administratability. Multiple concurrent read/write connections to the
same mailbox are permitted. The server supports access control lists on
mailboxes and storage quotas on mailbox hierarchies.

The Cyrus IMAP server supports the IMAP4rev1 protocol described
in RFC 3501. IMAP4rev1 has been approved as a proposed standard.
It supports any authentication mechanism available from the SASL
library, imaps/pop3s/nntps (IMAP/POP3/NNTP encrypted using SSL and
TLSv1) can be used for security. The server supports single instance
store where possible when an email message is addressed to multiple
recipients, SIEVE provides server side email filtering.

%package devel
Group: Development/Libraries
Summary: Cyrus IMAP server development files

%description devel
The %{name}-devel package contains header files and libraries
necessary for developing applications which use the imclient library.

%prep
%setup -q -n %{_name}-%{real_version}

%if 0%{?with_bdb} < 1
sed -i -e 's/,berkeley//g' cunit/db.testc
sed -r -i -e 's/"berkeley(|-[a-z-]+)", //g' lib/imapoptions
%endif

# only to update config.* files
autoreconf -vi || (libtoolize --force && autoreconf -vi)

# Modify docs master --> cyrus-master
%{__perl} -pi -e "s@master\(8\)@cyrus-master(8)@" man/*5 man/*8 lib/imapoptions
%{__sed} -i -e 's|\([^-]\)master|\1cyrus-master|g;s|^master|cyrus-master|g;s|Master|Cyrus-master|g;s|MASTER|CYRUS-MASTER|g' \
        man/master.8 doc/man.html

%if 0%{?rrzk}
# Modify docs httpd --> cyrus-httpd
%{__perl} -pi -e "s@httpd\(8\)@cyrus-httpd(8)@" man/*5 man/*8 lib/imapoptions
%{__sed} -i -e 's|\([^-]\)httpd|\1cyrus-httpd|g;s|^httpd|cyrus-httpd|g;s|Httpd|Cyrus-httpd|g;s|HTTPD|CYRUS-HTTPD|g' \
        man/httpd.8 doc/man.html
%endif

# Modify path in perl scripts
find . -type f -name "*.pl" | xargs %{__perl} -pi -e "s@/usr/local/bin/perl@%{__perl}@"

# modify lmtp socket path in .conf files
%{__perl} -pi -e "s@/var/imap/@%{_var}/lib/imap/@" master/conf/*.conf doc/cyrusv2.mc doc/m4/%{name}-sendmail-8.12.9-cyrusv2.m4

# enable idled in .conf files to prevent error messages
%{__perl} -pi -e "s/#  idled/  idled/" master/conf/*.conf

%build
CPPFLAGS="%{?optflags} -I%{_includedir}/et -I%{_includedir}/kerberosIV"; export CPPFLAGS
CFLAGS="%{?optflags} -fPIC"; export CFLAGS
CXXFLAGS="%{?optflags} -fPIC"; export CXXFLAGS
CCDLFLAGS="-rdynamic"; export CCDLFLAGS
%ifnarch ppc ppc64
LDFLAGS="$LDFLAGS -pie"; export LDFLAGS
%endif

%{configure} \
    --enable-event-notification \
    --enable-gssapi \
    --enable-idled \
    --enable-murder \
    --enable-netscapehack \
    --enable-nntp \
    --enable-replication \
    --enable-unit-tests \
%if 0
    --enable-xapian \
%endif
%if 0%{?with_bdb}
%if 0%{?fedora} >= 20 || 0%{?rhel} || 0%{?suse_version}
    --with-bdb-incdir=%{_includedir}/db4 \
%else
    --with-bdb-incdir=%{_includedir}/libdb4 \
%endif
%else
    --without-bdb \
%endif
    --with-cyrus-prefix=%{_cyrexecdir} \
    --with-extraident="RRZK-%{version}-%{release}" \
    --with-krbimpl=mit \
    --with-ldap=/usr \
%if 0%{?with_mysql}
    --with-mysql=%{_prefix} \
    --with-mysql-incdir=%{_includedir}/mysql/ \
    --with-mysql-libdir=%{_libdir}/mysql/ \
%endif
    --with-perl=%{__perl} \
%if 0%{?with_pgsql}
    --with-pgsql=%{_includedir} \
%endif
%if 0%{?rrzk}
    --build=x86_64-redhat-linux-gnu \
    --host=x86_64-redhat-linux-gnu \
    --target=x86_64-redhat-linux-gnu \
    --without-snmp \
    --enable-http \
    --with-syslogfacility=LOCAL6 \
    --disable-static \
%endif
    --with-service-path=%{_cyrexecdir} \

%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}

# Fix permissions on perl programs
find . -type f -name "*.pl" -exec %{__chmod} 755 {} \;

# Do what the regular make install does
%{__make} install DESTDIR=%{buildroot} PREFIX=%{_prefix} mandir=%{_mandir} INSTALLDIRS=vendor

# Install tools
for tool in tools/* ; do
  test -f ${tool} && %{__install} -m 755 ${tool} %{buildroot}%{_cyrexecdir}/
done

# Create directories
%{__install} -d \
  %{buildroot}%{_sysconfdir}/{logrotate.d,pam.d,cron.daily} \
  %{buildroot}%{_libdir}/sasl \
  %{buildroot}%{_var}/spool/imap \
  %{buildroot}%{_var}/lib/imap/{user,quota,proc,log,msg,socket,db,sieve,sync,md5,rpm,backup,meta} \
  %{buildroot}%{_var}/lib/imap/ptclient \
  %{buildroot}%{_sysconfdir}/pki/%{_name} \
  doc/contrib

# Install additional files
%{__install} -p -m 644 master/conf/prefork.conf %{buildroot}%{_sysconfdir}/cyrus.conf
%{__install} -p -m 644 %{SOURCE1}    %{buildroot}%{_sysconfdir}/imapd.conf
%{__install} -p -m 755 %{SOURCE2}   %{buildroot}%{_cyrexecdir}/cvt_cyrusdb_all
%{__install} -p -m 644 %{SOURCE3}   %{buildroot}%{_var}/lib/imap/rpm/magic
%{__install} -p -m 644 %{SOURCE11}    %{buildroot}%{_sysconfdir}/logrotate.d/%{_name}
%{__install} -p -m 644 %{SOURCE12}    %{buildroot}%{_sysconfdir}/pam.d/pop
%{__install} -p -m 644 %{SOURCE12}    %{buildroot}%{_sysconfdir}/pam.d/imap
%{__install} -p -m 644 %{SOURCE12}    %{buildroot}%{_sysconfdir}/pam.d/sieve
%{__install} -p -m 644 %{SOURCE12}    %{buildroot}%{_sysconfdir}/pam.d/mupdate
%{__install} -p -m 644 %{SOURCE12}    %{buildroot}%{_sysconfdir}/pam.d/lmtp
%{__install} -p -m 644 %{SOURCE12}    %{buildroot}%{_sysconfdir}/pam.d/nntp
%{__install} -p -m 644 %{SOURCE12}    %{buildroot}%{_sysconfdir}/pam.d/csync
%{__install} -p -m 755 %{SOURCE13}   %{buildroot}%{_sysconfdir}/cron.daily/%{_name}
%if 0%{?suse_version}
%{__install} -d %{buildroot}%{_localstatedir}/adm/fillup-templates/
%{__install} -p -m 644 %{SOURCE22}   %{buildroot}%{_localstatedir}/adm/fillup-templates/sysconfig.%{_name}
%else
%{__install} -d %{buildroot}%{_sysconfdir}/sysconfig/
%{__install} -p -m 644 %{SOURCE22}   %{buildroot}%{_sysconfdir}/sysconfig/%{_name}
%endif

%if 0%{?with_systemd}
%{__install} -p -D -m 644 %{SOURCE31}   %{buildroot}%{_unitdir}/cyrus-imapd.service
%{__install} -p -D -m 755 %{SOURCE32}   %{buildroot}%{_cyrexecdir}/cyr_systemd_helper
%else
%{__install} -d %{buildroot}%{_sysconfdir}/rc.d/init.d
%{__install} -p -m 755 %{SOURCE21}   %{buildroot}%{_sysconfdir}/rc.d/init.d/%{_name}
%endif

# Cleanup of doc dir
find doc perl -name CVS -type d | xargs -r %{__rm} -rf
find doc perl -name .cvsignore -type f | xargs -r %{__rm} -f
%{__rm} -f doc/Makefile.dist*
%{__rm} -f doc/text/Makefile
%{__rm} -rf doc/man

# fix permissions on perl .so files
find %{buildroot}%{perl_vendorarch} -type f -name "*.so" -exec %{__chmod} 755 {} \;

# fix conflicts with uw-imap
mv %{buildroot}%{_mandir}/man8/imapd.8 %{buildroot}%{_mandir}/man8/imapd.8cyrus
mv %{buildroot}%{_mandir}/man8/pop3d.8 %{buildroot}%{_mandir}/man8/pop3d.8cyrus

# Install templates
%{__install} -m 755 -d doc/conf
%{__install} -m 644 master/conf/*.conf doc/conf/

# Generate db config file
( grep '^{' lib/imapoptions | grep _db | grep -v _db_path | cut -d'"' -f 2,4 | \
  sed -e 's/^ *//' -e 's/-nosync//' -e 's/ *$//' -e 's/"/=/'
  echo sieve_version=2.2.3 ) | sort > %{buildroot}%{_var}/lib/imap/rpm/db.cfg

# create the ghost pem file
touch %{buildroot}%{ssl_pem_file}

# Rename 'master' binary and manpage to avoid clash with postfix
%{__mv} -f %{buildroot}%{_cyrexecdir}/master        %{buildroot}%{_cyrexecdir}/cyrus-master
%{__mv} -f %{buildroot}%{_mandir}/man8/master.8     %{buildroot}%{_mandir}/man8/cyrus-master.8

# Rename 'httpd' binary and manpage to avoid clash with apache httpd
%if 0%{?rrzk}
%{__mv} -f %{buildroot}%{_cyrexecdir}/httpd         %{buildroot}%{_cyrexecdir}/cyrus-httpd
%{__mv} -f %{buildroot}%{_mandir}/man8/httpd.8      %{buildroot}%{_mandir}/man8/cyrus-httpd.8
%endif

# Rename 'fetchnews' binary and manpage to avoid clash with leafnode
%{__mv} -f %{buildroot}%{_cyrexecdir}/fetchnews     %{buildroot}%{_cyrexecdir}/cyrfetchnews
%{__mv} -f %{buildroot}%{_mandir}/man8/fetchnews.8  %{buildroot}%{_mandir}/man8/cyrfetchnews.8
%{__perl} -pi -e 's|fetchnews|cyrfetchnews|g;s|Fetchnews|Cyrfetchnews|g;s/FETCHNEWS/CYRFETCHNEWS/g' \
        %{buildroot}%{_mandir}/man8/cyrfetchnews.8

# compress manpages
[ -x /usr/lib/rpm/brp-compress ] && /usr/lib/rpm/brp-compress

# remove executable bit from docs
for ddir in doc perl/imap/examples
do
  find $ddir -type f -exec %{__chmod} -x {} \;
done

# Remove installed but not packaged files
%{__rm} -f %{buildroot}%{_cyrexecdir}/not-mkdep
%{__rm} -f %{buildroot}%{_cyrexecdir}/config2header*
%{__rm} -f %{buildroot}%{_cyrexecdir}/config2man
%{__rm} -f %{buildroot}%{_cyrexecdir}/pop3proxyd
%{__rm} -f %{buildroot}%{_cyrexecdir}/htmlstrip.c
find %{buildroot} -type f -name "perllocal.pod" -exec %{__rm} -vf {} \;
find %{buildroot} -type f -name ".packlist" -exec %{__rm} -vf {} \;
find %{buildroot} -type f -name ".gitignore" -exec %{__rm} -vf {} \;
%{__rm} -f %{buildroot}%{_mandir}/man8/syncnews.8*
find %{buildroot}%{perl_vendorarch} -type f -name "*.bs" -exec %{__rm} -vf {} \;

%check
make check || :

%clean
%{__rm} -rf %{buildroot}

%pre
# Create 'cyrus' user on target host
/usr/sbin/groupadd -g %{gid} -r saslauth 2> /dev/null || :
/usr/sbin/useradd -c "Cyrus IMAP Server" -d %{_var}/lib/imap -g %{_cyrusgroup} \
  -G saslauth -s /sbin/nologin -u %{uid} -r %{_cyrususer} 2> /dev/null || :

%post
%if 0%{?suse_version}
/sbin/ldconfig
%endif

CHATTRSYNC=0

%if 0%{?suse_version}
%if 0%{?with_systemd}
    %fillup_only %{_name}
%else
    %fillup_and_insserv %{_name}
%endif
if [[ ! -e "%{_sysconfdir}/pam.d/runuser" ]]; then
    ln -s %{_sysconfdir}/pam.d/su %{_sysconfdir}/pam.d/runuser
fi
if [[ ! -e "%{_sysconfdir}/pam.d/runuser-l" ]]; then
    ln -s %{_sysconfdir}/pam.d/su-l %{_sysconfdir}/pam.d/runuser-l
fi
%endif

if [ -f "%{_sysconfdir}/sysconfig/cyrus-imapd" ]; then
    source %{_sysconfdir}/sysconfig/cyrus-imapd
fi

if [ $CHATTRSYNC -eq 1 ]; then
    # Force synchronous updates of files in the following directories
    chattr -R +S \
        $(grep ^configdirectory: /etc/imapd.conf | cut -d':' -f2) \
        $(grep ^partition- /etc/imapd.conf | cut -d':' -f2) \
        $(grep ^metapartition- /etc/imapd.conf | cut -d':' -f2) 2>/dev/null ||:
fi

# Create SSL certificates
exec > /dev/null 2> /dev/null

if [ ! -z "%{ssl_pem_file}" -a -z "$(cat %{ssl_pem_file})" ]; then
    %{__rm} -f "%{ssl_pem_file}" || :
fi

if [ ! -f %{ssl_pem_file} -a -d "%{_sysconfdir}/pki/tls/certs" ]; then
    pushd %{_sysconfdir}/pki/tls/certs
    umask 077
    %{__cat} << EOF | make %{_name}.pem
--
SomeState
SomeCity
SomeOrganization
SomeOrganizationalUnit
localhost.localdomain
root@localhost.localdomain
EOF

    %{__chown} root.%{_cyrusgroup} %{_name}.pem
    %{__chmod} 640 %{_name}.pem
    mv %{_name}.pem %{ssl_pem_file}
    popd
fi

%if 0%{?with_systemd}
%if 0%{?suse_version}
    %service_add_post cyrus-imapd.service
%else
    %systemd_post cyrus-imapd.service
%endif
%else
    /sbin/chkconfig --add %{_name}
%endif

%preun
%if 0%{?with_systemd}
%if 0%{?suse_version}
    %service_del_preun cyrus-imapd.service
%else
    %systemd_preun cyrus-imapd.service >/dev/null 2>&1 || :
%endif
%else
    if [ $1 = 0 ]; then
        /sbin/service %{_name} stop >/dev/null 2>&1 || :
        /sbin/chkconfig --del %{_name}
    fi
%endif

%postun
%if 0%{?suse_version}
/sbin/ldconfig
%endif

%if 0%{?with_systemd}
%if 0%{?suse_version}
    %service_del_postun cyrus-imapd.service
%else
    %systemd_postun_with_restart cyrus-imapd.service
%endif
%else
    if [ $1 != 0 ]; then
        /sbin/service %{_name} condrestart >/dev/null 2>&1 || :
    fi
%endif

%files
%defattr(-,root,root,-)
%doc COPYING README
%doc doc/*
%config(noreplace) %{_sysconfdir}/cyrus.conf
%config(noreplace) %{_sysconfdir}/imapd.conf
%if 0%{?with_systemd}
%{_unitdir}/cyrus-imapd.service
%{_cyrexecdir}/cyr_systemd_helper
%else
%{_sysconfdir}/rc.d/init.d/%{_name}
%endif
%dir %{_sysconfdir}/pki
%config(noreplace) %{_sysconfdir}/logrotate.d/%{_name}
%if 0%{?suse_version}
%config(noreplace) %{_localstatedir}/adm/fillup-templates/sysconfig.%{_name}
%else
%attr(0640,root,%{_cyrusgroup}) %config(noreplace) %{_sysconfdir}/sysconfig/%{_name}
%endif
%config(noreplace) %{_sysconfdir}/pam.d/pop
%config(noreplace) %{_sysconfdir}/pam.d/imap
%config(noreplace) %{_sysconfdir}/pam.d/sieve
%config(noreplace) %{_sysconfdir}/pam.d/lmtp
%config(noreplace) %{_sysconfdir}/pam.d/mupdate
%config(noreplace) %{_sysconfdir}/pam.d/csync
%config(noreplace) %{_sysconfdir}/pam.d/nntp
%attr(0755,root,root) %{_bindir}/cyradm
%{_bindir}/imtest
%{_bindir}/installsieve
%{_bindir}/lmtptest
%{_bindir}/mupdatetest
%{_bindir}/nntptest
%{_bindir}/pop3test
%{_bindir}/sieveshell
%{_bindir}/sivtest
%{_bindir}/smtptest
%{_bindir}/synctest
%{_sysconfdir}/cron.daily/%{_name}
%dir %{_cyrexecdir}
%{_cyrexecdir}/arbitron
%{_cyrexecdir}/arbitronsort.pl
%{_cyrexecdir}/chk_cyrus
%{_cyrexecdir}/compile_st.pl
%{_cyrexecdir}/convert-sieve.pl
%{_cyrexecdir}/cyr_deny
%{_cyrexecdir}/cyr_df
%{_cyrexecdir}/cyr_info
#%{_cyrexecdir}/ctl_conversationsdb
%{_cyrexecdir}/ctl_cyrusdb
%{_cyrexecdir}/ctl_deliver
%{_cyrexecdir}/ctl_mboxlist
%{_cyrexecdir}/cvt_cyrusdb
%{_cyrexecdir}/cyr_dbtool
%{_cyrexecdir}/cyr_expire
%{_cyrexecdir}/cyr_sequence
%{_cyrexecdir}/cyr_synclog
%{_cyrexecdir}/cyr_userseen
%{_cyrexecdir}/cyrdump
%if 0%{?rrzk}
%{_cyrexecdir}/cyrus-httpd
%{_cyrexecdir}/dav_reconstruct
%{_cyrexecdir}/ctl_zoneinfo
%endif
%{_cyrexecdir}/cyrus-master
%{_cyrexecdir}/deliver
%{_cyrexecdir}/dohash
%{_cyrexecdir}/fixsearchpath.pl
%{_cyrexecdir}/fud
#%{_cyrexecdir}/hammer_cyrusdb
%{_cyrexecdir}/imapd
%{_cyrexecdir}/ipurge
%exclude %{_cyrexecdir}/jenkins-build.sh
%{_cyrexecdir}/lmtpd
%{_cyrexecdir}/lmtpproxyd
%{_cyrexecdir}/masssievec
%{_cyrexecdir}/mbexamine
%{_cyrexecdir}/mbpath
%{_cyrexecdir}/mbtool
#%{_cyrexecdir}/message_test
%{_cyrexecdir}/migrate-metadata
%{_cyrexecdir}/mkimap
%{_cyrexecdir}/mknewsgroups
%{_cyrexecdir}/notifyd
%{_cyrexecdir}/pop3d
%{_cyrexecdir}/quota
%{_cyrexecdir}/reconstruct
%{_cyrexecdir}/rehash
#%{_cyrexecdir}/search_test
%{_cyrexecdir}/sievec
%{_cyrexecdir}/sieved
%{_cyrexecdir}/smmapd
#%{_cyrexecdir}/squat_dump
%{_cyrexecdir}/squatter
%{_cyrexecdir}/timsieved
%{_cyrexecdir}/tls_prune
%{_cyrexecdir}/translatesieve
%{_cyrexecdir}/undohash
%{_cyrexecdir}/unexpunge
%{_cyrexecdir}/upgradesieve
%{_cyrexecdir}/cvt_cyrusdb_all
%{_cyrexecdir}/idled
%{_cyrexecdir}/mupdate
%{_cyrexecdir}/mupdate-loadgen.pl
%{_cyrexecdir}/proxyd
%{_cyrexecdir}/sync_client
%{_cyrexecdir}/sync_reset
%{_cyrexecdir}/sync_server
%{_cyrexecdir}/cyrfetchnews
%{_cyrexecdir}/nntpd
%{_cyrexecdir}/ptdump
%{_cyrexecdir}/ptexpire
%{_cyrexecdir}/ptloader
%attr(0750,%{_cyrususer},%{_cyrusgroup}) %dir %{_var}/lib/imap
%attr(0750,%{_cyrususer},%{_cyrusgroup}) %dir %{_var}/lib/imap/backup
%attr(0750,%{_cyrususer},%{_cyrusgroup}) %dir %{_var}/lib/imap/db
%attr(0750,%{_cyrususer},%{_cyrusgroup}) %dir %{_var}/lib/imap/log
%attr(0750,%{_cyrususer},%{_cyrusgroup}) %dir %{_var}/lib/imap/meta
%attr(0750,%{_cyrususer},%{_cyrusgroup}) %dir %{_var}/lib/imap/md5
%attr(0750,%{_cyrususer},%{_cyrusgroup}) %dir %{_var}/lib/imap/msg
%attr(0750,%{_cyrususer},%{_cyrusgroup}) %{_var}/lib/imap/proc
%attr(0750,%{_cyrususer},%{_cyrusgroup}) %{_var}/lib/imap/ptclient
%attr(0750,%{_cyrususer},%{_cyrusgroup}) %dir %{_var}/lib/imap/quota
%attr(0750,%{_cyrususer},%{_cyrusgroup}) %dir %{_var}/lib/imap/rpm
%attr(0750,%{_cyrususer},%{_cyrusgroup}) %dir %{_var}/lib/imap/sieve
%attr(0750,%{_cyrususer},%{_cyrusgroup}) %{_var}/lib/imap/socket
%attr(0750,%{_cyrususer},%{_cyrusgroup}) %dir %{_var}/lib/imap/sync
%attr(0750,%{_cyrususer},%{_cyrusgroup}) %dir %{_var}/lib/imap/user
%attr(0750,%{_cyrususer},%{_cyrusgroup}) %dir %{_var}/spool/imap
%{_libdir}/*.so.*
%{_var}/lib/imap/rpm/*
%doc perl/imap/README
%doc perl/imap/Changes
%doc perl/imap/examples
%dir %{perl_vendorarch}/Cyrus
%dir %{perl_vendorarch}/Cyrus/IMAP
%{perl_vendorarch}/Cyrus/IMAP/Admin.pm
%{perl_vendorarch}/Cyrus/IMAP/Shell.pm
%{perl_vendorarch}/Cyrus/IMAP/IMSP.pm
%{perl_vendorarch}/Cyrus/IMAP.pm
%dir %{perl_vendorarch}/Cyrus/SIEVE
%{perl_vendorarch}/Cyrus/SIEVE/managesieve.pm
%dir %{perl_vendorlib}/Cyrus/
%dir %{perl_vendorlib}/Cyrus/Annotator
%{perl_vendorlib}/Cyrus/Annotator/Daemon.pm
%{perl_vendorlib}/Cyrus/Annotator/Message.pm
%dir %{perl_vendorarch}/auto
%dir %{perl_vendorarch}/auto/Cyrus
%dir %{perl_vendorarch}/auto/Cyrus/IMAP
%{perl_vendorarch}/auto/Cyrus/IMAP/IMAP.so
%dir %{perl_vendorarch}/auto/Cyrus/SIEVE
%dir %{perl_vendorarch}/auto/Cyrus/SIEVE/managesieve
%{perl_vendorarch}/auto/Cyrus/SIEVE/managesieve/managesieve.so
%{_mandir}/man1/*
%{_mandir}/man3/*
%{_mandir}/man5/*
%{_mandir}/man8/*
%dir %{_sysconfdir}/pki/%{_name}
%attr(0640,root,%{_cyrusgroup}) %ghost %config(missingok,noreplace) %verify(not md5 size mtime) %{ssl_pem_file}

%files devel
%defattr(0644,root,root,0755)
%files devel
%defattr(0644,root,root,0755)
%{_includedir}/cyrus
%{_libdir}/pkgconfig/*cyrus*.pc
%{_libdir}/*.so
%{_libdir}/*.la

%changelog
* Fri Jul 29 2016 Sebastian Hagedorn <Hagedorn@uni-koeln.de> 2.5.9-1.RRZK
- ? (Hagedorn@uni-koeln.de)
- doh (Hagedorn@uni-koeln.de)
- Revision 2 (Hagedorn@uni-koeln.de)
- SOURCES (apparently) need to be in root directory for tito (Hagedorn@uni-
  koeln.de)

* Fri Jul 29 2016 Sebastian Hagedorn <Hagedorn@uni-koeln.de>
- Revision 2 (Hagedorn@uni-koeln.de)
- SOURCES (apparently) need to be in root directory for tito (Hagedorn@uni-
  koeln.de)

* Fri Jul 29 2016 Sebastian Hagedorn <Hagedorn@uni-koeln.de>
- SOURCES (apparently) need to be in root directory for tito (Hagedorn@uni-
  koeln.de)

* Fri Jul 29 2016 Sebastian Hagedorn <Hagedorn@uni-koeln.de> 2.5.9-1
- new package built with tito

* Fri Jul 29 2016 Unknown name 2.5.9-1
- new package built with tito

* Fri Jul 29 2016 Sebastian Hagedorn <Hagedorn@uni-koeln.de> - 2.5.9-1
- bump
* Fri Feb 05 2016 Sebastian Hagedorn <Hagedorn@uni-koeln.de> - 2.5.7-1
- bump

* Wed May 13 2015 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 2.5.2.3-1
- Check in 2 revisions ahead of new upstream release 2.5.2

* Tue May 12 2015 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 2.5.2.1-1
- Check in 1 revision ahead of new upstream release 2.5.2

* Tue Apr 28 2015 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 2.5.1-19.1
- Check in 19 revisions ahead of new upstream release 2.5.1

* Mon Apr 27 2015 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 2.5.1-5.1
- Check in 5 revisions ahead of new upstream release 2.5.1

* Sat Apr 11 2015 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 2.5.0-65.1
- Check in 65 revisions ahead of new upstream release 2.5.0

* Fri Mar 20 2015 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 2.5.0-45.1
- Check in 45 revisions ahead of new upstream release 2.5.0

* Tue Mar 10 2015 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 2.5.0-30.1
- Check in 30 revisions ahead of new upstream release 2.5.0

* Fri Feb 13 2015 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 2.5-12.git
- New snapshot

* Tue Dec  9 2014 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 2.5-11.git
- Fix Murder topologies not handling null ACLs at all

* Thu Sep 25 2014 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 2.5-10.git
- Fix event notifications

* Fri Aug 29 2014 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 2.5-9.git
- Snapshot of (b2ef80be)
- Merge enhanced Sieve Date and Index extension

* Mon Mar  3 2014 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 2.5-8.git
- Fix shared folder deleted namespace prefix

* Tue Mar 12 2013 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 2.4.17-2
- Refresh patch for normalization of the UID - actually enable disabling it

* Sat Dec  1 2012 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 2.4.17-1
- New upstream version

* Wed Nov 21 2012 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 2.4.15-2
- Ship fix for APPEND BINARY GUID (#3754)

* Thu Apr 15 2012 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 2.4.15-1
- New upstream version

* Mon Apr 15 2012 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 2.4.15-0.1
- Pre-release of 2.4.15

* Wed Mar 14 2012 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 2.4.14-1
- New upstream version

* Mon Jan 02 2012 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 2.4.13-1
- New upstream version

* Wed Oct 26 2011 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 2.4.12-1
- New upstream version

* Wed Sep 14 2011 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 2.4.11-2
- Fix #3553: QRESYNC parentheses missing when forwarding command to backends.

* Fri Sep  9 2011 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 2.4.11-1
- http://www.cyrusimap.org/mediawiki/index.php/Bugs_Resolved_in_2.4.11
- Fix CVE-2011-3208 (remote buffer overflow exploit in nntpd)

* Sun Jul 17 2011 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 2.4.10-3
- Ship first version of LDAP ptclient canonification

* Tue Jul 12 2011 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 2.4.10-2
- Fix quota legacy bugs (Bron Gondwana)
- Fix sync when message appears on both sides (Greg Banks)

* Wed Jul  6 2011 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 2.4.10-1
- New upstream version

* Thu Jun 15 2011 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 2.4.9-0.2
- Rebuild with fewer dependencies

* Sun May 08 2011 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 2.4.9-0.1
- Add in the post 2.4.8 patches from the cyrus-imapd-2.4 branch

* Sun May 01 2011 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 2.4.8-2
- Add QUICK setting to sysconfig and make init.d honor it
- Fix pam to include system-auth rather then password-auth

* Fri Apr 15 2011 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 2.4.8-1
- New upstream release

* Mon Jan 10 2011 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 2.4.6-1
- New upstream release

* Sun Nov 14 2010 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 2.4.4-1
- New upstream release

* Wed Nov 10 2010 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 2.4.3-1
- New upstream release

* Wed Oct 20 2010 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 2.4.2-1
- New upstream release

* Mon Oct 11 2010 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 2.4.0-0.5.alpha1.20101011
- Rebase onto latest dev/2.4.0-alpha1
- Attempt to enable SQL backends for most databases
- Enable the mysql / postgresql db backend engines by including brs (0.3)
- Incorporate the latest changes (0.2)
- Build from new upstream tarball (git archive)
- New upstream version, pre-release (0.1)

* Tue Aug  3 2010 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 2.3.19-3.1
- Strip out changelog history from before 2009
- Rebuild with sane patches only

* Tue Apr 20 2010 Michal Hlavinka <mhlavink@redhat.com> - 2.3.19-3
- add support for QoS marked traffic (#576752)

* Thu Jan 14 2010 Michal Hlavinka <mhlavink@redhat.com> - 2.3.19-2
- ignore user_denny.db if missing (#553011)
- fix location of certificates in default imapd.conf

* Tue Dec 22 2009 Michal Hlavinka <mhlavink@redhat.com> - 2.3.19-1
- updated to 2.3.19

* Fri Dec 04 2009 Michal Hlavinka <mhlavink@redhat.com> - 2.3.15-10
- fix shell for daily cron job (#544182)

* Fri Dec 04 2009 Stepan Kasal <skasal@redhat.com> - 2.3.15-9
- rebuild against perl 5.10.1

* Thu Nov 26 2009 Michal Hlavinka <mhlavink@redhat.com> - 2.3.15-8
- spec cleanup

* Tue Nov 24 2009 Michal Hlavinka <mhlaivnk@redhat.com> - 2.3.15-7
- rebuild with new db4 (#540093)
- spec cleanup

* Fri Nov 06 2009 Michal Hlavinka <mhlavink@redhat.com> - 2.3.15-6
- fix sourcing of /etc/sysconfig/cyrus-imapd (#533320)

* Thu Nov 05 2009 Michal Hlavinka <mhlavink@redhat.com> - 2.3.15-5
- do not fill logs with mail (de)compression messages (#528093)

* Thu Oct 29 2009 Michal Hlavinka <mhlavink@redhat.com> - 2.3.15-4
- spec cleanup

* Fri Oct 09 2009 Michal Hlavinka <mhlavink@redhat.com> - 2.3.15-3
- fix cyrus user shell for db import (#528126)

* Fri Sep 18 2009 Michal Hlavinka <mhlavink@redhat.com> - 2.3.15-2
- make init script LSB-compliant (#523227)

* Fri Sep 18 2009 Michal Hlavinka <mhlavink@redhat.com> - 2.3.15-1
- fix buffer overflow in cyrus sieve (CVE-2009-3235)

* Wed Sep 15 2009 Tomas Mraz <tmraz@redhat.com> - 2.3.14-6
- use password-auth common PAM configuration instead of system-auth

* Mon Sep 07 2009 Michal Hlavinka <mhlavink@redhat.com> - 2.3.14-5
- fix buffer overflow in cyrus sieve (#521010)

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 2.3.14-4
- rebuilt with new openssl

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.14-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon May 25 2009 Michal Hlavinka <mhlavink@redhat.com> - 2.3.14-2
- rebuild because of changed dependencies

* Thu Apr 02 2009 Michal Hlavinka <mhlavink@redhat.com> - 2.3.14-1
- updated to 2.3.14

* Wed Apr 01 2009 Michael Schwendt <mschwendt@fedoraproject.org> - 2.3.13-5
- fix unowned directory (#491336).

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.13-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 02 2009 Michal Hlavinka <mhlavink@rehdat.com> - 2.3.13-3
- fix directory ownership

* Wed Jan 21 2009 Michal Hlavinka <mhlavink@redhat.com> - 2.3.13-2
- fix: #480138 - assertion failed: libcyr_cfg.c: cyrus_options[opt].opt == opt

* Tue Jan 13 2009 Michal Hlavinka <mhlavink@redhat.com> - 2.3.13-1
- updated to 2.3.13
