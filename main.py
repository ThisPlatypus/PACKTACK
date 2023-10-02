import functools
import numpy as np
import pandas as pd
import sklearn
from sklearn.datasets import load_iris
import functools
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, precision_score, recall_score, ConfusionMatrixDisplay
from sklearn.model_selection import RandomizedSearchCV, train_test_split
from scipy.stats import randint

dataset_name=['CTU-IoT-Malware-Capture-21-1','CTU-IoT-Malware-Capture-42-1', 'CTU-IoT-Malware-Capture-3-1']


dati = {
    data_name: pd.read_csv(
        f"/Users/chiara/PycharmProjects/PACKTACK/CleanData/{data_name}.txt",
        sep="\t",
        header=0,
    )
    for data_name in dataset_name
}
# Standardizzation
from sklearn import preprocessing
import numpy as np


Ys_label={}
Xs_fact, Xs_num, Xs_std={}, {},{}
for dato in dati:
    Ys_label[dato]= dati[dato].label.map({'Benign':0,'Malicious':1})
    Xs_fact = dati[dato].drop(labels=["duration","orig_bytes","resp_bytes","local_orig","local_resp","missed_bytes","tunnel_parents" ,"label","detailed.label"], axis=1)
    Xs_num[dato]= dati[dato].select_dtypes(include=np.number).drop(labels=['ts', 'id.orig_p', 'id.resp_p' ], axis=1)

    Xs_std[dato] = preprocessing.scale(Xs_num[dato])

# Split data
X_train={}
X_test={}
y_train={}
y_test={}

for dato in dati:
    X_train[dato], X_test[dato], y_train[dato], y_test[dato] = train_test_split(Xs_std[dato], Ys_label[dato], test_size=0.2)



# FIND THE BEST PARAMETER

best_rf={}
for dato in dati:
    param_dist = {'n_estimators': randint(50,500),
                  'max_depth': randint(1,20)}

    # Create a random forest classifier
    rf = RandomForestClassifier()

    # Use random search to find the best hyperparameters
    rand_search = RandomizedSearchCV(rf,
                                     param_distributions = param_dist,
                                     n_iter=5,
                                     cv=5)

    # Fit the random search object to the data
    rand_search.fit( X_train[dato], y_train[dato])
    # Create a variable for the best model
    best_rf[dato] = rand_search.best_estimator_

    # Print the best hyperparameters
    print(f'{dato} - Best hyperparameters:',  rand_search.best_params_)

# Function for generate the RF_Classifier
def generate_rf(X_train, y_train, X_test, y_test, best_param):
    rf = best_param
    rf.fit(X_train, y_train)
    print ("rf score ", rf.score(X_test, y_test))
    y_pred = rf.predict(X_test)
    #accuracy = accuracy_score(y_test, y_pred)
    return rf

# Aggregation RF
def combine_rfs(rf_a, rf_b):
    rf_a.estimators_ = rf_a.estimators_  + rf_b.estimators_
    rf_a.n_estimators = len(rf_a.estimators_)
    return rf_a


# TRAIN
rfs = [
    generate_rf(
        X_train[dato], y_train[dato], X_test[dato], y_test[dato], best_rf[dato]
    )
    for dato in [
        'CTU-IoT-Malware-Capture-21-1',
        'CTU-IoT-Malware-Capture-42-1',
        'CTU-IoT-Malware-Capture-3-1',
    ]
]
rf_combined = functools.reduce(combine_rfs,rfs)
# the combined model scores better than *most* of the component models
X=np.concatenate([X_test['CTU-IoT-Malware-Capture-21-1'],X_test['CTU-IoT-Malware-Capture-42-1'],X_test['CTU-IoT-Malware-Capture-3-1']], axis=0)
Y=np.concatenate([y_test['CTU-IoT-Malware-Capture-21-1'],y_test['CTU-IoT-Malware-Capture-42-1'], y_test['CTU-IoT-Malware-Capture-3-1']], axis=0)
print ("rf combined score", rf_combined.score(X, Y))