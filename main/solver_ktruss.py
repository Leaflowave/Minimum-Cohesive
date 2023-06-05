import random
import time
import networkx as nx
from networkx import k_truss
import copy
from Chang1 import subgraph

def MinimalSubgraph(G, k, d, X, count=None):
    """
    implementation of the Mincoh algorithm on k-truss index
    :param G: a k-truss graph
    :param k: cohesiveness level
    :param d: record of total number of randomly removed vertices
    :param X: query set
    :param count: the value r, meaning the num of randomly sampled vertices each step
    :return: a small k-truss subgraph
    """
    red=[]
    ansg = G
    step = 0
    anssize = len(ansg)
    ansgNodes = set(ansg.nodes())
    redSet = set(red)
    while step < 5 and len(ansgNodes - redSet - X) > 0:
        anssize = len(ansg)
        g = copy.deepcopy(ansg)

        if count is None: count = max(len(g) // (k + 1), 2)
        while count > len(ansgNodes - set(red) - set(X)):
            count = max(count // 2, 2)
        S = random.sample(list(ansgNodes - redSet - X), count)  # random sampling
        redSet.update(S)
        red.extend(S)
        g.remove_nodes_from(S)

        vccs = FindktrussSubgraph(g, k)
        if len(vccs) >= 1:
            step = 0
            for vcc in vccs:
                if len(X - vcc) > 0:
                    continue
                subg = subgraph(ansg, vcc)
                if count > 1:
                    d += count
                if count == 1:
                    d += 1
                ansg = subg
                ansgNodes = set(ansg.nodes())
                break
        else:
            if count > 1:
                for i in range(count):
                    tmp = red.pop()
                    redSet.remove(tmp)

            step += 1
            if step == 5 and count > 2:
                step = 0
                count = max(count // 2, 2)
    return ansg, anssize, d


def FindktrussSubgraph(g, k):
    g_truss = k_truss(g, k)

    components = list(nx.connected_components(g_truss))
    ans = []
    for c in components:
        tmp = len(set(X) - c)
        if tmp == 0:
            ans.append(c)
            break
        elif tmp > 0 and tmp < len(X):
            break
    return ans


if __name__ == '__main__':
    import gc
    starttime = time.time()
    finalsize = 0
    density = 0
    finald = 0
    for k in [4, 8, 12, 16, 20]:
        for querysize in [2, 4, 8, 16]:
            starttime = time.time()
            finalsize = 0
            density = 0
            finald = 0
            for _ in range(10):
                readfile = open('dataEpoch//Truss_power_' + str(k) + '.txt', "r+")
                kedges = eval(readfile.readline())
                subg = nx.Graph()
                subg.add_edges_from(kedges)
                print(len(subg))
                print(k)
                ansG = subg
                aved = 0
                denominator = 0
                X = set(random.sample(list(subg.nodes()), querysize))
                finalsizestep = len(subg)
                for count in range(7):
                    red = []
                    d = 0
                    ans, anssize, d = MinimalSubgraph(copy.deepcopy(subg), k, red, d, X)
                    print("d=", d)
                    denominator += 1
                    aved += d
                    if len(ans) < len(ansG):
                        del ansG
                        ansG = ans
                        gc.collect()
                    finalsizestep = min(finalsizestep, anssize)
                    if anssize == k + 1:
                        break
                finalsize += finalsizestep
                finald += aved / denominator
                density += nx.density(ansG)

            endtime = time.time()
            print("k=", k)
            print("querysize=", querysize)
            print("size=", finalsize / 10)
            print("d=", finald / 10)
            print("density", density / 10)
            print("ave time=", (endtime - starttime) / 10)
            print("=====================")
