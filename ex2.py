import time
import math
import heapq
import matplotlib.pyplot as plt

class Graph:
    def __init__(self):
        self.adj_list = {}
    
    def add_node(self, node):
        if node not in self.adj_list:
            self.adj_list[node] = []
    
    def add_edge(self, u, v, w):
        self.add_node(u)
        self.add_node(v)
        self.adj_list[u].append((v, w))
        self.adj_list[v].append((u, w))
    
    def get_all_nodes(self):
        return list(self.adj_list.keys())
    
    def slowSP(self, source):
        dist = {node: math.inf for node in self.adj_list}
        dist[source] = 0
        
        visited = set()
        total_nodes = len(self.adj_list)
        
        while len(visited) < total_nodes:
            u = None
            min_dist = math.inf
            for node in self.adj_list:
                if node not in visited and dist[node] < min_dist:
                    min_dist = dist[node]
                    u = node
            
            if u is None:
                break
            
            visited.add(u)
            
            for (neighbor, weight) in self.adj_list[u]:
                if neighbor not in visited:
                    new_dist = dist[u] + weight
                    if new_dist < dist[neighbor]:
                        dist[neighbor] = new_dist
        
        return dist
    
    def fastSP(self, source):
        dist = {node: math.inf for node in self.adj_list}
        dist[source] = 0
        
        visited = set()
        pq = []
        
        heapq.heappush(pq, (0, source))
        
        while pq:
            current_dist, u = heapq.heappop(pq)
            if u in visited:
                continue
            visited.add(u)
            
            for (neighbor, weight) in self.adj_list[u]:
                if neighbor not in visited:
                    new_dist = current_dist + weight
                    if new_dist < dist[neighbor]:
                        dist[neighbor] = new_dist
                        heapq.heappush(pq, (new_dist, neighbor))
        
        return dist


def load_dot_file(filename):
    graph = Graph()
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if '--' not in line or 'weight=' not in line:
                continue
            
            if line.endswith(';'):
                line = line[:-1].strip()
            
            parts = line.split('--')
            if len(parts) < 2:
                continue
            
            left = parts[0].strip()
            right = parts[1].strip()
            
            if '[' in right:
                node_str, weight_str = right.split('[', 1)
                node_str = node_str.strip()
                weight_str = weight_str.strip('[]')
                if '=' in weight_str:
                    wparts = weight_str.split('=')
                    weight_val_str = wparts[1].strip()
                    try:
                        w = float(weight_val_str)
                    except:
                        w = 1.0
                else:
                    w = 1.0
                
                try:
                    u = int(left)
                except ValueError:
                    u = left  
                try:
                    v = int(node_str)
                except ValueError:
                    v = node_str  
                
                graph.add_edge(u, v, w)
    
    return graph


def main():
    filename = 'random.dot'  
    graph = load_dot_file(filename)
    
    all_nodes = graph.get_all_nodes()
    print(f"Loaded graph with {len(all_nodes)} nodes.")
    
    times_slow = []
    for n in all_nodes:
        start = time.time()
        _ = graph.slowSP(n)
        end = time.time()
        times_slow.append(end - start)
    
    avg_slow = sum(times_slow) / len(times_slow)
    max_slow = max(times_slow)
    min_slow = min(times_slow)
    
    print("SLOW version => avg: {:.5f}, max: {:.5f}, min: {:.5f}"
          .format(avg_slow, max_slow, min_slow))
    
    times_fast = []
    for n in all_nodes:
        start = time.time()
        _ = graph.fastSP(n)
        end = time.time()
        times_fast.append(end - start)
    
    avg_fast = sum(times_fast) / len(times_fast)
    max_fast = max(times_fast)
    min_fast = min(times_fast)
    
    print("FAST version => avg: {:.5f}, max: {:.5f}, min: {:.5f}"
          .format(avg_fast, max_fast, min_fast))
    
    plt.hist(times_slow, bins=30, alpha=0.5, label='Slow Dijkstra')
    plt.hist(times_fast, bins=30, alpha=0.5, label='Fast Dijkstra')
    plt.xlabel('Execution time (seconds)')
    plt.ylabel('Number of nodes')
    plt.title('Distribution of Dijkstra Execution Times')
    plt.xlim(0.0, 0.03) 
    plt.legend()
    plt.show()


if __name__ == "__main__":
    main()
