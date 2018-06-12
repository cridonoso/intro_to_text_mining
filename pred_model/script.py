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

def get_abstract(pmid):
    handle = Entrez.efetch(db='pubmed', id=pmid, retmode='xml', rettype='abstract')
    return handle.read()

def remove_text_inside_brackets(text, brackets="()"):
    count = [0] * (len(brackets) // 2) # count open/close brackets
    saved_chars = []
    for character in text:
        for i, b in enumerate(brackets):
            if character == b: # found bracket
                kind, is_close = divmod(i, 2)
                count[kind] += (-1)**is_close # `+1`: open, `-1`: close
                if count[kind] < 0: # unbalanced bracket
                    count[kind] = 0  # keep it
                else:  # found bracket to remove
                    break
        else: # character is not a [balanced] bracket
            if not any(count): # outside brackets
                saved_chars.append(character)
    return ''.join(saved_chars)

def get_sentences(text):
    find = re.findall(r"<AbstractText[>]?.*</AbstractText>", text, re.U | re.I | re.S)
    text = re.sub(r'<[^<]+>', "", str(find), re.U)
    text = ''.join([t for t in text])
    print remove_text_inside_brackets(text)
    text_splitted =  text.split('.')

    patterns = r'\w+'
    senteces = []
    for text in text_splitted:
        text_new = ' '.join(re.findall(patterns, text))

        tokens = word_tokenize(text_new)
        tokens = [token.lower() for token in tokens]
        senteces.append(tokens)

    for i,(tokens) in enumerate(senteces):
        for j,(token) in enumerate(tokens):
            if (token == 'xc2') or (token == 'xa9'):
                del senteces[i][j]

    return senteces

def standarize_numbers(sentences):
    for i,(tokens) in enumerate(sentences):
        for j,(u) in enumerate(tokens):
            if re.match(r'[0-9]+', u):
                if len(u) == 4 and u[0]!='0':
                    sentences[i][j] = '2018'
                else:
                    sentences[i][j] = '1'
    return sentences

def generate_model(query, ngrams):

    idList = search(query)['IdList']
    resources = []
    for i,(pid) in enumerate(idList):
        print 'reading abstract number',i
        xml = str(get_abstract(pid))
        sentences = get_sentences(xml)
        standar = standarize_numbers(sentences)
        #print standar
        uniques = np.unique(standar)
        resources.append(uniques)
    #unique_words =  len(list(set().union(resources[0],resources[1],resources[2])))

generate_model('cancer', 2)




