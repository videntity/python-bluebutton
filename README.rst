Bluebutton File Format Parser
(c.) Alan Viars - Videntity Systems Inc. - 2011

Version 0.1.3

This library is dual licensed.  It is realeased under the GPL licnese 
agreement and under a commercial license by Videntity systems Inc.



Installation
=============

Use pip to install the parser.
::
    pip install python-bluebutton


Using the Parser
================

Here is a simple example.
::
    # Import the library
    >>> from bluebutton.parse import *
    
    # Open and parse the bluebutton file.
    >>> parsed = simple_parse("va_sample_file.txt")
    

    # Get the bloodpressure readings
    >>> build_bp_readings(parsed)
    
    [{'Date': '08/02/2010', 'bp_sys': '141', 'bp_dia': '76', 'bp': 'bp=141/76', 'Time': ' 17:30'}, {'Date': '08/02/2010', 'bp_sys': '150', 'bp_dia': '76', 'bp': 'bp=150/76', 'Time': ' 17:20'}]
    
    # Get the weight readings
    >>> build_wt_readings(parsed)
    
    [{'Date': '06/02/2010', 'wt': 'wt=242l', 'Time': ' 17:20'}, {'Date': '05/02/2010', 'wt': 'wt=244l', 'Time': ' 17:20'}, {'Date': '04/02/2010', 'wt': 'wt=246l', 'Time': ' 17:20'}]
    
    
    #Get demographics
    >>> build_simple_demographics_readings(parsed)
    
    {'middle_initial': 'A', 'first_name': 'ONE', 'last_name': 'MHVVETERAN', 'gender': 'Male', 'num_age': 64, 'date_of_birth': '03/01/1948'}
    
    #Convert demographics to JSON
    
    print tojson(build_simple_demographics_readings(parsed))
    
    {
    "middle_initial": "A", 
    "first_name": "ONE", 
    "last_name": "MHVVETERAN", 
    "gender": "Male", 
    "num_age": 64, 
    "date_of_birth": "03/01/1948"
    }

    # Get the medications
    >>> build_mds_readings(parsed)
    ...
    
    