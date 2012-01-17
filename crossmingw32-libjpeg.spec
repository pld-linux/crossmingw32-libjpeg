%define		realname	libjpeg
Summary:	Library for handling different jpeg files - MinGW32 cross version
Summary(pl.UTF-8):	Biblioteka do manipulacji plikami w formacie jpeg - wersja skrośna dla MinGW32
Name:		crossmingw32-%{realname}
Version:	8d
Release:	1
License:	distributable
Group:		Development/Libraries
Source0:	http://www.ijg.org/files/jpegsrc.v%{version}.tar.gz
# Source0-md5:	52654eb3b2e60c35731ea8fc87f1bd29
Patch0:		%{realname}-maxmem-sysconf.patch
URL:		http://www.ijg.org/
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
BuildRequires:	crossmingw32-gcc
BuildRequires:	libtool
Requires:	crossmingw32-runtime
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		no_install_post_strip	1

%define		target			i386-mingw32
%define		target_platform 	i386-pc-mingw32

%define		_sysprefix		/usr
%define		_prefix			%{_sysprefix}/%{target}
%define		_libdir			%{_prefix}/lib
%define		_dlldir			/usr/share/wine/windows/system
%define		__cc			%{target}-gcc
%define		__cxx			%{target}-g++

%ifnarch %{ix86}
# arch-specific flags (like alpha's -mieee) are not valid for i386 gcc
%define		optflags	-O2
%endif
# -z options are invalid for mingw linker
%define		filterout_ld	-Wl,-z,.*

%description
The libjpeg package contains a library of functions for manipulating
JPEG images.

This package contains the cross version for Win32.

%description -l pl.UTF-8
Ten pakiet zawiera bibliotekę funkcji do manipulacji plikami jpeg.

Ten pakiet zawiera wersję skrośną dla Win32.

%package static
Summary:	Static libjpeg library (cross MinGW32 version)
Summary(pl.UTF-8):	Statyczna biblioteka libjpeg (wersja skrośna MinGW32)
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description static
Static libjpeg library (cross MinGW32 version).

%description static -l pl.UTF-8
Statyczna biblioteka libjpeg (wersja skrośna MinGW32).

%package dll
Summary:	libjpeg - DLL library for Windows
Summary(pl.UTF-8):	libjpeg - biblioteka DLL dla Windows
Group:		Applications/Emulators
Requires:	wine

%description dll
libjpeg - DLL library for Windows.

%description dll -l pl.UTF-8
libjpeg - biblioteka DLL dla Windows.

%prep
%setup -q -n jpeg-%{version}
%patch0 -p1

%build
%configure \
	--target=%{target} \
	--host=%{target} \
	--disable-silent-rules

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install jversion.h $RPM_BUILD_ROOT%{_includedir}

# remove HAVE_STD{DEF,LIB}_H
# (not necessary but may generate warnings confusing autoconf)
sed -i -e 's#.*HAVE_STD..._H.*##g' $RPM_BUILD_ROOT%{_includedir}/jconfig.h

install -d $RPM_BUILD_ROOT%{_dlldir}
mv -f $RPM_BUILD_ROOT%{_prefix}/bin/*.dll $RPM_BUILD_ROOT%{_dlldir}

%if 0%{!?debug:1}
%{target}-strip --strip-unneeded -R.comment -R.note $RPM_BUILD_ROOT%{_dlldir}/*.dll
%{target}-strip -g -R.comment -R.note $RPM_BUILD_ROOT%{_libdir}/*.a
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README change.log
%{_libdir}/libjpeg.dll.a
%{_libdir}/libjpeg.la
%{_includedir}/jconfig.h
%{_includedir}/jerror.h
%{_includedir}/jmorecfg.h
%{_includedir}/jpeglib.h
%{_includedir}/jversion.h

%files static
%defattr(644,root,root,755)
%{_libdir}/libjpeg.a

%files dll
%defattr(644,root,root,755)
%{_dlldir}/libjpeg-*.dll
