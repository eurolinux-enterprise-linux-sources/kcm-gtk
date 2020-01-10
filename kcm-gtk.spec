
# Fedora package review: http://bugzilla.redhat.com/530342

Summary: Configure the appearance of GTK apps in KDE 
Name:    kcm-gtk 
Version: 0.5.3
Release: 12%{?dist}

License: GPLv2+
Group:   User Interface/Desktops
URL:     https://launchpad.net/kcm-gtk 
Source0: http://launchpad.net/kcm-gtk/0.5.x/%{version}/+download/kcm-gtk_%{version}.orig.tar.gz 
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n) 

## upstreamable patches
# fix so it appears in systemsettings, not Lost+Found
Patch50: kcm-gtk-0.5.3-settings_category.patch
# ensures GTK2_RC_FILES gets used/updated on first use, avoids 
# possible need for logout/login, code borrowed from kdebase-workspace's krdb.cpp
Patch51: kcm-gtk-0.5.3-gtkrc_setenv.patch
# fix missing umlauts and sharp s in the German translation
# The translations need a lot more fixing than that, but this looks very broken!
Patch52: kcm-gtk-0.5.3-fix-de.patch
# http://bazaar.launchpad.net/~ubuntu-branches/ubuntu/precise/kcm-gtk/precise/view/head:/debian/patches/kubuntu_01_xsettings_kipc.patch
Patch53: kubuntu_01_xsettings_kipc.patch

## upstream patches

BuildRequires: gettext
BuildRequires: kdelibs4-devel

# need kcmshell4 from kdebase-runtime at least
Requires: kdebase-runtime%{?_kde4_version: >= %{_kde4_version}}

%description
This is a System Settings configuration module for configuring the
appearance of GTK apps in KDE.

%prep
%setup -q 

%patch50 -p1 -b .settings_category
%patch51 -p1 -b .gtkrc_setenv
%patch52 -p1 -b .fix-de
%patch53 -p1 -b .xsettings_kipc

%if "%{?_kde4_version}" > "4.5.0"
# fixup for kde-4.5, see http://bugzilla.redhat.com/628381
sed -i.kde45 -e 's|^X-KDE-System-Settings-Parent-Category=appearance$|X-KDE-System-Settings-Parent-Category=application-appearance|' \
  kcmgtk.desktop
%endif


%build

mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kde4} ..
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
rm -rf %{buildroot} 

make install/fast DESTDIR=%{buildroot} -C %{_target_platform}

%find_lang kcm_gtk


%clean
rm -rf %{buildroot} 


%files -f kcm_gtk.lang
%defattr(-,root,root,-)
%doc Changelog COPYING
%{_kde4_libdir}/kde4/kcm_gtk.so
%{_kde4_iconsdir}/kcm_gtk.png
%{_kde4_datadir}/kde4/services/kcmgtk.desktop


%changelog
* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.3-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.3-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon May 14 2012 Rex Dieter <rdieter@fedoraproject.org>
- 0.5.3-10
- update kcm_category patch
- kubuntu_01_xsettings_kipc.patch
- drop old Obsoletes: gtk-qt-engine

* Tue Jan 17 2012 Kevin Kofler <Kevin@tigcc.ticalc.org> 0.5.3-9
- drop gtk3 patch again, the new plan is to handle this through xsettings-kde

* Fri Jan 06 2012 Kevin Kofler <Kevin@tigcc.ticalc.org> 0.5.3-8
- add support for GTK+ 3 (backported from upstream bzr gtk3 branch)
- drop ancient Fedora < 13 env_script conditional, now always in kde-settings

* Mon Mar 14 2011 Kevin Kofler <Kevin@tigcc.ticalc.org> 0.5.3-7
- drop cursortheme patch, now set automatically by xsettings-kde (#591746)

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> 0.5.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Sep 08 2010 Rex Dieter <rdieter@fedoraproject.org> 0.5.3-5
- kcm-gtk : "GTK+ Appearance" in systemsettings->lost and found (#628381)
- Requires: kdebase-runtime

* Wed Jul  7 2010 Ville Skyttä <ville.skytta@iki.fi> 0.5.3-4
- Apply modified upstream patch to add cursor theme support (#600976).

* Fri Dec 25 2009 Rex Dieter <rdieter@fedoraproject.org> 0.5.3-3
- GTK2_RC_FILES handling moved to kde-settings (#547700)

* Sun Dec 20 2009 Kevin Kofler <Kevin@tigcc.ticalc.org> 0.5.3-2
- fix missing umlauts and sharp s in the German translation

* Fri Oct 30 2009 Rex Dieter <rdieter@fedoraproject.org> 0.5.3-1
- kcm-gtk-0.5.3
- .gtkrc-2.0-kde4 doesn't get used (#531788)

* Thu Oct 22 2009 Rex Dieter <rdieter@fedoraproject.org> 0.5.1-2
- Requires: kde4-macros(api)...

* Thu Oct 22 2009 Rex Dieter <rdieter@fedoraproject.org> 0.5.1-1
- kcm-gtk-0.5.1 (first try)

