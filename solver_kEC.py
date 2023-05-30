import random
import time
import networkx as nx
from networkx import k_core
import networks as ns
import copy
import collections
from tools import min_edge_cut,EdgeCertificate,FindEdgeCut
from MinCut_Sample import build_auxiliary_edge_connectivity
from Chang1 import KECC


def MinimalSubgraph(G,k,red,d,X,count=None):
    ansg=G
    anssize = len(ansg)
    step=0  #r=4 delta=0.001
    while step<5  and len(set(ansg.nodes())-set(red)-set(X))>0:
        anssize = len(ansg)
        g = copy.deepcopy(ansg)
        if count is None: count=max(len(g)-2*k,1)
        while count > len(set(g.nodes()) - set(red)-set(X)):
            count = max(count // 2, 1)
        S=random.sample(list(set(g.nodes())-set(red)-set(X)),count)   # random sampling

        red.extend(S)
        g.remove_nodes_from(S)
        vccs=KECC(g,k,X)
        if len(vccs)>=1:
            step=0
            for vcc in vccs:
                if len(set(X)-set(vcc))>0:
                    continue
                subg=nx.Graph(nx.subgraph(ansg,vcc))
                if count > 1:
                    d += count
                if count==1:
                    d+=1
                ansg=subg
                count=count
                break
        else:
            if count>1:
                for i in range(count):
                    red.pop()
            else:
                step+=1
            count=max(count//2,1)

    return ansg,anssize,d

def FindkECSubgraph(og,g,k,X=None,dependencyMap=None,ccid=None):
    eccs = []
    if len(og) == len(g):
        eccs.append(list(og.nodes()))
        return eccs
    g_core = k_core(g, k)
    components = list(nx.connected_components(g_core))
    
    
    for component in components:
        if len(component) < k + 1: continue
        
        if X is not None and len(set(X) - set(component)) > 0: continue
        Nu = list(nx.node_boundary(og, set(og.nodes()) - component,set(component)))
        
        component_g = nx.Graph(og.subgraph(component))

        
        curdependencyMap=nx.Graph(dependencyMap.subgraph(list(g.nodes())))
        cur_ccid=dict()
        update(cur_ccid, curdependencyMap)
        print("enter",len(Nu))
        cutEdges = FindEdgeCut(component_g, k, Nu,cur_ccid,curdependencyMap)

        # cutEdges=nx.algorithms.connectivity.stoer_wagner(component_g,cutoff=k)
        # print(cutEdges)
        if cutEdges is None:
            # print("cut is None")
            eccs.append(component)
        else:
            # print("component",component_g is None)
            # print("cutedge",cutEdges is None)
            component_g.remove_edges_from(cutEdges)
            for edge in cutEdges:
                if dependencyMap.has_edge(edge[0],edge[1]):
                    dependencyMap.remove_edge(edge[0],edge[1])
            update(ccid, dependencyMap)
            sub_components=list(nx.connected_components(component_g))

            for sub_component in sub_components:
                if len(sub_component) < k + 1: continue
                if X is not None and len(set(X) - set(sub_component)) > 0: continue
                sub_component_g = g.subgraph(sub_component).copy()
                eccs = eccs + FindkECSubgraph(og, sub_component_g, k, X=X,dependencyMap=dependencyMap,ccid=ccid)
    return eccs
def FindCut(G,k,Nu,ccid,dependencyMap):
    g=EdgeCertificate(G,k)
    degNu = dict(nx.degree(g, Nu))
    sorted(Nu, key=lambda x: degNu[x])
    if degNu[Nu[0]] < k:
        return set(nx.neighbors(g,Nu[0]))
    flowg = build_auxiliary_edge_connectivity(g)
    #dependencyMap=nx.Graph()
    #dependencyMap.add_nodes_from([Nu[x] for x in range(len(Nu))])
    #for s in range(len(Nu)):
    #    for t in range(s + 1, len(Nu)):
    #        if len(set(nx.neighbors(g, Nu[s])).intersection(set(nx.neighbors(g, Nu[t]))))>=k:
    #            dependencyMap.add_edge(Nu[s],Nu[t])
    #ccid=collections.defaultdict(str)
    #update(ccid,dependencyMap)

    # ccs=list(nx.connected_components(dependencyMap))
    #
    # for i in range(len(ccs)):
    #     cc=ccs[i]
    #     for v in cc:
    #         ccid[v]=str(i)


    s=0
    # for s in range(len(Nu)):
    curIds=set()
    curIds.add(ccid[Nu[s]])
    for t in range(1, len(Nu)):
        print("s",s)
        if ccid[Nu[t]] in curIds:
            continue
        cut =min_edge_cut(g, k, Nu[s], Nu[t], flowg)
        if cut is not None and len(cut) < k:
            return cut
        curIds.add(ccid[Nu[t]])
    #     dependencyMap.add_edge(Nu[s],Nu[t])
    #     update(ccid, dependencyMap)
    # if len(Nu)<=k:
    #     return
    # u0 = "u0"
    # sparsegj = copy.deepcopy(g)
    # for x in range(k):
    #     sparsegj.add_edge(u0, Nu[x])
    # ccid[u0]=ccid[Nu[0]]
    # for j in range(k - 1, len(Nu) - 1):
    #     if ccid[u0]==ccid[Nu[j]]: continue
    #     cut = tools.min_edge_cut(sparsegj, k, u0, Nu[j + 1])
    #     if cut is not None and len(cut) < k:
    #         return cut
    #     sparsegj.add_edge(u0, Nu[j + 1])
    #     ccid[Nu[j+1]]=ccid[u0]
    #     dependencyMap.add_edge(Nu[j+1], u0)
    #     update(ccid,dependencyMap)
    return
def update(ccid,dependencyMap):
    # ccid = collections.defaultdict(str)
    ccs = list(nx.connected_components(dependencyMap))

    for i in range(len(ccs)):
        cc = ccs[i]
        for v in cc:
            ccid[v] = str(i)
    return
if __name__ == '__main__':
    # geng=nx.karate_club_graph()
    #geng=ns.advogado()
    # geng = nx.read_edgelist('dataEpoch/L1Anonymized.txt')
    # geng.remove_edges_from(nx.selfloop_edges(geng))
    # k=3

    #geng.remove_edges_from(nx.selfloop_edges(geng))
    #largest_cc = max(nx.connected_components(geng), key=len)
    #g = nx.Graph()
    #edges = geng.edges()
    #g.add_edges_from([(str(e[0]), str(e[1])) for e in edges])

    starttime = time.time()
    density = 0
    finald = 0
    import math
    finalsize = 0
    for _ in range(100):
        k = random.choice([20,30,40,50])
        querysize = random.choice([2, 4, 8, 16, 32])
        readfile = open('dataEpoch//youtube_' + str(k) + 'EC.txt', "r+")
        kedges = eval(readfile.readline())
        subg=nx.Graph()
        subg.add_edges_from(kedges)

        print(len(subg))
        print('query size', querysize)
        
        ansG = subg
        
        denominator = 0
        if querysize > len(subg): continue
        X = set(random.sample(list(subg.nodes()), querysize))
        finalsizestep = len(subg)
        aved=0
        for count in range(int(math.log(len(subg)) * 2)):
            red = []
            d = 0
            
            if len(subg)!=1035:  ans, anssize, d = MinimalSubgraph(copy.deepcopy(subg), k, red, d, X)
            else: 
                ans=subg
                anssize=len(subg)
                d=0
            print("d=", d)
            denominator += 1
            aved += d
            if len(ans) < len(ansG):
                ansG = ans
            finalsizestep = min(finalsizestep, anssize)
            if anssize == k + 1:
                break
            print(finalsizestep)
        finalsize += finalsizestep
        finald += aved / denominator
        density += nx.density(ansG)

    endtime = time.time()
    print("size=", finalsize / 100)
    print("d=", finald / 100)
    print("density", density / 100)
    print("ave time=", (endtime - starttime) / 100)
    print("=====================")
