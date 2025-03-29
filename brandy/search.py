import sys

class Node:
    def __init__(self, node_id: int, coord: tuple):
        self.node_id = node_id
        self.coord = coord
        self.edges = [] # list of neighbours and their cost

    def add_edge(self, neighbor, cost):
        self.edges.append((neighbor, cost))

    def __repr__(self):
        return f"Node {self.node_id} at {self.coord}"

def dfs(nodes, start, goals):
    frontier = [(start, [start])] # frontier has the current node that is popped and the edges 
    visited = set()
    
    while frontier:
        # last in first out for dfs
        node, current_path = frontier.pop()
        
        if node in visited:
            continue
        
        visited.add(node)
        
        # If the node is one of the goal nodes, return the path
        if node in goals:
            return current_path
        
        # add the neighbour nodes of the current node into the frontier
        # we are not tracking the cost of changing nodes
        for neighbor, _ in nodes[node].edges:
            if neighbor not in visited:
                new_path = current_path + [neighbor]
                frontier.append((neighbor, new_path))
    
    return None  # No path found


def read_inputs(filename):
    nodes = {}
    origin = None
    destinations = []

    with open(filename, 'r') as file:
        lines = file.readlines()
        reading_nodes = False
        reading_edges = False
        reading_destinations = False
        reading_origin = False

        for line in lines:
            line = line.strip()
            if not line:
                continue

            if line.startswith("Nodes:"):
                reading_nodes = True
                reading_edges = False
                reading_destinations = False
                reading_origin = False
                continue
            elif line.startswith("Edges:"):
                reading_nodes = False
                reading_edges = True
                reading_destinations = False
                reading_origin = False
                continue
            
            elif line.startswith("Origin:"):
                reading_nodes = False
                reading_edges = False
                reading_destinations = False
                reading_origin = True
                continue

            elif line.startswith("Destinations:"):
                reading_nodes = False
                reading_edges = False
                reading_destinations = True
                reading_origin = False
                continue

            if reading_nodes:
                parts = line.split(":")
                node_id = int(parts[0].strip())
                coord_str = parts[1].strip()
                # remove brackets
                coord_str = coord_str[1:-1]
                # Split the string by comma to get x and y values as a list of strings
                coord_list = coord_str.split(',')
                # convert into int tuple
                coord = tuple(map(int, coord_list))
                # Create a new Node object and add it to the nodes dictionary
                nodes[node_id] = Node(node_id, coord)
                continue 

            if reading_edges:
                parts = line.split(":")
                edge_str = parts[0].strip()
                # remove brackets
                edge_str = edge_str[1:-1]
                # split into list
                edge_list = edge_str.split(',')

                # create a tuple based on edges in edge list
                edge = tuple(map(int, edge_list))

                cost = int(parts[1].strip())
                # Add edge to the start node's list of edges
                nodes[edge[0]].add_edge(edge[1], cost)
                continue

            if reading_origin:
                value = line.strip()
                origin = int(value)

            if reading_destinations:
                parts = line.split(";")
                for part in parts:
                    stripped_part = part.strip()
                    destination = int(stripped_part)
                    destinations.append(destination)
                continue
    
    return nodes, origin, destinations

def main():
    filename = sys.argv[1]  # Path to the input file
    method = sys.argv[2]  # Search method (should be 'dfs')

    nodes, origin, destinations = read_inputs(filename)
    
    print(f"filename: {filename} | method: {method}")
    
    # Perform DFS to find path to any of the destination nodes
    if method == "dfs":
        goals = destinations  # A list of possible goal nodes
        path = dfs(nodes, origin, goals)
        
        if path:
            # Extract the goal node(s) and total number of nodes
            goal_nodes = ",".join(map(str, goals))
            print(f"goal: {goal_nodes}")
            print(f"number_of_nodes: {len(nodes)}")
            print(f"path: {','.join(map(str, path))}")
        else:
            print("No path found")

if __name__ == "__main__":
    main()
