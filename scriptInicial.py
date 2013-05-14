#!/usr/bin/python2.7
# -*- coding: latin-1 -*-

import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import urllib2
import feedparser
import re
import hashlib
import os
from whoosh.index import create_in
from whoosh.fields import *
from BeautifulSoup import BeautifulSoup
#from bs4 import BeautifulSoup
import index #importe do ficheiro index.py
import feeds
import sentiments
import findEntities
import search

print "scriptinicial"
# Processamento das bibliotecas... Colocar o ficheiro personalidades e e sentilex em dicionarios
politiciansList = []
opinionDic = {}
lexiDic = {} # Dicionario que contem como key -> primeira palavra value e uma lista com tuplas
tuple = ()	# (resto da frase, comprimento da frase, polaridade)
list_personalities = []

#Tratamento com o sentilex
sentiments.sentilexTratamento(lexiDic, tuple)
findEntities.personalidadesTratamento(list_personalities)

#Feeds das noticias
feeds.feeds(lexiDic, list_personalities, opinionDic)

print "\nNoticias:"
for op in opinionDic:
	print op
	print "\nPoliticos:"
	for i in opinionDic[op][0]:
		print i
	print "\nValor da noticia: ",opinionDic[op][1],"\n\n"
#Extração dos dados para um ficheiro.dat
sentiments.analiseSentimentos(opinionDic)
#sentiments. analiseSentimentos(opinionDic):
#Pesquisa BM25
search.search(list_personalities)