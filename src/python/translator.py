#!/usr/bin/env python
# translator.py
# attempts to translate old mediawiki 1.4 database-edits into 1.5 syntax

# mostly copied from insert_parser.py
import sys, re
from parser import *
from mysql_connect import *

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
                print "Let's map this:" 
                print str(parsed_query)
                cur = parsed_query
    
    for parsed_query in insert_queries:
        if parsed_query[0] == 'old':
            print "With this:"
            print str(parsed_query)
            old = parsed_query
    if old != None and cur != None:
        # TODO: To make consistent, the dict-mapping should be moved to parse_updates script
        # DONE!
        #cur_values = dict(map(lambda x: [x[0].strip(), x[1]], cur[1])) # make a cleaned dict from VALUES of cur. mapped to corresponding db-columns
        cur_values = cur[1]
        cur_id = cur[2].split()[0].split("=")[1].strip("\"'`") #cur_id
        
        print "Mapping to 1.5 is:"
        
        print "TODO! First, we can insert the new cur-update to old-table (used as a text-table in 1.5)"
        print "INSERT INTO `text` "
        print "old_id= " + "NULL" 
        print "old_text =" + cur_values['cur_text']
        print "old_flags= " + old[1]['old_flag']
        
        """ THE Schema for text (just the same as old old-table)
        CREATE TABLE `text` (
          `old_id` int(8) unsigned NOT NULL AUTO_INCREMENT,
          `old_namespace` tinyint(2) unsigned NOT NULL DEFAULT '0',
          `old_title` varchar(255) CHARACTER SET latin1 COLLATE latin1_bin NOT NULL DEFAULT '',
          `old_text` mediumtext NOT NULL,
          `old_comment` tinyblob NOT NULL,
          `old_user` int(5) unsigned NOT NULL DEFAULT '0',
          `old_user_text` varchar(255) CHARACTER SET latin1 COLLATE latin1_bin NOT NULL,
          `old_timestamp` char(14) CHARACTER SET latin1 COLLATE latin1_bin NOT NULL DEFAULT '',
          `old_minor_edit` tinyint(1) NOT NULL DEFAULT '0',
          `old_flags` tinyblob NOT NULL,
          `inverse_timestamp` char(14) CHARACTER SET latin1 COLLATE latin1_bin NOT NULL DEFAULT '',
        
        """
        
        
        print "INSERT INTO `revision` "
            
        print "rev_id = NULL" # Should get auto-incremented from old_id?
        print "rev_page = " + cur_id
        print "rev_comment =" + cur_values['cur_comment']
        print "rev_user = " + cur_values['cur_user']
        print "rev_user_text = " + cur_values['cur_user_text']
        print "rev_timestamp = " + cur_values['cur_timestamp']
        print "rev_minor_edit = " + cur_values['cur_minor_edit']
        print "rev_text_id =" + "we get this from the previous insert into text as old_id"
        
        print "INSERT INTO wikidb-page "
        print "page_id =" + cur_id
        print "page_namespace =" + old[1]['old_namespace']  # not included in an update, but in the update-script, old_namespace = cur_namespace
        print "page_title =" + "TODO! Check how a title-update is added" # cur_values['cur_title']  # not included in update
        print "page_restrictions =" + "NULL" #cur_values['cur_restrictions']    # cur_restriction can be empty. Tells us who can edit an article.
                                                                        # TODO: try editing article rights and see how this gets updated
        print "page_counter =" + "NULL" # cur_values['cur_counter']     # Cur_counter is not that mandatory. Could be read with external db-query and updated last?
        print "page_is_redirect =" + cur_values['cur_is_redirect']
        print "page_is_new =" + cur_values['cur_is_new']
        print "page_random =" + "NULL" # cur_values['']      # used by random-page function. Can be re-generated randomly between 0-1
        print "page_touched =" + cur_values['cur_touched']
        print "page_latest =" + 
        """
                INSERT
                  INTO /*$wgDBprefix*/page
                    (page_id,
                    page_namespace,
                    page_title,
                    page_restrictions,
                    page_counter,
                    page_is_redirect,
                    page_is_new,
                    page_random,
                    page_touched,
                    page_latest)
                  SELECT
                    cur_id,
                    cur_namespace,
                    cur_title,
                    cur_restrictions,
                    cur_counter,
                    cur_is_redirect,
                    cur_is_new,
                    cur_random,
                    cur_touched,
                    rev_id
        """
                
                
                
                
"""
Update looks like:
UPDATE
['cur', [
            [' cur_text', "'Hello world!\n\nLet me add an update to this page!'"], 
            ['cur_comment', "'A small update'"], 
            ['cur_minor_edit', "'0'"], 
            ['cur_user', "'0'"], 
            ['cur_timestamp', "'20111213222908'"], 
            ['cur_user_text', "'127.0.0.1'"], 
            ['cur_is_redirect', "'0'"], 
            ['cur_is_new', "'0'"], 
            ['cur_touched', "'20111213222908'"], 
            ['inverse_timestamp', "'79888786777091' "]
        ], 
// WHERE
    " cur_id='935' AND cur_timestamp='20111212223014'", 
// LIMIT
'']
                
//Where the old-table gets updated as follows:
INSERT INTO 
[`old`, [
    [old_id, NULL]
    [old_namespace, '0']
    [old_title, 'Foobar_article']
    [old_text, 'Hello, world!']
    [old_comment, 'Initial update']
    [old_user, '0']
    [old_user_text, '127.0.0.1']
    [old_timestamp, '20111212223014']
    [old_minor_edit, '0']
    [inverse_timestamp, '79888787776985']
    [old_flags, 'utf-8']
]
                    
                 
                
-- Now, copy all old data except the text into revisions
INSERT
  INTO /*$wgDBprefix*/revision
    (rev_id,
    rev_page,
    rev_comment,
    rev_user,
    rev_user_text,
    rev_timestamp,
    rev_minor_edit)
  SELECT
    old_id,
    cur_id,
    old_comment,
    old_user,
    old_user_text,
    old_timestamp,
    old_minor_edit
  FROM /*$wgDBprefix*/old,/*$wgDBprefix*/cur
  WHERE old_namespace=cur_namespace
    AND old_title=cur_title;
                
"""

