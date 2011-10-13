#!/bin/bash

# in Amazon Linux, requires yum to install
# patch, readline-devel, zlib-devel, openssl-devel
# groupinstall 'Development Tools'

echo "Downloading and patching Postgresql+Gorda"
echo "-----"
./download_gorda_psql.sh
echo "Packages complete\n-----"
# move to psql dir and start compling
cd ./postgresql-8.1.3/
./configure
make
# can't run default install without sudo
# make install


