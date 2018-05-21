import urllib2
from urllib2 import urlopen as uReq
from bs4 import BeautifulSoup as soup
import re
from nltk import ngrams

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

	for i,(c) in enumerate(containers[0:5]):
		paragraph = c.text
		find = re.search(r"\b(es|fue)\s[\w\s ,]+[\b|\.]",paragraph, re.U)
		if find:
			sentence = find.group()
			print 'Answer ',str(i),':',sentence
				
				
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

	for i,(c) in enumerate(containers[0:5]):
		paragraph = c.text
		find = re.search(r"\b(se|esta|estaba)*(ubicada|ubicado|en|localizada|localizado)\s[\w\s ,]+[\b|\.]",paragraph, re.U)
		if find:
			sentence = find.group()
			print 'Answer ',str(i),':',sentence
				