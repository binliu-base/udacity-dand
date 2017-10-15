# Identifying Persons of Interest from the Enron Corpus
##### By Bin LIu

#### Question 1 *Summarize for us the goal of this project and how machine learning is useful in trying to accomplish it. As part of your answer, give some background on the dataset and how it can be used to answer the project question. Were there any outliers in the data when you got it, and how did you handle those?*

The goal of this project is to create a model (a Person Of Interest (POI) Classifier),  which will accurately predict if someone should be a person of interest for fraud by using the Enron email and financial dataset. Machine learning is useful in trying to accomplish this goal because of it's ability to find trends, categorize data and learn from this information in order to apply these learnings to new datasets. The dataset used for this project was preprocessed and stitched together by Katie Malone from Udacity.

The interesting and hard part of the dataset is that the distribution of the non-POI's to POI's is very skewed, given that from the 146 there are only 18 people or data points labeled as POI's or guilty of fraud. We are interested in labeling every person in the dataset into either a POI or a non-POI (POI stands for Person Of Interest).  Each person had 21 possible features. These features are either financial data or features extracted from emails. Financial data includes features like salary and bonus while the email features include number of messages written/received and to whom/form.

**Missing Values of Each Feature in the Dataset**: 

| Feature                    | # NaN values   |
| -------------------------- |:--------------:|
| salary                     | 51             |
| to_messages                | 60             |
| deferral_payments          | 107            |
| total_payments             | 21             |
| loan_advances              | 142            |
| bonus                      | 64             |
| email_address              | 35             |
| restricted_stock_deferred  | 128            |
| total_stock_value          | 20             |
| shared_receipt_with_poi    | 60             |
| long_term_incentive        | 80             |
| exercised_stock_options    | 44             |
| from_messages              | 60             |
| other                      | 53             |
| from_poi_to_this_person    | 60             |
| from_this_person_to_poi    | 60             |
| poi                        | 0              |
| deferred_income            | 97             |
| expenses                   | 51             |
| restricted_stock           | 36             |
| director_fees              | 129            |

Sixty of the people in the dataset had no values for the email features (including 4 Persons of Interest) and 3 people had no values for the finanical features (Ronnie Chan, William Powers, and Eugene E. Lockhart, none of them are Persons of Interest).

 I plot salaries and bonuses on Enron data to check the outliers, A scatterplot of these features revealed one point with values much larger than the other points.  Comparing the values to the financial information given in 'enron61702insiderpay.pdf' revealed that the point belonged to 'TOTAL'.  This point was removed from the dictionary of data as being an artifact of the spreadsheet.  A second scatterplot revealed two different point with values much larger than all of the other points.  This point belonged to Kenneth Lay and Skilling Jeffery, both are Person of Interest. These very meaningful point was left in the dataset. 

The outlier point is "TOTAL"  
![outlier_of_TOTAL](/p5/final_project/outlier_of_TOTAL.png)  
Two more outlier point "LAY KENNETH L" and "SKILLING JEFFREY K"  
![two_more_outliers](/p5/final_project/two_more_outliers.png)

#### Question 2 *What features did you end up using in your POI identifier, and what selection process did you use to pick them? Did you have to do any scaling? Why or why not? As part of the assignment, you should attempt to engineer your own feature that does not come ready-made in the dataset -- explain what feature you tried to make, and the rationale behind it. (You do not necessarily have to use it in the final analysis, only engineer and test it.) In your feature selection step, f you used an algorithm like a decision tree, please also give the feature importances of the features that you use, and if you used an automated feature selection function like SelectKBest, please report the feature scores.*

Feature selection was performed by recursive feature elimination with cross-validation. For each feature, a coefficient was calculated assuming that all other features were held constant. This was done by a DecisionTree classifier. Min-Max scaling preserves zero values in the data, which is useful in this case because missing values are coded as zero within the featureFormat function.  After the coefficients are calculated, the feature whose coefficient is closest to zero is discarded and the process is repeated.  At each step, the overall model is evaluated using F1 score as a metric. 

![](/p5/final_project/featureSelection1.png)  

Two features were engineered for testing of the model.
* fraction_to_poi - a fraction of the total 'to' emails that were sent to a POI 
* fraction_from_poi - a fraction of the total 'from' emails that were received from a POI

 I added the two engineered features to those selected above and ran the recursive feature elimination again.  This time, the best results came from using  5 features and the F1 score improved from 0.214 to 0.334.  The final features were: 'expenses', 'exercised_stock_options', 'total_payments','shared_receipt_with_poi' and one of the engineered features, 'fraction to POI'.  This is the feature set that will be used to select a classification algorithm.  
![](/p5/final_project/featureSelection2.png)  


#### Question 3 *What algorithm did you end up using? What other one(s) did you try? How did model performance differ between algorithms?*

I tried two of the most popular algorithms: random forest and adaboost. In random forest, a series of decision trees are built on randomized subsets of the data.  At each node, a randomized subset of variables is evaluated to find the best split.  This creates a “forest” of independent, randomized trees.  The predictions of all the trees are averaged to assign a predicted label.  I started with the default options, though I set class weights to be inversely proportional to their representation in the dataset.  AdaBoost is also an ensemble of decision trees, but the trees are not independent.  First, a single tree is fit using all of the data.  Incorrectly assigned points are then given a higher weight (boosted) and the process is repeated.  By default, adaboost uses trees of depth 1, single feature trees called decision stumps.

Model|Time|F1 Score|Precision|Recall
----|---|---|----|----  
Random Forest|1.441s|0.250|0.523|0.165
AdaBoost|6.421s|0.406|0.486|0.350

AdaBoost was better than random forest according to each metric, but took almost 5 times as long. so I will select AdaBoost and attempt to tune the algorithms.

#### Question 4 *What does it mean to tune the parameters of an algorithm, and what can happen if you don’t do this well?  How did you tune the parameters of your particular algorithm? (Some algorithms do not have parameters that you need to tune -- if this is the case for the one you picked, identify and briefly explain how you would have done it for the model that was not your final choice or a different model that does utilize parameter tuning, e.g. a decision tree classifier).*

Tuning the parameters of an algorithm refers to adjustments made when training the algorithm to improve the fit on the test data set.  It is very easy to overfit the training data by including too many features, but such an algorithm will not make good predictions.  Overfitting can be avoided by holding make a subset of the data to test the algorithm's predictions against.  

I used the GridSearchCV function to determine the optimized parameters. Given a set of parameters, this function evaluates (fit, transforms) all of the possible combinations, then returns a classifier, that provides the best score. For adaboost, the main parameters for tuning are the number of weak estimators and their complexity.  In this case the estimators are decision trees, so I tune the number of them and their maximum depth.  


#### Question 5 *What is validation, and what’s a classic mistake you can make if you do it wrong? How did you validate your analysis?*

Validation refers to checking the algorithm's predictions against data that was not used for training the algorithm to prevent the algorithm from simply memorizing the training data (overfitting).  However, this dataset is already very small with only 14 Persons of Interest.  A single split into a training and test set would not give a very accurate estimate of error.  Instead, throughout this analysis, I use the StratifiedShuffleSplit function to randomly split the data into 30% test set and 70% training while keeping the fraction of POIs in each split relatively constant.

#### Question 6 *Give at least 2 evaluation metrics and your average performance for each of them.  Explain an interpretation of your metrics that says something human-understandable about your algorithm's performance.*

The final model (AdaBoost) had precision = 0.46, recall = 0.39, and F1 = 0.42.  This means that given a Person of Interest, the algorithm will recognize it almost of the time and that 46% of POIs flagged by the algorithm will have actually pled guilty to a crime connected to the Enron scandal. The F1 score is a combination of the two metrics, F1 = 2 * (precision * recall) / (precision + recall).
