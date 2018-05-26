# coding: utf-8

import urllib2
from urllib2 import urlopen as uReq
from bs4 import BeautifulSoup as soup
import re
from util import *
import nltk
import numpy as np
from sklearn.cluster import DBSCAN,KMeans
from sklearn.cluster import AgglomerativeClustering
import pandas as pd


print 'Ingrese busqueda...'
question = raw_input()
questions = re.split(r'[^\w\s\á\ó\í\é\ú]', question, re.U|re.I)
quest = ' '
for q in questions:
    if q != '':
        quest += q

formal_question = quest.replace(' ','+')
print '\nBuscando',quest,'...\n'
text = nltk.tokenize.word_tokenize(quest)
my_url = 'https://www.google.ru/search?q='+formal_question
print my_url



req = urllib2.Request(my_url, headers={'User-Agent' : "Magic Browser"}) 
con = urllib2.urlopen(req)
page_html = con.read()

page_soup = soup(page_html, "html.parser")

containers = page_soup.findAll("div", {'class':'g'})

answers = []
for container in containers:
    if 'href' in str(container):
        link = container.a['href'].split('&sa=')[0].split('/url?q=')
        if (len(link)>1) and (str(link).find("youtube") == -1):
            if text[0].lower() == 'donde':
                answer = get_info_where(link[1])
            else:
                answer = get_info_who(link[1])
            answers.append(answer)
print 'Ready!'



word_chain = []
for answer in answers:
    if answer != None and answer != []:
        for sentence in answer:
            s = sentence.split()
            for word in s:
                w = word
                word_ = re.split(r'[\.|,|\;|\:]', w, re.U|re.I)[0]
                word_chain.append(word_.lower())



unique_words = list(set(word_chain))



X2 = []
sentences = []
for answer in answers:
    if answer != None:
        for sentence in answer:
            vector_ngram = np.zeros(len(unique_words))
            splitted = sentence.split()
            sentences.append(sentence)
            print sentence
            for word in splitted:
                w = word
                word_ = re.split(r'[\.|,|\;|\:]', w, re.U|re.I)[0]
                index = list(unique_words).index(word_.lower())
                vector_ngram[index] = 1
            X2.append(vector_ngram)

model = AgglomerativeClustering(linkage='complete',
                                affinity='cosine',
                                n_clusters=4).fit(X2)
labels = model.labels_
labels_u = np.unique(labels )



all_clusters = []
for k in range(0,len(labels_u)):
    print'label:',k
    partial_cluster = []
    for i,(label) in enumerate(labels):
        if label == k:
            partial_cluster.append(sentences[i])
            print sentences[i]
    all_clusters.append(partial_cluster)        
    print '----'



final_answer = []
for sentence in all_clusters:
    if sentence[0] not in final_answer:
        final_answer.append(sentence[0])
                

if text[0].lower() == 'donde':
	df = pd.read_csv('paises.csv')
	countries = df['Pais'].str.lower()
	a = np.array(countries)
	#print a
else:
	df = pd.read_csv('profesiones.csv')
	profesions = df['Profesion'].str.lower()
	a = np.array(profesions)

app = []
for i,(answer) in enumerate(final_answer[0:5]):
    item = str(i+1)+')'
    print item,answer
    answer_splitted = answer.split()
    count = 0
    for word in answer_splitted:
        word_ = re.split(r'[\.|,|\;|\:]', word, re.U|re.I)[0]
        if word_ in str(a):
            #print word_
            count+=1
    app.append(count)

print app