#!/usr/bin/env python
# coding: utf-8

## Introduction
# 
# Machine learning (ML) workflows orchestrate and automate sequences of ML tasks by enabling activities such as:
# - data collection and transformation, 
# - model training, testing, evaluation and tuning
# - online/offline access to the model's predictive capabilities via an API.
# 
# In this notebook, a cloud-based ML worflow is proposed using as example the well-known [breast cancer Winsconsin diagnostics dataset](https://www.kaggle.com/uciml/breast-cancer-wisconsin-data). 
# 
# It is assumed that the data has been cleaned and prepared beforehand. Likewise, data exploration and feature engineering are left out of the scope of this notebook. *We will focus solely on data ingestion, model building and model serving aspects of the worflow.*

## Imports
import warnings

from joblib import dump
from datetime import date

import pandas as pd

import seaborn as sn
import matplotlib.pyplot as plt

from sklearn.metrics import confusion_matrix
from sklearn.datasets import load_breast_cancer
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import GridSearchCV, train_test_split

BASE_PATH = '/usr/local/automated_workflow'

## Data Ingestion
print("Ingesting data...")

# Load and show data from breast cancer dataset.
bc_dataset = load_breast_cancer()
bc_df = pd.DataFrame(data=bc_dataset.data, columns=bc_dataset.feature_names)
bc_df.head()

## Automated Model Training
print("Training model...")
# I'll keep `train_test_split` parameters as close to default as possible, but still reproductible with random_state and test_size manually set`

# Split train and test data.
X = bc_dataset.data
y = bc_dataset.target
class_names = bc_dataset.target_names

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.25,
    random_state=42
)

# Filter warning from GridSearchCV.
warnings.filterwarnings('ignore')

# Grid search parameteres setup.
param_grid = {
    'criterion':['gini', 'entropy'],
    'splitter':['best', 'random'],
    'max_features':['sqrt', 'log2', None],
}

# Run grid search on a Decision Tree model.
clf = GridSearchCV(
    DecisionTreeClassifier(random_state=42),
    param_grid,
    scoring='precision_macro',
    cv=10,
    n_jobs=4
)

# Fit best Decision Tree model according to the grid search.
clf.fit(X_train, y_train);

# See best estimator's parameteres.
print("Best estimator:", clf.best_estimator_)

# Set up confusion matrix.
y_pred = clf.predict(X_test)
df_cm = pd.DataFrame(confusion_matrix(y_test, y_pred))

# Plot confusion matrix.
sn.heatmap(df_cm, annot=True, cbar=False, xticklabels=class_names, yticklabels=class_names).set_ylim([0,2])
plt.ylabel('Actual')
plt.xlabel('Predicted')
plt.show()

## Model Persistence
datetime_string = date.today().strftime("%Y_%m_%d")
SAVED_MODEL_PATH = f"{BASE_PATH}/api/saved_models/saved_model_{datetime_string}.joblib"
print(f"Saving best automatically generated model at: {SAVED_MODEL_PATH} ...")

# Save trained model and append today's date to its filename.
dump(clf.best_estimator_, f'{BASE_PATH}/api/saved_models/saved_model_{datetime_string}.joblib')

print("Finished training worflow. Waiting for the API to load...")
