#!/bin/env python
#
# Usage: First, pipe a general mysql-log file to local machine via ssh.
# e.g. 
# $ ssh mysql@foo.com 'tail -f /var/log/mysqld.general.log' > remote_log.txt
# Then run this script to parse stuff

import time
import re

def parse_line(line):
    if re.search(r"\s.+Query.+SELECT.+FROM.+", line, flags=re.IGNORECASE):
        print "*SELECT QUERY*"
    elif re.search(r"\s.+Query.+INSERT.+INTO.+", line, flags=re.IGNORECASE):
        
        table_name = re.search(r"insert.+into\s*(`|\"|')\S+(`|\"|')", line, flags =re.IGNORECASE).group(0).split().pop().strip("\"\'\`")
        print "INSERT QUERY TO " + table_name
    elif re.search(r"\s.+Query.+UPDATE.+SET.+", line, flags=re.IGNORECASE):
        print "*UPDATE QUERY*"

def main():
    file = open('remote_log.txt','r')
    while 1:
        where = file.tell()
        line = file.readline()
        if not line:
            time.sleep(1)
            file.seek(where)
        else:
            parse_line(line)
            # print line, # already has newline
main()

