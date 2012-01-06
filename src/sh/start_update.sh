# Start the update. Run this on the replicated MW1.4->MW1.5 environment

# First, load the configuration variables:
source configs.replica
# check the first line number 
first_line_number=$(wc -l $logfile |tr " " "\n"|head -1)

# gather log-file
#ssh $username@$original_address "tail -f ${logfile} -n +${first_line_number}" |tee $(local_log_cache)
# maybe should parallelize to create a single executable?
((ssh $aws_original_hostname "tail -f ${logfile} -n +${first_line_number}" > $local_log_cache) &)

# remember to terminate that ssh+tail process from memory
