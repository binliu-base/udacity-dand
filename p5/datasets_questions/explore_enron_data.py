#!/usr/bin/python
# -*- coding: utf-8 -*-


# Reference
# http://napitupulu-jon.appspot.com/posts/datasets-questions.html
""" 
    Starter code for exploring the Enron dataset (emails + finances);
    loads up the dataset (pickled dict of dicts).

    The dataset has the form:
    enron_data["LASTNAME FIRSTNAME MIDDLEINITIAL"] = { features_dict }

    {features_dict} is a dictionary of features associated with that person.
    You should explore features_dict as part of the mini-project,
    but here's an example to get you started:

    enron_data["SKILLING JEFFREY K"]["bonus"] = 5600000
    
"""

import pickle
import pandas as pd

enron_data = pickle.load(open("../final_project/final_project_dataset.pkl", "r"))

enron_df = pd.DataFrame(enron_data)

# print enron_df.shape

# print enron_df.index
# poi_df = enron_df [enron_df.ix['poi'] == True]
# poi =[ for x in enron_df.ix['poi'] if x == True]

poi =  [ column for column in enron_df.columns if enron_df[column]['poi'] == True]
# print len(poi)

#18 practice 查询数据集
# print enron_data['PRENTICE JAMES']['total_stock_value']

#19 practice 查询数据集
# print enron_data['COLWELL WESLEY']['from_this_person_to_poi']

#20 practice 查询数据集
#print enron_data['SKILLING JEFFREY K']['exercised_stock_options']


#25 practice 查询数据集
# print enron_data['SKILLING JEFFREY K']['total_payments']
# print enron_data['LAY KENNETH L']['total_payments']
# print enron_data['FASTOW ANDREW S']['total_payments']

#27
count_salary = 0
count_email = 0
for key in enron_data.keys():
    if enron_data[key]['salary'] != 'NaN':
        count_salary+=1
    if enron_data[key]['email_address'] != 'NaN':
        count_email+=1
print count_salary
print count_email