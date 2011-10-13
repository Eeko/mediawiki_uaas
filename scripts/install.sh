#!/bin/bash

# in Amazon Linux, requires yum to install
# patch, readline-devel, zlib-devel, openssl-devel, java-1.6.0-openjdk-devel
# groupinstall 'Development Tools'
#... errr, apparently maven does not build GORDA correctly with jdk 1.6?


# GORDA needs to be made and installed before
echo "Downloading and patching Postgresql+Gorda"
echo "-----"
./download_gorda_psql.sh
echo "Packages complete\n-----"
# move to psql dir and start compling
cd ./postgresql-8.1.3/
./configure --enable-depend --prefix=$gorda/install
make
# can't run default install without sudo
# make install


