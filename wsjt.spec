BuildRequires: gcc-gfortran tcl-devel tk-devel 
BuildRequires: alsa-oss-devel python-devel python-imaging python-numpy libsamplerate-devel
BuildRequires: f2c portaudio-devel fftw3-devel

BuildRequires: python-numpy-devel

%define Werror_cflags %nil
%define	short_ver 9.1

Name:		wsjt	
Summary:	Weak-signal amateur radio communications
Version:	9.1.r2512
Release:	1
Source0:	%{name}-%{short_ver}.tar.bz2
Source1:        wsjt.png
Group:		Communications
License:	GPL
URL:		http://physics.princeton.edu/pulsar/K1JT
Requires:	python
Requires:	python-imaging
Requires:	python-numpy

%description
WSJT is a computer program designed to facilitate Amateur Radio
communication under extreme weak-signal conditions.  Three very
different coding and modulation methods are provided: one for
communication by "meteor scatter" techniques on the VHF bands; one for
meteor and ionospheric scatter, primarily on the 6 meter band; and one
for the very challenging EME (Earth-Moon-Earth) path.

 Authors:  
 --------  
     K1JT    -   Joe Taylor


%description
The Weak Signal Propagation Reporter Network
is a group of amateur radio operators using
K1JT's MEPT_JT digital mode to probe radio
frequency propagation conditions using
very low power (QRP/QRPp) transmissions.

%package -n     python-%{name}
Summary:        WSJT library Python binding
Group:          Development/Python
Requires:       hamlib = %{version}-%{release}

%description -n python-%{name}
WSJT python bindings





%prep
%setup -q -n %{name}-%{short_ver}

%build 

./configure --with-portaudio-include-dir=/usr/include \
	    --with-portaudio-lib-dir=%{_libdir} \
	    --libdir=%{_libdir}

make

%install
        mkdir -p  %{buildroot}/usr
	mkdir -p  %{buildroot}/%{_bindir}
	mkdir -p  %{buildroot}/%{py_sitedir}
	mkdir -p  %{buildroot}/%{py_sitedir}/WsjtMod
	mkdir -p  %{buildroot}/%{_datadir}
	mkdir -p  %{buildroot}/%{_datadir}/doc
	mkdir -p  %{buildroot}/%{_datadir}/doc/wsjt
	mkdir -p  %{buildroot}/%{_datadir}/doc/wsjt/examples
	mkdir -p  %{buildroot}/%{_datadir}/pixmaps
	mkdir -p  %{buildroot}/%{_datadir}/wsjt

	strip --strip-unneeded WsjtMod/Audio.so

	cp wsjt %{buildroot}/%{_bindir}
	cp wsjt.py %{buildroot}/%{_bindir}
	cp CALL3.TXT wsjtrc dmet_*.dat %{buildroot}/%{_datadir}/wsjt
	cp WsjtMod/* %{buildroot}/%{py_sitedir}/WsjtMod
	chmod -x %{buildroot}/%{py_sitedir}/WsjtMod/Audio.so
	cp RxWav/Samples/* %{buildroot}/%{_datadir}/doc/wsjt/examples
	cp WSJT_User_600.pdf %{buildroot}/%{_datadir}/doc/wsjt
	cp WSJT_Quick_Reference.pdf %{buildroot}/%{_datadir}/doc/wsjt

%files
%{_bindir}/wsjt.py
%{_bindir}/wsjt
%dir %{_bindir}
%dir %attr(0755 root root) "%{_datadir}/doc/wsjt"
%doc %attr(0644 root root) "%{_datadir}/doc/wsjt/WSJT_User_600.pdf"
%doc %attr(0644 root root) "%{_datadir}/doc/wsjt/WSJT_Quick_Reference.pdf"
%dir %attr(0755 root root) "%{_datadir}/doc/wsjt/examples"
%doc %attr(0644 root root) "%{_datadir}/doc/wsjt/examples/W8WN_010809_110400.WAV"
%dir %attr(0755 root root) "%{_datadir}/wsjt"
%attr(0644 root root) "%{_datadir}/wsjt/CALL3.TXT"
%attr(0644 root root) "%{_datadir}/wsjt/wsjtrc"
%attr(0644 root root) %{_datadir}/wsjt/dmet*.dat

%files -n python-%{name}
%{py_sitedir}/WsjtMod
