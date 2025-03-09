import numpy as np
import pandas as pd
import torch
import json


def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius in km
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat / 2.0) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2.0) ** 2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    return R * c  # Distance in km

def create_graph_from_csv(df, threshold=7):  

    #Reading from df rather than csv. 
    print("Graph creating fuction invoked`!!")
    pm2_5=df['pm2_5'].values
    pm10=df['pm10'].values
    wind_speeds = df['wind_speed'].values
    wind_dirs = df['wind_direction'].values
    latitudes = df['latitude'].values
    longitudes = df['longitude'].values
    altitudes = df['altitude'].values

    # Create the node feature matrix x
    # You can adjust the feature set depending on which columns you want to use
    x = np.column_stack(( pm2_5, pm10,wind_speeds, wind_dirs))

    num_stations = len(df)
    edge_indices = []
    edge_weights = []

    # Create the edges based on your similarity criteria
    for i in range(num_stations):
        for j in range(i + 1, num_stations):  # Avoid duplicate edges
            distance = haversine(latitudes[i], longitudes[i], latitudes[j], longitudes[j])
            altitude_diff = abs(altitudes[i] - altitudes[j])
            wind_speed_diff = abs(wind_speeds[i] - wind_speeds[j])
            wind_dir_diff = abs((wind_dirs[i] - wind_dirs[j] + 180) % 360 - 180)

            similarity_score = ((distance / 300) * 1.01 + (altitude_diff / 350) + (wind_speed_diff) + (wind_dir_diff / 18))

            if similarity_score < threshold:
                weight = 1.0 / (7 + similarity_score)
            else:
                weight = 0.0000000001

            edge_indices.append([i, j])
            edge_indices.append([j, i])  # Undirected graph
            edge_weights.append(weight)
            edge_weights.append(weight)

    edge_index = torch.tensor(edge_indices, dtype=torch.long).t().contiguous()
    edge_attr = torch.tensor(edge_weights, dtype=torch.float).tolist()

    # Convert node features (x) to a list of lists (since JSON cannot store torch tensors)
    x = torch.tensor(x, dtype=torch.float).tolist()
    print("Graph created")
    # print("Graph created")

    # Create a dictionary to return
    

    # Convert the dictionary to JSON
    # json_graph_data = json.dumps(graph_data, indent=4)
   

    return x, edge_index.tolist(), edge_attr

