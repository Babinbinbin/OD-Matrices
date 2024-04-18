import pandas as pd
import os
path='C:\\Users\\babin\\OneDrive\\Desktop'
os.chdir(path)
def filter_users(csv_file):
    
    df = pd.read_csv(csv_file)
    
    #  out users with less than 5 rows
    filtered_df = df.groupby('user_id').filter(lambda x: len(x) >= 5)
    
    
    filtered_df.to_csv('morethan4.csv', index=False)


if __name__ == "__main__":
    input_csv_file = 'datasorted2.csv' 
    filter_users(input_csv_file)
