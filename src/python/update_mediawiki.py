#!/usr/bin/env python
#update_mediawiki.py
#the main program to perform the update
from translator import *
from mysql_connect import *


def main():
    
    print sys.argv[1]
    cut_queries_from_file(sys.argv[1])
    
main()
