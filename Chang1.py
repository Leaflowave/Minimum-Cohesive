import collections
import copy
import random

from FibonacciHeap import *
import networkx as nx
from tools import EdgeCertificate
from k_core import Allkcore
import time


def KECC(G, k, X):
    """
    :param G:
    :param k:
    :return: a list of k-ecc nodes
    """
    ans = []
    # sparseg=EdgeCertificate(G,k)
    sparseg = G

    L = [set(sparseg.nodes())]
    while len(L) > 0:
        gset = L.pop()
        curg=subgraph(sparseg,gset)
        # curg = nx.Graph(nx.subgraph(sparseg, gset))
        yk = Partition(curg, k, X)
        for y in yk:
            if len(X - y) > 0:
                continue
            if len(yk) == 1 and len(y) > 1:
                ans.append(y)
            else:
                L.append(y)
    return ans
def subgraph(g,cc):
    newg=nx.Graph()
    for v in cc:
        for nei in nx.neighbors(g,v):
            if nei>v and nei in cc:
                newg.add_edge(v,nei,weight=1)
                newg[nei][v]['weight']=newg[v][nei]['weight']
    return newg
def Partition(g, k, X):
    """
    return: a set of vertices
    """
    # g_core=nx.k_core(g,k)
    k_cores = Allkcore(g, k)  # a list of sets
    if len(k_cores) == 0: return []
    k_core = k_cores[0]
    for i in range(len(k_cores)):
        tmp = len(X - k_cores[i])
        if tmp == 0:
            k_core = k_cores[i]
            break
        elif tmp > 0 and tmp < len(X):
            return []

    g_core = subgraph(g,k_core)
    G1 = copy.deepcopy(g_core)
    nx.set_node_attributes(G1, {v:{v} for v in G1.nodes()}, name="contain")
    while G1.number_of_edges()> 1:
        # start = time.time()
        # print(G1.edges())

        MAS_OPT(G1, k, g_core)
        # print(time.time() - start)
    ans = []
    for cc in nx.connected_components(g_core):
        ans.append(cc)
    return ans


def weight(L, v, g):
    count=0
    if v in L: return count
    for nei in nx.neighbors(g,v):
        # print('weight',nei,g[v][nei]['weight'])
        if nei in L:
            count+=g[v][nei]['weight']
    return count


def MAS_OPT(gprime, k, g):
    V_gprime = list(gprime.nodes())
    L = [random.choice(V_gprime)]
    # Lmapping = []
    # w = makefheap()
    wprime = makefheap()
    # nodemapping = dict()
    for v in V_gprime:
        tmpweight=-weight(L, v, gprime)
        if v not in L:fheappush(wprime, [tmpweight, v], v)

    # while len(L) != len(V_gprime):
    while wprime.num_nodes>0:
        wt, u= wprime.extract_min().key
        # print(u,len(V_gprime))
        if u not in gprime or u in L:
            # print(u,L)
            continue

        # print(u,len(L), len(V_gprime))
        L.append(u)
        # Lmapping.append(set(nodemapping[u]))
        # print(L)
        Q = [u]
        vis=set()

        while len(Q) > 0:
            v = Q.pop(0)
            # print(Lmapping)

            if v not in set(gprime.nodes()): continue
            for nei in list(nx.neighbors(gprime, v)):
                if nei in L: continue
                # target_value = w.mapping[nei].key
                # w.decrease_key(w.mapping[nei], [target_value[0] - gprime[nei][v]['weight'], str(target_value[1])])

                if wprime.mapping[nei].key[0]- gprime[nei][v]['weight'] <= -k:
                    Q.append(nei)
                    continue
                vis.update([(nei,v),(v,nei)])
                target_value = wprime.mapping[nei].key
                wprime.decrease_key(wprime.mapping[nei],[target_value[0] - gprime[nei][v]['weight'], str(target_value[1])])
                # wprime.decrease_key(wprime.mapping[nei],[target_value[0] - 1, str(target_value[1])])

            if u != v:
                # print(u,v)
                #merge u and v into u:
                # add v's mapping to u
                # nodemapping[u].update(nodemapping[v])
                # Lmapping[-1].update(nodemapping[v])
                gprime.nodes[u]['contain'].update(gprime.nodes[v]['contain'])

                for vnei in list(nx.neighbors(gprime, v)):
                    if vnei==u:continue
                    if vnei not in L and (vnei,v) not in vis:  #update the heap value of vnei
                        target_value = wprime.mapping[vnei].key
                        wprime.decrease_key(wprime.mapping[vnei], [target_value[0] - gprime[vnei][v]['weight'], str(target_value[1])])
                    if gprime.has_edge(u,vnei):  # increase v's neighbors weights by 'weight'.
                        gprime[vnei][u]['weight']+=gprime[vnei][v]['weight']
                        gprime[u][vnei]['weight'] = gprime[vnei][u]['weight']
                    else:
                        gprime.add_edge(vnei, u,weight=gprime[vnei][v]['weight'])
                        gprime[u][vnei]['weight']=gprime[vnei][u]['weight']
                #remove v from gprime
                gprime.remove_node(v)

        V_gprime=list(gprime.nodes())
    cutEdges = []
    if len(L) > 1: cutEdges = deconstruction_cut(g, gprime.nodes[L[-1]]['contain'])
    while len(L) > 1 and len(cutEdges) < k:
        # print(cutEdges)
        v = L.pop()
        if v in gprime:
            # print("remove v from gprime")
            gprime.remove_node(v)
        g.remove_edges_from(cutEdges)
        cutEdges = deconstruction_cut(g, gprime.nodes[L[-1]]['contain'])
        # Lmapping.pop()
    return


def deconstruction_cut(g, a):
    """the adjacent edges of a is an edge cut"""
    cutEdges=[]
    for v in a:
        for nei in nx.neighbors(g,v):
            if nei not in a:
                cutEdges.append((v,nei))
    return cutEdges



if __name__ == '__main__':
    import networks as ns
    import time
    from tools import EdgeCertificate
    # G=ns.B_A_2000()
    subg=nx.read_edgelist('dataEpoch//flights_3core.txt')
    # readfile = open('dataEpoch//dblp_16core.txt', "r+")
    # kedges = eval(readfile.readline())
    # subg = nx.Graph()
    # subg.add_edges_from(kedges)
    # G.remove_edges_from(nx.selfloop_edges(G))
    # g=nx.Graph()
    # for edge in subg.edges():
    #     g.add_edge(str(edge[0]),str(edge[1]))
    # kecc=list(nx.k_edge_subgraphs(g,3))
    #
    # print(len(max(kecc,key=len)))
    # print(kecc)
    start = time.time()
    print(len(subg))
    # print(list(nx.neighbors(subg,'2504')))
    #sparseg=EdgeCertificate(g,4)
    kecc=KECC(subg,3,set())   #[7, 4, 1, 4, 1440]
    # Id1 = {'2581', '2640', '2636', '2638', '2928', '2639', '2637'}
    # Id2 = {'2687', '2690', '2505', '2688'}
    # ID3 = {'2504'}
    # print(nx.degree_histogram(subg))
    # kecc=list(nx.k_edge_subgraphs(subg,3))
    # print(len(max(kecc, key=len)))
    end=time.time()
    print(end-start)
    print(list(len(kecc[i]) for i in range(len(kecc))))
    print(nx.edge_connectivity(nx.subgraph(subg,kecc[0])))
    # print(kecc)

