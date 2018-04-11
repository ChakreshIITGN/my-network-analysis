
# coding: utf-8

# In[27]:


N = 4
A = range(N)


# In[28]:


for j in range(N):
    s = A[j]
    for k in range(j+1,N):
        t = A[k]
        print s,t


# In[29]:


import networkx as nx 
from networkx.algorithms import bipartite


# In[69]:


Gp = nx.read_gexf('/Users/csingh/Dropbox/UoA_project/bipartite_graphs/bip_2013.gexf')
G = nx.read_gexf('/Users/csingh/Dropbox/UoA_project/bipartite_graphs/bip_1980.gexf')


# In[31]:


t_nodes = {n for n, d in G.nodes(data=True) if d['bipartite']==0}
b_nodes = set(G) - t_nodes
    
B_b = bipartite.projected_graph(G, b_nodes)


# In[32]:


len(B_b)


# In[33]:


# pairs = nx.all_pairs_dijkstra_path_length(B_b,cutoff=1)


# In[34]:


get_ipython().run_cell_magic(u'time', u'', u'N = len(b_nodes)\nb_nodes = list(b_nodes)\nc=0\nfor i in range(N):\n    \n    s = b_nodes[i]\n        \n    for j in range(i+1,N):\n\n        t = b_nodes[j]\n        \n        try:\n            distance = nx.shortest_path_length(B_b,s,t)\n            if distance == 1:\n            \n                c+=1\n        \n        except:\n            continue')


# In[35]:


c


# In[18]:


get_ipython().magic(u'load_ext Cython')


# In[48]:


def loop_n(n,N=N,bnodes=b_nodes,G=B_b,nx=nx):
    
    s = b_nodes[n]
    cn=0
    for j in range(n+1,N):

        t = b_nodes[j]
        
        try:
            distance = nx.shortest_path_length(B_b,s,t)
            if distance == 1:
            
                cn+=1
        
        except:
            continue
    
    return cn
    
    


# In[50]:


loop_n(0)


# In[51]:


import multiprocessing
Nodes = range(N)
pool = multiprocessing.Pool(processes=4)


# In[52]:


get_ipython().run_cell_magic(u'time', u'', u'cn=0\ncn = pool.map(loop_n,Nodes)\npool.close()')


# In[53]:


sum(cn)


# In[56]:


import numpy as np
A = np.zeros((100,100))
B = np.zeros((100,100))


# In[57]:


A[1][10] = 4
B[1][10] = 5


# In[58]:


C = A+B


# In[59]:


C[1][10]


# In[60]:


D = [A,B]


# In[61]:


E = sum(D)


# In[62]:


E[1][10]


# In[63]:


F = []

for i in range(43):
    
    A = np.zeros((8084,8084))
    A[1][100] = 2
    F.append(A)


# In[65]:


get_ipython().run_cell_magic(u'time', u'', u'D = sum(F)')


# In[66]:


D[1][100]


# In[67]:


def index_of_node(node_list, ParentList):
    
    indexList = []
    
    for i in node_list:
        
        indexList.append(ParentList.index(i))
    
    return indexList


# In[71]:


len(b_nodes)


# In[82]:


Pt_nodes = {n for n, d in Gp.nodes(data=True) if d['bipartite']==0}
Pb_nodes = set(Gp) - Pt_nodes
    
B_b = bipartite.projected_graph(Gp, Pb_nodes)

Pb_nodes = list(Pb_nodes)


# In[110]:


get_ipython().run_cell_magic(u'time', u'', u'indexlist = index_of_node(b_nodes,Pb_nodes)')


# In[111]:


print len(indexlist), len(Pb_nodes)

# print indexlist

