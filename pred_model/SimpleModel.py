from tools import generate_model, get_proportional
import random
import numpy as np

class SimpleModel:
    def __init__(self, word, ngram, max_docs = None):
        self.ngram = ngram
        self.word = word
        self.max_docs = max_docs
        self.table, self.tuple, self.uniques = generate_model(word, ngram, max_docs)
        self.table_2, self.tuple_2, self.uniques_2 = generate_model(self.word, self.ngram-1, self.max_docs)
        print self.tuple

    def __call__(self, query, steps=100):
        if len(query.split()) != self.ngram:
            print '[SYSTEM MESSAGE] Please start with',self.ngram,'words'

        entry = map(tuple, [query.split()])[0]
        '''performed', 'to'''
        response = ' '.join(entry)
        while(steps):
            try:
                index = self.tuple.index(entry)
            except:
                try:
                    self.ngram_r = self.ngram
                    self.table_r = self.table
                    self.tuple_r = self.tuple
                    self.uniques_r = self.uniques
                    self.ngram = self.ngram-1
                    self.table = self.table_2
                    self.tuple = self.tuple_2
                    self.uniques = self.uniques_2 
                    print entry
                    entry = tuple(x for x in entry[1:len(entry)])
                    print entry
                    print ngram
                    index = self.tuple.index(entry)
                except:
                    self.ngram = self.ngram_r
                    self.table = self.table_r
                    self.tuple = self.tuple_r
                    self.uniques = self.uniques_r
                    print 'No more matching entries. Your response: '
                    return response
            vector_of_words = self.table[index]
            vector_prob = get_proportional(vector_of_words, self.uniques)

            secure_random = random.SystemRandom()
            next = secure_random.choice(vector_prob)
            response = response+' '+next
            new = []
            if self.ngram == 1:
                entry = map(tuple, [next.split()])[0]
            if self.ngram == 2:
                entry = (entry[-1], next)
            if self.ngram == 3:
                entry = (entry[-2], entry[-1], next)
            steps -=1
        return response