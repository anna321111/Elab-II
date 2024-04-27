import pandas as pd
import numpy as np
from collections import defaultdict
import networkx as nx
import matplotlib.pyplot as plt

def build_network(csv_file_path):
    df = pd.read_csv(csv_file_path)
    network = defaultdict(lambda: defaultdict(list))

    for trip_id, trip in df.groupby('tripnumber'):
        departments = trip['departmentnumber'].tolist()
        times = trip['timebetween'].tolist()
        for i in range(len(departments) - 1):
            source = departments[i]
            target = departments[i + 1]
            time = times[i]
            network[source][target].append(time)

    edges_info = {}
    for source, targets in network.items():
        for target, times in targets.items():
            total_trips = len(times)
            mean_time = np.mean(times)
            variance_time = np.var(times)
            edges_info[(source, target)] = {
                'total_trips': total_trips,
                'mean_time': mean_time,
                'variance_time': variance_time
            }

    return edges_info

def visualize_network(edges_info, min_trips=500, output_file='network_visualization.png'):
    G = nx.DiGraph()
    for (source, target), info in edges_info.items():
        if info['total_trips'] >= min_trips:
            G.add_edge(source, target, weight=info['total_trips'])

    pos = nx.kamada_kawai_layout(G)
    weights = [info['weight'] for u, v, info in G.edges(data=True)]

    if not weights:
        print("No edges with the minimum number of trips were found.")
        return

    plt.figure(figsize=(12, 12))
    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=500,
            font_size=8, edge_color='grey', width=[(weight/max(weights))*5 for weight in weights])
    plt.savefig(output_file, format='png', dpi=300, bbox_inches='tight')
    plt.show()

def flag_suspicious_purchases(csv_file_path, edges_info):
    df = pd.read_csv(csv_file_path)[:1000]
    df['flagged'] = 0
    counter = 0
    for index, row in df.iterrows():
        counter += 1
        print(counter)
        source = row['departmentnumber']
        next_rows = df[(df['tripnumber'] == row['tripnumber']) & (df['purchasenumber'] == row['purchasenumber'] + 1)]
        if not next_rows.empty:
            next_dept = next_rows.iloc[0]['departmentnumber']
            if (source, next_dept) in edges_info:
                edge_data = edges_info[(source, next_dept)]
                mean_time = edge_data['mean_time']
                std_dev = np.sqrt(edge_data['variance_time'])
                if row['timebetween'] > mean_time + 1.5 * std_dev:
                    df.at[index, 'flagged'] = 1

    return df

edges_info = build_network('Data/supermarket_enhanced.csv')
flagged_df = flag_suspicious_purchases('Data/supermarket_enhanced.csv', edges_info)
flagged_df.to_csv('Data/supermarket_flagged.csv', index=False)

