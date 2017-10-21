#!/usr/bin/python

""" 
    This is the code to accompany the Lesson 3 (decision tree) mini-project.

    Use a Decision Tree to identify emails from the Enron corpus by author:    
    Sara has label 0
    Chris has label 1
"""
    
import sys
from time import time
sys.path.append("../tools/")
from email_preprocess import preprocess

# from class_vis import prettyPicture, output_image
# from prep_terrain_data import makeTerrainData

import matplotlib.pyplot as plt
import numpy as np
import pylab as pl
# from classifyDT import classify


### features_train and features_test are the features for the training
### and testing datasets, respectively
### labels_train and labels_test are the corresponding item labels
features_train, features_test, labels_train, labels_test = preprocess()


#########################################################
### your code goes here ###


#########################################################

def classify(features_train, labels_train):
    
    ### your code goes here--should return a trained decision tree classifer
    from sklearn import tree
    clf = tree.DecisionTreeClassifier(min_samples_split=40)
    clf = clf.fit(features_train, labels_train)
    
    return clf

### the classify() function in classifyDT is where the magic
### happens--fill in this function in the file 'classifyDT.py'!
t0 = time()
clf = classify(features_train, labels_train)
print "training time:", round(time()-t0, 3), "s"

#### grader code, do not modify below this line

# prettyPicture(clf, features_test, labels_test)
# output_image("test.png", "png", open("test.png", "rb").read())

t1 = time()
pred =  clf.predict(features_test)
from sklearn.metrics import accuracy_score
acc = accuracy_score(labels_test, pred)
print "predict time:", round(time()-t1, 3), "s"

def submitAccuracies():
  return {"acc":round(acc,3)}

print submitAccuracies()
