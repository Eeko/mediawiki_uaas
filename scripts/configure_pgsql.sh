#!/bin/bash
#configure the postgresql cluster
# RUN AS ROOT USER/SUDO

mkdir /usr/local/pgsql/data
useradd postgres
chown postgres /usr/local/pgsql/data
su postgres --session-command=/usr/local/pgsql/bin/initdb -D /usr/local/pgsql/data

# launch pgsql
su postgres --session-command='/usr/local/pgsql/bin/pg_ctl -D /usr/local/pgsql/data -l -logfile start'

#ok, let's add postgresql commands to the path of postgres user
echo "export PATH=$PATH:/usr/local/pgsql" >> ~postgres/.bashrc