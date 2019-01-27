import os
import sys
from django.db import models
from quiz.models import machineLearn
# Import necessary libraries
import numpy as np
import pandas as pd

from django.apps import apps
from .models import machineLearn
# In[4]:

# Load data
#data = pd.read_csv("C:/Users/abich/OneDrive/Desktop/student-data-edited.csv")
#data = pd.read_csv("C:\\Users\\abich\\Documents\\owlLearning\\learning\\data\\student-data-edited.csv")
#data = pd.read_csv("C:/Users/aishw/Desktop/student-data-edited.csv")

#data = pd.DataFrame(list(machineLearn.objects.all().values()))
data = pd.DataFrame.from_records(machineLearn.objects.all().values())

# In[5]:

# Analyse the dataset
#Examine the first few rows of data
data.head()


# In[6]:


# Summary statistics for numerical variables
summary = data.describe()
summary = summary.transpose()
print(summary)


# In[7]:


# Prepare the data for processing
nrows = data.shape[0]
ncols = data.shape[1]

X = data.iloc[:,0:10]
Y = data["passed"]

# Preprocess feature columns
def preprocess_features(X):
    outX = pd.DataFrame(index=X.index)  # output dataframe, initially empty

    # Check each column
    for col, col_data in X.iteritems():
        # If data type is non-numeric, try to replace all yes/no values with 1/0
        if col_data.dtype == object:
            col_data = col_data.replace(['yes', 'no'], [1, 0])
        # Note: This should change the data type for yes/no columns to int

        # If still non-numeric, convert to one or more dummy variables
        if col_data.dtype == object:
            col_data = pd.get_dummies(col_data, prefix=col)  # e.g. 'school' => 'school_GP', 'school_MS'

        outX = outX.join(col_data)  # collect column(s) in output dataframe

    return outX

X = preprocess_features(X)
X.head()


# In[8]:


#Split the data into training and test sets
from sklearn.model_selection import train_test_split
import math

xTrain, xTest, yTrain, yTest = train_test_split(
  X, Y, test_size=1/3, random_state=0)


# In[9]:


#Training and evaluating the models:
#Models in consideration:
# 1) Gaussian Naive Bayes
# 2) Support Vector Machine
# 3) Random Forest
# 4) Logistic Regression (Ridge)
from sklearn.metrics import f1_score


# In[10]:


# Gaussian Naive Bayes:
from sklearn.naive_bayes import GaussianNB
clf_GNB = GaussianNB()
clf_GNB.fit(xTrain, yTrain)
y_pred_GNB = clf_GNB.predict(xTest)
f1score_GNB = f1_score(yTest,y_pred_GNB,pos_label="yes")
print(f1score_GNB)


# In[11]:


# Support Vector Machine:
from sklearn.svm import SVC
clf_SVC = SVC()
clf_SVC.fit(xTrain, yTrain)
y_pred_SVC = clf_SVC.predict(xTest)
f1score_SVC = f1_score(yTest,y_pred_SVC,pos_label="yes")
print(f1score_SVC)


# In[12]:


#Random Forest
from sklearn import ensemble
clf_RF = ensemble.RandomForestClassifier()
clf_RF.fit(xTrain, yTrain)
y_pred_RF = clf_RF.predict(xTest)
f1score_RF = f1_score(yTest,y_pred_RF,pos_label="yes")
print(f1score_RF)


# In[13]:


# Logistic Regression (Ridge)
from sklearn.linear_model import RidgeClassifier
clf_RIDGE = RidgeClassifier()
clf_RIDGE.fit(xTrain, yTrain)
y_pred_RIDGE = clf_RIDGE.predict(xTest)
f1score_RIDGE = f1_score(yTest,y_pred_RIDGE,pos_label="yes")
print(f1score_RIDGE)


# In[14]:


#Further evaluation of model (using AUC values)
from sklearn.metrics import roc_auc_score

def pred_to_num(yvec):
    new_yvec = []
    for i in range(len(yvec)):
        if yvec[i] == "yes":
            new_yvec.append(1)
        elif yvec[i] == "no":
            new_yvec.append(0)
    return new_yvec

def compute_auc(y_true,y_scores):
    y_true = np.array(pred_to_num(y_true))
    y_scores = np.array(pred_to_num(y_scores))
    roc_score = roc_auc_score(y_true, y_scores)
    return roc_score

#Compute the AUC values for all 4 models:
print(compute_auc(np.array(yTest),y_pred_GNB))
print(compute_auc(np.array(yTest),y_pred_SVC))
print(compute_auc(np.array(yTest),y_pred_RF))
print(compute_auc(np.array(yTest),y_pred_RIDGE))


# In[15]:


#Final Model Selection:
#Final Model Selected: Random Forest
#Reason: Larger AUC value corresponding to the area
# under the respective ROC curve

#F1 Score of chosen model:
print(f1score_RF)

#AUC value of chosen model:
print(compute_auc(np.array(yTest),y_pred_RF))

#Predicted Values from chosen model:
print(y_pred_RF)

