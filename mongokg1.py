from pymongo import MongoClient
import networkx as nx
import matplotlib.pyplot as plt

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["ocr_database"]
collection = db["ocr_results"]

# Initialize the graph
G = nx.Graph()

# Build the knowledge graph from MongoDB documents
for doc in collection.find():
    name = str(doc.get("Name", "")).strip().title()
    age = str(doc.get("Age", "")).strip()
    marks = str(doc.get("Marks", "")).strip()
    roll = str(doc.get("Roll No", "")).strip()

    if name:
        G.add_node(name, type="Person")

        if age:
            G.add_node(age, type="Age")
            G.add_edge(name, age, relation="hasAge")

        if marks:
            G.add_node(marks, type="Marks")
            G.add_edge(name, marks, relation="hasMarks")

        if roll:
            G.add_node(roll, type="RollNo")
            G.add_edge(name, roll, relation="hasRollNo")

# Print all nodes
print("All nodes in the graph:")
print(G.nodes)

# Safely query neighbors for a specific name
name_query = "Amit"
if name_query in G:
    neighbors = list(G.neighbors(name_query))
    print(f"\nNeighbors of {name_query}: {neighbors}")
else:
    print(f"\n'{name_query}' not found in the graph.")

# Optional: Visualize the graph
pos = nx.spring_layout(G, seed=42)
labels = nx.get_edge_attributes(G, 'relation')
nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=1500, font_size=10)
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
plt.title("Knowledge Graph from OCR Data")
plt.show()
