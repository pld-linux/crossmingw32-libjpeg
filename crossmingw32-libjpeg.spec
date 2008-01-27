%define		realname	libjpeg
Summary:	Library for handling different jpeg files - Mingw32 cross version
Summary(pl.UTF-8):	Biblioteka do manipulacji plikami w formacie jpeg - wersja skrośna dla Mingw32
Name:		crossmingw32-%{realname}
Version:	6b
Release:	5
License:	distributable
Group:		Development/Libraries
Source0:	ftp://ftp.uu.net/graphics/jpeg/jpegsrc.v%{version}.tar.gz
# Source0-md5:	dbd5f3b47ed13132f04c685d608a7547
Patch0:		%{realname}-DESTDIR.patch
Patch1:		%{realname}-include.patch
Patch2:		%{realname}-c++.patch
Patch3:		%{name}-shared.patch
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

%description
The libjpeg package contains a library of functions for manipulating
JPEG images.

This package contains the cross version for Win32.

%description -l pl.UTF-8
Ten pakiet zawiera bibliotekę funkcji do manipulacji plikami jpeg.

Ten pakiet zawiera wersję skrośną dla Win32.

%package static
Summary:	Static libjpeg library (cross mingw32 version)
Summary(pl.UTF-8):	Statyczna biblioteka libjpeg (wersja skrośna mingw32)
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description static
Static libjpeg library (cross mingw32 version).

%description static -l pl.UTF-8
Statyczna biblioteka libjpeg (wersja skrośna mingw32).

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
%patch1 -p1
%patch2 -p1
%patch3 -p1

cp /usr/share/automake/config.* .

# hack: use recent libtool by configuring for mingw32 in separate dir
# (cannot regenerate main ac/lt because of missing configure.in)
mkdir lthack
cd lthack
cat >configure.ac <<EOF
AC_INIT(lthack, 0)
AC_CONFIG_AUX_DIR(..)
AC_PROG_LIBTOOL
EOF

%build
cd lthack
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%configure \
	--target=%{target} \
	--host=%{target}
cd ..

%configure \
	--target=%{target} \
	--host=%{target} \
	--enable-shared \
	--enable-static

cp -f lthack/libtool .

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_includedir},%{_libdir},%{_dlldir}}

%{__make} install-headers install-lib \
	libdir=%{_libdir} \
	DESTDIR=$RPM_BUILD_ROOT

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

%files static
%defattr(644,root,root,755)
%{_libdir}/libjpeg.a

%files dll
%defattr(644,root,root,755)
%{_dlldir}/libjpeg-*.dll
