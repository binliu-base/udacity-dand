# -*- coding: UTF-8 -*-
#https://docs.python.org/2/library/collections.html#collections.defaultdict

"""
Your task in this exercise has two steps:

- audit the OSMFILE and change the variable 'mapping' to reflect the changes needed to fix 
    the unexpected street types to the appropriate ones in the expected list.
    You have to add mappings only for the actual problems you find in this OSMFILE,
    not a generalized solution, since that may and will depend on the particular area you are auditing.
- write the update_street_name function, to actually fix the street name.
    The function takes a string with street name as an argument and should return the fixed name
    We have provided a simple test so that you see what exactly is expected
"""
import xml.etree.cElementTree as ET 
from collections import defaultdict
import re
import pprint
import argparse
import os 

from config import *

def audit_street(osmfile):
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)

    for event, elem in ET.iterparse(osm_file, events=("start",)):
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])
                    # print tag.attrib['v']
    osm_file.close()
    return street_types

def audit_street_type(street_types, street_name):

    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()        
        if street_type not in street_expected:
              street_types[street_type].add(street_name)


def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")

def update_street_name(name, mapping):
    """
    Clean street name for insertion into database
    """
    changed = False
    for key in mapping.keys():
        if name.find(key) != -1 :
            if key in  ["Xi","Dong","Nan","Bei","Zhong"]:                                      
                m = pinyin_re.search(name)  
                if m:
                    name = name.replace(key,mapping[key])
                    changed = True
            else:
                name = name[:name.find(key)] + mapping[key]
                changed = True                
    return changed, name

def audit_city(osmfile):
    osm_file = open(osmfile, "r")  
    city_types = defaultdict(set)    
    for event, elem in ET.iterparse(osm_file, events=("start",)):
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_city_name(tag):
                    if tag.attrib['v'] not in city_expected:
                        audit_city_type(city_types,tag.attrib['v'])


    osm_file.close()                        
    return city_types

def is_city_name(elem):
    return (elem.attrib['k'] == "addr:city")

def audit_city_type(city_types, city_name):

    m = city_name_re.match(city_name)    
    if m:
        city_type = m.group()
        if isinstance(city_type, str):
            city_type = city_type.decode("utf8")        
        if city_type != city_expected:
              city_types[city_type].add(city_name)

def update_city_name(name, mapping):
    """
    Clean street name for insertion into database 
    """
    updated = False
    for key in mapping.keys():
        try:
            if isinstance(name, str):
                name = name.decode("utf8")
            if name.find(key) != -1 :                
                # m = city_name_re.match(key)
                name =city_expected
                return True, name 
            else:
                continue
                
        except Exception, e:
             print e
    return updated, name

def test():
    
    parser = argparse.ArgumentParser(description='Extract and process map data from a OSMFILE.')
    parser.add_argument('osmfile', type=str, nargs='?', default='shenzhen_sample.osm', help='input OSMFILE')    
    parser.add_argument('-t','--tag_type', type=str, nargs='?', default='city', help='auditing street, country, city,district,phonenum')
    parser.add_argument('-p','--audit_type',type=str, action="store",default='all',help='all,overabbreviated,pinyin,Inconsistentname')  

    args = parser.parse_args()
    OSMFILE = args.osmfile
    tag_type = args.tag_type
    audit_type= args.audit_type

    #https://pyformat.info/
    print '{}: auditing the tag {} for {} problem ...'.format(os.path.basename(__file__), tag_type,audit_type)    

    if tag_type == 'street':
        st_types = audit_street(OSMFILE)

        for st_type, ways in st_types.iteritems():
            for name in ways:
                if audit_type == 'overabbreviated':
                    updated, better_name = update_street_name(name, street_abbrev_mapping)
                    if updated:
                        print name, "=>", better_name
                if audit_type == 'pinyin':
                    updated,better_name = update_street_name(name, pinyin_mapping)
                    if updated:
                        print name, "=>", better_name
                if audit_type == 'all':
                    #https://stackoverflow.com/questions/38987/how-to-merge-two-python-dictionaries-in-a-single-expression                    
                    all_mapping = dict(street_abbrev_mapping.viewitems() | pinyin_mapping.viewitems() | mics_mapping.viewitems())     
                    updated,better_name = update_street_name(name, all_mapping)
                    if updated:
                        print name, "=>", better_name            

    if tag_type == 'city':
        city_types = audit_city(OSMFILE)

        for city_type, citys in city_types.iteritems():     
            for name in citys:               
                if audit_type == 'Inconsistentname':                
                    updated, better_name = update_city_name(name, city_mapping)
                    if updated:
                        print name, "=>", better_name                   
                

if __name__ == '__main__':
    test()