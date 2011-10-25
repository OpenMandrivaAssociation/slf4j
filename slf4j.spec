# Copyright (c) 2000-2009, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

Name:           slf4j
Version:        1.6.1
Release:        2
Summary:        Simple Logging Facade for Java
Group:          Development/Java
License:        MIT
URL:            http://www.slf4j.org/
Source0:        http://www.slf4j.org/dist/%{name}-%{version}.tar.gz
Patch0:         %{name}-pom_xml.patch
Requires(post): jpackage-utils >= 0:1.7.5
Requires(postun): jpackage-utils >= 0:1.7.5
BuildRequires:  jpackage-utils >= 0:1.7.5
BuildRequires:  java-devel >= 0:1.5.0
BuildRequires:  ant >= 0:1.6.5
BuildRequires:  ant-junit >= 0:1.6.5
BuildRequires:  javassist >= 0:3.4
BuildRequires:  junit >= 0:3.8.2
BuildRequires:  maven2 >= 2.0.7
BuildRequires:  maven-antrun-plugin
BuildRequires:  maven-compiler-plugin
BuildRequires:  maven-install-plugin
BuildRequires:  maven-jar-plugin
BuildRequires:  maven-javadoc-plugin
BuildRequires:  maven-resources-plugin
BuildRequires:  maven-source-plugin
BuildRequires:  maven-site-plugin
BuildRequires:  maven-doxia-sitetools
BuildRequires:  maven-surefire-plugin
BuildRequires:  maven-surefire-provider-junit
BuildRequires:  maven-plugin-build-helper
BuildRequires:  log4j
BuildRequires:  apache-commons-logging
BuildRequires:  cal10n
Requires:       jpackage-utils
Requires:       cal10n
Requires:       java
BuildArch:      noarch

%description
The Simple Logging Facade for Java or (SLF4J) is intended to serve
as a simple facade for various logging APIs allowing to the end-user
to plug in the desired implementation at deployment time. SLF4J also
allows for a gradual migration path away from
Jakarta Commons Logging (JCL).

Logging API implementations can either choose to implement the
SLF4J interfaces directly, e.g. NLOG4J or SimpleLogger. Alternatively,
it is possible (and rather easy) to write SLF4J adapters for the given
API implementation, e.g. Log4jLoggerAdapter or JDK14LoggerAdapter..

%package javadoc
Group:          Development/Java
Summary:        Javadoc for %{name}
Requires:       jpackage-utils

%description javadoc
API documentation for %{name}.

%package manual
Group:          Development/Java
Summary:        Documents for %{name}

%description manual
Manual for %{name}.

%prep
%setup -q
%patch0 -p0  -b .sav
find . -name "*.jar" | xargs rm

sed -i -e "s|ant<|org.apache.ant<|g" integration/pom.xml

%{_bindir}/find -name "*.css" -o -name "*.js" -o -name "*.txt" | \
    %{_bindir}/xargs -t %{__perl} -pi -e 's/\r$//g'

%build
export MAVEN_REPO_LOCAL=$(pwd)/.m2/repository
mvn-jpp \
        -e \
        -P skipTests \
        -Dmaven.repo.local=$MAVEN_REPO_LOCAL \
        -Dmaven.test.skip=true \
        install javadoc:aggregate

%install
# jars
install -d -m 0755 $RPM_BUILD_ROOT%{_javadir}/%{name}

install -m 644 jcl-over-slf4j/target/jcl-over-slf4j-%{version}.jar \
   $RPM_BUILD_ROOT%{_javadir}/%{name}/jcl-over-slf4j.jar
install -m 644 jul-to-slf4j/target/jul-to-slf4j-%{version}.jar \
   $RPM_BUILD_ROOT%{_javadir}/%{name}/jul-to-slf4j.jar
install -m 644 log4j-over-slf4j/target/log4j-over-slf4j-%{version}.jar \
   $RPM_BUILD_ROOT%{_javadir}/%{name}/log4j-over-slf4j.jar
install -m 644 slf4j-api/target/%{name}-api-%{version}.jar \
   $RPM_BUILD_ROOT%{_javadir}/%{name}/api.jar
install -m 644 slf4j-ext/target/%{name}-ext-%{version}.jar \
   $RPM_BUILD_ROOT%{_javadir}/%{name}/ext.jar
install -m 644 slf4j-jcl/target/%{name}-jcl-%{version}.jar \
   $RPM_BUILD_ROOT%{_javadir}/%{name}/jcl.jar
install -m 644 slf4j-jdk14/target/%{name}-jdk14-%{version}.jar \
   $RPM_BUILD_ROOT%{_javadir}/%{name}/jdk14.jar
install -m 644 slf4j-log4j12/target/%{name}-log4j12-%{version}.jar \
   $RPM_BUILD_ROOT%{_javadir}/%{name}/log4j12.jar
install -m 644 slf4j-migrator/target/%{name}-migrator-%{version}.jar \
   $RPM_BUILD_ROOT%{_javadir}/%{name}/migrator.jar
install -m 644 slf4j-nop/target/%{name}-nop-%{version}.jar \
   $RPM_BUILD_ROOT%{_javadir}/%{name}/nop.jar
install -m 644 slf4j-simple/target/%{name}-simple-%{version}.jar \
   $RPM_BUILD_ROOT%{_javadir}/%{name}/simple.jar

%add_to_maven_depmap org.slf4j jcl-over-slf4j %{version} JPP/slf4j jcl-over-slf4j
%add_to_maven_depmap org.slf4j jul-to-slf4j %{version} JPP/slf4j jul-to-slf4j
%add_to_maven_depmap org.slf4j log4j-over-slf4j %{version} JPP/slf4j log4j-over-slf4j
%add_to_maven_depmap org.slf4j %{name}-parent %{version} JPP/slf4j parent
%add_to_maven_depmap org.slf4j %{name}-api %{version} JPP/slf4j api
%add_to_maven_depmap org.slf4j %{name}-ext %{version} JPP/slf4j ext
%add_to_maven_depmap org.slf4j %{name}-jcl %{version} JPP/slf4j jcl
%add_to_maven_depmap org.slf4j %{name}-jdk14 %{version} JPP/slf4j jdk14
%add_to_maven_depmap org.slf4j %{name}-log4j12 %{version} JPP/slf4j log4j12
%add_to_maven_depmap org.slf4j %{name}-migrator %{version} JPP/slf4j migrator
%add_to_maven_depmap org.slf4j %{name}-nop %{version} JPP/slf4j nop
%add_to_maven_depmap org.slf4j %{name}-simple %{version} JPP/slf4j simple

# poms
install -d -m 755 $RPM_BUILD_ROOT%{_mavenpomdir}
install -pm 644 pom.xml \
    $RPM_BUILD_ROOT%{_mavenpomdir}/JPP.%{name}-parent.pom
install -pm 644 jcl-over-slf4j/pom.xml \
    $RPM_BUILD_ROOT%{_mavenpomdir}/JPP.%{name}-jcl-over-slf4j.pom
install -pm 644 jul-to-slf4j/pom.xml \
    $RPM_BUILD_ROOT%{_mavenpomdir}/JPP.%{name}-jul-to-slf4j.pom
install -pm 644 log4j-over-slf4j/pom.xml \
    $RPM_BUILD_ROOT%{_mavenpomdir}/JPP.%{name}-log4j-over-slf4j.pom
install -pm 644 slf4j-api/pom.xml \
    $RPM_BUILD_ROOT%{_mavenpomdir}/JPP.%{name}-api.pom
install -pm 644 slf4j-ext/pom.xml \
    $RPM_BUILD_ROOT%{_mavenpomdir}/JPP.%{name}-ext.pom
install -pm 644 slf4j-jcl/pom.xml \
    $RPM_BUILD_ROOT%{_mavenpomdir}/JPP.%{name}-jcl.pom
install -pm 644 slf4j-jdk14/pom.xml \
    $RPM_BUILD_ROOT%{_mavenpomdir}/JPP.%{name}-jdk14.pom
install -pm 644 slf4j-log4j12/pom.xml \
    $RPM_BUILD_ROOT%{_mavenpomdir}/JPP.%{name}-log4j12.pom
install -pm 644 slf4j-migrator/pom.xml \
    $RPM_BUILD_ROOT%{_mavenpomdir}/JPP.%{name}-migrator.pom
install -pm 644 slf4j-nop/pom.xml \
    $RPM_BUILD_ROOT%{_mavenpomdir}/JPP.%{name}-nop.pom
install -pm 644 slf4j-simple/pom.xml \
    $RPM_BUILD_ROOT%{_mavenpomdir}/JPP.%{name}-simple.pom

# javadoc
install -d -m 0755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}
cp -pr target/site/api*/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}/
rm -rf target/site/api*

# manual
install -d -m 0755 $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}
rm -f target/site/.htaccess
cp -pr target/site $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}/
install -m 644 LICENSE.txt $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}/

%pre javadoc
# workaround for rpm bug, can be removed in F-17
[ $1 -gt 1 ] && [ -L %{_javadocdir}/%{name} ] && \
rm -rf $(readlink -f %{_javadocdir}/%{name}) %{_javadocdir}/%{name} || :

%post
%update_maven_depmap

%postun
%update_maven_depmap

%files
%defattr(-,root,root,-)
%dir %{_docdir}/%{name}-%{version}
%doc %{_docdir}/%{name}-%{version}/LICENSE.txt
%{_javadir}/%{name}
%{_mavenpomdir}/*
%{_mavendepmapfragdir}/*

%files javadoc
%defattr(-,root,root,-)
%{_javadocdir}/%{name}

%files manual
%defattr(-,root,root,-)
%{_docdir}/%{name}-%{version}/site

