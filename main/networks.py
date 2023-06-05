import networkx as nx
import linecache

""" this file read the graphs.
"""
def read_graph(path,separator,flagInt=True):
    edges=set()
    readfile=open(path,'r')
    temp=readfile.readline()
    while temp:
        estr=temp.split(separator)
        if flagInt:
            edge = (str(eval(estr[0])), str(eval(estr[1])))
        else:
            edge = (str(estr[0]), str(estr[1]))
        edges.add(edge)
        temp=readfile.readline()
    G=nx.Graph()
    G.add_edges_from(edges)
    return G
