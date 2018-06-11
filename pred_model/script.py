# -*- coding: utf-8 -*-


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
    handle = Entrez.efetch(db='pubmed', id=pmid, retmode='text', rettype='abstract')
    print handle.read()

query = 'cancer'
idList = search(query)['IdList']
for pid in idList:
    print '-'*60
    print_abstract(pid)

