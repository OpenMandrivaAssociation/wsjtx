%define	_disable_ld_no_undefined 1

Name:		wsjtx
Summary:	Provides all popular modes for Weak Signal digital Amateur Radio
Version:	2.1.2
Release:	1
License:	GPLv3
Url:		http://www.physics.princeton.edu/pulsar/K1JT/wsjtx.html
Group:		Communications/Radio
Source0:	http://www.physics.princeton.edu/pulsar/K1JT/%{name}-%{version}.tgz
#Patch0:		wsjtx-2.0.0-compile-fix.patch

BuildRequires:	asciidoc
BuildRequires:	cmake
BuildRequires:	desktop-file-utils
BuildRequires:	libgomp-devel
BuildRequires:	gcc-gfortran
BuildRequires:	boost-devel
BuildRequires:	pkgconfig(fftw3)
BuildRequires:	pkgconfig(hamlib)
BuildRequires:	pkgconfig(libxslt)
BuildRequires:	pkgconfig(Qt5Concurrent)
BuildRequires:	pkgconfig(Qt5Core)
BuildRequires:	pkgconfig(Qt5Gui)
BuildRequires:	pkgconfig(Qt5Multimedia)
BuildRequires:	pkgconfig(Qt5OpenGL)
BuildRequires:	pkgconfig(Qt5PrintSupport)
BuildRequires:	pkgconfig(Qt5SerialPort)
BuildRequires:	pkgconfig(Qt5Sql)
BuildRequires:	pkgconfig(Qt5Widgets)
BuildRequires:	cmake(Qt5Multimedia)
BuildRequires:  qmake5
BuildRequires:  a2x, dos2unix
#BuildRequires:	texinfo
# kvasd is no longer required by wsjtx > 1.7.0 so there is no need for it.
# kvasd-installer has been moved to obsoletes.
Obsoletes:	kvasd-installer < 1.12.15-3

%description
WSJT-X is a program designed to facilitate basic amateur radio communication
using very weak signals. The first four letters in the program name stand for
“Weak Signal communication by K1JT,” while the suffix “-X” indicates that
WSJT-X started as an extended (and experimental) branch of the program WSJT.
This package is aimed primarily at the LF, MF, and HF bands and now includes
the following modes: FT8, JT4, JT9, JT65, QRA64, ISCAT, MSK144, WSPR and Echo.

%prep
%setup -q -n %{name}-%{version}
# remove bundled hamlib
rm -f src/hamlib.tgz*
tar -xzf src/%{name}.tgz
%patch0 -p1
# remove archive
rm -f src/wsjtx.tgz*
pushd %{name}
# remove bundled boost. EL 7 is not required version.
rm -rf boost
# convert CR + LF to LF
dos2unix *.ui *.iss *.rc *.txt
popd

%build
export CFLAGS="-Os -fomit-frame-pointer -gdwarf-4 -Wstrict-aliasing=2 -pipe"
export CXXFLAGS=$CFLAGS
export LDFLAGS="-Os -fomit-frame-pointer -gdwarf-4"
export CC=gcc
export CXX=g++
# workaround for hamlib check, i.e. for hamlib_LIBRARY_DIRS not to be empty
export PKG_CONFIG_ALLOW_SYSTEM_LIBS=1
mkdir -p %{name}/build
cd %{name}
%cmake -Dhamlib_STATIC=FALSE \
       -DWSJT_GENERATE_DOCS=OFF \
       -DBoost_NO_SYSTEM_PATHS=FALSE

#cmake -DBoost_NO_SYSTEM_PATHS=FALSE  -Dhamlib_STATIC=FALSE -DWSJT_GENERATE_DOCS=OFF ../

%make_build
#make


%install
cd %{name}/build
%make_install

# Make sure the right style is used.
desktop-file-edit --set-key=Exec --set-value="wsjtx --style=fusion" \
    %{buildroot}/%{_datadir}/applications/%{name}.desktop
# desktop files
desktop-file-validate %{buildroot}%{_datadir}/applications/wsjtx.desktop
desktop-file-validate %{buildroot}%{_datadir}/applications/message_aggregator.desktop

# fix docs
rm -f %{buildroot}%{_datadir}/doc/WSJT-X/{INSTALL,COPYING,copyright,changelog.Debian.gz}
cd ..
mv %{buildroot}%{_datadir}/doc/WSJT-X %{buildroot}%{_datadir}/doc/%{name}
install -p -m 0644 -t %{buildroot}%{_datadir}/doc/%{name} GUIcontrols.txt jt9.txt \
  mouse_commands.txt prefixes.txt shortcuts.txt v1.7_Features.txt \
  wsjtx_changelog.txt

%files
%license COPYING
%doc %{_datadir}/doc/%{name}
%{_bindir}/fcal
%{_bindir}/fmeasure
%{_bindir}/fmtave
%{_bindir}/jt4code
%{_bindir}/jt65code
%{_bindir}/jt9
%{_bindir}/jt9code
%{_bindir}/ft8code
%{_bindir}/message_aggregator
%{_bindir}/msk144code
%{_bindir}/qra64code
%{_bindir}/qra64sim
%{_bindir}/udp_daemon
%{_bindir}/wsjtx
%{_bindir}/wsprd
%{_mandir}/man1/*.1.*
%{_datadir}/applications/wsjtx.desktop
%{_datadir}/applications/message_aggregator.desktop
%{_datadir}/pixmaps/wsjtx_icon.png
%{_datadir}/%{name}
