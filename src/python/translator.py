# translator.py
# attempts to translate old mediawiki 1.4 database-edits into 1.5 syntax

# mostly copied from insert_parser.py
import sys, re, os
from parser import *
from mysql_connect import *

wikiusername = "wikiuser"
wikipassword = "xxxxxxxx"
wikidb = "wikidb"

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
                # print (parse_updates(query))
                check_for_article_update(parse_inserts(query), parse_updates(query))
                query = ""
            query = query + line

# detect if the query is one we want to intercept
# we only need to parse the updates to cur, since in 1.5, they get flattened to the database
def check_for_article_update(insert_queries,update_queries):
    old = None
    cur = None
    for parsed_query in update_queries:
        if parsed_query[0] == 'cur':
            #print "cur -query:"

            #do the mapping
            #updates to cur_counter are useless
            # print str(parsed_query[1][0][0])
            # checks from the first tuple of parameter-array the first value
            if "cur_counter" not in parsed_query[1]:
                #print "Let's map this:" 
                #print str(parsed_query)
                cur = parsed_query
    
    for parsed_query in insert_queries:
        if parsed_query[0] == 'old':
            #print "With this:"
            #print str(parsed_query)
            old = parsed_query
    if old != None and cur != None:
        # TODO: To make consistent, the dict-mapping should be moved to parse_updates script
        # DONE!
        #cur_values = dict(map(lambda x: [x[0].strip(), x[1]], cur[1])) # make a cleaned dict from VALUES of cur. mapped to corresponding db-columns
        # ask for the next text_id from the database
        dbconn = MySQLCon( wikiusername, wikipassword, wikidb)
        
        rev_text_id = str(dbconn.get_next_rev_text_id())
        
        cur_values = cur[1]
        cur_id = cur[2].split()[0].split("=")[1].strip("\"'`") #cur_id
        page_latest = dbconn.make_query("SELECT page_latest FROM `page` WHERE page_id = "+ str(cur_id))[0][0]
        
        sql_text_insert = ("INSERT INTO `text` (old_id,old_text,old_flags) VALUES (NULL, " 
            + cur_values['cur_text'] + ", " 
            + old[1]['old_flag'] + ")")
        
        print "Mapping to 1.5 is:"
        sql_revision_insert = ("INSERT INTO `revision` (rev_id,rev_page,rev_text_id,rev_comment,rev_minor_edit,rev_user,rev_user_text,rev_timestamp,rev_deleted) VALUES (NULL, \'" 
            + cur_id + "\', \'"
            + rev_text_id + "\', "
            + cur_values['cur_comment'] + ", "
            + cur_values['cur_minor_edit'] + ", "
            + cur_values['cur_user'] + ", "
            + cur_values['cur_user_text'] + ", "
            + cur_values['cur_timestamp'] + ", "
            + "0"
            + ")")
        
        sql_page_update = ("UPDATE `page` SET page_latest = \'"
            + rev_text_id + "\', page_touched = "
            + cur_values['cur_touched'] + ", page_is_new=\'0\', page_is_redirect = "
            + cur_values['cur_is_redirect'] + ", page_len =\'"
            + str(len(cur_values['cur_text'].strip("'"))) + "\' WHERE page_id=\'"
            + cur_id + "\' AND page_latest=\'"
            + str(page_latest) + "\'")
        
        print sql_text_insert
        print sql_revision_insert
        print sql_page_update
        #make queries
        # NOTE, WE NEED TO EXECUTE A QUERY BEFORE THE NEXT ONE CAN BE RELIABLY BE GENERATED IN THIS SOFTWARE :(
        # can't generate next id's  (actually, queried from db...) without...
        dbconn.make_query(sql_text_insert)
        dbconn.make_query(sql_revision_insert)
        dbconn.make_query(sql_page_update)
        