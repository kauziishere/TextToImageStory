import nltk, webbrowser
from nltk.tag.util import untag
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.tree import Tree
from googleapiclient.discovery import build
from bs4 import BeautifulSoup
import requests
import re
import urllib2
import os
import cookielib
import json

def get_soup(url,header):
    return BeautifulSoup(urllib2.urlopen(urllib2.Request(url,headers=header)),'html.parser')

def function(words,i,DirName):
	query = words# you can change the query for the image  here
	image_type="ActiOn"
	url="https://www.google.co.in/search?q="+query+"&source=lnms&tbm=isch"
	print url
	#add the directory for your image here
	DIR="Pictures" 
	header={'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"
	}
	soup = get_soup(url,header)
	ActualImages=[]# contains the link for Large original images, type of  image
	cnt = 0
	for a in soup.find_all("div",{"class":"rg_meta"}):
	    link , Type =json.loads(a.text)["ou"]  ,json.loads(a.text)["ity"]
	    if (cnt < 1):
	        ActualImages.append((link,Type))
	        cnt += 1

	print  "there are total" , len(ActualImages),"images"
	print('DIR: ' + str(DIR))
	if not os.path.exists(DIR):
	            os.mkdir(DIR)
	DIR = os.path.join(DIR, DirName)
	print 'Dir: ',str(DIR) 
	if not os.path.exists(DIR):
		os.mkdir(DIR)
###print images
	for i , (img , Type) in enumerate( ActualImages):
	    	try:
	        	req = urllib2.Request(img, headers={'User-Agent' : header})
	        	raw_img = urllib2.urlopen(req).read()

		        cntr = len([i for i in os.listdir(DIR) if image_type in i]) + 1
		        print cntr
		        if len(Type)==0:
		            f = open(os.path.join(DIR , image_type + "_"+ str(cntr)+"." +"jpg"), 'wb')
		       	else :
		            f = open(os.path.join(DIR , image_type + "_"+ str(cntr)+"."+Type), 'wb')
	
	
		        f.write(raw_img)
		        f.close()
		except Exception as e:
		        print "could not load : "+img
		        print e
name = str(raw_input())
fo = open(name,"r+")
tokenized = sent_tokenize(fo.read());
i = 0
for i in range(0,len(tokenized)):
	#print(tokenized[i])
	one = word_tokenize(tokenized[i])
	tagged = nltk.pos_tag(one)
	#print(tagged) 
	chunkgram = r"""Chunk: {<NN|NNS|NNP|NNPS|VB|VBD|VBG|VBN|VBP|VBZ>}""" 				#NN* - NNP + VB+ VBG
	chunkParser = nltk.RegexpParser(chunkgram)
	chunked = chunkParser.parse(tagged)
#	chunked.draw()
	flag = 1
	Dir_Name = name.split('.')
	for t in chunked.subtrees(filter = lambda x: x.label() == "Chunk"):
		extract = t.leaves()
		extract = untag(extract)
		for j in extract:
			if  flag== 1 :
				words = j
				flag = 0
			else:
				words = words + '+' + j
	print words
	function(words,i,str(Dir_Name[0]))
