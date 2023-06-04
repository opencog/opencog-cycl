Opencog-Cycl

This project is an attempt to map Cyc KBs to atomspace (e.g. the OpenCyc Knowledgebase) which are written in the Cycl knowledge representation language.
It originates from a discussion between Linas and Prokhor. 
One main purpose willbe to provide new inference mechanisms for improved reasoning on the KB.

I am still in an early stage. Have a look at continuous_notes to get an idea what's going on!


    - cycl-opencog-0-2.py
        translates the rules from the Cyc-KB dump into opencog rules.
        A large set of those rules have been tested an at least compile without errors...

        Usage:  cycl-opencog-0-2.py -i infile -o outfile
