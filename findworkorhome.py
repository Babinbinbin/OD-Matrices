import pandas as pd
import os
path='C:\\Users\\babin\\OneDrive\\Desktop'
os.chdir(path)
def find_home_id(group):
    # print(group)
    # print(group[['latitude','longitude']].nunique(),"h1")
    uniqueCords = group[['latitude','longitude']].nunique() 
    no_unique_cords = uniqueCords['latitude'] * uniqueCords['longitude']
    if no_unique_cords == 1:
        # print(group[['latitude','longitude']].iloc[0])
        return group[['latitude','longitude']].iloc[0]
    else:
        max_num_entries = group['num_entries'].max()
        if (group['num_entries'] == max_num_entries).sum() == 1:
            max_num_entries_idx = group['num_entries'].idxmax()
            print(0)
            #print(max_num_entries_idx)
            #print(group.loc[max_num_entries_idx, 'latitude'])
            return group.loc[max_num_entries_idx, ['latitude', 'longitude']]
        else:
            max_stay_time_idx = group['stay_time'].idxmax()
            # print(max_stay_time_idx)
            #print(group.loc[max_stay_time_idx, ['latitude', 'longitude']])
            return group.loc[max_stay_time_idx, ['latitude','longitude']]
        

def assign_latitude(group,home_locs):
    final_df = home_locs.loc[group['user_id']]
    return final_df['latitude']

def assign_longitude(group,home_locs):
    final_df = home_locs.loc[group['user_id']]
    return final_df['longitude']
    


def calculate_stay_time(input_file, output_file):

    df = pd.read_csv(input_file)

    #time diff bw consecutive rows for each user
    df['call_time'] = pd.to_datetime(df['call_time'],format= '%H:%M:%S')
    # print(df.groupby('user_id')['call_time'].diff().fillna(pd.Timedelta(seconds=0)))
    df['time_diff'] = df.groupby(['user_id','latitude','longitude'])['call_time'].diff().fillna(pd.Timedelta(seconds=0))

    #stay time at each location
    df['stay_time'] = df['time_diff'].dt.total_seconds()
    df['stay_time'] = df.groupby(['user_id', 'latitude', 'longitude'])['stay_time'].transform('sum')

    #number of entries at each location for each user
    df['num_entries'] = df.groupby(['user_id', 'latitude', 'longitude'])['latitude'].transform('count')

    # Findhome location for each user
    #print(df.groupby('user_id'))
    home_locs = df.groupby('user_id').apply(find_home_id)

    df['work_latitude'] =df.apply(assign_latitude,axis=1,args=[home_locs])
    df['work_longitude'] =df.apply(assign_longitude,axis=1,args=[home_locs])

    
    
    # df[]=df.groupby('user_id').apply(find_home_id)


    
    df.drop(columns=['time_diff'], inplace=True)

    #df to new CSV file
    df.to_csv(output_file, index=False)

if __name__ == "__main__":
    input_file = "9amto5pm.csv"
    output_file = "workid.csv"
    calculate_stay_time(input_file, output_file)
    print("Stay time calculated and home ID identified. Results saved in", output_file)
    