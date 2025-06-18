import json
import os

MEMORY_FILE = "clicked_resources.json"

def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return {"collected": [], "impossible": []}
    with open(MEMORY_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_memory(memory):
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(memory, f, indent=2)

def is_node_collected(coord, memory):
    return coord in memory["collected"] or coord in memory["impossible"]

def add_node(coord, memory, status="collected"):
    if status == "collected" and coord not in memory["collected"]:
        memory["collected"].append(coord)
    elif status == "impossible" and coord not in memory["impossible"]:
        memory["impossible"].append(coord)
    save_memory(memory)