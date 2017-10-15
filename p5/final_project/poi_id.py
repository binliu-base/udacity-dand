#!/usr/bin/python

import sys
import pickle
sys.path.append("../tools/")

from feature_format import featureFormat, targetFeatureSplit
from tester import dump_classifier_and_data
import pandas as pd
from sklearn.tree import DecisionTreeClassifier


### Task 1: Select what features you'll use.
### features_list is a list of strings, each of which is a feature name.
### The first feature must be "poi".
# features_list = ['poi','salary'] # You will need to use more features

### Load the dictionary containing the dataset
data_dict = pickle.load(open("final_project_dataset.pkl", "r") ) 

print('#######  Task 1. Data Exploration #########')
# people = data_dict.keys()
data_df = pd.DataFrame(data_dict)
people = data_df.columns.tolist()
print('Total number of data points: %d' % data_df.shape[1])

def poi_count():
    poi_count = 0
    # for person in data_dict.keys():
    for person in people:            
        poi_count += data_df[person]['poi']    
    return poi_count

POI_count = poi_count()

print('Number of people with POI flag: {}'.format(POI_count))
print('Number of people without POI flag: {}'.format((len(people) - POI_count)))

### Feature Exploration
all_features = data_df.index.tolist()
print('Each person has {} features available'.format(len(all_features)))

### Evaluate dataset for completeness
missing_values = {}
for feature in all_features:
    missing_values[feature] = 0
for person in people:
    records = 0
    for feature in all_features:
        if data_dict[person][feature] == 'NaN':
            missing_values[feature] += 1
        else:
            records += 1

### Print results of completeness analysis
print('Number of Missing Values for Each Feature:')
for feature in all_features:
    print("%s: %d" % (feature, missing_values[feature]))

### Is anyone missing all financial information?
incomplete_money = []
for person in data_dict.keys():  
    if data_dict[person]['total_payments'] == 'NaN' and \
    data_dict[person]['total_stock_value'] == 'NaN':
        incomplete_money.append(person)
print
if len(incomplete_money) > 0:
    print('The following people have no data for payments and stock value:')
    counter = 0
    for person in incomplete_money:
        print person        
        counter += data_dict[person]['poi']
    print('Of these %d people %d of them are POIs' % (len(incomplete_money), 
          counter))
else:
    print('No person is missing both payments and stock value.')
print
    
### Is anyone missing all email information?
incomplete_email = []
for person in data_dict.keys():
    if data_dict[person]['to_messages'] == 'NaN' and \
       data_dict[person]['from_messages'] == 'NaN':
        incomplete_email.append(person)    
if len(incomplete_email) > 0:
    print('The following people have no message data for emails:')
    counter = 0
    for person in incomplete_email:
        print("%s, POI: %r" % (person, data_dict[person]['poi']))        
        counter += data_dict[person]['poi']
    print('Of these %d people, %d of them are POIs' % (len(incomplete_email), counter))
else:
    print('No person is missing both to and from message records.')


### Task 2: Remove outliers
import matplotlib.pyplot as plt
# %matplotlib inline  

def OutlierPlot(data_dict, xFeature, yFeature, outliers,figname,flag='poi'):
    'Create a scatterplot to identify outliers. Use first feature to flag data.'
    
    data = featureFormat(data_dict, [flag, xFeature, yFeature])  
    ### Plot features with flag=True in red

    for point in data:
        x = point[1]
        y = point[2]
        if point[0]:
            poi = plt.scatter(x, y, color="r", marker="*", label='poi')
        else:
            nopoi = plt.scatter(x, y, color='b', marker=".",label='non-poi')
    plt.xlabel(xFeature,fontsize=12)
    plt.ylabel(yFeature,fontsize=12)
    plt.legend(loc='best',handles=[poi, nopoi])
    
    for outlier in outliers:    
        plt.annotate(outlier[2], xy=(outlier[0], outlier[1]), xytext=(outlier[0]*.7, outlier[1]*.7),
                    arrowprops=dict(facecolor='black', shrink=0.05,width=1),
                    )
    plt.title(figname,fontsize=16)    
    picture = figname + '.png'         
    plt.savefig(picture, transparent=False)    
    plt.show()  

### Check for outliers between financial features
print ""
print('#######  Task 2. Remove outliers in financial features #########')
outliers = [(data_df['TOTAL']['salary'],data_df['TOTAL']['bonus'],data_df['TOTAL'].name)]
OutlierPlot(data_dict, 'salary', 'bonus',outliers,'outlier_of_TOTAL')
print('The obvious outlier belongs to TOTAL, so it is removed')

data_dict.pop( 'TOTAL', 0 ) # remove spreadsheet total line
outliers = [
    (data_df['LAY KENNETH L']['salary'],data_df['LAY KENNETH L']['bonus'],data_df['LAY KENNETH L'].name),
    (data_df['SKILLING JEFFREY K']['salary'],data_df['SKILLING JEFFREY K']['bonus'],data_df['SKILLING JEFFREY K'].name)           
          ]
OutlierPlot(data_dict, 'salary', 'bonus',outliers,'two_more_outliers')          
print('The obvious outlier point belongs to Ken Lay and Skilling Jeffrey, so it is left in.')


### Explore email features
# OutlierPlot(data_dict, 'from_poi_to_this_person', 'from_this_person_to_poi')
# print 'Email messages with POIs has a large range of values.'
# OutlierPlot(data_dict, 'from_messages', 'to_messages')
# print 'Total emails also have a large range.'  


### Task 3: Create new feature(s)
print ""
print('#######  Task 3.a. Create new feature(s) #########')
def computeFraction( poi_messages, all_messages ):
    """ given a number messages to/from POI (numerator) 
        and number of all messages to/from a person (denominator),
        return the fraction of messages to/from that person
        that are from/to a POI
   """

    fraction = 0.
    if all_messages > 0:
        fraction=float(poi_messages)/float(all_messages)
    else:
        fraction = 0.

    return fraction

for name in data_dict.keys():
    data_point = data_dict[name]

    to_poi = float(data_point["from_this_person_to_poi"])
    to_all = float(data_point["from_messages"])
    fraction_to_poi = computeFraction(to_poi,to_all)    
    data_point["fraction_to_poi"] = fraction_to_poi

    from_poi = float(data_point["from_poi_to_this_person"])
    from_all = float(data_point["to_messages"])
    fraction_from_poi = computeFraction(from_poi,from_all)
    data_point["fraction_from_poi"] = fraction_to_poi

############# Evaluate new features
print ""
print('#######  Task 3.b. Evaluate new feature(s) #########')
# print('############### Feature Selection ###################')
### features_list is a list of strings, each of which is a feature name.
### The first feature must be "poi". Start with all features except email addr.

# the email_address feature being removed
features_list = ['poi', 'salary', 'bonus', 'long_term_incentive', \
                 'deferred_income', 'deferral_payments', 'loan_advances', \
                 'other', 'expenses', 'director_fees', 'restricted_stock', \
                 'exercised_stock_options', 'restricted_stock_deferred', \
                 'total_payments', 'total_stock_value', \
                 'from_poi_to_this_person', 'from_this_person_to_poi', \
                 'shared_receipt_with_poi', 'from_messages', 'to_messages']


from sklearn.feature_selection import RFECV 
# Recursive Feature Elimination with Cross Validation
from sklearn.svm import SVC
# Support Vector Classifier to estimate fit coefficients for each feature
from sklearn.cross_validation import StratifiedShuffleSplit
# cross validation maintain roughly equal number of POIs in each split
from sklearn.preprocessing import MinMaxScaler

def FeatureSelection(data_dict, features_list,figname):                
# def FeatureSelection(labels, features):                
    # Convert dictionary to numpy array, converts NaN to 0.0                  
    data = featureFormat(data_dict, features_list, \
                            sort_keys = True, remove_all_zeroes = False)
    # Separate into labels = 'poi' and features = rest of features_list
    labels, features = targetFeatureSplit(data)

    ### Create Estimator 
    # which will update the coefficients with each iteration
    # class weight is set to auto because of unbalanced data classes
    # weight will be inversely proportional to class size

    svc = SVC(kernel='linear', class_weight='balanced', random_state=42)    
    # clfDT= DecisionTreeClassifier(min_samples_split=7)    

    ############## Scale features ######################
    # SVC algorithm requires use scaled features
    # missing values are coded 0.0, so MinMax will preserve those zero values
    scaler = MinMaxScaler()
    features = scaler.fit_transform(features)
    
    ### Select cross-validation method
    # StratifiedShuffleSplit keeps roughly the same number of POIs in each split 
    sss = StratifiedShuffleSplit(labels, 100, test_size=0.3, random_state=42)
    ### Select evaluation metric
    # Evaluate model using f1 = 2 * (precision * recall) / (precision + recall)
    # Model should be able to predict POIs, which are a small percentage of cases
    metric = 'f1'
    # run the feature eliminater
    rfecv = RFECV(estimator=svc, cv=sss, scoring=metric, step=1)
    # rfecv = RFECV(estimator=clfDT, cv=sss, scoring=metric, step=1)    
    rfecv = rfecv.fit(features, labels)
    
    # view results
    import matplotlib.pyplot as plt
    plt.figure()
    plt.xlabel("Number of features selected", fontsize=12)
    plt.ylabel("Cross validation score using F1 (precision&recall)",fontsize=12)
    plt.plot(range(1, len(rfecv.grid_scores_) + 1), rfecv.grid_scores_)
    plt.title('Feature Selection', fontsize=16)
    picture = figname + '.png'
    plt.savefig(picture, transparent=False)    
    plt.show()
    print("Optimal number of features is %d" % rfecv.n_features_)
    print('Features selected by recursive feature elimination with cross validation:')
    F1_score = round(rfecv.grid_scores_[rfecv.n_features_], 3)
    print('F1 score from optimal features: %r' % F1_score)
    selection = rfecv.get_support()
    selected_features = ['poi']
    rejected_features = []
    for i in range(len(selection)):
        if selection[i]:
            selected_features.append(features_list[i + 1]) # first feature is 'poi'=the label
        else:
            rejected_features.append(features_list[i + 1])
    print(selected_features[1:])
    print('Features eliminated:')
    print(rejected_features)
    return selected_features, F1_score
    
features_list, initial_F1 = FeatureSelection(data_dict, features_list,'featureSelection1')

### Add new feature to features_list
features_list.extend(['fraction_to_poi', 'fraction_from_poi'])
features_list, second_F1 = FeatureSelection(data_dict, features_list,'featureSelection2')

#### keep the engineered features added to data_dict
my_dataset = data_dict

# ### Extract features and labels from dataset for local testing
# data = featureFormat(my_dataset, features_list, sort_keys = True)
# labels, features = targetFeatureSplit(data)

# ### Task 4: Try a varity of classifiers
# ### Please name your classifier clf for easy export below.
# ### Note that if you want to do PCA or other multi-stage operations,
# ### you'll need to use Pipelines. For more info:
# ### http://scikit-learn.org/stable/modules/pipeline.html

print ""
print('#######  Task 4.a. Select Classifier #########')

##### Random Forest
from sklearn.ensemble import RandomForestClassifier
clf_rf = RandomForestClassifier(class_weight='balanced', random_state=42)
from time import time
from tester import test_classifier
t0 = time()
test_classifier(clf_rf, data_dict, features_list, folds = 100)
print("Random forest fitting time: %rs" % round(time()-t0, 3))

###### Adaboost
from sklearn.ensemble import AdaBoostClassifier
clf_ab = AdaBoostClassifier(random_state=42)
t0 = time()
test_classifier(clf_ab, data_dict, features_list, folds = 100)
print("AdaBoost fitting time: %rs" % round(time()-t0, 3))

# ### Task 5: Tune your classifier to achieve better than .3 precision and recall 
# ### using our testing script. Check the tester.py script in the final project
# ### folder for details on the evaluation method, especially the test_classifier
# ### function. Because of the small size of the dataset, the script uses
# ### stratified shuffle split cross validation. For more info: 
# ### http://scikit-learn.org/stable/modules/generated/sklearn.cross_validation.StratifiedShuffleSplit.html
print ""
print('#######  Task 5. Tune Parameters of Classifier #########')
# # Example starting point. Try investigating other evaluation techniques!
# from sklearn.cross_validation import train_test_split
# features_train, features_test, labels_train, labels_test = \
#     train_test_split(features, labels, test_size=0.3, random_state=42)

# Convert dictionary to numpy array, converts NaN to 0.0                  
data = featureFormat(data_dict, features_list, \
                     sort_keys = True, remove_all_zeroes = False)
# Separate into labels = 'poi' and features = rest of features_list
labels, features = targetFeatureSplit(data)

from sklearn.grid_search import GridSearchCV
from sklearn.cross_validation import StratifiedShuffleSplit

sss = StratifiedShuffleSplit(labels, 100, test_size=0.3, random_state=42)
metric = 'f1'

### Tuning Random Forest
# rf_params = {'max_features': range(1,5), 'n_estimators': range(10, 101, 10),'n_jobs': [4]}
rf_params = {'max_features': range(1,5), 'n_estimators': range(10, 101, 10)}
# use same estimator (rf, random forest) as above; add suffix t for tuned
t0 = time()
rft = GridSearchCV(clf_rf, rf_params, scoring=metric, cv=sss)
print("Random Forest tuning: %r" % round(time()-t0, 3))
t0 = time()
rft = rft.fit(features, labels)
print("Random forest fitting time: %rs" % round(time()-t0, 3))
rf = rft.best_estimator_
t0 = time()
test_classifier(rf, data_dict, features_list, folds = 100)
print("Random Forest evaluation time: %rs" % round(time()-t0, 3))

### Tuning AdaBoost
dt = []
for i in range(5):
    # dt.append(DecisionTreeClassifier(max_depth=(i+1)))
    dt.append(DecisionTreeClassifier(max_depth=(i+1),min_samples_leaf=2, class_weight='balanced'))    

# ab_params = {'base_estimator': dt, 'n_estimators': range(50, 101, 10),'learning_rate':[.2]}
ab_params = {'base_estimator': dt, 'n_estimators': range(50, 101, 10),'learning_rate':[.8]}
t0 = time()
abt = GridSearchCV(clf_ab, ab_params, scoring=metric, cv=sss)
print("AdaBoost tuning: %r" % round(time()-t0, 3))
t0 = time()
abt = abt.fit(features, labels)
print("AdaBoost fitting time: %rs" % round(time()-t0, 3))
ab = abt.best_estimator_
t0 = time()
test_classifier(ab, data_dict, features_list, folds = 100)
print("AdaBoost evaluation time: %rs" % round(time()-t0, 3))

### Select tuned adaboost as best classifier
clf = ab
# ### Task 6: Dump your classifier, dataset, and features_list so anyone can
# ### check your results. You do not need to change anything below, but make sure
# ### that the version of poi_id.py that you submit can be run on its own and
# ### generates the necessary .pkl files for validating your results.

dump_classifier_and_data(clf, my_dataset, features_list)