from SimpleModel import *

'''
========= Script prinicipal. ===========
Aquí importamos la clase SimpleModel la cual crea un objeto del modelo.
Con el modelo instanciado seteamos los parametros necesarios; como el numero de
n grams y el topico que buscamos.
Podemos hacer todas las consultas que queramos hasta que ingresemos "0".
'''

ngrams = 3
topic = 'cancer'
sm = SimpleModel(topic, ngrams, 2)


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
