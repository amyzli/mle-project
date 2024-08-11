import pandas as pd
import os 

def load_data(file_path):
    return pd.read_csv(file_path)

def ingest_datasets(dir_path, dataset1_path, dataset2_path):
    df1 = load_data(os.path.join(dir_path, dataset1_path))
    df2 = load_data(os.path.join(dir_path, dataset2_path))
    
    # Save ingested datasets
    df1.to_csv(os.path.join(dir_path, 'ingested_data1.csv'), index=False)
    df2.to_csv(os.path.join(dir_path, 'ingested_data2.csv'), index=False)

if __name__ == "__main__":
    py_dir_path = os.path.dirname(os.path.realpath(__file__))
    parent_dir = os.path.dirname(py_dir_path)
    dir_path = os.path.join(parent_dir, 'data')
    dataset1_path = 'application_data.csv'
    dataset2_path = 'previous_application.csv'
    ingest_datasets(dir_path, dataset1_path, dataset2_path)
