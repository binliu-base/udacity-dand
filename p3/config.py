# -*- coding: UTF-8 -*-
#https://my.oschina.net/panjavay/blog/142682
import re

OSMFILE = "shenzhen_china.osm"
# SAMPLE_FILE = "shenzhen_sample.osm"
SAMPLE_FILE = "shenzhen_sample.osm.bck"

street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)
lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')
pinyin_re = re.compile(r"\b(Xi|Dong|Nan|Bei|Zhong)\b")
city_name_re = re.compile(u'(广东省深圳市|深圳+|Shenzhen|shenzhen)',re.IGNORECASE & re.UNICODE)    

street_expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road", 
            "Trail", "Parkway", "Commons", "West","East","North","South"]    

# UPDATE THIS VARIABLE
street_abbrev_mapping  = { 
            "St": "Street",
            "St.": "Street",
            "str": "Street",
            "Ave": "Avenue",
            "Ave.":"Avenue",
            "AV": "Avenue",            
            "Rd.":  "Road",
            "Rd":  "Road",
            "RD": "Road",            
            "PKWY": "Parkway",
            "Pkwy": "Parkway",            
            "Blvd": "Boulevard",
            "Blvd.": "Boulevard",
            "Boulavard": "Boulevard",
            "Pl": "Place",
            "Pl.": "Place",
            "Ln": "Lane",
            "Ln.": "Lane",
            "Dr": "Drive",
            "Dr.": "Drive"
            }

#http://wiki.openstreetmap.org/wiki/WikiProject_China#Generics_in_Chinese
pinyin_mapping = {
    "Dayuan":"Courtyard",
    "Jie":"Street",
    "Dajie":"Main Street",
    "Dong":"East",
    "Xi":"West",
    "Nan":"South",
    "Bei":"North",
    "Zhong":"Middle",
    "Qiao":"Bridge",
    "Lu":"Road",
    "Dadao":"Avenue", 
    u"Gaoxin S.":u"高新区南",
    "S.":"South",
    "N.":"North",
    "Tai zi":"Prince Road",
    u"Houhaibin":u"华强北路 Huangqiang North Road"
}

mics_mapping ={
    "road":"Road"

}

city_expected=u"深圳 Shenzhen"
city_mics=[u"大运新城",u"龙岗中心城",u"深圳市宝安区",u"深圳市罗湖区",u"深圳市南山区",u"体育新城",u"罗湖区 Luohu",u"盐田区"]

city_mapping ={
    u"广东省深圳市":u"深圳 Shenzhen",        
    u"深圳":u"深圳 Shenzhen",    
    u"深圳市 Shenzhen":u"深圳 Shenzhen",
    u"深圳市":u"深圳 Shenzhen",
    u"Shenzhen City":u"深圳 Shenzhen",
    u"Shenzhen, China":u"深圳 Shenzhen",
    u"shenzhen":u"深圳 Shenzhen",
    u"Shenzhen":u"深圳 Shenzhen"    
}


NODES_PATH = "nodes.csv"
NODE_TAGS_PATH = "nodes_tags.csv"
WAYS_PATH = "ways.csv"
WAY_NODES_PATH = "ways_nodes.csv"
WAY_TAGS_PATH = "ways_tags.csv"

LOWER_COLON = re.compile(r'^([a-z]|_)+:([a-z]|_)+')
PROBLEMCHARS = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')
UNDER_SCORE = re.compile(r'([a-zA-Z0-9_])([a-zA-Z0-9])', re.IGNORECASE)
SEMI_COLON = re.compile(r'([a-zA-Z0-9_ \t\n\r\f\v]);([a-zA-Z0-9_ \t\n\r\f\v])')    

# Make sure the fields order in the csvs matches the column order in the sql table schema
NODE_FIELDS = ['id', 'lat', 'lon', 'user', 'uid', 'version', 'changeset', 'timestamp']
NODE_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_FIELDS = ['id', 'user', 'uid', 'version', 'changeset', 'timestamp']
WAY_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_NODES_FIELDS = ['id', 'node_id', 'position']        


NODES_PATH = "nodes.csv"
NODE_TAGS_PATH = "nodes_tags.csv"
WAYS_PATH = "ways.csv"
WAY_NODES_PATH = "ways_nodes.csv"
WAY_TAGS_PATH = "ways_tags.csv"

LOWER_COLON = re.compile(r'^([a-z]|_)+:([a-z]|_)+')
PROBLEMCHARS = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')
PHONENUM = re.compile(r'\+1\s\d{3}\s\d{3}\s\d{4}')
POSTCODE = re.compile(r'[A-z]\d[A-z]\s?\d[A-z]\d')