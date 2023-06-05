import networkx as nx
import gc

if __name__ == '__main__':

    namestr = "dataEpoch//Truss_power_"
    for k in [4,8,12,16,20]:

        # read a list of edges ([edge1,edge2,...]) as input graph
        #readfile = open('dataEpoch//power_' + str(k) + 'core.txt', "r+")
        #kedges = eval(readfile.readline())
        #subg = nx.Graph()
        #subg.add_edges_from(kedges)

        # read an edgelist (each line represent an edge)
        subg=nx.read_edgelist('dataEpoch//power_' + str(k) + 'core.txt')
        subg.remove_edges_from(nx.selfloop_edges(subg))
        print(len(subg),nx.number_of_edges(subg))

        with open(namestr + str(k) + ".txt", 'w') as f:
            g_truss=nx.k_truss(subg,k)
            trusses = list(nx.connected_components(g_truss))
            if trusses is None or len(trusses) == 0:
                f.flush()
            print(k)
            maxtruss=max(trusses,key=len)
            maxG = nx.subgraph(g_truss,maxtruss)
            maxEdges = maxG.edges()
            del trusses, subg
            gc.collect()

            # save the edgelist of the k-ec
            f.write(str(maxEdges))
            f.write("\n")
            f.flush()
