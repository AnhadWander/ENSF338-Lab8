## Q2
class UnionFind:
    def __init__(self, vertices):
        self.parent = {v: v for v in vertices}
        self.rank = {v: 0 for v in vertices}

    def find(self, node):
        if self.parent[node] != node:
            self.parent[node] = self.find(self.parent[node])  # Path compression
        return self.parent[node]

    def union(self, u, v):
        root_u = self.find(u)
        root_v = self.find(v)

        if root_u == root_v:
            return False 

        # Union by rank
        if self.rank[root_u] < self.rank[root_v]:
            self.parent[root_u] = root_v
        elif self.rank[root_u] > self.rank[root_v]:
            self.parent[root_v] = root_u
        else:
            self.parent[root_v] = root_u
            self.rank[root_u] += 1

        return True
    
## Q3
class Graph:
    def __init__(self):
        self.edges = []  # List of (weight, u, v)
        self.vertices = set()

    def add_edge(self, u, v, weight):
        self.edges.append((weight, u, v))
        self.vertices.update([u, v])

    def mst(self):
        mst_tree = Graph()
        uf = UnionFind(self.vertices)
        sorted_edges = sorted(self.edges)

        for weight, u, v in sorted_edges:
            if uf.union(u, v):
                mst_tree.add_edge(u, v, weight)

        return mst_tree

    def print_graph(self):
        for weight, u, v in self.edges:
            print(f"{u} -- {v} [{weight}]")

g = Graph()
g.add_edge('A', 'B', 2)
g.add_edge('A', 'C', 3)
g.add_edge('A', 'D', 1)
g.add_edge('B', 'E', 6)
g.add_edge('C', 'E', 4)
g.add_edge('D', 'E', 5)

print("Original graph:")
g.print_graph()

mst = g.mst()
print("\nMinimum Spanning Tree:")
mst.print_graph()
