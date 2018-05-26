# -*- coding: utf-8 -*-
import urllib2
from urllib2 import urlopen as uReq
from bs4 import BeautifulSoup as soup
import re
from nltk import ngrams
import sys
import unicodedata

def get_info_who(link):
	print 'Reading ',link
	req = urllib2.Request(str(link), headers={'User-Agent' : "Magic Browser"}) 
	try:
		con = urllib2.urlopen(req)

	except urllib2.HTTPError, e:
		print e.code
		print e.msg
		return
	
	
	try:
	    page_html = con.read()
	except SocketError as e:
	    if e.errno != errno.ECONNRESET:
	        raise # Not error we are looking for
	    return

	page_soup = soup(page_html, "html.parser")

	containers = page_soup.findAll('p')
	counter = 1
	answers = []
	for i,(c) in enumerate(containers):
		paragraph = c.text
		find = re.search(r"\b(es|fue)\s(un|una)[\w\s ,]+[\b|\.]",paragraph, re.U|re.I)
		if find:
			sentence = find.group()
			#print 'Answer ',str(counter),':',sentence
			counter+=1
			if sentence != None:
				answers.append(sentence)
	print '-----------------------------------------------------------------------'
	return answers			
				
def get_info_where(link):
	print 'Reading ',link
	req = urllib2.Request(str(link), headers={'User-Agent' : "Magic Browser"}) 
	try:
		con = urllib2.urlopen(req)
	except urllib2.HTTPError, e:
		print e.code
		print e.msg
		return
	
	page_html = con.read()

	page_soup = soup(page_html, "html.parser")

	containers = page_soup.findAll('p')
	counter = 1
	answers = []
	for i,(c) in enumerate(containers):
		paragraph = c.text
		find = re.search(r"\b(esta|estaba|ubicada|ubicado|ubica|localizada|localizado)\s[\w\s ,]+[\b|\.]",paragraph, re.U)
		if find:
			sentence = find.group()
			#print 'Answer ',str(counter),':',sentence
			counter+=1
			answers.append(sentence)
	print '-----------------------------------------------------------------------'	
	return answers

def get_n_grams(answers, n):
	all_ngrams = []
	for answer in answers:
		if answer == None:
			print answer
		else:
			for sentence in answer:
				ngrams_ = ngrams(sentence.split(), n)
				all_ngrams.append(ngrams_)
	
	return all_ngrams

def print_unicode(text):
    try:
        text = unicode(text.decode('string-escape'), 'utf-8')
    except:
        text = text.decode('unicode-escape')
    return text
