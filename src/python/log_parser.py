#!/bin/env python
#
# Usage: First, pipe a general mysql-log file to local machine via ssh.
# e.g. 
# $ ssh mysql@foo.com 'tail -f /var/log/mysqld.general.log' > remote_log.txt
# Then run this script to parse stuff

import time
import re

def parse_line(line):
    result = re.search("SELECT cur_id", line)
    if result:
        print "*HEY, WE HAVE SELECT cur_id HERE!*"

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
            print line, # already has newline

main()

