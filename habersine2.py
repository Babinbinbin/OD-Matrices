import pandas as pd
from math import radians, sin, cos, sqrt, atan2
import time
import os
path='C:\\Users\\babin\\OneDrive\\Desktop'
os.chdir(path)
home_data = pd.read_csv('homefinal2.csv')  
work_data = pd.read_csv('.csv')


cdr_data = pd.merge(home_data, work_data, on='UserID')


def haversine(lat1, lon1, lat2, lon2):
   
    R = 6371.0
    
    # latitude and longitude from degrees to radians
    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)
    
    # chang in coordinates
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    
    
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c
    
    return distance


def get_mode_of_transport(distance):
    
    if distance > 2:
        return "Driving"
    else:
        return "Walking"

sec=time.time()
data_list = []
#creating a new dataframe to store user id, home coordinate, work coordinate and mode
#new_data = pd.DataFrame(columns=['user_id', 'home_latitude', 'home_longitude', 'work_latitude', 'work_longitude', 'mode_of_transport'])

for index, row in cdr_data.iterrows():
    distance = haversine(row['home_lat'], row['home_lng'], row['work_lat'], row['work_lng'])
    
    
    mode_of_transport = get_mode_of_transport(distance)
    
    
    data_list.append({
        'user_id': row['UserID'],
        'home_latitude': row['home_lat'],
        'home_longitude': row['home_lng'],
        'work_latitude': row['work_lat'],
        'work_longitude': row['work_lng'],
        'mode_of_transport': mode_of_transport
    })
    #calculating distance between hoome and work
    #distance = haversine(row['home_lat'], row['home_lng'], row['work_lat'], row['work_lng'])
    
    #mode_of_transport = get_mode_of_transport(distance)
    
    #new_data = new_data.concat({
        #'user_id': row['user_id'],
        #'home_latitude': row['home_lat'],
        #'home_longitude': row['home_lng'],
        #'work_latitude': row['work_lat'],
        #'work_longitude': row['work_lng'],
        #'mode_of_transport': mode_of_transport
    #}, ignore_index=True)
new_data = pd.DataFrame(data_list)
new_data.to_csv('user_transport_data.csv', index=False)

print(time.time() - sec,"time taken")


