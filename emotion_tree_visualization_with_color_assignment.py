import csv
import requests
import networkx as nx
import matplotlib.pyplot as plt

# URL of the CSV file
csv_url = "https://gist.githubusercontent.com/mikail-eliyah-00/72d8fc806a5c60298e0b547bd5a4fcdb/raw/1ab7180edb15ed68e73828d437c811b54f8c8767/Emotions%2520Clusters.csv"

# Download CSV data
response = requests.get(csv_url)
csv_data = response.text

# Function to parse CSV data into a tree dictionary
def parse_csv_data(csv_data):
    reader = csv.reader(csv_data.strip().split('\n'))
    tree = {}
    parent_stack = []

    for row in reader:
        # Skip empty rows
        if all(cell == "" for cell in row):
            continue

        # Find the level and value
        level = next(i for i, cell in enumerate(row) if cell != "")
        value = row[level]

        # Update parent stack
        parent_stack = parent_stack[:level]
        if parent_stack:
            parent = parent_stack[-1]
        else:
            parent = None

        # Add the node to the tree
        if parent:
            tree[parent].append(value)
        else:
            tree[value] = []

        tree[value] = tree.get(value, [])
        parent_stack.append(value)

    return tree

# Build the tree using networkx
def build_tree(tree):
    G = nx.DiGraph()

    def add_edges(parent, children):
        for child in children:
            G.add_edge(parent, child)
            add_edges(child, tree[child])

    for root in tree:
        add_edges(root, tree[root])

    return G

# Function to assign colors based on clusters
def assign_colors(G, clusters):
    color_map = []
    for node in G:
        for cluster, color in clusters.items():
            if node.startswith(cluster):  # Assuming cluster names are prefixes of node names
                color_map.append(color)
                break
        else:
            color_map.append('grey')  # Default color for nodes not in any cluster
    return color_map

# Define cluster colors (you can modify this dictionary as needed)
clusters = {
    'Joy': 'yellow',
    'Sadness': 'blue',
    'Anger': 'green',
    'Fear': 'purple',
    'Disgust': 'green',
    'Surprise': 'orange',
    'Love': 'red'
}

def visualize_tree(G, color_map):
    options = {
        'node_color': color_map,
        'node_size': 3000,
        'width': 3,
        'arrowstyle': '->',
        'arrowsize': 10,
        'font_size': 10
    }

    plt.figure(figsize=(25, 25))
    nx.draw_networkx(G, arrows=True, **options)
    plt.title("Emotion Tree")
    plt.show()

tree_dict = parse_csv_data(csv_data)  # Parse the CSV data
G = build_tree(tree_dict)
color_map = assign_colors(G, clusters)  # Assign colors to nodes based on clusters
visualize_tree(G, color_map)  # Visualize the tree with assigned colors

