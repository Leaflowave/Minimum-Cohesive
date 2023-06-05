from collections import defaultdict
import networkx as nx
import networks
""" this procedure preprocess an input graph, outputs and stores all maximal k-cores subgraphs.
"""


class Graph:
    def __init__(self, candidate=None):
        # default dictionary to store graph
        self.graph = defaultdict(set)
        self.candidate = candidate

    def readgraph(self, path):
        readfile = open(path, 'r+')
        temp = readfile.readline()
        while temp:
            temp = temp.split(" ")
            temp1 = str(temp[0]).strip()
            temp2 = temp[1].strip()
            self.addEdge(temp1, temp2)
            temp = readfile.readline()

    def convert2graph(self, g):
        for e in g.edges():
            self.addEdge(e[0], e[1])

    # function to add an edge to undirected graph
    def addEdge(self, u, v):
        self.graph[u].add(v)
        self.graph[v].add(u)

    # A recursive function to call DFS starting from v.
    # It returns true if vDegree of v after processing is less
    # than k else false
    # It also updates vDegree of adjacent if vDegree of v
    # is less than k. And if vDegree of a processed adjacent
    # becomes less than k, then it reduces of vDegree of v also,
    def DFSUtil(self, degree, k, stack):
        # Mark the current node as visited
        while len(stack) > 0:
            v = stack.pop()
            for i in list(self.graph[v]):
                # vDegree of v is less than k, then vDegree of
                # adjacent must be reduced
                self.graph[i].remove(v)
                degree[i] -= 1
                if degree[i] < k: stack.append(i)
            self.graph[v].clear()
    def PrintKCores(self, k):
        degree = defaultdict(lambda: 0)
        for i in list(self.graph):
            degree[i] = len(self.graph[i])
        if self.candidate is None:
            self.candidate = list(self.graph)
        stack = []
        for i in self.candidate:
            if degree[i] < k:
                stack.append(i)

        self.DFSUtil(degree, k, stack)
        g = nx.Graph()
        for i in self.graph:
            if len(self.graph[i]) >= k:
                for j in list(self.graph[i]):
                    if len(self.graph[j]) >= k:
                        g.add_edge(i, j)
        return g


def Allkcore(G, k, candi=None):
    a = Graph(candi)
    a.convert2graph(G)
    return list(nx.connected_components(a.PrintKCores(k)))


if __name__ == '__main__':
    # read an input graph
    G = networks.read_graph("dataEpoch//power-eris1176.txt")
    print(len(G))
    namestr = "dataEpoch//power_"
    for k in [4, 8, 12, 16, 20]:
        with open(namestr + str(k) + "core.txt", 'w') as f:
            kcores = Allkcore(G, k)
            if kcores is None or len(kcores) == 0:
                f.flush()
                break
            print(k)
            print(len(kcores))
            maxkcore = max(kcores, key=len)
            maxG = G.subgraph(maxkcore)
            print(nx.edge_connectivity(maxG))
            maxEdges = maxG.edges()
            for edge in maxEdges:
                f.write(str(edge[0]) + " " + str(edge[1]))
                f.write("\n")
                f.flush()

