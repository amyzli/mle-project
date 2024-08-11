import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
import os

def process_data(app_df, prev_df):

    # Handle null columns
    null_columns = app_df.isnull().sum()[app_df.isnull().sum() > app_df.shape[0]*0.5 ].index.tolist()
    avg_columns = list(filter(lambda col: col.endswith('_AVG'), null_columns))
    drop_columns = list(set(null_columns)-set(avg_columns)-set(['EXT_SOURCE_1']))
    app_df = app_df.drop(columns=drop_columns)

    # Convert negative 'days since' columns
    app_df['DAYS_BIRTH'] = abs(app_df['DAYS_BIRTH'])
    app_df['DAYS_EMPLOYED'] = abs(app_df['DAYS_EMPLOYED'])
    app_df['DAYS_ID_PUBLISH'] = abs(app_df['DAYS_ID_PUBLISH'])
    app_df['DAYS_REGISTRATION'] = abs(app_df['DAYS_REGISTRATION'])
    app_df['DAYS_LAST_PHONE_CHANGE'] = abs(app_df['DAYS_LAST_PHONE_CHANGE'])

    # Drop meaningless date feature: WEEKDAY_APPR_PROCESS_START
    app_df = app_df.drop(columns='WEEKDAY_APPR_PROCESS_START')

    # Combine excess categories for: ORGANIZATION_TYPE, OCCUPATION_TYPE
    occ_type_dict = {
    'Accountants': 'Finance',
    'Cleaning staff': 'Maintenance',
    'Cooking staff': 'Hospitality',
    'Core staff': 'Administrative',
    'Drivers': 'Transportation',
    'HR staff': 'Human Resources',
    'High skill tech staff': 'Technology',
    'IT staff': 'Technology',
    'Laborers': 'Labor',
    'Low-skill Laborers': 'Labor',
    'Managers': 'Management',
    'Medicine staff': 'Healthcare',
    'Private service staff': 'Hospitality',
    'Realty agents': 'Real Estate',
    'Sales staff': 'Sales',
    'Secretaries': 'Administrative',
    'Security staff': 'Security',
    'Waiters/barmen staff': 'Hospitality'
    }

    org_type_dict = {
    'Advertising': 'Marketing',
    'Agriculture': 'Agriculture',
    'Bank': 'Finance',
    'Business Entity Type 1': 'Business',
    'Business Entity Type 2': 'Business',
    'Business Entity Type 3': 'Business',
    'Cleaning': 'Maintenance',
    'Construction': 'Construction',
    'Culture': 'Culture',
    'Electricity': 'Utilities',
    'Emergency': 'Emergency Services',
    'Government': 'Government',
    'Hotel': 'Hospitality',
    'Housing': 'Housing',
    'Industry: type 1': 'Industry',
    'Industry: type 10': 'Industry',
    'Industry: type 11': 'Industry',
    'Industry: type 12': 'Industry',
    'Industry: type 13': 'Industry',
    'Industry: type 2': 'Industry',
    'Industry: type 3': 'Industry',
    'Industry: type 4': 'Industry',
    'Industry: type 5': 'Industry',
    'Industry: type 6': 'Industry',
    'Industry: type 7': 'Industry',
    'Industry: type 8': 'Industry',
    'Industry: type 9': 'Industry',
    'Insurance': 'Finance',
    'Kindergarten': 'Education',
    'Legal Services': 'Legal',
    'Medicine': 'Healthcare',
    'Military': 'Government',
    'Mobile': 'Telecom',
    'Other': 'Miscellaneous',
    'Police': 'Public Safety',
    'Postal': 'Public Services',
    'Realtor': 'Real Estate',
    'Religion': 'Religion',
    'Restaurant': 'Hospitality',
    'School': 'Education',
    'Security': 'Security',
    'Security Ministries': 'Security',
    'Self-employed': 'Business',
    'Services': 'Services',
    'Telecom': 'Telecom',
    'Trade: type 1': 'Trade',
    'Trade: type 2': 'Trade',
    'Trade: type 3': 'Trade',
    'Trade: type 4': 'Trade',
    'Trade: type 5': 'Trade',
    'Trade: type 6': 'Trade',
    'Trade: type 7': 'Trade',
    'Transport: type 1': 'Transport',
    'Transport: type 2': 'Transport',
    'Transport: type 3': 'Transport',
    'Transport: type 4': 'Transport',
    'University': 'Education',
    'XNA': 'Unknown'
    }

    # Map new simplified categories
    app_df['ORGANIZATION_TYPE'] = app_df['ORGANIZATION_TYPE'].map(org_type_dict)
    app_df['OCCUPATION_TYPE'] = app_df['OCCUPATION_TYPE'].map(occ_type_dict)

    # Label encode categorical columns
    label_encoders = {col: LabelEncoder() for col in app_df.select_dtypes(include=['object', 'category'])}
    for col, encoder in label_encoders.items():
        app_df[col] = encoder.fit_transform(app_df[col])

    # Create historical features
    # Keep only the primary keys that exists in current application data
    prev_app_cleaned = prev_df.merge(app_df[['SK_ID_CURR']], on='SK_ID_CURR', how='inner')

    # Create label encoding for contract status - only keep 'Approved'
    status = {
    'Approved': 1,
    'Canceled': 0,
    'Refused': 0,
    'Unused offer': 0
    }

    # Apply the mapping to the DataFrame
    prev_app_cleaned['NAME_CONTRACT_STATUS'] = prev_app_cleaned['NAME_CONTRACT_STATUS'].map(status)

    # Convert negative 'days since' columns
    prev_app_cleaned['DAYS_DECISION'] = abs(prev_app_cleaned['DAYS_DECISION'])
    prev_app_cleaned['DAYS_FIRST_DUE'] = abs(prev_app_cleaned['DAYS_FIRST_DUE'])
    prev_app_cleaned['DAYS_LAST_DUE_1ST_VERSION'] = abs(prev_app_cleaned['DAYS_LAST_DUE_1ST_VERSION'])
    prev_app_cleaned['DAYS_LAST_DUE'] = abs(prev_app_cleaned['DAYS_LAST_DUE'])
    prev_app_cleaned['DAYS_TERMINATION'] = abs(prev_app_cleaned['DAYS_TERMINATION'])

    # Create historical features based on application date and approval status
    prev_features = prev_app_cleaned[['SK_ID_CURR', 'DAYS_DECISION', 'NAME_CONTRACT_STATUS']]

    # Define time periods
    bins = [0, 30, 60, 90, 120, 360, 720, 1080, 1800, 3600]
    labels = ['0-30 days', '31-60 days', '61-90 days', '91-120 days', '121-360 days', '1-2 years', '2-3 years', '3-5 years', '5-10 years']
    prev_features['Time Period'] = pd.cut(prev_features['DAYS_DECISION'], bins=bins, labels=labels, right=True)

    # Create an indicator column for applications
    prev_features['Application'] = 1

    # Create pivot tables to aggregate data by primary key and Time Period for application and approvals
    loan_applications_pivot = prev_features.pivot_table(index='SK_ID_CURR', columns='Time Period', values='Application', aggfunc='max', fill_value=0)
    loan_defaults_pivot = prev_features.pivot_table(index='SK_ID_CURR', columns='Time Period', values='NAME_CONTRACT_STATUS', aggfunc='max', fill_value=0)

    # Flatten the column indexes
    loan_applications_pivot.columns = [f'Application {col}' for col in loan_applications_pivot.columns]
    loan_defaults_pivot.columns = [f'Approved {col}' for col in loan_defaults_pivot.columns]

    # Merge the pivot tables on primary key
    combined_data = pd.merge(loan_applications_pivot, loan_defaults_pivot, on='SK_ID_CURR').reset_index()
    pivot_result = pd.DataFrame(combined_data)

    # Merge historical features
    df = pd.merge(app_df, pivot_result, on='SK_ID_CURR', how='left')

    # Drop highly correlated columns
    df = df.drop(columns=['AMT_GOODS_PRICE','FLAG_EMP_PHONE','REGION_RATING_CLIENT_W_CITY','YEARS_BEGINEXPLUATATION_MODE', 'FLOORSMAX_MODE','YEARS_BEGINEXPLUATATION_MEDI','FLOORSMAX_MEDI','OBS_60_CNT_SOCIAL_CIRCLE'])

    df = df.fillna(0)

    return df

def process_datasets():
    py_dir_path = os.path.dirname(os.path.realpath(__file__))
    parent_dir = os.path.dirname(py_dir_path)
    dir_path = os.path.join(parent_dir, 'data')
    df1 = pd.read_csv(os.path.join(dir_path,'ingested_data1.csv'))
    df2 = pd.read_csv(os.path.join(dir_path,'ingested_data2.csv'))
    
    processed_df = process_data(df1, df2)
    
    # Split the data into train and test sets
    x = processed_df.drop('TARGET', axis=1)
    y = processed_df['TARGET']
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=12)

    # Save the splits
    x_train.to_csv(os.path.join(dir_path,'x_train.csv'), index=False)
    x_test.to_csv(os.path.join(dir_path, 'x_test.csv'), index=False)
    y_train.to_csv(os.path.join(dir_path, 'y_train.csv'), index=False)
    y_test.to_csv(os.path.join(dir_path, 'y_test.csv'), index=False)

if __name__ == "__main__":
    process_datasets()
