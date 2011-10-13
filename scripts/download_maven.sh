#!/bin/bash

if [ -f "apache-maven-3.0.3-bin.tar.gz" ]

then
        echo "maven found, skipping download";
else
        echo "maven missing, downloading"
        wget http://mirror.mkhelif.fr/apache//maven/binaries/apache-maven-3.0.3-bin.tar.gz

fi

if [ -d "apache-maven-3.0.3" ]
then
        echo "maven-dir found, skipping extraction"
else
        echo "extracting maven"
        tar zxvf apache-maven-3.0.3-bin.tar.gz
fi

# install maven

# first do some environment-magick & spells

if [ ! -d "$HOME/bin" ];
then
        mkdir $HOME/bin
fi

export PATH=$PATH:$HOME/bin
echo "export PATH=$PATH:$HOME/bin" >> $HOME/.bashrc

# make a local link to the unarchived maven binaries
ln -s $PWD/apache-maven-3.0.3/bin/mvn $HOME/bin/mvn

