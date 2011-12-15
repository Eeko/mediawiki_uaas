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
        match = re.search(r"insert.+into\s*(`|\"|')\S+(`|\"|')", line, flags =re.IGNORECASE)
        table_name = match.group(0).split().pop().strip("\"\'\`")
        remainder = line.split(match.group(0))[1]   # removes the beginning of the line to parse the rest of values
        table_columns = re.split("values", remainder, flags=re.IGNORECASE)[0].strip(" ()").split(",")   # re.IGNORECASE requires python > 2.7
                                                                                                        # easy to parse, since column names are pretty strictly defined
        # The rest of the query can easily be something like (NULL, "Foo, bar", 1 'another text\n\' foo'...)
        # harder to parse...
        # maybe I need to do it one char at a time?
        column_values = re.split("values", remainder, flags=re.IGNORECASE)[1].strip(" ();\n")
        # first, split with commas (,)
        column_values = column_values.split(",")
        # then check each item in list for unclosed strings
        for index, item in enumerate(column_values):
            if not check_for_complete_parameter(item):
                column_values[index+1] = item + "," + column_values[index+1]
                column_values.pop(index)
        print "INSERT QUERY " + table_name + " INTO " + str(table_columns) + " WITH VALUES " + str(column_values)
        print "columns_size("+ str(len(table_columns)) +") = arguments_size("+ str(len(column_values)) +"): " + str(len(table_columns) == len(column_values))
    elif re.search(r"\s.+Query.+UPDATE.+SET.+", line, flags=re.IGNORECASE):
        print "*UPDATE QUERY*"


def check_for_complete_parameter(item):
    begin_quote = re.match(r"\s*(\"|'|`)", item)
    end_quote = re.search(r"\s*(\"|'|`)$", item)
    if begin_quote != None and end_quote != None and begin_quote.group(0) == end_quote.group(0):
        return True
    else:
        return False

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

