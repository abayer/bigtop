# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
%define mahout_name mahout
%define lib_mahout /usr/lib/%{mahout_name}
%define etc_mahout /etc/%{mahout_name}
%define config_mahout %{etc_mahout}/conf
%define log_mahout /var/log/%{mahout_name}
%define bin_mahout /usr/bin
%define man_dir /usr/share/man
%define doc_mahout %{_docdir}/mahout-%{mahout_version}

# disable repacking jars
%define __os_install_post %{nil}

Name: mahout
Version: %{mahout_version}
Release: %{mahout_release}
Summary: Scripts and libraries for running software services on cloud infrastructure.
URL: http://mahout.apache.org
Group: Development/Libraries
BuildArch: noarch
Buildroot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
License: ASL 2.0 
Source0: %{name}-distribution-%{mahout_base_version}-src.tar.gz
Source1: install_%{name}.sh

# RHEL6 provides natively java
%if 0%{?rhel} == 6
BuildRequires: java-1.6.0-sun-devel
Requires: java-1.6.0-sun
%else
BuildRequires: jdk >= 1.6
Requires: jre >= 1.6
%endif


%description 
Mahout provides, well, Mahout.
    
%prep
%setup -n %{name}-distribution-%{mahout_base_version}

%build

mvn clean install -Dmahout.skip.distribution=false -DskipTests

%install
%__rm -rf $RPM_BUILD_ROOT
sh $RPM_SOURCE_DIR/install_mahout.sh \
          --build-dir=distribution/target/mahout-distribution-%{mahout_base_version}/mahout-distribution-%{mahout_base_version} \
          --prefix=$RPM_BUILD_ROOT \
          --doc-dir=%{doc_mahout} 

#######################
#### FILES SECTION ####
#######################
%files 
%defattr(-,root,root,755)
%config %{etc_mahout}/conf
%doc %{doc_mahout}
%{lib_mahout}
%{bin_mahout}/mahout


