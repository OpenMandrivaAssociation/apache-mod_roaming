#Module-Specific definitions
%define mod_name mod_roaming
%define mod_conf 18_%{mod_name}.conf
%define mod_so %{mod_name}.so

Summary:	Enables Netscape Communicator roaming profiles with apache
Name:		apache-%{mod_name}
Version:	2.0.0
Release:	%mkrel 8
Group:		System/Servers
License:	BSD-style
URL:		http://www.klomp.org/mod_roaming/
Source0:	%{mod_name}-%{version}.tar.bz2
Source1:	%{mod_conf}.bz2
Patch:		%{mod_name}-register.patch
Requires(pre): rpm-helper
Requires(postun): rpm-helper
Requires(pre):	apache-conf >= 2.2.0
Requires(pre):	apache >= 2.2.0
Requires:	apache-conf >= 2.2.0
Requires:	apache >= 2.2.0
BuildRequires:	apache-devel >= 2.2.0
BuildRequires:	file
Epoch:		1
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
With mod_roaming you can use your apache webserver as a
Netscape Roaming Access server. This allows you to store your
Netscape Communicator 4.5 preferences, bookmarks, address books,
cookies etc. on the server so that you can use (and update) the
same settings from any Netscape Communicator 4.5 that can access
the server. 

%prep

%setup -q -n %{mod_name}-%{version}
%patch

# strip away annoying ^M
find . -type f|xargs file|grep 'CRLF'|cut -d: -f1|xargs perl -p -i -e 's/\r//'
find . -type f|xargs file|grep 'text'|cut -d: -f1|xargs perl -p -i -e 's/\r//'

%build

%{_sbindir}/apxs -c mod_roaming.c


%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

install -d %{buildroot}%{_libdir}/apache-extramodules
install -d %{buildroot}%{_sysconfdir}/httpd/modules.d
install -d %{buildroot}/var/lib/mod_roaming

install -m0755 .libs/*.so %{buildroot}%{_libdir}/apache-extramodules/
bzcat %{SOURCE1} > %{buildroot}%{_sysconfdir}/httpd/modules.d/%{mod_conf}

install -d %{buildroot}%{_var}/www/html/addon-modules
ln -s ../../../..%{_docdir}/%{name}-%{version} %{buildroot}%{_var}/www/html/addon-modules/%{name}-%{version}

%post
if [ -f %{_var}/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart 1>&2;
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f %{_var}/lock/subsys/httpd ]; then
	%{_initrddir}/httpd restart 1>&2
    fi
fi

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc CHANGES INSTALL LICENSE README
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/%{mod_conf}
%attr(0755,root,root) %{_libdir}/apache-extramodules/%{mod_so}
%{_var}/www/html/addon-modules/*
%attr(-,apache,apache) %dir /var/lib/mod_roaming


