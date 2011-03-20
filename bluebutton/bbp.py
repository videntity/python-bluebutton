#!/usr/bin/env python

# An Bluebutton parser command line utility.
# Alan Viars, Videntity 2011

import os, sys
from bluebutton.parse import *

if __name__ == "__main__":    
    """
    Accept a singe VA bluebutton file and convert it into json.  Return the
    whole parsed file (all), or just a subset (i.e. bp)
    """
    try: 
        infile=sys.argv[2]
        outfile=sys.argv[3]
        outtype=sys.argv[1]
    except(IndexError):
        print "You must supply an an infile and an outfile."
        print "Example: bbp.py [all|bp|wt|mds] bluebutton_infile.txt bluebutton_outfile.json "
        exit(1)
        
    try:
        items = simple_parse(infile, outfile)
        
        if outtype=="all":
            print tojson(items)
        
        if outtype=="bp":
            bpdictlist = build_bp_readings(items)
            print tojson(bpdictlist)
        
        if outtype=="wt":
            wtdictlist = build_wt_readings(items)
            print tojson(wtdictlist)

        if outtype=="mds":
            mdsdictlist = build_mds_readings(items)
            print tojson(mdsdictlist)
            
        if outtype=="d":
            demodict = build_simple_demographics_readings(items)
            print tojson(demodict)
          

    except():
        print "An unexpected error occured. Here is the post-mortem:"
        print sys.exc_info()