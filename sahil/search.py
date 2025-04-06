import re
import sys
from collections import defaultdict

class Graph:
    def __init__(self):
        self.nodes = {}  # Node positions
        self.edges = defaultdict(dict)  # Adjacency list for edges
        self.origin = None
        self.destinations = []

    def load_from_file(self, filename):
        with open(filename, 'r') as file:
            content = file.read()

        # Extract nodes
        nodes_section = re.search(r"Nodes:(.*?)(Edges:|$)", content, re.DOTALL)
        if nodes_section:
            for line in nodes_section.group(1).strip().splitlines():
                node_id, x, y = re.match(r"(\d+): \((\d+),(\d+)\)", line).groups()
                self.nodes[int(node_id)] = (int(x), int(y))

        # Extract edges
        edges_section = re.search(r"Edges:(.*?)(Origin:|$)", content, re.DOTALL)
        if edges_section:
            for line in edges_section.group(1).strip().splitlines():
                start, end, cost = re.match(r"\((\d+),(\d+)\): (\d+)", line).groups()
                self.edges[int(start)][int(end)] = int(cost)

        # Extract origin
        origin_section = re.search(r"Origin:\s*(\d+)", content)
        if origin_section:
            self.origin = int(origin_section.group(1))

        # Extract destinations
        destination_section = re.search(r"Destinations:\s*(.+)", content)
        if destination_section:
            self.destinations = list(map(int, destination_section.group(1).split(';')))

    def dls(self, node, depth, visited, path, cost):
        if depth < 0:
            return None, len(visited), [], 0

        visited.add(node)
        path.append(node)

        if node in self.destinations:
            return node, len(visited), list(path), cost

        for neighbor, edge_cost in sorted(self.edges[node].items()):
            if neighbor not in visited:
                result = self.dls(neighbor, depth - 1, visited, path, cost + edge_cost)
                if result[0] is not None:
                    return result

        path.pop()
        return None, len(visited), [], 0

    def iddfs(self):
        depth = 0
        while True:
            visited = set()
            path = []
            goal, node_count, found_path, cost = self.dls(self.origin, depth, visited, path, 0)
            if goal is not None:
                return goal, node_count, found_path, cost
            depth += 1

    def __str__(self):
        return f"Nodes: {self.nodes}\nEdges: {dict(self.edges)}\nOrigin: {self.origin}\nDestinations: {self.destinations}"

# Command-line interface for search methods
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python search.py <filename> <method>")
        sys.exit(1)

    filename = sys.argv[1]
    method = sys.argv[2].upper()  # Make method case-insensitive

    graph = Graph()
    graph.load_from_file(filename)

    if method == "IDDFS":
        goal, node_count, path, cost = graph.iddfs()
        if goal is not None:
            print(f"Goal: {goal}")
            print(f"Number of Nodes Visited: {node_count}")
            print(f"Path: {path}")
            print(f"Cost: {cost}")
        else:
            print("No path found.")
    else:
        print(f"Method '{method}' not supported yet.")
