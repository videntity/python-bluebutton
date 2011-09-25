#!/usr/bin/env python
"""
convert bluebutton to json
"""

import json
import os, sys
from datetime import datetime, date, timedelta

#inPath="va_sample_file.txt"
#OutPath="va_sample_file.json"
sections={
    "MY HEALTHEVET PERSONAL HEALTH INFORMATION":
    [
        None,
        None,
        None,
        ['Date of Birth']
    ],
    "MY HEALTHEVET ACCOUNT SUMMARY":
    [
        None,
        None,
        None,
        None
    ],
    "DEMOGRAPHICS":
    [
        None,
        [
            'First Name',
            'Middle Initial',
            'Last Name',
            'Suffix',
            'Alias',
            'Mailing Address',
            'Mailing Address2',
            'Mailing City',
            'Mailing State',
            'Mailing Country',
            'Mailing Province',
            'Mailing Zip/Postal Code',
            'Alternate Address',
            'Alternate Address2',
            'Alternate City',
            'Alternate State',
            'Alternate Country',
            'Alternate Province',
            'Alternate Zip/Postal Code',
            'Home Phone Number',
            'Work Phone Number',
            'Pager Number',
            'Cell Phone Number',
            'FAX Number',
            'Email Address',
            'Preferred Method of Contact',
            'Contact First Name',
            'Contact Last Name',
            'Relationship',
            'Address Line 1',
            'Address Line 2',
            'City',
            'State',
            'Country',
            'Province',
            'Zip/Post Code',
            'Email Address'
        ],
        ['Marital Status', 'Current Occupation'],
        ['Date of Birth']
    ],
    "ALLERGIES/ADVERSE REACTIONS":
    [
        None,
        None,
        None,
        ['Date']
    ],
    "MEDICAL EVENTS":
    [
        None,
        None,
        None,
        ['Start Date','Stop Date']
    ],
    "IMMUNIZATIONS":
    [
        None,
        None,
        None,
        ['Date Received']
    ],
    "FAMILY HEALTH HISTORY":
    [
        None,
        None,
        ['all'],
        None
    ],
    "MILITARY HEALTH HISTORY":
    [
        None,
        None,
        ['all'],
        None
    ],
    "VA MEDICATION HISTORY":
    [
        None,
        None,
        None,
        [ 'Last Filled On', 'Initially Ordered On']
    ],
    "MEDICATIONS AND SUPPLEMENTS":
    [
        None,
        None,
        None,
        [ 'Start Date', 'Stop Date' ]
    ],
    "VA WELLNESS REMINDERS":
    [
        None,
        ['all'],
        None,
        None
    ],
    "VITALS AND READINGS":
    [
        None,
        None,
        None,
        ['Date']
    ],
    "LABS AND TESTS":
    [
        None,
        None,
        None,
        ['Date']
    ]
}

vitals= ("Blood pressure", "Body weight")


def age(dob):
    import datetime
    today = datetime.date.today()

    if today.month < dob.month or (today.month == dob.month and today.day < dob.day):
        return today.year - dob.year - 1
    else:
        return today.year - dob.year


def simple_parse(inPath, OutPath):
    outfile =open(OutPath, 'w')
    line=[]
    items=[]
    generic_dict={}
    with open(inPath, 'r') as f:
        for i, l in enumerate(f):
            generic_dict={}
            line=l.split(":")
            if len(line)>1:
                k=line[0]
                v=line[1]
                if v[0]==" ":
                    v=v.lstrip()
                    if len(line)>2 and k=="Time":
                        v="%s:%s" % (line[1], line[2])
                        v=v.rstrip()
                        generic_dict[k]=v
                        items.append(generic_dict)
                        f.close()
                        return items

def green_parse(inPath, outPath, level):
    import re

    outfile =open(outPath, 'w')
    RE_SECTION = re.compile('-*\s([^-]*)\s-*')
    RE_SUBSECTION = re.compile('([^:]*):')
    open_section = None

    with open(inPath, 'r') as f:
        for i, l in enumerate(f):
            #print l
            group_name = RE_SECTION.match(l)

            #This is where we start a new major section of the document
            # we need to reset our set of restricted subsection according to level
            if(group_name and group_name.group(1) in sections.keys()):
                #print 'opening group '+group_name.group(1)
                open_section=group_name.group(1)
                restricted_subsections = []
                for i in range(0,level+1):
                    if sections[open_section][i]:
                        for restriction in sections[open_section][i]:
                            restricted_subsections.append(restriction)
                    #print 'appending %s ' % sections[open_section][i]

                #print 'matched on group_name '+open_section+' - Opening section'
                #print restricted_subsections
            subsection = RE_SUBSECTION.match(l)
            if(
                (
                        subsection
                        and
                        restricted_subsections
                        and
                        subsection.group(1) in restricted_subsections
                    )
                    or
                    'all' in restricted_subsections
                ):
                #print 'subsection '+subsection.group(1)+' will not be kept'
                continue
            outfile.write(l)

    outfile.close()

def build_bp_readings(items):

    bpdictlist=[]
    i=0
    for it in items:
        if it.has_key("Measurement Type"):
            if it['Measurement Type']=="Blood pressure":
                """The next 4 lines are date time systolic and diastolic"""
                bpdict={}
                bpdict.update(items[i+1])
                bpdict.update(items[i+2])
                bpdict['bp']="bp=%s/%s" % (items[i+3]['Systolic'], items[i+4]['Diastolic'])
                bpdict['bp_sys']=items[i+3]['Systolic']
                bpdict['bp_dia']=items[i+4]['Diastolic']
                bpdictlist.append(bpdict)
        i+=1
    return bpdictlist

def build_wt_readings(items):

    wtdictlist=[]
    i=0
    for it in items:
        if it.has_key("Measurement Type"):
            if it['Measurement Type']=="Body weight":
                """The next 4 lines are date time systolic and diastolic"""
                wtdict={}
                wtdict.update(items[i+1])
                wtdict.update(items[i+2])
                wtdict['wt']="wt=%sl" % (items[i+3]['Body Weight'])
                wtdictlist.append(wtdict)
        i+=1
    return wtdictlist

def build_mds_readings(items):
    print "here"
    mdsdictlist=[]
    i=0
    for it in items:
        if it.has_key("Medication"):
            mdsdict={}
            mdsdict.update(items[i])
            j=0
            while not items[i+j].has_key('Prescription Number'):
                print items[i+j]
                j+=1
                mdsdict.update(items[i+j])
                mdsdictlist.append(mdsdict)
        i+=1
    return mdsdictlist



def build_simple_demographics_readings(items):
    fnfound=False
    lnfound=False
    mifound=False
    gfound=False
    dobfound=False

    demodict={}
    for it in items:
        if it.has_key("First Name") and fnfound==False:
            demodict['first_name']=it['First Name']
            fnfound=True

        if it.has_key("Middle Initial") and mifound==False:
            demodict['middle_initial']=it['Middle Initial']
            mifound=True

        if it.has_key("Last Name") and lnfound==False:
            demodict['last_name']=it['Last Name']
            lnfound=True

        if it.has_key("Gender") and gfound==False:

            g=it['Gender'].split(" ")
            demodict['gender']=g[0]
            gfound=True

        if it.has_key("Date of Birth") and dobfound==False:
            (m, d, y)=it['Date of Birth'].split("/")
            demodict['date_of_birth']=it['Date of Birth']
            dob=date(int(y),int(m),int(d))
            today = date.today()
            demodict['num_age']=age(dob)
            dobfound=True

    return demodict

def tojson(items):
    """tojson"""
    itemsjson = json.dumps(items, indent=4)
    return itemsjson

