#
# Conditional build:
%bcond_without	prof	# profiling library
#
%define		pkgname	cmdargs
Summary:	Command line argument processing
Name:		ghc-%{pkgname}
Version:	0.10.20
Release:	2
License:	BSD
Group:		Development/Languages
#Source0Download: http://hackage.haskell.org/package/cmdargs
Source0:	http://hackage.haskell.org/package/%{pkgname}-%{version}/%{pkgname}-%{version}.tar.gz
# Source0-md5:	744e15b86ef774ed06af4e37a565f36b
URL:		http://hackage.haskell.org/package/cmdargs
BuildRequires:	ghc >= 6.12.3
BuildRequires:	ghc-base >= 4.4
BuildRequires:	ghc-base < 5
BuildRequires:	ghc-filepath
BuildRequires:	ghc-process >= 1.0
BuildRequires:	ghc-transformers >= 0.2
%if %{with prof}
BuildRequires:	ghc-prof >= 6.12.3
BuildRequires:	ghc-base-prof >= 4.4
BuildRequires:	ghc-base-prof < 5
BuildRequires:	ghc-filepath-prof
BuildRequires:	ghc-process-prof >= 1.0
BuildRequires:	ghc-transformers-prof >= 0.2
%endif
BuildRequires:	rpmbuild(macros) >= 1.608
Requires(post,postun):	/usr/bin/ghc-pkg
%requires_eq	ghc
Requires:	ghc-base >= 4.4
Requires:	ghc-base < 5
Requires:	ghc-filepath
Requires:	ghc-process >= 1.0
Requires:	ghc-transformers >= 0.2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# debuginfo is not useful for ghc
%define		_enable_debug_packages	0

# don't compress haddock files
%define		_noautocompressdoc	*.haddock

%description
This library provides an easy way to define command line parsers.

%package prof
Summary:	Profiling %{pkgname} library for GHC
Summary(pl.UTF-8):	Biblioteka profilująca %{pkgname} dla GHC
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	ghc-base-prof >= 4.4
Requires:	ghc-base-prof < 5
Requires:	ghc-filepath-prof
Requires:	ghc-process-prof >= 1.0
Requires:	ghc-transformers-prof >= 0.2

%description prof
Profiling %{pkgname} library for GHC. Should be installed when
GHC's profiling subsystem is needed.

%description prof -l pl.UTF-8
Biblioteka profilująca %{pkgname} dla GHC. Powinna być zainstalowana
kiedy potrzebujemy systemu profilującego z GHC.

%prep
%setup -q -n %{pkgname}-%{version}

%build
runhaskell Setup.hs configure -v2 \
	%{?with_prof:--enable-library-profiling} \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--libexecdir=%{_libexecdir} \
	--docdir=%{_docdir}/%{name}-%{version}

runhaskell Setup.hs build
runhaskell Setup.hs haddock --executables

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d

runhaskell Setup.hs copy --destdir=$RPM_BUILD_ROOT

# work around automatic haddock docs installation
%{__rm} -rf %{name}-%{version}-doc
cp -a $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version} %{name}-%{version}-doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

runhaskell Setup.hs register \
	--gen-pkg-config=$RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%ghc_pkg_recache

%postun
%ghc_pkg_recache

%files
%defattr(644,root,root,755)
%doc %{name}-%{version}-doc/*
%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHScmdargs-%{version}-*.so
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHScmdargs-%{version}-*.a
%exclude %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHScmdargs-%{version}-*_p.a
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Generics
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Generics/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Generics/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Generics/Any
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Generics/Any/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Generics/Any/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/System
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/System/Console
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/System/Console/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/System/Console/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/System/Console/CmdArgs
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/System/Console/CmdArgs/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/System/Console/CmdArgs/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/System/Console/CmdArgs/Implicit
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/System/Console/CmdArgs/Implicit/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/System/Console/CmdArgs/Implicit/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/System/Console/CmdArgs/Explicit
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/System/Console/CmdArgs/Explicit/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/System/Console/CmdArgs/Explicit/*.dyn_hi

%if %{with prof}
%files prof
%defattr(644,root,root,755)
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHScmdargs-%{version}-*_p.a
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Generics/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Generics/Any/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/System/Console/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/System/Console/CmdArgs/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/System/Console/CmdArgs/Implicit/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/System/Console/CmdArgs/Explicit/*.p_hi
%endif
