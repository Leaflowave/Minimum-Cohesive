import random
import time
import networkx as nx
import copy
from k_core import Allkcore

#sys.setrecursionlimit(1000000)
def MinimalSubgraph(G,k,red,d,X,count=None):
    ansg=G
    step=0
    anssize = len(ansg)
    while step<5 and len(set(ansg.nodes())-set(red)-set(X))>0:
        anssize = len(ansg)
        #print(anssize)
        g = copy.deepcopy(ansg)
        if count is None: count=max(len(g)-2*k,1)
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
        # g1= copy.deepcopy(g)
        # g.remove_node(v)
        g.remove_nodes_from(S)

        # print(count)

        vccs=FindkcoreSubgraph(ansg,g,k,X)
        # print(vccs)
        # print("len of vccs:", len(vccs))
        if len(vccs)>=1:
            step=0
            for vcc in vccs:
                # print("size of vcc:",len(vcc))
                # print(v)
                if len(set(X)-set(vcc))>0:
                    continue
                subg=nx.Graph(nx.subgraph(ansg,vcc))
                if count > 1:
                    d += count
                if count==1:
                    d+=1
                # print("next")
                ansg=subg
                # count=count
                break
                #return MinimalSubgraph(subg,k,red,d,X,count*2)
                # if subanssize<anssize:
                #     anssize=subanssize
                #     ansg=subans
        else:
            if count>1:
                for i in range(count):
                    red.pop()
            else:
                step+=1
            count=max(count//2,1)

    return ansg,anssize,d

def FindkcoreSubgraph(og,g,k,X):
    #import time
    #start=time.time()
    components = Allkcore(g,k) #,list(nx.node_boundary(og, set(og.nodes())-set(g.nodes())))
    #print(time.time()-start)
    ans=[]
    for c in components:
        if len(set(X)-set(c))==0:
            ans.append(c)
    return ans


if __name__ == '__main__':

    # geng=nx.karate_club_graph()
    # geng=ns.dolphins()
    # geng=ns.CollegeMsgNetwork()
    # geng=ns.election_Data()
    # geng=ns.MySmall()
    # geng=ns.Email_eucore()
    # geng=ns.facebook_combined()
    # geng=ns.USpowergrid_n4941()
    # geng=ns.USairport500()
    # geng=ns.USairport_2010()
    # geng=ns.celegans_n306()
    # geng=ns.escorts()
    # geng=ns.primarySchool()
    # geng=ns.highschool()
    # geng=nx.karate_club_graph()
    #geng=ns.advogado()
    # geng=ns.zacharyclub()

    # geng = nx.read_edgelist('dataEpoch/L1Anonymized.txt')
    # geng.remove_edges_from(nx.selfloop_edges(geng))
    # k=3
    #geng.remove_edges_from(nx.selfloop_edges(geng))
    #largest_cc = max(nx.connected_components(geng), key=len)
    #g = nx.Graph()
    #edges = geng.edges()
    #g.add_edges_from([(str(e[0]), str(e[1])) for e in edges])

    starttime = time.time()
    finalsize = 0
    density=0
    finald=0

    import math
    for _ in range(100):
        k = random.choice([5,10,15,20,25])
        querysize = random.choice([2, 4, 8, 16, 32])
        readfile=open('dataEpoch//advogado_' + str(k) + 'core.txt',"r+")
        kedges = eval(readfile.readline())
        subg=nx.Graph()
        subg.add_edges_from(kedges)
        print(len(subg))
        ansG=subg
        aved=0
        denominator=0
        X = set(random.sample(list(subg.nodes()), querysize))
        finalsizestep=len(subg)
        for count in range(int(math.log(len(subg)))):
            red =[]
            d=0
            ans, anssize,d = MinimalSubgraph(copy.deepcopy(subg), k, red,d,X)
            print("d=",d)
            denominator+=1
            aved+=d
            if len(ans)<len(ansG):
                ansG=ans
            finalsizestep=min(finalsizestep,anssize)
            if anssize==k+1:
                break
        finalsize += finalsizestep
        finald+=aved/denominator
        density+=nx.density(ansG)

    endtime = time.time()
    print("size=", finalsize/100)
    print("d=", finald/100)
    print("density",density/100)
    print("ave time=",(endtime-starttime)/100)
    print("=====================")
