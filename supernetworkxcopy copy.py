import pandas as pd
import numpy as np
import geopandas as gpd
import networkx as nx
from shapely.geometry import Point, LineString
import time

start=time.time()
cnt=0
def load_data(user_csv, tower_csv, shapefile_path):
    user_data = pd.read_csv(user_csv)
    tower_data = pd.read_csv(tower_csv)
    roads = gpd.read_file(shapefile_path)
    print(0)
    return user_data, tower_data, roads
    #this works
cnt4=0
end=0

def getCoordinatesAsFloat(start_coord:list) :
    ''' 
    converts coordinates from * ' " format to float
    '''
    start = []
    for xi in start_coord:
        coord = int(xi[0][:-1]) # getting the string as int except the * like 79.04*
        minutes = int(xi[1][:-1]) # getting the string as int except the ' like 79.04'
        seconds = int(xi[1][:-1]) # getting the string as int except the " like 79.04"
        total_sec = minutes * 60 + seconds # total seconds in a coordinate
        start.append(round(coord + (total_sec / (3600.0)), 5) ) 

    return start

def create_road_network(roads):
    G = nx.Graph()
    global cnt, cnt4, end
    for idx, road in roads.iterrows():
        #each segment is a simple LineString
        if isinstance(road.geometry, LineString):
            cnt+=1
            print("adding road", cnt)
            start_coord = [road.get('start_x').split(),road.get('start_y').split()]
            end_coord = [road.get('end_x').split(),road.get('end_y').split()]
            


            start = tuple( getCoordinatesAsFloat(start_coord) )
            end = tuple(getCoordinatesAsFloat(end_coord) )
            # print(start,end)
            G.add_edge(start,end, road_id = road.get('OBJECTID', idx) )
                
            
    print(cnt)
    print(G.edges((76.35583, 9.57611)))

    return G
    #this works
def map_towers_to_nearest_nodes(tower_data, G):
    global cnt4
    tower_data['geometry'] = tower_data.apply(lambda row: Point(row['longitude'], row['latitude']), axis=1)
    tower_gdf = gpd.GeoDataFrame(tower_data, geometry='geometry')
    node_map = {}
    print(4)
    for index, tower in tower_gdf.iterrows():
        cnt4+=1
        nearest_node = min(G.nodes, key=lambda node: Point(node).distance(tower.geometry))
        #print(nearest_node,tower.geometry,cnt4)
        node_map[tower['tower_id']] = nearest_node
        print("tower no :",cnt4)
        #if cnt4==100:
            #break
    
        
    print("towers identified..")
    #end=time.time()
    return node_map


def getDistanceFromLine(lineStart,lineEnd,point:Point):
    '''
    Gives the distance of point from line
    lineStart : x1
    lineEnd : x2
    point : p
    '''
    A = lineStart[0] - lineEnd[0]
    B = lineStart[1] - lineEnd[1]
    C = lineStart[0] * (-A) - lineStart[1]* (B)
    return abs(A * point.x + B * point.y + C) / np.sqrt(A ** 2 + B **2)
    #thi too works
def estimate_traffic(user_data, node_map, G:nx.Graph,tower_data):
    # Initialize dictionary to count traffic on each edge
    traffic_count = {}
    print("Calculating Trafic ...")
    for _, user in user_data.iterrows():
        # Strip quotes and split the string into a list of integers
        tower_ids_prev = [t.strip() for t in user['trip_chain'][2:-2].split(',')]
        tower_ids = [int(tid) for tid in tower_ids_prev if tid.isdigit()]  # Convert to integer and handle possible empty strings
        
        # Get the corresponding nodes from the node map for each tower ID
        path_nodes = [(node_map[tid],tid) for tid in tower_ids if tid in node_map.keys()]
        # Iterate over each pair of consecutive nodes and compute the shortest path
        for i in range(len(path_nodes) - 1):
            try:
                # print(tower_ids)
                # print("noded",user['user_id'],path_nodes)
                nearest_node = path_nodes[i][0]
                tid = path_nodes[i][1]
                edge_ends = G.edges(nearest_node) 
                min_edge = min(edge_ends,key= lambda edge: getDistanceFromLine(nearest_node,edge[1],tower_data.loc[tower_data["tower_id"] == tid]["geometry"].values[0]) )
                # print(min_edge,'Min')
                # path = nx.shortest_path(G, path_nodes[i], path_nodes[i + 1], weight='weight')
                edge_data = G.get_edge_data(nearest_node,min_edge[1])
                road_id = edge_data['road_id']
                if road_id in traffic_count:
                    # print("add")
                    traffic_count[road_id] += 1
                else:
                    # print("new")
                    traffic_count[road_id] = 1
            except nx.NetworkXNoPath:
                continue  # No path found between these nodes, continue to next pair
    
    return traffic_count


def main(user_csv, tower_csv, shapefile_path,output_csv):
    user_data, tower_data, roads = load_data(user_csv, tower_csv, shapefile_path)
    G = create_road_network(roads)
    node_map = map_towers_to_nearest_nodes(tower_data, G)
    traffic_counts = estimate_traffic(user_data, node_map, G,tower_data)
    for road_id, count in traffic_counts.items():
        print(f"Road ID {road_id} has traffic count: {count}")
    # # Convert traffic_counts dictionary to DataFrame
    traffic_df = pd.DataFrame(list(traffic_counts.items()), columns=['Road_ID', 'Traffic_Count'])
    # # Save to CSV
    traffic_df.to_csv(output_csv, index=False)
    print(f"Traffic data saved to {output_csv}")
# To run the code, uncomment and replace with actual paths to your files
main("C:\\Users\\babin\\OneDrive\\Desktop\\oelp\\finaltrip.csv",'C:\\Users\\babin\\OneDrive\\Desktop\\uniquetowersid.csv' ,'C:\\Users\\babin\\OneDrive\\Desktop\\road.shp','C:\\Users\\babin\\OneDrive\\Desktop\\oelp\\finalout.csv')
#