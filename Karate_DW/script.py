#Deepwalk - Suriya - 22/07/16
from matplotlib import pyplot as plt
from collections import defaultdict
from gensim.models import Word2Vec
from plot import plot_output
import random
import numpy as np
from fileinput import filename

number_of_walks_per_node=10
rand=random.Random(0)
#filename="youtube_input.edgelist"
#filename="combined.csv"
filename="input"
graph=defaultdict(list)
embedding_size=2
im_threshold=1

def random_walk(graph,start,rand=random.Random(0),length=40,restart=0):
    walk=[start]
    node=start
    while len(walk)<length:
        if len(graph[node])>0:
            alpha=random.random()
            if alpha >=restart:
                next_node=rand.choice(graph[node])
                walk.append(next_node)
                node=next_node
            else:
                #next_node=rand.choice(graph[start])
                walk.append(start)
                node=start
        else:
            break
    return walk

def read_adj_matrix(file_name,graph,neighbourhood_propagation=False):
    filename=open(file_name)
    count=1
    for row in filename:
        row_processed=row.split(" ")
        for index,element in enumerate(row_processed):
            if element=='1':
                graph[count].append(index+1)
        count=count+1

    if neighbourhood_propagation:
        temp_graph=defaultdict(list)
        nodes=list(graph.keys())
        for node in nodes:
            adj_list=graph[node]
            for element in adj_list:
                if element not in temp_graph[node]:
                    temp_graph[node].append(element)
                next_adj_list=graph[element]
                for next_adj_list_element in next_adj_list:
                    if next_adj_list_element not in temp_graph[node]:
                        temp_graph[node].append(next_adj_list_element)
                
        for element in temp_graph.keys():
            #temp_graph[element].sort()
            graph[element]=temp_graph[element]
    print graph

def read_edge_list(file_name,graph,undirected=True):
    filename=open(file_name)
    for row in filename:
        row_processed=map(int,row.strip().split(" "))
        graph[row_processed[0]].append(row_processed[1])
        if undirected:
            graph[row_processed[1]].append(row_processed[0])

def read_adj_file(file_name,graph,neighbourhood_propagation=False):
    filename=open(file_name)
    for row in filename:
        row_processed=row.strip().split(" ",1)
        adj_list=row_processed[1].split()
        #adj_list=row_processed[1]
        adj_list=map(int,adj_list)
        for element in adj_list:
            graph[int(row_processed[0])].append(element)
            #graph[row_processed[0]].append(element)
    if neighbourhood_propagation:
        temp_graph=defaultdict(list)
        nodes=list(graph.keys())
        for node in nodes:
            adj_list=graph[node]
            for element in adj_list:
                if element not in temp_graph[node]:
                    temp_graph[node].append(element)
                next_adj_list=graph[element]
                for next_adj_list_element in next_adj_list:
                    if next_adj_list_element not in temp_graph[node]:
                        temp_graph[node].append(next_adj_list_element)
                
        for element in temp_graph.keys():
            #temp_graph[element].sort()
            graph[element]=temp_graph[element]

def build_data_matrix(graph,number_of_walks_per_node=10,rand=random.Random(0),restart=0):
    data=[]
    nodes=graph.keys()
    for _ in xrange(number_of_walks_per_node):
        rand.shuffle(nodes)
        for vertex in nodes:
            walk=random_walk(graph=graph,start=vertex,rand=rand,restart=restart)
            data.append(walk)
    return data

def build_word2vec_model(data,embedding_size=2,save=True):
    model=Word2Vec(data,min_count=0,size=embedding_size)
    if save:
        model.save_word2vec_format('output')
    return model 

def im_to_graph(im,graph):
    im=im.ravel()
    for i,value_i in enumerate(im):
        for j,value_j in enumerate(im): 
            if abs(value_i - value_j) < im_threshold and i!=j:
                graph[i+1].append(j+1)

#read_adj_file(file_name=filename,graph=graph,neighbourhood_propagation=False)
read_adj_file(filename, graph)
#print "finished building the graph",len(graph.keys())
data=build_data_matrix(graph,number_of_walks_per_node,rand=rand)
import pickle
f = open('adj','w')
pickle.dump(data,f)
f.close()
#print "finished building the data matrix now going for training",len(data),len(data[0])
for embedding_size in [2,4,8,16,32,64,128,256,512,1024]:
	build_word2vec_model(data,embedding_size=embedding_size,save=True)
#	print "training over now plotting"
	print "Embedding_size =" , embedding_size
	plot_output('output')
#	break

"""
for count in xrange(0,101):
    data=build_data_matrix(graph,number_of_walks_per_node,rand=rand,restart=count/100.0)
    #print "finished building the data matrix now going for training",len(data),len(data[0])
    build_word2vec_model(data,embedding_size=embedding_size,save=True)
    #print "training over now plotting"
    plot_output('output',count)
    print count
"""
"""
for count in xrange(0,101):
    data=build_data_matrix(graph,number_of_walks_per_node,rand=rand,restart=(count/100.0))
    build_word2vec_model(data,embedding_size=embedding_size,save=True)
    plot_output('output',count)
"""
"""
im=plt.imread('im.png')
im_to_graph(im, graph)
data=build_data_matrix(graph,number_of_walks_per_node,rand=rand)
build_word2vec_model(data,embedding_size=embedding_size,save=True)
plot_output('output',image=im)
"""
"""
A=adjacency_matrix(im,connectivity=4)
np.savetxt('test', A, fmt="%d")
read_adj_matrix('test', graph)
data=build_data_matrix(graph,number_of_walks_per_node,rand=rand)
build_word2vec_model(data,embedding_size=embedding_size,save=True)
plot_output('output',image=im)
"""
