import sys
import heapq

class Node:
    def __init__(self, node_id: int, coord: tuple):
        self.node_id = node_id
        self.coord = coord
        self.edges = []  # list of neighbors and their cost

    def add_edge(self, neighbor, cost):
        self.edges.append((neighbor, cost))

    def __repr__(self):
        return f"Node {self.node_id} at {self.coord}"

def dijkstra(nodes, start):
    '''
    this will return a dict with the shortest distance from start (current node)
    to all other nodes in the state space
    '''
    # dictionary and we set every node to infinity as a placeholder for now
    distances = {node: float('inf') for node in nodes}
    # set the current node to distance to 0 
    distances[start] = 0
    # a queue storing tuple with current node and distance to that node --> ensuring that the lowest
    # value node is expanded first 
    priority_queue = [(0, start)]

    while priority_queue:
        # pop the tuple with the lowest first value (distance value)
        current_distance, current_node = heapq.heappop(priority_queue)
        
        # checks if the current distance of the node in the prioirty queue is larger than the distance of the current node
        # tjos os dpme sp we don't add the same node multiple times as only the one with the lowest distance to the goal node is kept
        if current_distance > distances[current_node]:
            continue
        
        
        for neighbor, cost in nodes[current_node].edges:
            # check child / neighbour nodes and add the current distance to the current cost to child node
            distance = current_distance + cost
            # if the distance is less than the neighbour node we set the distance of this neighbour node to distances dict
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                # push to our priority queue
                heapq.heappush(priority_queue, (distance, neighbor))
    
    return distances

def heuristic(node, goals, nodes):
    # Uses the dijkstra tree search to look for the shortest path to all nodes including the goal node
    shortest_paths = dijkstra(nodes, node)
    # goes through the dict in shortest path checks the distances between the goal nodes and looks at which distance
    # between goal nodes is shorter and returns that one
    # if no goal node can be found then return inf value 
    return min((shortest_paths[goal] for goal in goals if goal in shortest_paths), default=float('inf'))

def greedy(nodes, start, goals):
    
    frontier = []
    # pushes the tuple with the hueristic(distances from current node to closest goal node)
    # it also has the start node and path taken so far 
    # heapq.heappush method pushes the tuple with the lowest first value (the heuristic in this case) to the front of the heap
    heapq.heappush(frontier, (heuristic(start, goals, nodes), start, [start]))  # (heuristic value, node, path)
    
    visited = set()

    while frontier:
        _, node, current_path = heapq.heappop(frontier)
        
        if node in visited:
            continue
        
        visited.add(node)
        
        if node in goals:
            return current_path

        for neighbor, _ in nodes[node].edges:
            if neighbor not in visited:
                new_path = current_path + [neighbor]
                heapq.heappush(frontier, (heuristic(neighbor, goals, nodes), neighbor, new_path))
    
    return None  # No path found

def dfs(nodes, start, goals):
    frontier = [(start, [start])]
    visited = set()
    
    while frontier:
        node, current_path = frontier.pop()
        
        if node in visited:
            continue
        
        visited.add(node)
        
        if node in goals:
            return current_path
        
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
                coord_str = parts[1].strip()[1:-1]
                coord = tuple(map(int, coord_str.split(',')))
                nodes[node_id] = Node(node_id, coord)
                continue 

            if reading_edges:
                parts = line.split(":")
                edge_str = parts[0].strip()[1:-1]
                edge = tuple(map(int, edge_str.split(',')))
                cost = int(parts[1].strip())
                nodes[edge[0]].add_edge(edge[1], cost)
                continue

            if reading_origin:
                origin = int(line.strip())

            if reading_destinations:
                destinations.extend(map(int, line.split(";")))
                continue
    
    return nodes, origin, destinations

def main():
    filename = sys.argv[1]  # Path to the input file
    method = sys.argv[2]  # Search method (should be 'dfs' or 'greedy')

    nodes, origin, destinations = read_inputs(filename)
    goals = destinations  # A list of possible goal nodes

    if method == "dfs":
        path = dfs(nodes, origin, goals)
    elif method == "greedy":
        path = greedy(nodes, origin, goals)
    else:
        print("Invalid method! Use 'dfs' or 'greedy'")
        return

    if path:
        print(f"goal: {','.join(map(str, goals))}")
        print(f"number_of_nodes: {len(nodes)}")
        print(f"path: {','.join(map(str, path))}")
    else:
        print("No path found")

if __name__ == "__main__":
    main()