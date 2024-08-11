
# import pandas as pd
# import mlflow
# import mlflow.sklearn
# from sklearn.ensemble import RandomForestClassifier
# from sklearn.model_selection import KFold, cross_val_score, GridSearchCV
# from sklearn.metrics import roc_auc_score
# import joblib

# mlflow.set_tracking_uri("file:/")
# experiment_name = "random_forest"
# mlflow.set_experiment(experiment_name)


# def train_random_forest():
#     x_train = pd.read_csv('x_train.csv')
#     y_train = pd.read_csv('y_train.csv').squeeze()
#     x_test = pd.read_csv('x_test.csv')
#     y_test = pd.read_csv('y_test.csv')

#     model = RandomForestClassifier(class_weight='balanced', random_state=42)

#     param_grid = {
#         'n_estimators': [50, 100],
#         'max_depth': [5, 10],
#         'min_samples_split': [2, 5]
#     }
    
#     grid_search = GridSearchCV(model, param_grid, cv=3)

#     with mlflow.start_run():
#         grid_search.fit(x_train, y_train)
#         mlflow.log_params(grid_search.best_params_)
       
#         y_pred_proba = grid_search.predict_proba(x_test)[:, 1]
#         auc_score = roc_auc_score(y_test, y_pred_proba)

#         # Log metrics
#         mlflow.log_metric('auc_score', auc_score)
#         mlflow.sklearn.log_model(grid_search.best_estimator_, 'random_forest_model')

#         print(f"Best parameters: {grid_search.best_params_}")
#         print(f"Test AUC Score: {auc_score:.4f}")

#         print(f"Run ID: {mlflow.active_run().info.run_id}")
    
#     best_model = grid_search.best_estimator_
#     joblib.dump(best_model, 'random_forest_model.pkl')

# if __name__ == "__main__":
#     train_random_forest()


import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import KFold, cross_val_score, GridSearchCV
from sklearn.metrics import roc_auc_score
import joblib
import pickle
import os



def train_random_forest():
    py_dir_path = os.path.dirname(os.path.realpath(__file__))
    parent_dir = os.path.dirname(py_dir_path)
    dir_path = os.path.join(parent_dir, 'data')
    x_train = pd.read_csv(os.path.join(dir_path,'x_train.csv'))
    y_train = pd.read_csv(os.path.join(dir_path,'y_train.csv')).squeeze()

    model = RandomForestClassifier(class_weight='balanced', random_state=42)

    param_grid = {
        'n_estimators': [50, 100],
        'max_depth': [5, 10],
        'min_samples_split': [2, 5]
    }
    
    grid_search = GridSearchCV(model, param_grid, cv=3, scoring = 'roc_auc')
    grid_search.fit(x_train, y_train)
       
    best_params = grid_search.best_params_
    best_model = grid_search.best_estimator_

    print(f"Best Parameters: {best_params}")
    print(f"Best Score: {grid_search.best_score_}")
    # joblib.dump(best_model, 'random_forest_model.pkl')

    with open(os.path.join(dir_path,'random_forest_model.pkl'), 'wb') as f:
        pickle.dump(best_model, f)

if __name__ == "__main__":
    train_random_forest()

   

   
