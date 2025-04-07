import time
import statistics

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
                self.removeEdge(node, self.nodes[neighbor])
            del self.nodes[node.data]
            del self.adj_list[node.data]

    def addEdge(self, n1, n2, weight):
        if n1.data not in self.nodes or n2.data not in self.nodes:
            return
        self.adj_list[n1.data].add((n2.data, weight))
        self.adj_list[n2.data].add((n1.data, weight))

    def removeEdge(self, n1, n2):
        if n1.data in self.adj_list and n2.data in self.adj_list:
            self.adj_list[n1.data] = {(n, w) for (n, w) in self.adj_list[n1.data] if n != n2.data}
            self.adj_list[n2.data] = {(n, w) for (n, w) in self.adj_list[n2.data] if n != n1.data}

    def importFromFile(self, file):
        try:
            with open(file, 'r') as f:
                lines = [line.strip() for line in f if line.strip()]
            if not lines[0].startswith('strict graph'):
                return None
            if lines[0][-1] != '{' and lines[1] != '{':
                return None
            self.nodes.clear()
            self.adj_list.clear()
            content = lines[1:] if lines[0][-1] == '{' else lines[2:]
            if content[-1] != '}':
                return None
            for line in content[:-1]:
                if '--' not in line:
                    return None
                parts = line.split('--')
                left = parts[0].strip()
                rest = parts[1].strip().rstrip(';')
                if '[' in rest:
                    right, attr = rest.split('[')
                    right = right.strip()
                    attr = attr.strip(' ]')
                    weight = 1
                    for a in attr.split(','):
                        key, val = a.split('=')
                        if key.strip() == 'weight':
                            weight = int(val.strip())
                else:
                    right = rest.strip()
                    weight = 1
                n1 = self.addNode(left)
                n2 = self.addNode(right)
                self.addEdge(n1, n2, weight)
        except:
            return None

    def dfs(self):
        visited = set()
        result = []

        def visit(node):
            if node in visited:
                return
            visited.add(node)
            result.append(node)
            for neighbor, _ in self.adj_list[node]:
                visit(neighbor)

        for node in self.nodes:
            if node not in visited:
                visit(node)
        return result


class Graph2:
    def __init__(self):
        self.nodes = []
        self.node_index = {}
        self.matrix = []

    def addNode(self, data):
        if data not in self.node_index:
            self.node_index[data] = len(self.nodes)
            self.nodes.append(data)
            for row in self.matrix:
                row.append(0)
            self.matrix.append([0] * len(self.nodes))

    def addEdge(self, n1, n2, weight):
        i = self.node_index[n1]
        j = self.node_index[n2]
        self.matrix[i][j] = weight
        self.matrix[j][i] = weight

    def importFromFile(self, file):
        try:
            with open(file, 'r') as f:
                lines = [line.strip() for line in f if line.strip()]
            if not lines[0].startswith('strict graph'):
                return None
            if lines[0][-1] != '{' and lines[1] != '{':
                return None
            self.nodes.clear()
            self.node_index.clear()
            self.matrix.clear()
            content = lines[1:] if lines[0][-1] == '{' else lines[2:]
            if content[-1] != '}':
                return None
            for line in content[:-1]:
                if '--' not in line:
                    return None
                parts = line.split('--')
                left = parts[0].strip()
                rest = parts[1].strip().rstrip(';')
                if '[' in rest:
                    right, attr = rest.split('[')
                    right = right.strip()
                    attr = attr.strip(' ]')
                    weight = 1
                    for a in attr.split(','):
                        key, val = a.split('=')
                        if key.strip() == 'weight':
                            weight = int(val.strip())
                else:
                    right = rest.strip()
                    weight = 1
                self.addNode(left)
                self.addNode(right)
                self.addEdge(left, right, weight)
        except:
            return None

    def dfs(self):
        visited = [False] * len(self.nodes)
        result = []

        def visit(i):
            if visited[i]:
                return
            visited[i] = True
            result.append(self.nodes[i])
            for j in range(len(self.nodes)):
                if self.matrix[i][j] != 0 and not visited[j]:
                    visit(j)

        for i in range(len(self.nodes)):
            if not visited[i]:
                visit(i)
        return result


# Measure DFS performance
g1 = Graph()
g1.importFromFile("random.dot")
g2 = Graph2()
g2.importFromFile("random.dot")

times1 = []
times2 = []

for _ in range(10):
    start = time.time()
    g1.dfs()
    end = time.time()
    times1.append(end - start)

    start = time.time()
    g2.dfs()
    end = time.time()
    times2.append(end - start)

print("Graph (adj list) DFS times:")
print("Max:", max(times1), "Min:", min(times1), "Avg:", statistics.mean(times1))

print("Graph2 (adj matrix) DFS times:")
print("Max:", max(times2), "Min:", min(times2), "Avg:", statistics.mean(times2))


"""Graph using adjacency list is consistently faster than the matrix version. This is expected because adjacency list only stores actual neighbors, 
making traversal more efficient, especially for sparse graphs. Adjacency matrix checks all possible nodes for each visit, even if no edge exists,
which adds unnecessary overhead. Therefore, adjacency list is typically preferred for sparse graphs."""
