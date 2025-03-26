class Node:
    def __init__(self, node_id: int, coord: tuple):
        self.node_id = node_id
        self.coord = coord
        self.edges = []  # list of (neighbor, cost) tuples

    def add_edge(self, neighbor, cost):
        self.edges.append((neighbor, cost))

    def __repr__(self):
        return f"Node {self.node_id} at {self.coord}"

def dfs(nodes, start, goals, visited=None, path=None, total_cost=0):
    if visited is None:
        visited = set()
    if path is None:
        path = []

    visited.add(start)
    path.append(start)

    # If the start node is one of the goal nodes, return the path and cost
    if start in goals:
        return path, total_cost

    for neighbor, cost in nodes[start].edges:
        if neighbor not in visited:
            result = dfs(nodes, neighbor, goals, visited, path.copy(), total_cost + cost)
            if result:  # If a path is found
                return result

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
    filename = "PathFinder-test.txt"  # Change this to your actual filename
    nodes, origin, destinations = read_inputs(filename)
    
    print(f"origin {origin}")
    print(f"destinations {destinations}")
    # Print out the nodes
    print("Nodes:")
    for node in nodes.values():
        print(node)

    # Print out the edges
    print("\nEdges:")
    for node in nodes.values():
        for neighbor, cost in node.edges:
            print(f"From Node {node.node_id} to Node {neighbor} with cost {cost}")

    # Perform DFS to find path to any of the destination nodes
    if destinations:
        goals = set(destinations)  # Convert destinations to a set for faster lookup
        path, total_cost = dfs(nodes, origin, goals)
        if path:
            print(f"\nPath from {origin} to one of the goals {goals}: {path} with total cost: {total_cost}")
        else:
            print(f"\nNo path found from {origin} to any of the goals.")
    else:
        print("\nNo destinations provided.")

if __name__ == "__main__":
    main()
