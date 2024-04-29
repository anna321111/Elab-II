import pandas as pd
from collections import defaultdict
import numpy as np
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

def visualize_network(edges_info, min_trips=500, output_file='Plots/network_visualization.png'):
    # Mapping of department numbers to names
    department_names = {
        1: "Bakery & Pastry", 2: "Beer & Wine", 3: "Books & Magazines", 4: "Candy & Chips",
        5: "Care & Hygiene", 6: "Cereals & Spreads", 7: "Cheese & Tapas", 8: "Dairy & Eggs",
        9: "Freezer", 10: "Fruit & Vegetables", 11: "Household & Pet", 12: "Meat & Fish",
        13: "Pasta & Rice", 14: "Salads & Meals", 15: "Sauces & Spices", 16: "Soda & Juices",
        17: "Special Diet", 18: "Vegetarian & Vegan"
    }

    G = nx.DiGraph()
    for (source, target), info in edges_info.items():
        if info['total_trips'] >= min_trips:
            G.add_edge(source, target, weight=info['total_trips'])

    pos = nx.kamada_kawai_layout(G, scale=2)  # Adjust layout scale
    weights = [info['weight'] for u, v, info in G.edges(data=True)]

    if not weights:
        print("No edges with the minimum number of trips were found.")
        return

    plt.figure(figsize=(18, 18))
    nx.draw(G, pos, labels={node: department_names.get(node, str(node)) for node in G.nodes()},
            with_labels=True, node_color='lightblue', node_size=10000,  # Significantly increased node size
            font_size=8, edge_color='grey', width=[(weight/max(weights))*5 for weight in weights])
    plt.savefig(output_file, format='png', dpi=300, bbox_inches='tight')
    plt.show()

def flag_suspicious_purchases(csv_file_path, edges_info):
    df = pd.read_csv(csv_file_path)[:1000]
    suspicious_trips = set()

    for index, row in df.iterrows():
        source = row['departmentnumber']
        next_rows = df[(df['tripnumber'] == row['tripnumber']) & (df['purchasenumber'] == row['purchasenumber'] + 1)]
        if not next_rows.empty:
            next_dept = next_rows.iloc[0]['departmentnumber']
            if (source, next_dept) in edges_info:
                edge_data = edges_info[(source, next_dept)]
                mean_time = edge_data['mean_time']
                std_dev = np.sqrt(edge_data['variance_time'])
                if row['timebetween'] > mean_time + 2 * std_dev:
                    suspicious_trips.add(row['tripnumber'])

    # Mark all purchases in suspicious trips as flagged
    df['flagged'] = df['tripnumber'].apply(lambda x: 1 if x in suspicious_trips else 0)

    return df

edges_info = build_network('Data/supermarket_enhanced.csv')
visualize_network(edges_info)
flagged_df = flag_suspicious_purchases('Data/supermarket_enhanced.csv', edges_info)
flagged_df.to_csv('Data/supermarket_flagged.csv', index=False)


