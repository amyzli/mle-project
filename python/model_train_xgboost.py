import pandas as pd
import xgboost as xgb
from sklearn.model_selection import KFold, cross_val_score, GridSearchCV
from sklearn.metrics import roc_auc_score
import joblib
import os

def train_xgboost():
    py_dir_path = os.path.dirname(os.path.realpath(__file__))
    parent_dir = os.path.dirname(py_dir_path)
    dir_path = os.path.join(parent_dir, 'data')
    x_train = pd.read_csv(os.path.join(dir_path,'x_train.csv'))
    y_train = pd.read_csv(os.path.join(dir_path,'y_train.csv')).squeeze()
    
    model = xgb.XGBClassifier()
    
    param_grid = {
        'max_depth': [3, 5, 10],
        'n_estimators': [100, 200],
        'learning_rate': [0.01, 0.1, 0.2],
        'min_child_weight': [1],
        'alpha': [0.1],
        'gamma': [2],
        'scale_pos_weight': [90],
        'objective': ['binary:logistic'],
    }
    
    grid_search = GridSearchCV(model, param_grid, cv=3, scoring = 'roc_auc')
    grid_search.fit(x_train, y_train)
    
    best_params = grid_search.best_params_
    best_model = grid_search.best_estimator_

    print(f"Best Parameters: {best_params}")
    print(f"Best Score: {grid_search.best_score_}")

    joblib.dump(best_model, os.path.join(dir_path,'xgboost_model.pkl'))


if __name__ == "__main__":
    train_xgboost()
