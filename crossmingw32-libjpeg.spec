%define		realname	libjpeg
Summary:	Library for handling different jpeg files
Summary(pl):	Biblioteka do manipulacji plikami w formacie jpeg
Name:		crossmingw32-%{realname}
Version:	6b
Release:	1
License:	distributable
Group:		Libraries
Source0:	ftp://ftp.uu.net/graphics/jpeg/jpegsrc.v%{version}.tar.gz
# Source0-md5:	dbd5f3b47ed13132f04c685d608a7547
Patch0:		%{realname}-DESTDIR.patch
Patch1:		%{realname}-include.patch
Patch2:		%{realname}-c++.patch
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

%description
The libjpeg package contains a library of functions for manipulating
JPEG images.

%description -l pl
Ten pakiet zawiera bibliotekê funkcji do manipulacji plikami jpeg.

%prep
%setup -q -n jpeg-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1

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

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{arch}/{include,lib}

%{target}-strip -g -R.comment -R.note libjpeg.a

install libjpeg.a $RPM_BUILD_ROOT%{arch}/lib
install jconfig.h jerror.h jmorecfg.h jpeglib.h jversion.h $RPM_BUILD_ROOT%{arch}/include

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%{arch}/include/*
%{arch}/lib/*
