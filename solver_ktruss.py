import random

import time
import networkx as nx
# import time
from networkx import k_truss
import copy
def MinimalSubgraph(G,k,red,d,X,count=None):
    ansg=G
    anssize=len(G)
    g = copy.deepcopy(G)
    if count is None: count=max(len(g)-2*k,1)

    # count=1
    while len(set(g.nodes())-set(red)-set(X))>0:
        # v=random.choice(list(set(g.nodes())-red))
        while count > len(set(g.nodes()) - set(red)-set(X)):
            count = max(count // 2, 1)
        # print("count",len(list(set(g.nodes())-set(red))))
        # print("count value:",count)
        S=random.sample(list(set(g.nodes())-set(red)-set(X)),count)   # random sampling
        # print(count)

        # v=list(set(g.nodes)-red)[0]
        # red.add(v)
        red.extend(S)
        # print("len of red",len(red))
        g1= copy.deepcopy(g)
        # g.remove_node(v)
        g.remove_nodes_from(S)

        print(count)
        vccs=FindCohesiveSubgraph(G,g,k,X)
        print("len of vccs:", len(vccs))
        if len(vccs)>=1:
            for vcc in vccs:
                # print("size of vcc:",len(vcc))
                # print(v)
                if len(set(X)-set(vcc))>0:
                    continue
                subg=nx.Graph(nx.subgraph(g,vcc))
                if count > 1:
                    d += count
                print("next")
                return MinimalSubgraph(subg,k,red,d,X,count*2)
                # if subanssize<anssize:
                #     anssize=subanssize
                #     ansg=subans
        if count>1:
            for i in range(count):
                red.pop()
        count=max(count//2,1)
        g=g1

    return ansg,anssize,d

def FindktrussSubgraph(og,g,k):

    vccs=[]
    if len(og) == len(g):
        vccs.append(list(og.nodes()))
        return vccs
    g_truss = k_truss(g, k)

    components = list(nx.connected_components(g_truss))
    return components


if __name__ == '__main__':
    # geng=ns.advogado()
    # geng=nx.read_edgelist("dataEpoch/L2Anonymized.txt")
    # geng=ns.zacharyclub()

    # geng = nx.read_edgelist('dataEpoch/L1Anonymized.txt')
    # geng.remove_edges_from(nx.selfloop_edges(geng))
    import networks
    # geng = networks.advogado()
    # k=3

    # geng.remove_edges_from(nx.selfloop_edges(geng))
    # largest_cc = max(nx.connected_components(geng), key=len)
    # g = nx.Graph()
    # edges = geng.edges()
    # g.add_edges_from([(str(e[0]), str(e[1])) for e in edges])

    starttime = time.time()
    density = 0
    finald = 0
    import math
    finalsize = 0
    for _ in range(100):
        k = random.choice([6,12,18,24,30])
        querysize = random.choice([2, 4, 8, 16])
        readfile = open('dataEpoch//L2_' + str(k) + '.txt', "r+")
        kedges = eval(readfile.readline())
        subg = nx.Graph()
        subg.add_edges_from(kedges)

        print(len(subg))
        print('query size', querysize)

        ansG = subg

        denominator = 0
        if querysize > len(subg): continue
        X = set(random.sample(list(subg.nodes()), querysize))
        finalsizestep = len(subg)
        aved = 0
        for count in range(int(math.log(len(subg)) * 2)):
            red = []
            d = 0

            if len(subg) != 1035:
                ans, anssize, d = MinimalSubgraph(copy.deepcopy(subg), k, red, d, X)
            else:
                ans = subg
                anssize = len(subg)
                d = 0
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
