
# coding: utf-8

from __future__ import division
from numba import jit
from networkx.algorithms import bipartite

import os
import networkx as nx
import json
import pandas as pd
import numpy as np
import multiprocessing

bip_path = '/Users/csingh/Dropbox/UoA_project/bipartite_graphs/'
cit_path = '/Users/csingh/Dropbox/UoA_project/citation_graphs/'

bip_graphs = os.listdir(bip_path)
cit_graphs = os.listdir(cit_path)

bip_graphs = bip_graphs[1:]  # only for imac comment in ubuntu
cit_graphs = cit_graphs[1:]  # only for imac comment in ubuntu 

bip_graphs.sort()
cit_graphs.sort()


# print bip_graphs
# print cit_graphs

# print len(bip_graphs)

######## creating the Base Matrix by extracting ordered nodes from the last co-authorship graph for 2013 #######


Gr = nx.read_gexf('/Users/csingh/Dropbox/UoA_project/co_authorshipProjection/bip_2013_coAuth.gexf')
node_list = list(Gr.nodes())
node_list.sort()
N0 = len(node_list)

global DF_Dij, DF_Cij, ts

ts = 0

DF_Dij = pd.DataFrame(np.zeros([N0,N0]),index=node_list,columns=node_list)
DF_Cij = pd.DataFrame(np.zeros([N0,N0]),index=node_list,columns=node_list)

# DF_Dij = DF_Dij.values
# DF_Cij = DF_Cij.values

# Definition of our measures :
# 
# 1. D = d if there is a path of length d between i and j,  0 otherwise
# 2. C = a directed asymmetric matrix where Cij is citations from j to i(incoming) and vice versa (Newman's book convention. Easy Mathematically)




##### Functions needed for the code ###########

def index_of_nodes(node_list, ParentList=node_list):
    
    indexList = []
    
    for i in node_list:
        
        indexList.append(ParentList.index(i))
    
    return indexList

def edge_crossing(G, G_r, setA, setB,NX=nx):
    
    '''
        The order of choosing i and j will effect the count of incoming and outgoing citations
    '''
    
    out_cite = 0
    in_cite = 0
    
    for i in setA:

        g_nbrs = list(NX.neighbors(G,i))
        gr_nbrs = list(NX.neighbors(G_r,i))
        
        for j in setB:
            
            if i in G.nodes() and j in  g_nbrs:
                                
                out_cite += 1
                
            if i in G_r.nodes() and j in gr_nbrs:
                
                in_cite += 1
        
    return out_cite, in_cite

def loop_through_j(j,bottom_nodes,bipGrph,citGrph,citRGrph,bipProj,NX=nx,Dist_dataframe,Cit_dataframe):

    D_df,C_df = Dist_dataframe,Cit_dataframe

    btm_nodes = bottom_nodes
    s = btm_nodes[j]
    seta = list(NX.neighbors(bipGrph,s))
    
    for k in range(j+1,N):

        t = btm_nodes[k]
        setb = list(NX.neighbors(bipGrph,t))
        
        c_out,c_in = edge_crossing(citGrph,citRGrph,seta,setb) 
        
        C_df.loc[s,t] = c_in
        C_df.loc[t,s] = c_out
        
        if NX.has_path(bipProj,s,t) == True :
            
            path_length = NX.shortest_path_length(bipProj,s,t,weight='True')
            D_df.loc[s,t] = path_length
            D_df.loc[t,s] = path_length

    return D_df,C_df


def loop_through_pairs(bottom_nodes,bipGrph,citGrph,citRGrph,bipProj,NX=nx,Dist_dataframe=DF_Dij,Cit_dataframe=DF_Cij):

    df_Dij = Dist_dataframe
    df_Cij = Cit_dataframe

    B_nodes = bottom_nodes

    N = len(B_nodes)

    node_index = range(N)

    pool = multiprocessing.Pool(processes=4)

    df_Dij,df_Cij = pool.map(loop_through_j(j,B_nodes,bipGrph,citGrph,citRGrph,bipProj,df_Dij,df_Cij),node_index)

    return df_Dij, df_Cij



def calculate_data_matrices(time_step,NX=nx):

    B = NX.read_gexf('/Users/csingh/Dropbox/UoA_project/bipartite_graphs/%s'%(bip_graphs[time_step]))
    C = NX.read_gexf('/Users/csingh/Dropbox/UoA_project/citation_graphs/%s'%(cit_graphs[time_step]))

    Cr = NX.DiGraph.reverse(C,copy=True)

    t_nodes = {n for n, d in B.nodes(data=True) if d['bipartite']==0}
    b_nodes = set(B) - t_nodes

    B_b = bipartite.collaboration_weighted_projected_graph(B, b_nodes)
    b_nodes = list(b_nodes)
    b_nodes.sort()

    df_Dij, df_Cij = loop_through_pairs(b_nodes,B,C,Cr,B_b)


    return df_Dij, df_Cij




def save_data_matrices(time_step):

    df_Dij,df_Cij = calculate_data_matrices(time_step)

    df_Dij.to_csv('/Users/csingh/Dropbox/UoA_project/data_matrices/Dij_%s'%(str(time_step + 1970)),compression='gzip')
    df_Cij.to_csv('/Users/csingh/Dropbox/UoA_project/data_matrices/Cij_%s'%(str(time_step + 1970)),compression='gzip')

    return None



save_data_matrices(ts)