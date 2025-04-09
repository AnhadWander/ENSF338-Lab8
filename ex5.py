# Q1: Topological sorting can be implemented using **Kahn’s Algorithm** or **Depth-First Search (DFS)**.
# - We use **Kahn’s Algorithm** because it efficiently detects cycles and performs topological sort in one pass.
# - It works by removing nodes with in-degree 0 and updating neighbors, which is ideal for DAGs.
# - It returns a valid topological ordering if and only if the graph has no cycles.

class GraphNode:
    def __init__(self, data):
        self.data = data

class Graph:
    def __init__(self):
        self.nodes = {}
        self.adj_list = {}

    def addNode(self, data):
        if data not in self.nodes:
            node = GraphNode(data)
            self.nodes[data] = node
            self.adj_list[data] = set()
        return self.nodes[data]

    def removeNode(self, node):
        if node.data in self.nodes:
            for neighbor in list(self.adj_list[node.data]):
                self.removeEdge(node, self.nodes[neighbor[0]])
            for src in self.adj_list:
                self.adj_list[src] = {(n, w) for (n, w) in self.adj_list[src] if n != node.data}
            del self.nodes[node.data]
            del self.adj_list[node.data]

    def addEdge(self, n1, n2, weight):
        if n1.data not in self.nodes or n2.data not in self.nodes:
            return
        # Directed edge: only n1 -> n2
        self.adj_list[n1.data].add((n2.data, weight))

    def removeEdge(self, n1, n2):
        if n1.data in self.adj_list:
            self.adj_list[n1.data] = {(n, w) for (n, w) in self.adj_list[n1.data] if n != n2.data}
## Q2
    def isdag(self):
        in_degree = {node: 0 for node in self.nodes}
        for u in self.adj_list:
            for v, _ in self.adj_list[u]:
                in_degree[v] += 1

        queue = [node for node in in_degree if in_degree[node] == 0]
        visited_count = 0

        while queue:
            current = queue.pop(0)
            visited_count += 1
            for neighbor, _ in self.adj_list[current]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

        return visited_count == len(self.nodes)
## Q3
    def toposort(self):
        if not self.isdag():
            return None

        in_degree = {node: 0 for node in self.nodes}
        for u in self.adj_list:
            for v, _ in self.adj_list[u]:
                in_degree[v] += 1

        queue = [node for node in in_degree if in_degree[node] == 0]
        topo_order = []

        while queue:
            current = queue.pop(0)
            topo_order.append(current)
            for neighbor, _ in self.adj_list[current]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

        return topo_order


# Example usage for testing
if __name__ == "__main__":
    g = Graph()
    a = g.addNode("A")
    b = g.addNode("B")
    c = g.addNode("C")
    d = g.addNode("D")
    e = g.addNode("E")

    g.addEdge(a, b, 1)
    g.addEdge(b, c, 1)
    g.addEdge(a, d, 1)
    g.addEdge(d, e, 1)

    print("Is DAG:", g.isdag())
    print("Topological Sort:", g.toposort())
