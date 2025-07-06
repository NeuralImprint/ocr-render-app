from pymongo import MongoClient
import networkx as nx

# === Step 1: Load Knowledge Graph from MongoDB ===
client = MongoClient("mongodb://localhost:27017/")
db = client["ocr_database"]
collection = db["ocr_results"]

G = nx.Graph()

for doc in collection.find():
    name = str(doc.get("Name", "")).strip().title()
    age = str(doc.get("Age", "")).strip()
    marks = str(doc.get("Marks", "")).strip()
    roll = str(doc.get("Roll No", "")).strip()

    if name:
        G.add_node(name, type="Person")
        if age:
            G.add_node(age)
            G.add_edge(name, age, relation="hasAge")
        if marks:
            G.add_node(marks)
            G.add_edge(name, marks, relation="hasMarks")
        if roll:
            G.add_node(roll)
            G.add_edge(name, roll, relation="hasRollNo")

# === Step 2: Simple Query Parser ===
def parse_query(query):
    query = query.lower()
    attr_map = {
        "marks": "hasMarks",
        "score": "hasMarks",
        "roll": "hasRollNo",
        "roll no": "hasRollNo",
        "roll number": "hasRollNo",
        "age": "hasAge"
    }

    attr = None
    for key in attr_map:
        if key in query:
            attr = attr_map[key]
            break

    name = None
    # Try to extract name from the query
    for word in query.split():
        if word.istitle() and word in G.nodes:
            name = word
            break

    return name, attr

# === Step 3: Answering the Query ===
def answer_query(query):
    name, attr = parse_query(query)

    if not name:
        return "❌ Could not identify the name in the query."
    if name not in G:
        return f"❌ {name} not found in the knowledge graph."

    attributes = {}
    for neighbor in G.neighbors(name):
        relation = G[name][neighbor].get("relation")
        attributes[relation] = neighbor

    if attr:
        return f"✅ {attr[3:]} of {name} is: {attributes.get(attr, 'Not available')}"
    else:
        return f"✅ All details of {name}: {attributes}"

# === Step 4: Interactive Loop ===
print("🔍 Ask your question (e.g., 'What are the marks of Amit?'). Type 'exit' to quit.")

while True:
    user_input = input("\nYour Query: ")
    if user_input.strip().lower() in ["exit", "quit"]:
        print("👋 Exiting. Have a nice day!")
        break

    response = answer_query(user_input)
    print(response)
