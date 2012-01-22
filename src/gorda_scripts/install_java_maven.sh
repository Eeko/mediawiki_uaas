#!/bin/bash

#downloads and installs sun java 1.5 jdk and maven

#java
wget http://download.oracle.com/otn-pub/java/java_ee_sdk/5.0_01-fcs/java_ee_sdk-5_01-linux.bin -Ojava-1.5.0-jdk.bin
chmod +x java-1.5.0-jdk.bin
./java-1.5.0-jdk.bin
#TODO: SET $JAVA_HOME to point to extracted files

#maven
wget http://mirror.mkhelif.fr/apache//maven/binaries/apache-maven-3.0.3-bin.tar.gz
tar zxvf apache-maven-3.0.3-bin.tar.gz 
#TODO: SET maven/bin to $PATH


