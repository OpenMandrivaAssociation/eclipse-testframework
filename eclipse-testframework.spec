%global eclipse_base   %{_libdir}/eclipse
%global install_loc    %{_datadir}/eclipse/dropins/testframework
%global tag            R3_6_1

Name:           eclipse-testframework
Version:        3.6.1
Release:        4
Summary:        Eclipse Test Framework

Group:          Development/Java
License:        EPL
URL:            http://eclipse.org
## sh %{name}-fetch-src.sh %{tag}
Source0:        %{name}-fetched-src-%{tag}.tar.bz2
Source1:        %{name}-fetch-src.sh
# Remove win32 fragment from test feature
Patch0:         eclipse-nowin32testfragment.patch
# Some fixes for library.xml
# FIXME:  submit upstream
Patch1:        eclipse-tests-libraryXml.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch: noarch

BuildRequires: eclipse-pde >= 0:3.5.0
BuildRequires: easymock2
Requires: eclipse-platform >= 3.4.0
Requires: easymock2
Requires: eclipse-jdt

%description
Eclipse Test Framework. Used in conjunction with Eclipse JUnit tests.

%prep
%setup -q -n %{name}-fetched-src-%{tag}
chmod -x org.eclipse.test-feature/*.html
%patch0
%patch1
sed -i "s:/usr/lib/eclipse:%{_libdir}/%{name}:" org.eclipse.test/library.xml

mkdir orbitDeps
pushd orbitDeps
ln -s %{_javadir}/easymock2.jar org.easymock_2.4.0.v20090202-0900.jar
popd

%build
%{eclipse_base}/buildscripts/pdebuild -f org.eclipse.test -o `pwd`/orbitDeps

%install
%{__rm} -rf %{buildroot}
install -d -m 755 %{buildroot}%{install_loc}

%{__unzip} -q -d %{buildroot}%{install_loc} \
     build/rpmBuild/org.eclipse.test.zip

pushd $RPM_BUILD_ROOT%{install_loc}/eclipse/plugins
rm -fr org.junit*
rm org.easymock_2.4.0.v20090202-0900.jar
ln -s ../../../../../java/easymock2.jar org.easymock_2.4.0.v20090202-0900.jar
popd

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{install_loc}
%doc org.eclipse.test-feature/license.html
%doc org.eclipse.test-feature/epl-v10.html

