from SimpleModel import *

ngrams = 3
topic = 'cancer'
sm = SimpleModel(topic, ngrams)



while True:
    print 'Please, input your query: (0 to exit) '
    query = raw_input()
    if query == '0':
        print 'Bye'
        break
    else:
        print '..' * 40
        response = sm(query)
        print response
        print '..' * 40