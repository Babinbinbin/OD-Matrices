import pandas as pd
import os
path='C:\\Users\\babin\\OneDrive\\Desktop'
os.chdir(path)
# Read the unique cell towers dataset
unique_cell_towers = pd.read_csv('unique_cell_towers.csv')

# Add a new column for cell tower IDs
unique_cell_towers['tower_id'] = range(1, len(unique_cell_towers) + 1)

# Save the updated dataset to a new CSV file
unique_cell_towers.to_csv('unique_cell_towersid.csv', index=False)
