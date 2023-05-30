import gc
from collections import defaultdict
import networkx as nx
from Chang1 import KECC
import networks
import tools
if __name__ == '__main__':
    # a=Graph()
    # import networks as ns
    # import matplotlib.pyplot as plt
    # # a.convert2graph(nx.karate_club_graph())
    # a.convert2graph(ns.IsolatedGraph())
    # # nx.draw(nx.karate_club_graph())
    # # plt.show()
    # # a.readgraph('dataEpoch//a.txt')
    # g=a.PrintKCores(1)
    # print(len(list(nx.connected_components(g))))
    # print(len(g))
    # nx.draw(g)
    # plt.show()
    # print(g.edges())
    # k=2
    # G=nx.erdos_renyi_graph(100,0.2)
    # G=networks.IsolatedGraph()
    # geng=networks.advogado()
    # geng=nx.karate_club_graph()
    #
    # geng.remove_edges_from(nx.selfloop_edges(geng))
    # largest_cc = max(nx.connected_components(geng), key=len)
    # G = nx.Graph()
    # edges = geng.edges()
    # G.add_edges_from([(str(e[0]), str(e[1])) for e in edges])
    #
    # import matplotlib.pyplot as plt
    # nx.draw(G,with_labels=True)
    # plt.show()

    namestr="dataEpoch//test_L2"

    # allkcore=Allkcore(G,k)
    # print(allkcore)
    # if len(allkcore)>0:    print(len(allkcore[0]))

    for k in [3,5,7,9,11]:
        with open(namestr + str(k) + ".txt", 'a+') as f:
            # print(k)
            # print(len(G))
            #
            # readfile = open('dataEpoch//CondMat_' + str(k) + 'core.txt', "r+")
            # kedges = eval(readfile.readline())
            # subg = nx.Graph()
            # subg.add_edges_from(kedges)dblp-reid
            # subg=nx.read_edgelist("dataEpoch//blog_"+str(k)+'core.txt',nodetype=str)
            subg = nx.read_edgelist("dataEpoch//p2p-Gnutella31.txt", nodetype=str)
            print("========")
            print(len(subg))
            # vcc = list(nx.k_edge_subgraphs(G, k))
            # print(len(max(vcc, key=len)))
            # print('39763' in subg)
            vcc=list(KECC(subg, k,set()))
            print(len(max(vcc, key=len)))

            vcc=[x for x in vcc if len(x)>2]
            # C = nx.k_core(G, k)
            print(k)
            # print(len(vcc))
            # print(set(C.nodes()))
            # print(len(C))
            # print([len(x) for x in vcc])
            if vcc is None or len(vcc) == 0:
                f.flush()
                break


            maxvcc = max(vcc, key=len)
            maxG = subg.subgraph(maxvcc)
            maxEdges = maxG.edges()
            print(len(maxG))
            # del vcc, kedges,subg
            gc.collect()
            f.write(str(maxEdges))
            f.write("\n")
            f.flush()

