import gc
# from Efficient and effective community search 2015 DMKD
import networkx as nx
import collections
from k_core import Allkcore
import tools
from SteinerTree import steiner_tree
import time
import random
import copy
from FibonacciHeap import makefheap, fheappush, fheappop


def SetMinDeg(g, S):
    G = nx.subgraph(g, S)
    ans = len(g)
    deg_S = dict()
    for v in S:
        deg_S[v] = len(list(nx.neighbors(G, v)))
        ans = min(ans, deg_S[v])
    return ans, deg_S


def Computeneigh(G, u, S):
    return set(nx.neighbors(G, u)).intersection(S)


def connection_score(G, S, v):
    return 0
    # before=len(list(nx.connected_components(nx.subgraph(G,S-{v}))))
    # print(before)
    # after=len(list(nx.connected_components(nx.subgraph(G,S|{v}))))
    # print(after)
    # return before-after


def p2pCompute(G, S, v, k):
    neighbors = list(nx.neighbors(G, v))
    subG = nx.subgraph(G, S)
    score = 0
    for x in neighbors:
        if x in S and len(list(nx.neighbors(subG, x))) < k:
            score += 1
    return score


def Greedy(G, Q, ustar=None, Hstar=None):
    if Hstar is None:
        Hstar = set(G.nodes())
    Hmin = set(Q)
    A = set()
    for cc in list(nx.connected_components(nx.subgraph(G, Hmin))):
        A.add(frozenset(cc))
    Pheap = makefheap()
    if ustar is None: ustar = SetMinDeg(G, Hstar)

    curMinDeg, Degs_Hmin = SetMinDeg(G, Hmin)
    # p1=dict()
    p2p = dict()
    p2m = dict()
    p2 = dict()
    p = dict()
    # neigh =collections.defaultdict(set)
    # for v in Hstar:
    #     neigh[v]=Computeneigh(G,v,Hstar)

    # Aprime=[]
    for q in Q:

        fheappush(Pheap, [-float('inf'), q], q)
        # p1[q]=float('inf')
        p2[q] = float('inf')
        p2p[q] = float('inf')
        p2m[q] = 0
        p[q] = -p2[q]
    # tmp_count=0
    while len(A) != 1 or curMinDeg < ustar:
        # print(tmp_count)
        # tmp_count+=1
        # candidates=set()
        for _ in range(len(Q) + 1):
            # print(len(Pheap.all_items), len(Q))
            uinfo, u = fheappop(Pheap)
            # print(_>0,len(Hmin),u in Hmin)
            Hmin.add(u)
            Degs_Hmin[u] = len(Computeneigh(G, u, Hmin))
            # update all adjacent vertices but vertices in P.
            candidates = Computeneigh(G, u, Hstar) - Hmin - Pheap.all_items
            # print(candidates)
            for v in candidates:
                p2p[v] = p2pCompute(G, Hmin, v, ustar)
                p2m[v] = max(0, ustar - len(Computeneigh(G, v, Hmin)))
                p2[v] = p2p[v] - p2m[v]
                p[v] = -p2[v]
                fheappush(Pheap, [p[v], v], v)
            if p2p[u] != float('inf'):
                break
        Aprime = set()  # the connected components of each u's neighbor
        # Aprime.add(frozenset({u}))
        neigh_u_Hmin = Computeneigh(G, u, Hmin)
        for v in neigh_u_Hmin:
            Degs_Hmin[v] += 1  # since the addition of u, the degree of v increases by 1.
            # print("deg",Degs_Hmin[v]==len(neigh(G,v,Hmin)))
            if Degs_Hmin[
                v] == ustar:  # once the degree of v has been ustar, the P2p of nodes in P\cap N[v] would decrease by 1.
                neigh_v_Hstar = Computeneigh(G, v, Hstar).intersection(Pheap.all_items) - Hmin
                for w in neigh_v_Hstar:
                    # if w==u: continue
                    if w not in p2p:
                        p2p[w] = 0
                        p2m[w] = 0
                    p2p[w] = p2p[w] - 1
                    p2[w] = p2p[w] - p2m[w]
                    p[w] = -p2[w]
                    if w not in Pheap.mapping:
                        fheappush(Pheap, [p[w], w], w)
                    else:
                        Pheap.delete(Pheap.mapping[w])
                        fheappush(Pheap, [p[w], w], w)
            for cc in A:
                if v in cc:
                    Aprime.add(frozenset(cc))
        astar = set()
        for cc in Aprime:
            astar.update(cc)
        astar.add(u)
        A = A - Aprime
        A.add(frozenset(astar))

        # UnionNeigh=set()
        # for a in Aprime:
        #     UnionNeigh1=set()
        #     for v in a:
        #         UnionNeigh1.update(Computeneigh(G,v,Hstar))
        #     UnionNeigh1=UnionNeigh1.intersection(Pheap.all_items) - Hmin
        #     UnionNeigh.update(UnionNeigh1)

        # neigh_u_Hstar=Computeneigh(G,u,Hstar).intersection(set([x[1] for x in Pheap]))
        UnionNeigh = set()

        for w in Computeneigh(G, u, Hstar).intersection(Pheap.all_items):
            if w not in p2p:
                # p1[w] = 0
                p2[w] = 0
                p2p[w] = 0
                p2m[w] = 0
            if w not in candidates:
                if Degs_Hmin[u] < ustar:
                    p2p[w] = p2p[w] + 1
                p2m[w] = max(0.0, p2m[w] - 1)
                p2[w] = p2p[w] - p2m[w]
                p[w] = -p2[w]
            if w not in Pheap.all_items:
                fheappush(Pheap, [p[w], w], w)
            else:
                Pheap.decrease_key(Pheap.mapping[w], [p[w], w])
        # if w in neigh_u_Hstar: p1[w] = connection_score(G, Hmin, w)
        # B=set()
        # for cc in list(nx.connected_components(nx.subgraph(G, Hmin))):
        #     B.add(frozenset(cc))
        # print(A==B)

        curMinDeg = min(Degs_Hmin.values())
        # print(curMinDeg)
    del p2, p2p, p2m, p, Pheap, Degs_Hmin, A, Aprime, Hstar, UnionNeigh, astar
    gc.collect()
    return Hmin


def Connection(G, Q, k, Hstar=None):
    # HminG=nx.subgraph(G,Hmin)
    # print(Hmin)
    HhatG = steiner_tree(G, Q)
    print(len(HhatG))
    print("end of steiner tree")
    Hhat = set(HhatG.nodes())
    ansstar = Greedy(G, Hhat, ustar=k, Hstar=Hstar)
    return ansstar


def framework(G, Q, k):
    # Hmin=Greedy(G,Q,Hstar=set(G.nodes()),ustar=k)
    # HminG=nx.Graph(nx.subgraph(G,Hmin))
    Hmin = set(G.nodes())
    HminG = G
    print("Hmin", len(Hmin))
    return Connection(HminG, Q, k, Hstar=Hmin)


if __name__ == '__main__':
    # G=nx.karate_club_graph()
    # import networks as ns
    # geng = ns.advogado()
    # geng.remove_edges_from(nx.selfloop_edges(geng))
    # largest_cc = max(nx.connected_components(geng), key=len)
    # g = nx.Graph()
    # edges = geng.edges()
    #
    # g.add_edges_from([(str(e[0]), str(e[1])) for e in edges])
    # X = {'1485', '1174', '1089', '1052', '1579', '1397', '1177', '426', '1604', '162'}

    # geng=nx.karate_club_graph()
    # print(dict(nx.degree(g)))
    # nx.draw(geng,with_labels=True)
    # import matplotlib.pyplot as plt
    # plt.show()
    # X={1,11}
    # ansG=framework(g,X)
    # print(len(ansG))
    # print(dict(nx.degree(nx.subgraph(g,ansG))))

    # geng = nx.read_edgelist('dataEpoch/L1Anonymized.txt')

    # import networks
    # geng=networks.advogado()
    # geng.remove_edges_from(nx.selfloop_edges(geng))
    # largest_cc = max(nx.connected_components(geng), key=len)
    # g = nx.Graph()
    # edges = geng.edges()
    # g.add_edges_from([(str(e[0]), str(e[1])) for e in edges])

    starttime = time.time()
    finalsize = 0
    density = 0
    for _ in range(100):
        k = random.choice([5,10])
        querysize = random.choice([2, 4, 8, 16, 32])
        readfile = open('dataEpoch//advogado_' + str(k) + 'core.txt', "r+")
        kedges = eval(readfile.readline())
        subg = nx.Graph()
        subg.add_edges_from(kedges)
        # subg=nx.read_edgelist('dataEpoch//lastfm_asia_edgesTrans.txt',nodetype=str)
        # subg=nx.k_core(subg,k)
        originalsize = len(subg)
        X = set(random.sample(list(subg.nodes()), querysize))
        finalsizestep = len(subg)
        ansG = framework(copy.deepcopy(subg), X, k)
        anssize = len(ansG)
        finalsizestep = min(finalsizestep, anssize)
        finalsize += finalsizestep
        density += nx.density(nx.subgraph(subg, ansG))
        print(finalsizestep)
        # del subg, kedges, ansG
        gc.collect()
    endtime = time.time()
    # print("k=", k)
    print("size=", finalsize / 100.0)
    # print("d=", aved/denominator)
    # print("original=", originalsize)
    print("density=", density / 100.0)
    print("ave time=", (endtime - starttime) / 100.0)
    print("=====================")









