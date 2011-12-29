#!/usr/bin/env python
# insert_parser.py
# 2011, Eetu Korhonen
# Reads a mysql query-log file and parses any INSERT INTO statements from individual query.

import re, time, sys

# reads a file and runs a loop until gets externally terminated. Just adds the queries to an array and prints them as they are read
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
            # check if we begin a new transaction
            # if re.match(r".{0,15}\s+\d+\sConnect\swikiuser@localhost on",line):
            if re.match(r"\s+\d+\sQuit\t\n", line):
                #grab the new line number
                linesplit = line.split()
                #linenumber = linesplit[linesplit.index("Connect") - 1]
                linenumber = linesplit[linesplit.index("Quit") - 1]
                # TODO: maybe should do this part when one reads a "Quit" command
                # DONE!
                queries.append(query)
                # print str(parse_inserts(query))
                query = line
            query = query + line

# A method to parse inserts in a full query.
# TODO: Split this into two methods. To parse query for matching inserts AND 
# then to a seperate method doing the argument parsing
def parse_inserts(query):
    results = []    # supports multiple inserts within a query
    match = re.search(r"\s+Query.+INSERT\s+INTO.+\)\n", query, flags=(re.DOTALL|re.IGNORECASE))  # --- 
    if match:
        inserts = re.split(r"INSERT\s+INTO", query, flags=re.IGNORECASE)    # might need better matching, since there may be words between insert and into in mysql.  Also, should ensure operability if the content contains "INSERT INTO"
        inserts.pop(0)  # remove the trail
        it = iter(inserts)  # creates an iterator of inserts
        for item in it:
            end_found = None
            while not end_found:
                end_found = re.match(r".+?(?<!\\)\)\n", item, flags=re.DOTALL ) # searchs for a query-line end
                #TODO: Fix this to not match other inline )\n's. Should
                #DONE! Now only matches ")\n" (how the queries are ended in query log) NOT "\)\n" (what a string-entry might contain)
                if not end_found:
                    itemtemp = item
                    item = next(it)
                    item = itemtemp + item  # adds the next part of splitted match to the prior one
                
            # print "*"  +end_found.group(0)
            # now do the parsing of the individual query
            target_table = re.search(r"\s*(`|\"|')\S+(`|\"|')", end_found.group(0)).group(0).split().pop().strip("\"\'\`")
            # print "Target table: " + target_table
            
            split_at_values = end_found.group(0).partition("VALUES")
            columns = split_at_values[0].split()[1].strip('\(\s\t\)').split(",")
            # print "Columns: " + str(len(columns)) + ": "+ str(columns)

            # the hard part...
            # print "1 " + str(split_at_values[2])
            values = split_at_values[2].strip().strip('\(\)\n').split(",")
            # print "2 " + str(values)
            for index, item in enumerate(values):
                if not check_for_complete_parameter(item):
                    #TODO: Need to support empty argument strings. Like ''
                    #DONE!
                    #print "Combining " + item + " & " + values[index+1]
                    values[index+1] = item + "," + values[index+1]
                    values.pop(index)
                
            # print "Values " + str(len(values)) + ": " + str(values)
            mapping = dict(zip(columns,values))
            results.append([target_table,mapping]) # adds the target table and final mapping to a results-list
            
    return results

# Similar method to parse update-queries
# required to detect updates to "cur"-table
def parse_updates(query):
    results = []
    # a more defined regex, since we do not want to match articles containing UPDATE...SET... in their text.
           
    
    match = re.search(r"\n\s+\d+\s+Query\s/\*\s\S+::\S+\s\*/\s+UPDATE\s`.+`\sSET.+\n", query, flags=(re.DOTALL)) 
    if match:
        #print "match"
        # updates = re.split(r"\s+\d+\s+Query\s/\*\s\S+::\S+\s\*/\s+UPDATE\s`.+`\s", query)    # might need better matching, since there may be words between insert and into in mysql.  Also, should ensure operability if the content contains "UPDATE"

        # updates.pop(0)
        # updates.pop(0)
        # updates = "".join(updates)
        print "Updates: {** " + str(query) + " **}"
        it =  query.split("\n")
        
        found_queries = []
        for index, item in enumerate(it):
        #for index, item in enumerate(it):
            # first, we need to find how many update-queries are within the parsed query
            a_full_command = count_brackets(item)
            #check if query begins with a proper UPDATE-statement and it does not leave open brackets
            if re.search(r"\s+\d+\s+Query\s/\*\s\S+::\S+\s\*/\s+UPDATE\s`.+`\s", item) and a_full_command:
                found_queries.append(item)
                print "appended " + item + "\n"
            elif re.search(r"\s+\d+\s+Query\s/\*\s\S+::\S+\s\*/\s+UPDATE\s`.+`\s", item):
                itemtemp = it[index+ 1]
                it[index + 1] = item + "\n" + itemtemp
                print "extended " + it[index+1]
        print "found_queries = " + str(found_queries) + "\n"
            #target_table = re.search(r"\s*(`|\"|')\S+(`|\"|')", item.partition("SET")[0]).group(0).split().pop().strip("\"\'\`")
            # print "Target table: " + target_table
            # HACK! HACK! HACK! HACK!
            # if target_table == "site_stats":
            #     break
            
"""
            mapping = {}
            values = split_at_set[2].strip().split(",")
            for index, item in enumerate(values):
                column = item.partition("=")[0]
                if not check_for_complete_parameter(item.partition("=")[2]):

                    values[index+1] = item + "," + values[index+1]
                    values.pop(index)
                else:
                    mapping[column] = item.partition("=")[2]
                
            # print "Values " + str(len(values)) + ": " + str(values)
            #mapping = dict(zip(columns,values))
            results.append([target_table,mapping]) # adds the target table and final mapping to a results-list
            
    return results
"""

# used to check if a complex parsed parameter is included wholly. 
# E.g. parameter " Hello, World" could be splitted into ['" Hello', ' World"']
def check_for_complete_parameter(item):
    begin_quote = re.match(r"\s*(?<!\\)(\"|'|`)", item)    # looks if the string begins with a quote
    end_quote = re.search(r"(?<!\\)(\"|'|`)\s*$", item)    # looks if the string ends in a quote
    if begin_quote == None and end_quote == None:
        return True
    elif (begin_quote != None and end_quote != None) and begin_quote.group(0).strip() == end_quote.group(0).strip():
        return True
    else:
        return False

#checks whether we have a matching number of "organic" brackets 
# -> the query forms a full line and a newline should terminate it
def count_brackets(line):
    quotes = len(re.findall(r"(?<!\\)\'", line))
    double_quotes = len(re.findall(r"(?<!\\)\"", line))
    ticks = len(re.findall(r"(?<!\\)\`", line))
    left_parentheses = len(re.findall(r"(?<!\\)\(", line))
    left_curlybrackets = len(re.findall(r"(?<!\\)\{", line))
    left_squarebrackets = len(re.findall(r"(?<!\\)\[", line))
    right_parentheses = len(re.findall(r"(?<!\\)\)", line))
    right_curlybrackets = len(re.findall(r"(?<!\\)\}", line))
    right_squarebrackets = len(re.findall(r"(?<!\\)\]", line))
    if  (quotes % 2 == 0 and 
        double_quotes % 2 == 0 and 
        ticks % 2 == 0 and 
        left_parentheses == right_parentheses and
        left_curlybrackets == right_curlybrackets and
        left_squarebrackets == right_squarebrackets):
        # print "*==\n\n" + line
        return True
        
    else:
        return False


def main():
    args = sys.argv[1]
    cut_queries_from_file(args)
    # print args
    
# main()
