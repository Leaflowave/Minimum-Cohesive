import collections

import networkx as nx
import MinCut_Sample
import copy
import gc
def min_node_cut(G, k, s, t, H=None):
    if H is None:
        H = MinCut_Sample.build_auxiliary_node_connectivity(G)
    mapping = H.graph.get("mapping", None)
    if G.has_edge(s, t) or G.has_edge(t, s):
        return None

    edge_cut = MinCut_Sample.minimum_st_edge_cut(H, f"{mapping[s]}B", f"{mapping[t]}A", auxiliary=H, cutoff=k)

    if edge_cut is None:
        cut = None
    else:
        node_cut = {H.nodes[node]["id"] for edge in edge_cut for node in edge}
        cut = node_cut - {s, t}
    if cut is not None and len(cut) < k and len(cut)>0:
        return cut
def read_cohesive_edges(file):
    readfile = open(file, "r+")
    edges = eval(readfile.readline())
    G=nx.Graph()
    G.add_edges_from(edges)
    return G
def min_edge_cut(G, k, s, t, H=None):
    if H is None:
        H = MinCut_Sample.build_auxiliary_edge_connectivity(G)
    cut = MinCut_Sample.minimum_st_edge_cut(H, s, t, auxiliary=H, cutoff=k)
    if cut is not None and len(cut) < k and len(cut)>0:
        return cut
def distance_neighbors(g,d,u):
    """
    find dist 2 neighbors of u
    :param g:
    :param d:
    :param u:
    :return:
    """
    S={u}
    level=[u]
    for _ in range(d):
        nextLevel=[]
        for v in level:
            nextLevel.extend(list(nx.neighbors(g,v)))
        S.update(nextLevel)
        level=nextLevel[:]
    return S
def setNeighbors(G,S):
    Nei=set()
    for v in S:
        Nei.update(set(nx.neighbors(G,v)))
    return Nei
def readGraph(filepath='ca-netscience.txt'):
    nodes = set()
    edges = set()

    readfile = open('dataEpoch//' + filepath, "r+")
    temp=readfile.readline()
    while temp:
        temp = temp.split(" ")
        temp1 = str(temp[0])
        temp2 = str(temp[1])
        edges.add((temp1, temp2))
        temp=readfile.readline()
    G = nx.Graph()
    G.add_edges_from(edges)
    return G

def FindEdgeCut(G,k,Nu,ccid,dependencyMap):
    g=copy.deepcopy(G)
    # degNu = dict(nx.degree(g, Nu))
    # Nu=sorted(Nu, key=lambda x: degNu[x])
    # if degNu[Nu[0]] < k:
    #     return set([(Nu[0],x) for x in nx.neighbors(g,Nu[0])])
    # By Lemma 1 of "Finding Maximal k-Edge-Connected Subgraphs from a Large Graph"


    sparseg=EdgeCertificate(g,k)
    print(len(g.edges())-len(sparseg.edges()))
    # for s in range(len(Nu)):
    flowg = MinCut_Sample.build_auxiliary_edge_connectivity(sparseg)
    curIds=set()
    scanned=set()
    unscanned=[Nu[0]]
    curIds.add(ccid[Nu[0]])
    cur=set()
    while len(unscanned)>0:
        cur.clear()
        for s in unscanned:
            scanned.add(s)
            for t in set(nx.neighbors(sparseg,s))-scanned:
                cur.add(t)
                # for t in range(len(Nu)-1,0,-1):
                # print("t", t)
                if ccid[t] in curIds:
                    continue
                cut = min_edge_cut(sparseg, k, s, t, flowg)
                if cut is not None and len(cut) < k:
                    print(s,t)
                    del sparseg
                    del flowg
                    gc.collect()
                    return cut
                curIds.add(ccid[t])
                if sparseg.has_edge(s,t):
                    dependencyMap.add_edge(s,t)

        unscanned=list(cur)[:]
    del sparseg,flowg
    gc.collect()
    return


def EdgeCertificate(G, k):
    # from networkx.algorithms.traversal.breadth_first_search import bfs_edges
    g = copy.deepcopy(G)
    E=set()
    unscanned=set(G.nodes())
    r={x:0 for x in G.nodes()}
    set_r=collections.defaultdict(set)
    set_r[0].update(unscanned)
    cur_max_r=0
    while len(unscanned)>0:
        while len(set_r[cur_max_r])==0:
            cur_max_r-=1
        x=set_r[cur_max_r].pop()
        unscanned.remove(x)
        for y in list(nx.neighbors(g,x)):
            set_r[r[y]].remove(y)
            r[y]+=1
            if r[y] < k + 1: E.add((x, y))
            if r[y]>cur_max_r: cur_max_r=r[y]
            set_r[r[y]].add(y)
            g.remove_edge(x,y)
    newg=nx.Graph()
    # newg.add_nodes_from(G.nodes())
    newg.add_edges_from(E)
    # print(len(newg))
    del set_r,r
    gc.collect()
    return newg

    # for i in range(k):
    #     components = list(nx.connected_components(g))
    #     sources = [component.pop() for component in components]
    #     edges = set()
    #     for source in sources:
    #         edges = edges.union(set(bfs_edges(g, source)))
    #     g.remove_edges_from(edges)
    # remove_edges = copy.deepcopy(g.edges)
    # g.add_edges_from(G.edges)
    # g.remove_edges_from(remove_edges)
    # return g


def update(ccid,dependencyMap):
    # ccid = collections.defaultdict(str)
    ccs = list(nx.connected_components(dependencyMap))

    for i in range(len(ccs)):
        cc = ccs[i]
        for v in cc:
            ccid[v] = str(i)
    return
def general_k_edge_subgraphs(g, k,dependencyMap=None,ccid=None):
    if k < 1:
        raise ValueError("k cannot be less than 1")
    # Node pruning optimization (incorporates early return)
    # find_ccs is either connected_components/strongly_connected_components
    eccs=[]
    # Quick return optimization
    G=copy.deepcopy(g)

    if dependencyMap is None:
        print("begin dependency")
        dependencyMap = nx.Graph()
        Nu=list(G.nodes())
        dependencyMap.add_nodes_from(Nu)
        for s in range(len(Nu)):
            for t in nx.neighbors(G,Nu[s]):
                if len(set(G.neighbors(Nu[s])).intersection(set(G.neighbors(t))))>=k:
                    # if len(set(nx.neighbors(G, Nu[s])).intersection(set(nx.neighbors(G, Nu[t])))) >= k:
                    dependencyMap.add_edge(Nu[s], t)
        ccid = dict()
        update(ccid, dependencyMap)
        print("dependency")
    # Intermediate results
    # Subdivide CCs in the intermediate results until they are k-conn
    candidates=list(nx.connected_components(G))
    while len(candidates)>0:
        oldcandidates=candidates[:]
        candidates.clear()
        for component in oldcandidates:
            if len(component)<k+1: continue
            print("component",len(component))
            print("candidate",len(candidates))
            G1=nx.Graph(nx.subgraph(G,component))
            # Find a global minimum cut
            cut_edges = FindEdgeCut(G1,k,Nu=list(component),ccid=ccid,dependencyMap=dependencyMap)
            # print(cut_edges)
            if cut_edges:print("cut",len(cut_edges))
            if cut_edges is not None and len(cut_edges) < k:
                # G1 is not k-edge-connected, so subdivide it
                G1.remove_edges_from(cut_edges)
                for edge in cut_edges:
                    if dependencyMap.has_edge(edge[0],edge[1]):
                        dependencyMap.remove_edge(edge[0],edge[1])
                update(ccid, dependencyMap)
                ccs=list(nx.connected_components(G1))
                if(len(ccs)==1): print(cut_edges)
                candidates.extend(ccs)
                del G1,cut_edges,component
                gc.collect()
                # for cc in list(nx.connected_components(G1)):
                #     if len(cc)<k+1: continue
                #     subg=nx.Graph(nx.subgraph(G1,cc))
                #     eccs.extend(general_k_edge_subgraphs(subg, k,dependencyMap,ccid))
                #     del subg
                #     gc.collect()
            else:
                eccs.append(list(component)[:])

    del G,dependencyMap,ccid,candidates
    gc.collect()
    return eccs

def dictGraph(filepath='ca-netscience.txt'):
    readfile = open('dataEpoch//' + filepath, "r+")

    # for _ in range(3): readfile.readline()
    temp = readfile.readline()
    # G = nx.Graph()
    g=collections.defaultdict(set)
    while temp:
        temp = temp.split(" ")
        temp1 = str(temp[0]).strip()
        print(temp[1])
        temp2 = str(temp[1]).strip()
        g[temp1].add(temp2)
        g[temp2].add(temp1)
        temp = readfile.readline()
        # G.add_edge(temp1, temp2)
    return g
if __name__ == '__main__':
    g=dictGraph()
    print(g)

    print(len(g))
