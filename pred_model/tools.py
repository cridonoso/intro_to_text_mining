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
    '''
    Retorna una respuesta con articulos desde pubmed
    :param query: Topico a buscar
    :return: Documentos  asociados al topico y ordenados por relevancia
    '''
    Entrez.email = 'your.email@example.com'
    handle = Entrez.esearch(db='pubmed',
                            sort='relevance',
                            retmax='20',
                            retmode='xml',
                            term=query)
    results = Entrez.read(handle)
    return results

def get_abstract(pmid):
    '''
    Entrega el abstract en formato xml. Gracias a los bracket de xml podemos extraer con mayor facilidad
    el texto que nos interesa
    :param pmid: id del documento
    :return: xml del articulo
    '''
    handle = Entrez.efetch(db='pubmed', id=pmid, retmode='xml', rettype='abstract')
    return handle.read()

def remove_text_inside_brackets(text, brackets="()"):
    '''
    Funcion para eliminar el texto entre parentesis. Dado que, generalmente, el texto entre parentesis carece de
    sentido eliminamos el contenido de este dentro de una oracion. Así por ej:
    "Las personas dentro del rango normal (50 - 80 kg) viven mejor"
    En este ejemplo (50 - 80 kg) aporta información pero no sigue la coherencia de la oración por lo tanto
    lo extraemos.
    :param text: texto en string
    :param brackets: tipo de bracket que queremos considerar
    :return: string sin contenido entre parentesis
    '''
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
    '''
    Funcion para extraer el contenido de los corpus separado por oraciones. Luego la gneración de ngrams será correcta:
    Por ejemplo:
    ....el gato subió por la pandereta."\n"Dada la creciente...
     debemos separar ambas oraciones ya que podría generarse un token del tipo:
     [pandereta, Dada] => y esto no tiene mucho sentido
    :param text: string en xml
    :return: lista con oraciones extraidas desde txto entre <AbstractText> </AbstractText>
    '''
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
    '''
    Las fechas y numero particulares responden a un contexto en particular. Sin embargo,
    como buscamos generar texto aleatorio no nos interesa mantener el significado conxtual. Así
    estandarizamos todas las fechas y numero particulares con el objetivo de aumentar su frecuencia
    Por ejemplo:
    1987 -> 2018
    1876 -> 2018
    :param sentences: Lista de oraciones
    :return: texto estandarizado
    '''
    for i,(tokens) in enumerate(sentences):
        for j,(u) in enumerate(tokens):
            if re.match(r'[0-9]+', u):
                if len(u) == 4 and u[0]!='0':
                    sentences[i][j] = '2018'
                else:
                    sentences[i][j] = '1'
    return sentences

def get_next_words(resources, n):
    '''
    Devuelve la siguiente palabra dado todo el corpus
    :param resources: lista con oraciones
    :param n: cantidad de ngrams
    :return: matrix con tuplas de todas las oraciones. Cada tupla es de la forma (ngram, siguiente_palabra)
    '''
    data = []
    for resource in resources:
        for sentence in resource:
            set_ngrams = ngrams(sentence, n)
            ngrams_vector = [ngram for ngram in set_ngrams]
            matrix = ngramos(ngrams_vector)
            data.append(matrix)

    return list(itertools.chain(*data))

def ngramos(ngrams_vector):
    '''
    retorna una tupla con el ngram actual y la siguiente palabra en la oracion
    :param ngrams_vector: vector con n-grams
    :return: tuplas del tipo (ngram, siguiente palabra)
    '''
    matrix = []
    for index in range(0, len(ngrams_vector)-1):
        partial = [ngrams_vector[index],ngrams_vector[index+1][-1]]
        matrix.append(partial)
    return matrix

def make_table(uniques, next_words):
    '''
    Crea la tabla de palabras unicas vs ngrams
    :param uniques: lista de palabras unicas
    :param next_words: matrix con ngrams y sus palabras siguientes segun el corpus
    :return: Matriz de frecuencia
    '''
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
    '''
    Invoca a todos los metodos de más arriba. Busca articulos en pudmed, extrae el abstract, normaliza, genera los ngrams
    y luego crea la matriz de frecuencia
    :param query: topico a buscar
    :param ngrams: cantidad de ngrams
    :param max_docs: maximo de documentos a buscar
    :return: tabla de frecuancia, lista de ngrams unicos, lista de palabras unicas
    '''
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
    '''
    Genera un vector con palabras siguientes. De acuerdo a la frecuencia aumentaremos las ocurrencias del elemento
    Por ejemplo:
                | corrio | hola | a |
    (el gato)   |   3    | 0    | 2 |   ==> v = [corrio, corrio, corrio, a, a]
    ===================================
    :param obj: vector de frecuancias asociado a un ngram especifico
    :param uniques: vector de palabras unicas
    :return: lista de palabras mas probables con cardinalidad aumentada
    '''
    vector = []
    for i in range(0, int(len(obj))):
        if obj[i]!=0:
            times = obj[i]
            for j in range(0, int(times)):
                vector.append(uniques[i])
    return vector




