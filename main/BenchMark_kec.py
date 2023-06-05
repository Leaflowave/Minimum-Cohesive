import random
import copy
import time
from SteinerTree import steiner_tree
import networkx as nx
import gc
from solver_kEC import KECC, MinimalSubgraph
import networks as ns
""" an implementation of the "Querying Minimal Steiner Maximum-Connected Subgraphs from Large Graphs"
"""

def Framework(G, Q, k):
    H = Expand(G, Q, k)
    print("expand end", len(H))
    GH = nx.Graph(nx.subgraph(G, H))

    HQ, anssize, d = MinimalSubgraph(GH, k, [], 0, Q)
    print(len(HQ))
    return HQ


def distkneighbors(G, Q, k):
    cur = set(Q)
    nxt = set()
    for i in range(k):
        nxt.update(ns.setNeighbors(G, cur))
        nxt = nxt - cur
        if len(nxt) == 0:
            break
    return nxt


def Expand(G, Q, k):
    print("start steiner tree")
    SG = steiner_tree(G, Q)
    print("end steiner tree")
    S = set(SG.nodes())
    theta = 10000
    NuS = []

    cur = set(Q)
    nxt = set()
    for i in range(len(G)):
        nxt.update(ns.setNeighbors(G, cur))
        nxt = nxt - cur

        if len(nxt) == 0:
            break
        NuS.append(set(nxt))

    while theta > 0:
        u = PickClosest(G, NuS, S)

        if u is None: break
        S.update(set(nx.neighbors(G, u)))
        GkS = nx.Graph(nx.subgraph(G, S))
        Hs = KECC(GkS, k, Q)
        for C in Hs:
            if len(Q - set(C)) == 0:
                return C

    return set(G.nodes())


def PickClosest(G, NuS, S):
    for d in range(len(NuS)):
        while len(NuS[d]) > 0:
            v = NuS[d].pop()
            vneighbor = set(nx.neighbors(G, v))
            if len(vneighbor - S) == 0:
                continue
            else:

                return v


def RefineInc(G, Q, k):
    H = set(G.nodes())
    T = set(nx.nodes(G)) - set(Q)
    i = len(H) - len(Q)
    while len(T) > 0:
        # print(len(H))
        i = min(i, len(T))
        U = set(random.sample(list(T), i))
        Hprime = set()
        HU = H - U
        GHU = nx.Graph(nx.subgraph(G, HU))
        Hs = KECC(GHU, k, Q)
        for C in Hs:
            if len(Q - set(C)) == 0:
                Hprime = C
                break
        if len(Hprime) == 0 and i == 1:
            T = T - U
        elif len(Hprime) == 0 and i > 1:
            i = 1
        else:
            H = copy.deepcopy(Hprime)
            T = T.intersection(Hprime)
            i += 1
    return H


if __name__ == '__main__':
    for k in [4, 8, 12, 16, 20]:
        for querysize in [2, 4, 8, 16]:
            starttime = time.time()
            finalsize = 0
            density = 0
            finald = 0
            for _ in range(10):
                readfile = open('dataEpoch//EC_power_' + str(k) + '.txt', "r+")
                print(k)
                kedges = eval(readfile.readline())
                subg = nx.Graph()
                subg.add_edges_from(kedges)
                print(len(subg))

                ansG = subg
                aved = 0
                X = set(random.sample(list(subg.nodes()), querysize))

                print(querysize)
                finalsizestep = len(subg)
                ans = Framework(copy.deepcopy(subg), X, k)
                anssize = len(ans)
                if len(ans) < len(ansG):
                    ansG = subg.subgraph(ans)
                finalsizestep = min(finalsizestep, anssize)

                finalsize += finalsizestep
                density += nx.density(ansG)
                del ans, readfile, kedges, subg
                gc.collect()
            endtime = time.time()
            print("k=", k)
            print("querysize", querysize)
            print("size=", finalsize / 10)
            print("density", density / 10)
            print("ave time=", (endtime - starttime) / 10)
            print("=====================")
