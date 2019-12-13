## Libraries
import os
import numpy as np
import pandas as pd
import time
## models
from sklearn.svm import LinearSVC
from sklearn.ensemble import RandomForestClassifier
from lightgbm import LGBMClassifier
# KFold
from sklearn.model_selection import KFold, cross_validate, GridSearchCV, train_test_split
# save model
from sklearn.externals import joblib
# ignore warnings
import warnings
warnings.filterwarnings("ignore")
# helper functions
from helper import save_model

# variables
data_location = '../../data/'
model_location = "./"
cv_fit = True

# read input data
print("Reading Data...")
start = time.time()
X_train = pd.read_pickle(data_location + 'X_train_scaled.pkl')
y_train = pd.read_pickle(data_location + '/train_test_v2/y_train.pkl')

# remove problematic points
X_train = X_train.drop([5983])
y_train = y_train.drop([5983])

if cv_fit == False:
    X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, random_state=2018, test_size=0.2)

print('Read Data!')
print('Time: ',time.time() - start)

print("Train balance: %.4f%%"% (y_train.loc[y_train['label'] == 1].shape[0] / y_train.shape[0]*100))

model = LGBMClassifier(n_estimators = 100, n_jobs = -1, verbose = 1)

if cv_fit == False:
    # model definition
    model.fit(X_train.values, y_train.values.astype('int'))
    print('Model Training Completed!')
    final_model_location = save_model(model= model, model_dir= model_location, model_name="LightGBM_Unoptimized_512_prep_text")

if cv_fit == True:
    # find cross validation score
    print("Starting Cross Validation on Base model...")
    start = time.time()
    scoring = {
        'acc':'accuracy',
        'average_precision':'average_precision',
        'roc_auc':'roc_auc',
        'f1': 'f1',
        'f1_macro':'f1_macro',
        'precision':'precision',
        'recall':'recall'
    }
    scores = cross_validate(model, 
                            X = X_train.values, 
                            y = y_train.values.astype('int'), 
                            scoring = scoring, 
                            cv = 5, 
                            n_jobs = -1, 
                            verbose = 1, 
                            return_train_score = True)
    print('Cross Val Scores Available!')
    print(scores)
    print('Time: ',time.time() - start)

    # GridSearchCV params
    params = {
    #     'max_depth': [5, 10, 15, 25, 35, 50, 63],
    #     'num_leaves': [10, 15, 31, 50, 65, 85, 100],
    #     'n_estimators': [5, 15, 25, 60, 75, 100, 200, 350, 500, 750, 1000],
    #     'scale_pos_weight': [1, 2, 4, 6, 8, 10, 15],
    #     'min_data_in_leaf': [5, 10, 15, 20, 25, 30, 35, 40, 45, 50],
    #     'bagging_fraction': [0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
    #     'feature_fraction': [0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
    #     'learning_rate': [0.01, 0.03, 0.1, 0.3, 1.0]
        'max_depth': [10, 15],
        'num_leaves': [10, 31, 50],
        'n_estimators': [25, 100, 500],
        'learning_rate': [0.01, 0.1, 1.0]
    }
    # fit cross validation
    cv = GridSearchCV(estimator=model,
                      param_grid=params, 
                      scoring = scoring, 
                      n_jobs=-1, 
                      cv = 5, 
                      refit = 'f1_macro', 
                      verbose = 2)
    print("Starting Grid Search...")
    start = time.time()
    cv.fit(X_train.values, y_train.values.astype('int'))
    model = cv.best_estimator_
    print('Grid Search Completed!')
    print('Time: ',time.time() - start)

    model_performance = pd.DataFrame(cv.cv_results_)
    final_model_location = save_model(model= model, model_dir= model_location, model_name="LightGBM_Optimized_full")
    model_performance.to_pickle(final_model_location + 'model_performance.pkl')