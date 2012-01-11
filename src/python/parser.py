#
# Scripts require python 2.7
# Amazon AWS default install includes only 2.6 :(
# parser.py
# 2011, Eetu Korhonen
# Reads a mysql query-log file and parses any INSERT INTO statements from individual query.

import re, time, sys

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
           
    
    match = re.search(r"\n\s+\d+\s+Query(\s/\*\s\S+::\S+\s\*/\s+|\s+)UPDATE\s`.+`\sSET.+\n", query, flags=(re.DOTALL)) 
    if match:
        it =  query.split("\n")
        
        found_queries = []
        for index, item in enumerate(it):
            # first, we need to find how many update-queries are within the parsed query
            a_full_command = count_brackets(item)
            #check if query begins with a proper UPDATE-statement and it does not leave open brackets
            if re.search(r"\s+\d+\s+Query(\s/\*\s\S+::\S+\s\*/\s+|\s+)UPDATE\s`.+`\s", item) and a_full_command:
                found_queries.append(item)
            elif re.search(r"\s+\d+\s+Query(\s/\*\s\S+::\S+\s\*/\s+|\s+)UPDATE\s`.+`\s", item): # just adds the next line to update statement if the current one is insufficient
                itemtemp = it[index+ 1]
                it[index + 1] = item + "\n" + itemtemp
        
        
        for fq in found_queries:
            
            # Now, we want to parse the queries
            columns = []
            where = ""
            limit = ""
            remainder = fq.partition("UPDATE")[2].partition("SET")
            target_table = remainder[0].strip(' \'`"`')
            comma_split = remainder[2].split(",")
            for index, item in enumerate(comma_split):
                column = item.partition("=")
                # need to split the "where" and "limit" clauses from query
                check_where = column[2].rpartition("WHERE")
                check_limit = column[2].rpartition("LIMIT")
                if check_for_complete_parameter(check_where[0]) and check_where[1] != '':
                    # print str(check_where)
                    columns.append([column[0],check_where[0]])
                    where = check_where[2]
                    #maybe should add limit-chek here too...
                elif check_for_complete_parameter(check_limit[0]) and check_limit[1] != '':
                    # print str(check_limit)
                    columns.append([column[0],check_limit[0]])
                    limit = check_limit[2]
                    
                elif check_for_complete_parameter(column[2]):
                    columns.append([column[0],column[2]])
                else:
                    comma_split[index + 1] = item + comma_split[index +1]
            # print "fq: " + str(fq) + "\n"
            # print "where: " + where
            # print "limit: " + limit
            #TODO: Map the columns by their index
            columns_dict = dict(map(lambda x: [x[0].strip(), x[1]], columns))
            results.append([target_table, columns_dict, where, limit])

    return results


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
