from networkx.algorithms import bipartite 
# from itertools import combinations as cb

import networkx as nx 
import matplotlib.pyplot as plt 
import os
import ast
import sys
reload(sys)
sys.setdefaultencoding('utf8')


def returnIndAuth(paperData):

	line = paperData
	i = line[2].split('"')
	index = 0

	IndianAuths = []
	for j in i:

		if 'India' in j:

			IndianAuths.append(ast.literal_eval(i[index])[0].encode('utf-8'))

		index += 1


	return IndianAuths


def return_uid_as_node(authname):

	id = ''
	file1 = open('IndAuth_uid.csv','rb+')
	auth_id = file1.readlines()
	auth_id = map(lambda x: x.strip(), auth_id)

	auth_id = map(lambda x: x.split(','),auth_id)

	for i in auth_id:

		if authname == i[0]:

			id = i[1]
			break

	return id

