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
