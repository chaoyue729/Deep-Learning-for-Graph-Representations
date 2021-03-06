from matplotlib import pyplot as plt
from sklearn.cluster import SpectralClustering as SC
import os
import numpy as np
import pickle
file_name='output'

def get_embeddings(file_name):
	f=open(file_name)
	s=f.readlines()
	s=[x.strip() for x in s]
	s=[row.split(" ") for row in s]
	label=[]
	data,t=[],[]
	for row in s[1:]:
		label.append(int(row[0]))
		t=[]
		for element in row[1:]:
			t.append(float(element))
		data.append(t)
	print np.array(data).shape,file_name
	return label,np.array(data)

def plot_output(file_name,count=None,image=None):
	label,data=get_embeddings(file_name)
	plt.scatter(data[:,0],data[:,1])
	plt.show()

def build_model(file_name):
	label,data=get_embeddings(file_name)
	print data.shape
	n_c = 8
	clf=SC(n_clusters=n_c)
	#temp=np.transpose(data)
	output=clf.fit_predict(data)
	s=open("color",'w')
	m={0:'+',1:'o',2:'^',3:'x',4:'D',5:'*',6:'>',7:'v'}
	c=['r','b','g','c','m','y','k','#eeefff']
	pickle.dump(output,s)
	for x in xrange(n_c):
		plt.scatter(data[:,0][output==x],data[:,1][output==x],marker=m[x],s=45,label='Class %s' %x,c=c[x])
	plt.legend(loc='upper left')
	plt.show()
	print "here"
	return output,np.array(label),data

def plot_traj_image(filename,data):
	output,label,_=build_model(filename)
	c=['r','b','g','c','m','y','k','#eeefff']
	m={0:'+',1:'o',2:'^',3:'x',4:'D',5:'*',6:'>',7:'v'}
	done=[]
	for l in set(output):
		index_of_data=label[output==l]
		for element in index_of_data:
			val=data[element]
			t=len(val)
			x,y=val[0:t/2],val[t/2:]
			if l in done:
				plt.scatter(x,y,marker=m[l],s=50,c=c[l])
			else:
				done.append(l)
				plt.scatter(x,y,marker=m[l],s=50,label='Class %s' %l,c=c[l])
	plt.legend(loc='upper left')
	plt.show()
