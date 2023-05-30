import collections
import random
import copy
import time
from SteinerTree import steiner_tree
import networkx as nx

from solver_kEC import KECC, MinimalSubgraph
import tools

def Framework(G,Q,k):
    # ECC=list(nx.k_edge_subgraphs(G,k))
    # ECCS=[]
    # for EC in ECC:
    #     if len(set(Q)-set(EC))==0:
    #         ECCS.append(EC)
    # if len(ECCS)==0:
    #     return set()
    # randomidx=random.choice(list(range(len(ECCS))))
    # GQ=nx.Graph(nx.subgraph(G,ECCS[randomidx]))

    H=Expand(G,Q,k)
    print("expand end",len(H))
    GH=nx.Graph(nx.subgraph(G,H))
    
    HQ, anssize, d=MinimalSubgraph(GH,k,[],0,Q)
    print(len(HQ))
    return HQ
def distkneighbors(G,Q,k):
    cur=set(Q)
    next=set()
    for i in range(k):
        next.update(tools.setNeighbors(G,cur))
        next=next-cur
    return next

def Expand(G,Q,k):
    print("start steiner tree")
    SG=steiner_tree(G,Q)
    print("end steiner tree")
    S=set(SG.nodes())
    H=[]
    NuS=[]
    for d in range(1, len(G)):
        dlayer = distkneighbors(G, Q, d)
        if len(dlayer) == 0: break
        NuS.append(dlayer)
    while len(H)==0:
        u=PickClosest(G,Q,NuS,S)
        if u is None: return set()
        S.update(set(nx.neighbors(G,u)))
        GkS=nx.Graph(nx.subgraph(G,S))
        Hs=KECC(GkS,k,Q)
        for C in Hs:
            if len(Q-set(C))==0:
                # print("len C",len(C))
                return C




def PickClosest(G,Q,NuS,S):
    for d in range(len(NuS)):
        while len(NuS[d]) > 0:
            v = NuS[d].pop()
            vneighbor = set(nx.neighbors(G, v))
            if len(vneighbor-S) == 0:
                NuS[d].remove(v)
            else:
                NuS[d].remove(v)
                return v

def RefineInc(G,Q,k):
    H=set(G.nodes())
    T=set(nx.nodes(G))-set(Q)
    i=len(H)-len(Q)
    while len(T)>0:
        # print(len(H))
        i=min(i,len(T))
        U=set(random.sample(list(T),i))
        Hprime =set()
        HU=H-U
        GHU=nx.Graph(nx.subgraph(G,HU))
        Hs=KECC(G,GHU,k,Q)
        # print(Hs)
        # Hs = list(nx.k_edge_subgraphs(GHU, k))
        # print(Hs)
        for C in Hs:
            if len(Q - set(C)) == 0:
                Hprime=C
                break
        if len(Hprime)==0 and i==1:
            T=T-U
        elif len(Hprime)==0 and i>1:
            i=max(i//2,1)
        else:
            H=copy.deepcopy(Hprime)
            T=T.intersection(Hprime)
            i*=2
    return H


if __name__ == '__main__':
    # g = nx.karate_club_graph()
    # X = {1, 33}
    # ansG = Framework(g,X,2)
    #import networks as ns
    #geng = ns.advogado()
    #geng.remove_edges_from(nx.selfloop_edges(geng))
    #largest_cc = max(nx.connected_components(geng), key=len)
    #g = nx.Graph()
    #edges = geng.edges()
    #g.add_edges_from([(str(e[0]), str(e[1])) for e in edges])

    starttime = time.time()
    finalsize = 0
    density = 0
    finald = 0

    import math

    for _ in range(100):
        k = random.choice([20,30,40,50])
        querysize = random.choice([2, 4, 8, 16, 32])
        # k=16
        # querysize=2
        #readfile = open('dataEpoch//Youtube-' + str(k) + '-ECC.txt', "r+")
        readfile = open('dataEpoch//youtube_' + str(k) + 'EC.txt', "r+")
        kedges = eval(readfile.readline())
        subg = nx.Graph()
        subg.add_edges_from(kedges)
        print(len(subg))
    
            
        ansG = subg
        aved = 0
        X = set(random.sample(list(subg.nodes()), querysize))

        print(querysize)
        finalsizestep = len(subg)
        # for count in range(int(math.log(len(subg)) * 2)):
        if len(subg)!=1035:  ans = Framework(copy.deepcopy(subg),X,k)
        else: ans=list(subg.nodes())
        anssize=len(ans)
        if len(ans) < len(ansG):
            ansG = subg.subgraph(ans)
        finalsizestep = min(finalsizestep, anssize)

        finalsize += finalsizestep
        density += nx.density(ansG)

    endtime = time.time()
    print("size=", finalsize / 100)
    print("density", density / 100)
    print("ave time=", (endtime - starttime) / 100)
    print("=====================")