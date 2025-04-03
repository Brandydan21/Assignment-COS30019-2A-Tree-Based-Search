import math
import sys

class Graph:
    def __init__(self):
        self.nodes = {}  
        self.edges = {}  
        self.origin = None
        self.destinations = []
        
    def add_node(self, node_id, x, y):
        self.nodes[node_id] = (x, y)
        
    def add_edge(self, from_node, to_node, cost):
        self.edges[(from_node, to_node)] = cost
        
    def set_origin(self, node_id):
        self.origin = node_id
        
    def add_destination(self, node_id):
        self.destinations.append(node_id)
        
    def get_neighbors(self, node_id):
        neighbors = []
        for edge in self.edges:
            if edge[0] == node_id:
                neighbors.append((edge[1], self.edges[edge]))
        return neighbors
    
    def distance(self, node1, node2):
        x1, y1 = self.nodes[node1]
        x2, y2 = self.nodes[node2]
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def astar_search(graph, origin, destinations):
    destination_set = set(destinations)
    open_set = []

    initial_h = min(graph.distance(origin, dest) for dest in destinations)
    open_set.append((initial_h, origin, [origin], 0))

    closed_set = set()
    
    while open_set:
        min_index = 0
        for i in range(1, len(open_set)):
            if open_set[i][0] < open_set[min_index][0]:
                min_index = i

        f_score, current_node, path, cost = open_set.pop(min_index)

        if current_node in destination_set:
            return path, cost

        if current_node in closed_set:
            continue

        closed_set.add(current_node)

        neighbors = graph.get_neighbors(current_node)
        
        neighbors.sort(key=lambda x: x[0])
        
        for neighbor, edge_cost in neighbors:
            if neighbor in closed_set:
                continue

            new_cost = cost + edge_cost
            new_path = path + [neighbor]

            h_score = min(graph.distance(neighbor, dest) for dest in destinations)

            f_score = new_cost + h_score

            open_set.append((f_score, neighbor, new_path, new_cost))

    return None, float('inf')

def parse_input(input_data):
    """Parse the input data and create a graph"""
    graph = Graph()
    
    lines = input_data.strip().split('\n')
    section = None
    
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"): 
            continue
            
        if "Nodes:" in line:
            section = "nodes"
            continue
        elif "Edges:" in line:
            section = "edges"
            continue
        elif "Origin:" in line:
            section = "origin"
            continue
        elif "Destinations:" in line:
            section = "destinations"
            continue
            
        if section == "nodes":
            parts = line.split(":")
            if len(parts) < 2:
                continue
            try:
                node_id = int(parts[0])
                coords_str = parts[1].strip().strip("()").split(",")
                if len(coords_str) < 2:
                    continue
                x, y = int(coords_str[0]), int(coords_str[1])
                graph.add_node(node_id, x, y)
            except (ValueError, IndexError):
                print(f"Warning: Could not parse node line: {line}")
            
        elif section == "edges":
            parts = line.split(":")
            if len(parts) < 2:
                continue
            try:
                edge_str = parts[0].strip().strip("()").split(",")
                if len(edge_str) < 2:
                    continue
                from_node, to_node = int(edge_str[0]), int(edge_str[1])
                cost = int(parts[1].strip())
                graph.add_edge(from_node, to_node, cost)
            except (ValueError, IndexError):
                print(f"Warning: Could not parse edge line: {line}")
            
        elif section == "origin":
            try:
                graph.set_origin(int(line))
            except ValueError:
                print(f"Warning: Could not parse origin: {line}")
            
        elif section == "destinations":
            destinations = line.split(";")
            for dest in destinations:
                dest = dest.strip()
                if dest:
                    try:
                        graph.add_destination(int(dest))
                    except ValueError:
                        print(f"Warning: Could not parse destination: {dest}")
    
    return graph

def main():
    file_name = sys.argv[1]
    method = sys.argv[2]
    try:
        with open(file_name, "r") as file:
            input_data = file.read()
    except FileNotFoundError:
        print(f"Error: File '{file_name}' not found.")
        return
    except Exception as e:
        print(f"Error reading file: {e}")
        return
    
    graph = parse_input(input_data)

    if not graph.nodes:
        print("Error: No nodes found in the input file.")
        return
    
    if graph.origin is None:
        print("Error: No origin node specified in the input file.")
        return
        
    if not graph.destinations:
        print("Error: No destination nodes specified in the input file.")
        return

    print(f"{file_name} {method}")
    print(f"Goal: {', '.join(map(str, graph.destinations))} \nNumber of nodes: {len(graph.nodes)}")
    
    path, cost = astar_search(graph, graph.origin, graph.destinations)
    
    if path:
        print(f"Path: {' -> '.join(map(str, path))}")
        print(f"Total cost: {cost}")
        
    else:
        print("No path found to any destination!")

if __name__ == "__main__":
    main()