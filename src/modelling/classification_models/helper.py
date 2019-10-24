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
from sklearn.model_selection import KFold, cross_validate, GridSearchCV
# save model
from sklearn.externals import joblib
# ignore warnings
import warnings
warnings.filterwarnings("ignore")

def save_model(model, model_dir, model_name):
    # save model to directory
    timestr = time.strftime("%Y%m%d-%H%M%S")
    directory = model_dir + model_name + "_" + timestr + '/'
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    # save model in folder
    file_name = model_name + timestr + '.pkl'
    joblib.dump(model, directory + file_name)
    return directory_file_name