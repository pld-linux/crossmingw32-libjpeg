%define		realname	libjpeg
Summary:	Library for handling different jpeg files - Mingw32 cross version
Summary(pl):	Biblioteka do manipulacji plikami w formacie jpeg - wersja skro¶na dla Mingw32
Name:		crossmingw32-%{realname}
Version:	6b
Release:	2
License:	distributable
Group:		Libraries
Source0:	ftp://ftp.uu.net/graphics/jpeg/jpegsrc.v%{version}.tar.gz
# Source0-md5:	dbd5f3b47ed13132f04c685d608a7547
Patch0:		%{realname}-DESTDIR.patch
Patch1:		%{realname}-include.patch
Patch2:		%{realname}-c++.patch
Patch3:		%{name}-shared.patch
URL:		http://www.ijg.org/
BuildRequires:	crossmingw32-gcc
BuildRequires:	crossmingw32-w32api
BuildRequires:	libtool
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		no_install_post_strip	1

%define		target		i386-mingw32
%define		target_platform	i386-pc-mingw32
%define		arch		%{_prefix}/%{target}
%define		gccarch		%{_prefix}/lib/gcc-lib/%{target}
%define		gcclib		%{_prefix}/lib/gcc-lib/%{target}/%{version}

%define		__cc		%{target}-gcc
%define		__cxx		%{target}-g++

%ifarch alpha sparc sparc64 sparcv9
%define		optflags	-O2
%endif

%description
The libjpeg package contains a library of functions for manipulating
JPEG images.

%description -l pl
Ten pakiet zawiera bibliotekê funkcji do manipulacji plikami jpeg.

%package dll
Summary:	libjpeg - DLL library for Windows
Summary(pl):	libjpeg - biblioteka DLL dla Windows
Group:		Applications/Emulators

%description dll
libjpeg - DLL library for Windows.

%description dll -l pl
libjpeg - biblioteka DLL dla Windows.

%prep
%setup -q -n jpeg-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
CC=%{target}-gcc ; export CC
CXX=%{target}-g++ ; export CXX
LD=%{target}-ld ; export LD
AR=%{target}-ar ; export AR
AS=%{target}-as ; export AS
CROSS_COMPILE=1 ; export CROSS_COMPILE
CPPFLAGS="-I%{arch}/include" ; export CPPFLAGS
RANLIB=%{target}-ranlib ; export RANLIB
LDSHARED="%{target}-gcc -shared" ; export LDSHARED
TARGET="%{target}" ; export TARGET

%configure \
	--target=%{target} \
	--host=%{target} \
	--build=i386-linux \
	--prefix=%{arch}

%{__make}
%{__make} jpeg.dll

%{target}-strip jpeg.dll
%{target}-strip -g -R.comment -R.note *.a

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{arch}/{include,lib}
install -d $RPM_BUILD_ROOT%{_datadir}/wine/windows/system

install jconfig.h jerror.h jmorecfg.h jpeglib.h jversion.h $RPM_BUILD_ROOT%{arch}/include
install *.a $RPM_BUILD_ROOT%{arch}/lib
install jpeg.dll $RPM_BUILD_ROOT%{_datadir}/wine/windows/system

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%{arch}/include/*
%{arch}/lib/*

%files dll
%defattr(644,root,root,755)
%{_datadir}/wine/windows/system/*
