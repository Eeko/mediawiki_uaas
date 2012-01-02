#!/usr/bin/env python
# insert_translator.py
# attempts to translate old mediawiki 1.4 database-edits into 1.5 syntax

# mostly copied from insert_parser.py
import sys, re
from insert_parser import *

def cut_queries_from_file(file):
    file = open(file,'r')
    queries = []
    query= ""
    transaction_number = None
    keep_on_reading = 1
    while keep_on_reading == 1:
            
        where = file.tell()
        line = file.readline()
        if not line:
            time.sleep(1)
            file.seek(where)
            # we can terminate reading here, for example
            # keep_on_reading == 1
        else:
            # check if we begin a new transaction
            if re.match(r"\s+\d+\sQuit\t\n", line):
                #print line
                print (parse_updates(query))
                query = ""
            query = query + line

# detect if the query is one we want to intercept
def check_for_cur_query(queries):
    for parsed_query in queries:
        if parsed_query[0] == 'cur':
            print "cur -query:"
            print str(parsed_query)

def main():
    
    print sys.argv[1]
    cut_queries_from_file(sys.argv[1])
    
main()

