import gc
import networkx as nx
from Chang1 import KECC
""" this procedure preprocess the input graph, outputs and stores all maximal k-EC subgraphs.
"""

if __name__ == '__main__':
    #use the Power dataset as an example.
    namestr="dataEpoch//EC_power_"
    for k in [4,8,12,16,20]:
        with open(namestr + str(k) + ".txt", 'w') as f:
            #read a k-core graph
            
            #read a list of edges ([edge1,edge2,...]) as input graph
            # readfile = open('dataEpoch//power_' + str(k) + 'core.txt', "r+")
            # kedges = eval(readfile.readline())
            # subg = nx.Graph()
            # subg.add_edges_from(kedges)
            
            #read an edgelist (each line represent an edge)
            subg = nx.read_edgelist("dataEpoch//power_"+str(k)+"core.txt", nodetype=str)
            print("========")
            print(len(subg))
            eccs=list(KECC(subg, k,set()))
            print("max EC:",len(max(eccs, key=len)))
            
            #exclude all isolated nodes
            ecc=[x for x in eccs if len(x)>2]
            # C = nx.k_core(G, k)
            print(k)
            if ecc is None or len(ecc) == 0:
                f.flush()
                break
            
            maxecc = max(eccs, key=len)
            maxG = subg.subgraph(maxecc)
            maxEdges = maxG.edges()
            print(len(maxG))
            
            #save the edgelist of the k-ec
            gc.collect()
            f.write(str(maxEdges))
            f.write("\n")
            f.flush()

