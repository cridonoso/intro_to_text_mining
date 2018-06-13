# -*- coding: utf-8 -*-
import re
from nltk.tokenize import sent_tokenize, word_tokenize
import numpy as np
from Bio import Entrez
import itertools
from nltk import ngrams
import os
import time

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

    text_wo_brackets = remove_text_inside_brackets(text)
    text_splitted =  text_wo_brackets.split('.')

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

def get_next_words(resources, n):
    data = []
    for resource in resources:
        for sentence in resource:
            set_ngrams = ngrams(sentence, n)
            ngrams_vector = [ngram for ngram in set_ngrams]
            matrix = ngramos(ngrams_vector)
            data.append(matrix)

    return list(itertools.chain(*data))

def ngramos(ngrams_vector):
    matrix = []
    for index in range(0, len(ngrams_vector)-1):
        partial = [ngrams_vector[index],ngrams_vector[index+1][-1]]
        matrix.append(partial)
    return matrix

def make_table(uniques, next_words):
    table = []
    tuple = []
    for i,nw in enumerate(next_words):
        if nw[0] in tuple:
            ub = tuple.index(nw[0])
            index = list(uniques).index(nw[1])
            table[ub][index] += 1
        else:
            f = np.zeros(len(uniques))
            index = list(uniques).index(nw[1])
            f[index] += 1
            table.append(f)
            tuple.append(nw[0])
        os.system('clear')
        print 'loading','.'*(i%3)
    print 'Ready!'
    return table,tuple

def generate_model(query, ngrams, max_docs):

    idList = search(query)['IdList']
    resources = []
    if max_docs!=None:
        print max_docs
        if max_docs>len(idList):
            print '[SYSTEM MESSAGE] ',max_docs, 'is greater than the numbers of documents ( =', len(idList), '). Please repeat it'
            return 0
        else:
            idList = idList[0:max_docs]

    for i,(pid) in enumerate(idList):
        print 'reading abstract number', i
        xml = str(get_abstract(pid))
        sentences = get_sentences(xml)
        standard = standarize_numbers(sentences)
        resources.append(standard)

    next_words = get_next_words(resources, ngrams)
    merged = list(itertools.chain(*resources))
    merged_ = list(itertools.chain(*merged))
    uniques =  np.unique(merged_)
    table,tuple = make_table(uniques, next_words)
    return table,tuple,uniques

def get_proportional(obj, uniques):
    vector = []
    for i in range(0, int(len(obj))):
        if obj[i]!=0:
            times = obj[i]
            for j in range(0, int(times)):
                vector.append(uniques[i])
    return vector




