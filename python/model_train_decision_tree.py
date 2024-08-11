import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import KFold, cross_val_score, GridSearchCV
from sklearn.metrics import roc_auc_score
import joblib
import os



def train_random_forest():
    py_dir_path = os.path.dirname(os.path.realpath(__file__))
    parent_dir = os.path.dirname(py_dir_path)
    dir_path = os.path.join(parent_dir, 'data')
    x_train = pd.read_csv(os.path.join(dir_path, 'x_train.csv'))
    y_train = pd.read_csv(os.path.join(dir_path,'y_train.csv')).squeeze()

    model = DecisionTreeClassifier(random_state=42)

    param_grid = {
        'min_samples_leaf': [1, 2],
        'max_depth': [5, 10],
        'min_samples_split': [5],
        'class_weight': ['balanced']
    }
    
    grid_search = GridSearchCV(model, param_grid, cv=3, scoring = 'roc_auc')
    grid_search.fit(x_train, y_train)
       
    best_params = grid_search.best_params_
    best_model = grid_search.best_estimator_

    print(f"Best Parameters: {best_params}")
    print(f"Best Score: {grid_search.best_score_}")
    joblib.dump(best_model, os.path.join(dir_path,'decision_tree_model.pkl'))

if __name__ == "__main__":
    train_random_forest()
