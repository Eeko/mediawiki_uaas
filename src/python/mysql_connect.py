#mysql_connect.py

import MySQLdb

class MySQLCon():
    
    def __init__(self, wikiuser, wikipass, wikidb):
        self.wikiuser = wikiuser
        self.wikipass = wikipass
        self.wikidb = wikidb
    
    
    #returns the next incrementable number of old_id from 'text' table
    def get_next_rev_text_id(self):
        conn = MySQLdb.connect (host = "localhost",
                                user = self.wikiuser,
                                passwd = self.wikipass,
                                db = self.wikidb)
        cursor = conn.cursor()
        cursor.execute("SELECT MAX(old_id) FROM `text`")
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        return int(row[0]) + 1
    
    # makes a query. TODO: Refactor, not very DRY
    def make_query(self, query):
        conn = MySQLdb.connect (host = "localhost",
                                user = self.wikiuser,
                                passwd = self.wikipass,
                                db = self.wikidb)
        cursor = conn.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        conn.commit() #autocommit is disabled in python-mysql
        conn.close()
        return result
        
        