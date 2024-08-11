import pandas as pd
from sklearn.metrics import roc_auc_score, accuracy_score, precision_score, recall_score, f1_score
import joblib
import os
import csv


# Function to evaluate and log metrics
def evaluate_model(model, x_test, y_test):
    y_pred = model.predict(x_test)
    y_pred_proba = model.predict_proba(x_test)[:, 1]
    
    auc = roc_auc_score(y_test, y_pred_proba)
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    
    return {
        'AUC': auc,
        'Accuracy': accuracy,
        'Precision': precision,
        'Recall': recall,
        'F1 Score': f1
    }

if __name__ == "__main__":
    # Load test data
    py_dir_path = os.path.dirname(os.path.realpath(__file__))
    parent_dir = os.path.dirname(py_dir_path)
    dir_path = os.path.join(parent_dir, 'data')
    x_test = pd.read_csv(os.path.join(dir_path, 'x_test.csv'))
    y_test = pd.read_csv(os.path.join(dir_path,'y_test.csv')).squeeze()

    # List of model file names
    model_files = ['xgboost_model.pkl', 'random_forest_model.pkl', 'decision_tree_model.pkl']
    out_csv_file_name = 'evaluation_results.csv'
    out_csv_path = os.path.join(dir_path,out_csv_file_name)
    line_count = 0
    for model_file_name in model_files:
        model_file_path = os.path.join(dir_path, model_file_name)
        model = joblib.load(model_file_path)
        metrics = evaluate_model(model, x_test, y_test)
        new_line = [model_file_name, metrics['AUC'], metrics['Accuracy'], metrics['Precision'], metrics['Recall'], metrics['F1 Score']]
        # add the header for the first row
        if line_count == 0:
            headerList = ['model', 'AUC', 'Accuracy', 'Precision', 'Recall', 'F1 Score'] 
            with open(out_csv_path, 'w') as file: 
                dw = csv.DictWriter(file, delimiter=',',  
                                    fieldnames=headerList) 
                dw.writeheader()
        # write the line
        with open(out_csv_path, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(new_line)
        line_count+=1
    print("Model evaluation completed")


