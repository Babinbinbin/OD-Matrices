import pandas as pd
import requests
import os
path='C:\\Users\\babin\\OneDrive\\Desktop'
os.chdir(path)
#get distance and duration between two coordinates ((((((((use Google Distance Matrix API))))))))))
def get_distance_duration(home_lat, home_lng, work_lat, work_lng):
    api_key = "AIzaSyAAiJ2m8hoCG3L7hO2KqiZxZBUHv_rx7P0"
    url = f"https://maps.googleapis.com/maps/api/distancematrix/json?origins={home_lat},{home_lng}&destinations={work_lat},{work_lng}&key={api_key}"
    response = requests.get(url)
    data = response.json()
    if data['status'] == 'OK':
        distance = data['rows'][0]['elements'][0]['distance']['value']  # yo 2000 is in meters
        duration = data['rows'][0]['elements'][0]['duration']['value']  # seconds
        return distance, duration
    else:
        print("Error:", data['status'])
        return None, None

home_df = pd.read_csv('trialhabersinebulkhome.csv')
work_df = pd.read_csv('trialhabersinebulkwork.csv')


merged_df = pd.merge(home_df, work_df, on='UserID')
print(0)

mode_choices = []
for index, row in merged_df.iterrows():
    print(1)
    home_lat, home_lng = row['home_lat'], row['home_lng']
    work_lat, work_lng = row['work_lat'], row['work_lng']
    
    distance, _ = get_distance_duration(home_lat, home_lng, work_lat, work_lng)
    print(distance,"@222")
    if distance is not None:
        if distance < 2000:  
            mode_choices.append('Walk')
            print("walk")
        else:
            mode_choices.append('Drive')
            print("drive")
    else:
        mode_choices.append('Unknown')  
        print("unknown")
        
# Adding mode choices to Df
merged_df['ModeChoice'] = mode_choices

# Output DataFrame along iwth mode choices
merged_df[['UserID','home_lat','home_lng','work_lat','work_lng', 'ModeChoice']].to_csv('mode_choices2.csv', index=False)
print("DONE!!!!!")
