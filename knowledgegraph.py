from pymongo import MongoClient
import networkx as nx
import matplotlib.pyplot as plt

# Step 1: Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["ocr_database"]
collection = db["ocr_results"]

# Step 2: Create the graph
G = nx.Graph()

# Step 3: Populate graph from database
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

# Step 4: Define a query function
def get_attributes(graph, person):
    if person not in graph:
        return f"{person} not found in the graph."
    
    attributes = {}
    for neighbor in graph.neighbors(person):
        relation = graph[person][neighbor].get("relation")
        attributes[relation] = neighbor
    return attributes

# Example query
print(get_attributes(G, "Amit"))
def get_attributes(graph, person):
    if person not in graph:
        return f"{person} not found in the graph."
    
    attributes = {}
    for neighbor in graph.neighbors(person):
        relation = graph[person][neighbor].get("relation")
        attributes[relation] = neighbor
    return attributes

print(get_attributes(G, "Amit"))
def find_people_by_marks(graph, marks_value):
    results = []
    for node in graph.nodes:
        if graph.nodes[node].get("type") == "Person":
            for neighbor in graph.neighbors(node):
                if graph[node][neighbor].get("relation") == "hasMarks" and neighbor == marks_value:
                    results.append(node)
    return results

print(find_people_by_marks(G, "90"))
people = [n for n, attr in G.nodes(data=True) if attr.get("type") == "Person"]
print(people)
import matplotlib.pyplot as plt

def draw_person_graph(graph, person):
    if person not in graph:
        print(f"{person} not found.")
        return
    
    subgraph_nodes = [person] + list(graph.neighbors(person))
    subgraph = graph.subgraph(subgraph_nodes)
    
    pos = nx.spring_layout(subgraph)
    labels = nx.get_edge_attributes(subgraph, 'relation')
    
    nx.draw(subgraph, pos, with_labels=True, node_color='lightgreen', node_size=1500, font_size=10)
    nx.draw_networkx_edge_labels(subgraph, pos, edge_labels=labels)
    plt.title(f"{person}'s Mini Knowledge Graph")
    plt.show()

draw_person_graph(G, "Yash")
#nx.shortest_path(G, source="Yash", target="Kundan")
