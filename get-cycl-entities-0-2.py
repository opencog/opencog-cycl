#! /usr/bin/python3

# 04 22 2023 by Prokhor

import sys
import time
import argparse
from sexpdata import loads, dumps, Symbol

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
    res = ""
    with open(cli_args.infile, mode='r') as infile:
        for line in infile:
            res += line

    return res

def get_top_level(input):
    prel = loads(input)
    res = []
    for dump_rule in prel:
        if(type(dump_rule) == list):
            res.append(dump_rule)

    return res

def parse_cycl(input):
    """Filters out every symbol out of the CYCL rule and returns them in a list."""
    res = []
    for entry in input:
        if(type(entry) == list):
            res.extend(parse_cycl(entry))
        elif(isinstance(entry, Symbol)):
            res.append(entry)
            if(entry.value() == '#$ist'):
                try:
                    entities.extend(input[(idx + 1) % len(input)])
                    print(input[(idx + 1) % len(input)])
                except:
                    print("error", entry)

            # print("entry", entry)
    #print('before', res)
    return res


def main():
    errors = 0
    done = 0
    global entities
    entities = []
    entities_set = ()
    entities_strings = []
    prel = ""
    start_time = time.time()
    get_cli_args()

    dump = read_file()
    content = get_top_level(dump)
    #print(content, "is content")
    for dump_rule in content:
        entities.extend(parse_cycl(dump_rule))
    #print(entities)
    for entry in entities:
        #for entity in entry:
        #if(type(entity) == list):
        #        for entity2 in entity:
        #            print(entity2)
        #    else:
        #        print(entry)
        if(entry == "" ):
            entities.remove(entry)
    entities_set = set(entities)

    for entity in entities_set:
        res = entity[2:]
        entities_strings.append(res)
    for s in entities_strings:
        if(s == ""):
            entities_strings.remove(s)


    with open(cli_args.outfile, 'w') as outfile:
        for entity in entities_strings:
            rule = [Symbol('find-or-create-constant'), str(entity)]
            line = dumps(rule)
            outfile.write(line)
            outfile.write("\n")
    end_time = time.time()
    print(end_time - start_time, "seconds")
    print(len(entities_set), "entities were found in the dump")

main()
