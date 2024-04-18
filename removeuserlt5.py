import pandas as pd
import os
path='C:\\Users\\babin\\OneDrive\\Desktop'
os.chdir(path)
def filter_users(csv_file):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file)
    
    # Count the number of rows for each user and filter out users with less than 5 rows
    filtered_df = df.groupby('user_id').filter(lambda x: len(x) >= 5)
    
    # Save the filtered data to a new CSV file
    filtered_df.to_csv('morethan4.csv', index=False)

# Example usage:
if __name__ == "__main__":
    input_csv_file = 'datasorted2.csv'  # Change this to your input CSV file
    filter_users(input_csv_file)
