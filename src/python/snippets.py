import re, time, sys
# code snippets for ing

# to parse an individual query like: 111213 15:17:13     8 Connect wikiuser@localhost on

def cut_queries_from_file(file):

    file = open(file,'r')
    queries = []
    query= ""
    linenumber = None
    while 1:
            
        where = file.tell()
        line = file.readline()
        if not line:
            time.sleep(1)
            file.seek(where)
        else:
            # check whether we have started to read a new transaction
            # regex matches YYMMDD hh:mm:ss     ta# 
            # Is useless, since there can be multiple transactions at the same moment?
            # if re.match(r"\d{6}\s\d{2}:\d{2}:\d{2}",line)
            
            # check if we begin a new transaction
            if re.match(r".{0,15}\s+\d+\sConnect\swikiuser@localhost on",line):
                #grab the new line number
                linesplit = line.split()
                # print "Match of connect"
                # print linesplit
                linenumber = linesplit[linesplit.index("Connect") - 1]
                # print linenumber
                # maybe should do this part when one reads a "Quit" command
                queries.append(query)
                # print query
                parse_insert(query)
                query = line
            query = query + line
            # print line
                
                
def parse_insert(query):
    print "****"
    # print query
    match = re.search(r"\s+Query.+INSERT INTO.+\)\n", query, flags=re.DOTALL)
    if match:
        inserts = query.split("INSERT INTO")    # might need better matching, since there may be words between insert and into in mysql
        inserts.pop(0)  # remove the trail
        for item in inserts:
            print "***MATCH FOUND:***"
            print re.match(r".+\)\n", item, flags=re.DOTALL ).group(0)
            # TODO: Search for multiple queries?
            # print match.group(0)
    
def main():
    args = sys.argv[1]
    cut_queries_from_file(args)
    print args
    
main()
