#! /usr/bin/python3

# 04 22 2023 by Prokhor

import sys
import time
import argparse
from sexpdata import loads, dumps, Symbol, Quoted

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

    print(res)
    print(parserrrs)
    return res

def extract_cycl_rule(rule):
    """Extracts the individual CYCL rules in the file content"""
    results = {}
    #for rule in rules:
    for  idx, entry in enumerate(rule):
        res = {}
        if(type(rule[idx]) == list):
            results.update(extract_cycl_rule(entry))
        elif(isinstance(entry, Symbol)):
            if(entry.value() == "#$ist"):
                res["Mt"] = rule[(idx + 1) % len(rule)]
                if(type(rule[(idx + 2) % len(rule)]) == list):
                    res["body"] = ((rule[(idx + 2) % len(rule)]))
                    results.update(res)
                else:
                    res["body"] = ((rule[(idx + 3) % len(rule)]))
                    results.update(res)
    #print("before", results)
    return results

def cycl_2_opencog(rule):
    """Translates CYCL to Atomspace"""
    res = [Symbol('Evaluate', [])]
    for idx, entry in enumerate(rule):
        res[-1].append([Symbol('Predicate'), entry])
        if(type(line[idx]) == list):
            res.append([Symbol('List'), []])

def write_2_file(rule):
    pass

def print_opencog(rule):
    pass

def main():
    errors = 0
    done = 0
    ruleset = []
    prel = ""
    start_time = time.time()
    get_cli_args()

    dump = read_file()
    content = get_top_level(dump)
    #print(content, "is content")
    for dump_rule in content:
        ruleset.append(extract_cycl_rule(dump_rule))
    for rule in ruleset:
        if(type(rule) == list):
            ruleset.remove(rule)

    #print("ruleset:",ruleset)
    print("items:", len(ruleset))
    with open(cli_args.outfile, 'w') as outfile:
        for rule in ruleset:
            for rule1 in rule:
              try:
                rule_final = [Symbol('cyc-assert'), Quoted(rule.get("body")), '"' + rule["Mt"] + '"',Quoted([Symbol(':direction'), Symbol(':forward')])]
                line = dumps(rule_final)
                #print(line)
                outfile.write(line)
                outfile.write("\n")
              except:
                if(rule["Mt"] and not ("" or type(rule["Mt"]) == int)):
                    rule_final = [Symbol('cyc-assert'), Quoted(rule.get("body")) ,Quoted([Symbol(':direction'), Symbol(':forward')])]
                    line = dumps(rule_final)
                    outfile.write(line)
                    outfile.write("\n")
                else:


                    print("error", rule)
                    errors += 1
    end_time = time.time()
    print(end_time - start_time, "seconds")
    print(errors, "errors encountered")
    print(done,"lines were processed.")

main()
