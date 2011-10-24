#!/bin/bash

# download psql 
if [ -f "postgresql-8.1.3.tar.bz2" ]
then   
        echo "psql found, skipping download";
else   
        echo "psql missing, downloading"
        wget ftp://ftp-archives.postgresql.org/pub/source/v8.1.3/postgresql-8.1.3.tar.bz2
fi



# unzip postgresql
if [ -d "postgresql-8.1.3" ]
then   
        echo "postgresql directory found, skipping unzip"
else   
        echo "directory not found, unzipping Posgresql"
        tar jxvf postgresql-8.1.3.tar.bz2
fi

# download gorda update
if [ -f "postgresql-g-0.4.zip" ]
then   
        echo "gorda update found, skipping download"
else   
        echo "gorda update missing, downloading"
        wget http://gorda.di.uminho.pt/download/postgresql-g-0.4.zip
fi

#update postgre with Gorda-api
# cp postgresql-g-0.4/csrc/postgresql-8.1.3-gorda-0.4.diff .

#unzip gorda
if [ -d "postgresql-g-0.4" ]
then   
        echo "gorda unzipped, skipping"
else   
        unzip postgresql-g-0.4.zip
	export gorda=$PWD/postgresql-g-0.4
fi

#check if patch is already applied
if [ -f "postgresql-8.1.3/src/backend/storage/lmgr/priority.c" ]
then   
        echo "patch applied, skipping..."
else
        echo "applying patch"
        patch -p0 < postgresql-g-0.4/csrc/postgresql-8.1.3-gorda-0.4.diff
fi
