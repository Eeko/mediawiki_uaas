#!/bin/bash

echo "Downloading and patching Postgresql+Gorda"
echo "-----"
./download_gorda_psql.sh
echo "Packages complete\n-----"
# move to psql dir and start compling
cd ./postgresql-8.1.3/
./configure
make
make install


