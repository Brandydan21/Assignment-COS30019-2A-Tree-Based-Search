import sys
from collections import deque

def parse_file(filename):
    with open(filename, 'r') as file:
        lines = file.read().strip().split('\n')
    
    nodes = {}
    edges = {}
    origin = None
    destinations = set()
    
    section = None
    
    for line in lines:
        line = line.strip()
        if line.startswith("Nodes:"):
            section = "nodes"
        elif line.startswith("Edges:"):
            section = "edges"
        elif line.startswith("Origin:"):
            section = "origin"
        elif line.startswith("Destinations:"):
            section = "destinations"
        elif section == "nodes" and ":" in line:
            node_id, coords = line.split(":")
            nodes[int(node_id.strip())] = tuple(map(int, coords.strip()[1:-1].split(",")))
        elif section == "edges" and ":" in line:
            edge, cost = line.split(":")
            n1, n2 = map(int, edge.strip()[1:-1].split(","))
            cost = int(cost.strip())
            edges.setdefault(n1, []).append((n2, cost))
        elif section == "origin" and line.isdigit():
            origin = int(line)
        elif section == "destinations":
            destinations.update(map(int, line.split(";")))
    
    return nodes, edges, origin, destinations

def bfs_search(filename):
    nodes, edges, origin, destinations = parse_file(filename)
    
    queue = deque([(origin, [origin])])  # (current node, path)
    visited = set()
    created_nodes = 1  # Count the origin node
    
    print(f"{filename} BFS")
    print(f"Goal: {', '.join(map(str, destinations))}")
    print(f"Number of nodes: {len(nodes)}")
    
    while queue:
        node, path = queue.popleft()
        if node in visited:
            continue
        visited.add(node)
        
        if node in destinations:
            print(f"Path: {' -> '.join(map(str, path))}")
            return
        
        if node in edges:
            for neighbor, _ in sorted(edges[node]):  # Expand in ascending order
                if neighbor not in visited:
                    created_nodes += 1
                    queue.append((neighbor, path + [neighbor]))

    print("No path found to any destination!")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python search.py <filename> <method>")
        sys.exit(1)
    
    filename = sys.argv[1]
    method = sys.argv[2].lower()
    
    if method != "bfs":
        print(f"Error: Method '{method}' not supported. Only 'bfs' is currently implemented.")
        sys.exit(1)
    
    bfs_search(filename)