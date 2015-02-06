#Module-Specific definitions
%define mod_name mod_roaming
%define mod_conf 18_%{mod_name}.conf
%define mod_so %{mod_name}.so

Summary:	Enables Netscape Communicator roaming profiles with apache
Name:		apache-%{mod_name}
Version:	2.0.0
Release:	15
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

%{_bindir}/apxs -c mod_roaming.c


%install

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

%files
%doc CHANGES INSTALL LICENSE README
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/%{mod_conf}
%attr(0755,root,root) %{_libdir}/apache-extramodules/%{mod_so}
%{_var}/www/html/addon-modules/*
%attr(-,apache,apache) %dir /var/lib/mod_roaming




%changelog
* Sat Feb 11 2012 Oden Eriksson <oeriksson@mandriva.com> 1:2.0.0-14mdv2012.0
+ Revision: 772753
- rebuild

* Tue May 24 2011 Oden Eriksson <oeriksson@mandriva.com> 1:2.0.0-13
+ Revision: 678407
- mass rebuild

* Sun Oct 24 2010 Oden Eriksson <oeriksson@mandriva.com> 1:2.0.0-12mdv2011.0
+ Revision: 588053
- rebuild

* Mon Mar 08 2010 Oden Eriksson <oeriksson@mandriva.com> 1:2.0.0-11mdv2010.1
+ Revision: 516169
- rebuilt for apache-2.2.15

* Sat Aug 01 2009 Oden Eriksson <oeriksson@mandriva.com> 1:2.0.0-10mdv2010.0
+ Revision: 406640
- rebuild

* Tue Jan 06 2009 Oden Eriksson <oeriksson@mandriva.com> 1:2.0.0-9mdv2009.1
+ Revision: 326227
- rebuild

* Mon Jul 14 2008 Oden Eriksson <oeriksson@mandriva.com> 1:2.0.0-8mdv2009.0
+ Revision: 235075
- rebuild

* Thu Jun 05 2008 Oden Eriksson <oeriksson@mandriva.com> 1:2.0.0-7mdv2009.0
+ Revision: 215626
- fix rebuild
- hard code %%{_localstatedir}/lib to ease backports

  + Pixel <pixel@mandriva.com>
    - adapt to %%_localstatedir now being /var instead of /var/lib (#22312)

* Fri Mar 07 2008 Oden Eriksson <oeriksson@mandriva.com> 1:2.0.0-6mdv2008.1
+ Revision: 181857
- rebuild

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Sat Sep 08 2007 Oden Eriksson <oeriksson@mandriva.com> 1:2.0.0-5mdv2008.0
+ Revision: 82665
- rebuild


* Sat Mar 10 2007 Oden Eriksson <oeriksson@mandriva.com> 2.0.0-4mdv2007.1
+ Revision: 140734
- rebuild

* Thu Nov 09 2006 Oden Eriksson <oeriksson@mandriva.com> 1:2.0.0-3mdv2007.1
+ Revision: 79493
- Import apache-mod_roaming

* Mon Aug 07 2006 Oden Eriksson <oeriksson@mandriva.com> 1:2.0.0-3mdv2007.0
- rebuild

* Fri Dec 16 2005 Oden Eriksson <oeriksson@mandriva.com> 1:2.0.0-2mdk
- rebuilt against apache-2.2.0

* Mon Nov 28 2005 Oden Eriksson <oeriksson@mandriva.com> 1:2.0.0-1mdk
- fix versioning

* Sun Jul 31 2005 Oden Eriksson <oeriksson@mandriva.com> 2.0.54_2.0.0-2mdk
- fix deps

* Fri Jun 03 2005 Oden Eriksson <oeriksson@mandriva.com> 2.0.54_2.0.0-1mdk
- rename the package
- the conf.d directory is renamed to modules.d
- use new rpm-4.4.x pre,post magic

* Sun Mar 20 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.53_2.0.0-4mdk
- use the %1

* Mon Feb 28 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.53_2.0.0-3mdk
- fix %%post and %%postun to prevent double restarts
- fix bug #6574

* Wed Feb 16 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.53_2.0.0-2mdk
- spec file cleanups, remove the ADVX-build stuff

* Tue Feb 08 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.53_2.0.0-1mdk
- rebuilt for apache 2.0.53

* Wed Sep 29 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.52_2.0.0-1mdk
- built for apache 2.0.52

* Fri Sep 17 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.51_2.0.0-1mdk
- built for apache 2.0.51

* Tue Jul 13 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.50_2.0.0-1mdk
- built for apache 2.0.50
- remove redundant provides

* Tue Jun 15 2004 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.49_2.0.0-1mdk
- built for apache 2.0.49

