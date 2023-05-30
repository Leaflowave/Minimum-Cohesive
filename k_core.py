from collections import defaultdict
import networkx as nx

import networks


class Graph:
    def __init__(self,candidate=None):
        # default dictionary to store graph
        self.graph = defaultdict(set)
        self.candidate=candidate
    def readgraph(self,path):
        readfile=open(path,'r+')
        temp=readfile.readline()
        while temp:
            temp = temp.split(" ")
            temp1 = str(temp[0]).strip()
            temp2 = temp[1].strip()
            self.addEdge(temp1,temp2)
            temp=readfile.readline()
    def convert2graph(self,g):
        for e in g.edges():
            self.addEdge(e[0],e[1])
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
    def DFSUtil(self, degree,k,stack):
        # Mark the current node as visited
        while len(stack)>0:
            v=stack.pop()
            for i in list(self.graph[v]):
                # vDegree of v is less than k, then vDegree of
                # adjacent must be reduced
                self.graph[i].remove(v)
                degree[i]-=1
                if degree[i]<k: stack.append(i)
            self.graph[v].clear()
        # visited.add(v)
        # Recur for all the vertices adjacent to this vertex
        # for i in self.graph[v]:
            # vDegree of v is less than k, then vDegree of
            # adjacent must be reduced
            # if vDegree[v] < k:
            #     vDegree[i] = vDegree[i] - 1
            # If adjacent is not processed, process it
            # if i not in visited:
                # If vDegree of adjacent after processing becomes
                # less than k, then reduce vDegree of v also
                # self.DFSUtil(i, visited, vDegree, k)
                # stack.append(i)
    # def UpdateKCores(self, k,stack):
    #     visit = set()
    #     self.DFSUtil(visit, k,stack)
    #     g=nx.Graph()
    #     for i in self.graph:
    #         if len(self.graph[i])>=k:
    #             for j in list(self.graph[i]):
    #                 if len(self.graph[j])>=k:
    #                     g.add_edge(i,j)
    #     return g

    def PrintKCores(self, k):
        visit = set()
        degree = defaultdict(lambda: 0)
        for i in list(self.graph):
            degree[i] = len(self.graph[i])
        # print(degree)
        if self.candidate is None:
            self.candidate=list(self.graph)
        for i in self.candidate:
            if degree[i]<k:
                self.DFSUtil(degree, k,[i])
        # print(degree)
        g=nx.Graph()
        for i in self.graph:
            if len(self.graph[i])>=k:
                for j in list(self.graph[i]):
                    if len(self.graph[j])>=k:
                        g.add_edge(i,j)
        return g
def Allkcore(G,k,candi=None):
    a=Graph(candi)
    a.convert2graph(G)
    return list(nx.connected_components(a.PrintKCores(k)))

if __name__ == '__main__':
    # a=Graph()
    # import networks as ns
    # import matplotlib.pyplot as plt
    # # a.convert2graph(nx.karate_club_graph())
    # a.convert2graph(ns.IsolatedGraph())
    # # nx.draw(nx.karate_club_graph())
    # # plt.show()
    # # a.readgraph('dataEpoch//a.txt')
    # g=a.PrintKCores(1)
    # print(len(list(nx.connected_components(g))))
    # print(len(g))
    # nx.draw(g)
    # plt.show()
    # print(g.edges())
    # k=2
    # G=nx.erdos_renyi_graph(100,0.2)
    # G=networks.IsolatedGraph()
    # geng=networks.advogado()
    #geng=nx.karate_club_graph()
    G = nx.read_edgelist("dataEpoch//p2p-Gnutella31.txt",nodetype=str)
    print(len(G))
    #geng.remove_edges_from(nx.selfloop_edges(geng))
    #largest_cc = max(nx.connected_components(geng), key=len)
    #G = nx.Graph()
    #edges = geng.edges()
    #G.add_edges_from([(str(e[0]), str(e[1])) for e in edges])


    namestr="dataEpoch//p2p_"

    # allkcore=Allkcore(G,k)
    # print(allkcore)
    # if len(allkcore)>0:    print(len(allkcore[0]))

    for k in [2,3,4,5,6]:
        with open(namestr + str(k) + "core.txt", 'a+') as f:
            vcc=Allkcore(G, k)
            # C = nx.k_core(G, k)
            # print(set(C.nodes()))
            # print(len(C))
            # print([len(x) for x in vcc])
            if vcc is None or len(vcc) == 0:
                f.flush()
                break
            print(k)
            print(len(vcc))
            
            maxvcc=max(vcc,key=len)
            maxG=G.subgraph(maxvcc)

            maxEdges=maxG.edges()
            for edge in maxEdges:
                f.write(str(edge[0])+" "+str(edge[1]))
                f.write("\n")
                f.flush()

