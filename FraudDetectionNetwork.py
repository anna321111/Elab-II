import pandas as pd
import numpy as np
from collections import defaultdict
import networkx as nx
import matplotlib.pyplot as plt

class FraudDetectionNetwork:
    def __init__(self, csv_file_path, predictions_df):
        self.csv_file_path = csv_file_path
        self.predictions_df = predictions_df
        self.edges_info = self.build_network()

    def build_network(self):
        df = pd.read_csv(self.csv_file_path)
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

    def visualize_network(self, min_trips=500, output_file='Plots/network_visualization.png'):
        department_names = {
            1: "Bakery & Pastry", 2: "Beer & Wine", 3: "Books & Magazines", 4: "Candy & Chips",
            5: "Care & Hygiene", 6: "Cereals & Spreads", 7: "Cheese & Tapas", 8: "Dairy & Eggs",
            9: "Freezer", 10: "Fruit & Vegetables", 11: "Household & Pet", 12: "Meat & Fish",
            13: "Pasta & Rice", 14: "Salads & Meals", 15: "Sauces & Spices", 16: "Soda & Juices",
            17: "Special Diet", 18: "Vegetarian & Vegan"
        }
        G = nx.DiGraph()
        for (source, target), info in self.edges_info.items():
            if info['total_trips'] >= min_trips:
                G.add_edge(source, target, weight=info['total_trips'])

        pos = nx.kamada_kawai_layout(G, scale=2)
        weights = [info['weight'] for u, v, info in G.edges(data=True)]

        if not weights:
            print("No edges with the minimum number of trips were found.")
            return

        plt.figure(figsize=(18, 18))
        nx.draw(G, pos, labels={node: department_names.get(node, str(node)) for node in G.nodes()},
                with_labels=True, node_color='lightblue', node_size=10000,
                font_size=8, edge_color='grey', width=[(weight / max(weights)) * 5 for weight in weights])
        plt.savefig(output_file, format='png', dpi=300, bbox_inches='tight')
        plt.show()

    def flag_suspicious_purchases(self, test_file_path):
        df = pd.read_csv(test_file_path)
        suspicious_trips = set()

        for index, row in df.iterrows():
            source = row['departmentnumber']
            next_rows = df[(df['tripnumber'] == row['tripnumber']) & (df['purchasenumber'] == row['purchasenumber'] + 1)]
            if not next_rows.empty:
                next_dept = next_rows.iloc[0]['departmentnumber']
                if (source, next_dept) in self.edges_info:
                    edge_data = self.edges_info[(source, next_dept)]
                    mean_time = edge_data['mean_time']
                    std_dev = np.sqrt(edge_data['variance_time'])
                    if row['timebetween'] > mean_time + 4 * std_dev:
                        suspicious_trips.add(row['tripnumber'])

        df['flagged'] = df['tripnumber'].apply(lambda x: 1 if x in suspicious_trips else 0)

        # Update predictions_df
        flagged_results = df.groupby('tripnumber')['flagged'].max().reset_index()
        self.predictions_df['Network'] = self.predictions_df['tripnumber'].map(flagged_results.set_index('tripnumber')['flagged']).fillna(0)

        return self.predictions_df

    def run(self):
        self.visualize_network()
        updated_predictions_df = self.flag_suspicious_purchases('Data/TestFileFormatted.csv')
        updated_predictions_df.to_csv('Data/predictions_flagged.csv', index=False)
        return updated_predictions_df
