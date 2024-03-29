#! /usr/bin/python3

# 04 22 2023 by Prokhor
# This script takes a dump of a cyc kb and writes the rules tranlated into opencog scheme syntax.

import sys
import time
import argparse
import itertools
from sexpdata import loads, dumps, Symbol
import re
import logging
import sys



def get_cli_args():
    """Gets CLI arguments, makes them available gobally"""
    arg_parser = argparse.ArgumentParser("Converts a dump of a CYC KB into Opencog Atomspace")
    
    arg_parser.add_argument("-i", "--infile", help="The input file. If no file is specified. it will read from stdin.")
    arg_parser.add_argument("-o", "--outfile", help="The output fiel to write to. If no file is specified, the program will print to sttout.")
    arg_parser.add_argument("-v", "--verbose", default=False, help="If set to 'True', it will print the actual rule processed")

    global cli_args
    #arguments are made global so they dont have to be passed around....
    cli_args = arg_parser.parse_args()

def read_file():
    """Reads all lines in the dump file and appends them to one large string. Unfortunately this has to be done as some rules occupy more than one line."""
    res = ""
    with open(cli_args.infile, mode='r') as infile:
        for line in infile:
            res += line

    return res

def get_top_level(input):
    """Gets all top-level functions. Warning they all have to be enclosed by one major function."""
    prel = loads(input)
    res = []
    for entry in prel:
        if(type(entry) == int):
            prel.remove(entry)
    try:
        for dump_rule in prel:
            if(type(dump_rule) == list):
                res.append(dump_rule)
    except:
        print("parsing error!")
    #print(res)
    return res

def parse_cycl(input):
    """Parses the CYC KB dump into a nested list"""
    res = []
    parserrrs = 0
    with open(cli_args.infile, 'r') as infile:
        for line in infile:
            try:
                rule = extract_cycl_rule(loads(line))
                if(rule != 'none'):
                    res.append(rule)

            except:
                print("parsing Error!", line)
                parserrrs += 1

    #print(res)
    print(parserrrs)
    return res

    
def extract_cycl_rule(rule):
    """Extracts the individual CYCL rules in the file content. It does so by picking the first list after '#$ist'."""
    #result = []

    #nextlist = False
    #for rule in rules:
    #for  idx, entry in enumerate(rule):
    #
    #    if((isinstance(rule[idx], list)) and (nextlist == False)):
    #        result.extend(extract_cycl_rule(entry))
    #    elif((isinstance((rule[idx]), list)) and (nextlist == True)):
    #        #print(entry)
    #        result.extend(entry)
    #    elif(isinstance(entry, Symbol)):
    #        if(entry.value() == "#<"):
    #            nextlist = True
    #for rule in rules:

    for  entry in rule:
        if(isinstance(entry, list)) :
            for entry2 in entry:
                if(isinstance(entry2, list)) :
                    for idx, entry3 in enumerate(entry2):
                        if(isinstance(entry3, list)) :
                            #print(entry3)
                            #logger.info("midst:" + str(entry3))
                            #if(isinstance(entry3, None)):
                            #    return entry2
                            #else:
                            return(entry3)
                        elif((not isinstance(entry3, list) and (entry3 is entry2[-1]))):
                            return entry2











def conceptify(x):
    """This translates from CYCL into opencog. Credits for this snippets go to Gandro from Luxeria."""
    if isinstance(x, list):
        return list(map(conceptify, x))
    else:
        if(isinstance(x, Symbol)):
            x = x.value()

        return [Symbol('Concept'), x]

#def main():

errors = 0
done = 0
ruleset = []
ruleset2 = []
prel = ""
start_time = time.time()
get_cli_args()
next_count = 0
nextlist = False


logger = logging.getLogger()
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')

stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setLevel(logging.DEBUG)
stdout_handler.setFormatter(formatter)

file_handler = logging.FileHandler('/home/user/log-2.log')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)


logger.addHandler(file_handler)
logger.addHandler(stdout_handler)



dump = read_file()
content = get_top_level(dump)
del dump
    #print(content, "is content")

for dump_rule in content:
    #print(dump_rule)

    if(isinstance(dump_rule, list)):
        ruleset.append((extract_cycl_rule(dump_rule)))
        done += 1
        #logger.info("before:" + str(dump_rule))
        #logger.info("after" + str(extract_cycl_rule(dump_rule)))
        if(isinstance(extract_cycl_rule(dump_rule), type(None))):
            logger.error(str(dump_rule))
    else:
        logger.error(done + "wrong entry:" + str(dump_rule))

ruleset[:] = [rule for rule in ruleset if not  []]
"""I know this is messy but it was my quickest solution..."""
    #print("ruleset",ruleset)
for rule in ruleset:
        #print(rule)
        #rule2 = []
        #print(rule, "\m")
    try:
        input = rule
        head, *tail = input
        if(isinstance(head, Symbol)):
            head = head.value()
        output = [Symbol('Predicate'), head] + conceptify(tail)

        #print(output)
        ruleset2.append(output)
    except:
        #print("unpacking went wrong", rule)
        pass
del content
    #print("ruleset:",ruleset)
print("items:", len(ruleset2))
with open(cli_args.outfile, 'w') as outfile:
    for rule in ruleset2:
            #print("rule before dumps:", rule)
        line = dumps(rule)
            #print("line after:",line)
        outfile.write(line)
        outfile.write("\n")
end_time = time.time()
print(end_time - start_time, "seconds")
print(errors, "errors encountered")
print(done,"lines were processed.")

#nextlist and next_count are used for rule extraction. I know it is ugly but with recursion it is the simplest way...

#main()
