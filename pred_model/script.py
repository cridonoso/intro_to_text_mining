# -*- coding: utf-8 -*-
import re
from nltk.tokenize import sent_tokenize, word_tokenize
import numpy as np
from Bio import Entrez

def search(query):
    Entrez.email = 'your.email@example.com'
    handle = Entrez.esearch(db='pubmed',
                            sort='relevance',
                            retmax='20',
                            retmode='xml',
                            term=query)
    results = Entrez.read(handle)
    return results

def print_abstract(pmid):
    handle = Entrez.efetch(db='pubmed', id=pmid, retmode='xml', rettype='abstract')
    return handle.read()

query = 'cancer'
idList = search(query)['IdList']
for pid in idList[0:3]:
    print '-'*60
    xml = str(print_abstract(pid))
    find = re.findall(r"<AbstractText[>]?.*</AbstractText>", xml, re.U | re.I | re.S)
    text = re.sub(r'<[^<]+>', "", str(find), re.U)
    text = ''.join([t for t in text])

    patterns = r'\w+'
    text = ' '.join(re.findall(patterns, text))
    #print text

    tokens = word_tokenize(text)
    tokens = [token.lower() for token in tokens]

    uniques = np.unique(tokens)
    print uniques



