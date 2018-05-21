import urllib2
from urllib2 import urlopen as uReq
from bs4 import BeautifulSoup as soup
import re
from util import *
import nltk
#nltk.download('punkt')
#nltk.download('averaged_perceptron_tagger')
#nltk.download('cess_esp')

print 'Ingrese busqueda...'
question = raw_input()
formal_question = question.replace(' ','+')
print '\nBuscando',question,'...'

text = nltk.tokenize.word_tokenize(question)
print text[0]



my_url = 'https://www.google.ru/search?q='+formal_question


req = urllib2.Request(my_url, headers={'User-Agent' : "Magic Browser"}) 
con = urllib2.urlopen(req)
page_html = con.read()

page_soup = soup(page_html, "html.parser")

containers = page_soup.findAll("div", {'class':'g'})


for container in containers:
	if 'href' in str(container):
		link = container.a['href'].split('&sa=')[0].split('/url?q=')
		if (len(link)>1) and (str(link).find("youtube") == -1):
			if text[0].lower() == 'donde':
				get_info_where(link[1])
			else:
				get_info_who(link[1])

