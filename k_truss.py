import networkx as nx
import gc

if __name__ == '__main__':

    namestr = "dataEpoch//Truss_Wiki_"
    for k in [10, 20, 30, 40, 50]:
        # for k in range(2,8,2):
        # readfile = open('dataEpoch//Wiki_' + str(k) + 'core.txt', "r+")
        # kedges = eval(readfile.readline())
        # subg = nx.Graph()
        # subg.add_edges_from(kedges)
        subg=nx.read_edgelist('dataEpoch//Wiki_' + str(k) + 'core.txt',)
        subg.remove_edges_from(nx.selfloop_edges(subg))
        print(len(subg),nx.number_of_edges(subg))

        with open(namestr + str(k) + ".txt", 'a+') as f:
            vcc=nx.k_truss(subg,k)
            print(len(vcc))
            if vcc is None or len(vcc) == 0:
                f.flush()
            # flag=False
            print(k)
            # print(len(vcc))

            maxG = vcc
            maxEdges = maxG.edges()
            # print(len(vcc))
            del vcc, subg
            gc.collect()
            f.write(str(maxEdges))
            f.write("\n")
            f.flush()
