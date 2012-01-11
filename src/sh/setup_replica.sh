#!/usr/bin/env bash
# transfer the fiels needed to the parallel universe.
source configs.replica
ssh -o StrictHostKeyChecking=no $aws_replica_hostname 'mkdir ~/mw15_update' #we add the replica automatically to ~/.ssh/known_hosts/
scp configs.replica $aws_replica_hostname:~/mw15_update/
#move the relevant .sh scripts
scp start_update.sh $aws_replica_hostname:~/mw15_update/
scp std_update_mwiki14-15.sh $aws_replica_hostname:~/mw15_update/
scp ../python/*.py $aws_replica_hostname:~/mw15_update/

echo "DONE!"
echo "Now connect into the parallel universe with:"
echo "ssh $aws_replica_hostname"
echo "And in dir ~/mw15_update/ execute \"start_update.sh\""