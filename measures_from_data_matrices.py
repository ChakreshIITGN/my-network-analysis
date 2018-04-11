from __future__ import division
from numba import jit
import os
import networkx as nx
import json
import pandas as pd
import numpy as np


global node_list

Gr = nx.read_gexf('/home/chakresh/Dropbox/UoA_project/co_authorshipProjection/bip_2013_coAuth.gexf')
node_list = Gr.nodes()

node_list.sort()

N0 = len(node_list)

years = range(1970,1990)

@jit
def dij_pairs_m(N_n,M,dist):

    
    node_index = range(N_n)
    dij_pairs = []
    
    for i in node_index:

        s = i

        for t in node_index[i+1:]:

            if M[s][t] == dist:

                dij_pairs.append((s,t,dist))
    
    return dij_pairs

@jit
def non0_pairs_m(N_n,M):

    
    node_index = range(N_n)
    non0_pairs = []
    
    for i in node_index:

        s = i

        for t in node_index[i+1:]:
            
            val = M[s][t]
            if val >= 1:

                non0_pairs.append((s,t,val))
    
    return non0_pairs

@jit
def cij_pairs_m(N_n,M):

    node_index = range(N_n)
    cij_pairs = []
    
    for i in node_index:

        s = i

        for t in node_index[i+1:]:
            
            cin = M[s][t] 
            cout =  M[t][s]
            
            if cin + cout > 0:

                cij_pairs.append((s,t,cin,cout))
    
    return cij_pairs


for yr in years:


    df_dij = pd.read_csv('/home/chakresh/Dropbox/UoA_project/data_matrices_old/Dij_%s'%(str(yr)),compression='gzip',header=0,index_col=0)
    df_cij = pd.read_csv('/home/chakresh/Dropbox/UoA_project/data_matrices_old/Cij_%s'%(str(yr)),compression='gzip',header=0,index_col=0)


    df_dij_copy = df_dij
    df_cij_copy = df_cij

    D = df_dij_copy.values
    C = df_cij_copy.values

    pairs = cij_pairs_m(N0,C)

    new_pairs = []
    
    for i,j,k,l in pairs:

        # cin = C[i][j]
        # cout = C[j][i]

        # new_pairs.append((i,j,k,cin,cout))
        if D[i][j] == 0:

            new_pairs.append((i,j,k,l))

    
    f0 = open('/home/chakresh/zero_dij_nzcit_pairs/zero_pairs_%s.txt'%(str(yr)),'wb+')
    
    f0.write('source,target,dij,cin,cout\n')

    for i,j,k,l in new_pairs:
             
        f0.write('%d,%d,0,%d,%d\n'%(int(i),int(j),int(k),int(l)))
        
    f0.close()