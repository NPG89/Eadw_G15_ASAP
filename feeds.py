#!/usr/bin/python

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
import sentiments

def feeds(lexiDic, list_personalities, opinionDic):
	print "feeds"
	with open("feeds.txt",'a+') as f:
		
	####################################################################################################
	#											VARIAVEIS											   #
	####################################################################################################

		listHash = []
		#listHash.append('ccfaa96301a3e11a1add20e1d1ce4dedf0743a71')
	####################################################################################################
	#								FUNCOES PARA IR BUSCAR OS FEEDS	DN								   #
	####################################################################################################
		feed = raw_input("Insert the feed address please: ")

		dn = feedparser.parse(feed)

		for i, post in enumerate(dn.entries):

			
		
			html = urllib2.urlopen(post.link).read()
			soup = BeautifulSoup(html)
			artigo = soup.find(id = 'Article')
			summ = soup.find(id = 'NewsSummary')


			print "############### Titulo noticia:", i, " ###################"
			sha = hashlib.sha1(unicode(post.title)).hexdigest() #hash para certificar que nao existem 2 noticias iguais
			print post.title
			print "Hash da noticia:", sha, "\n"
			#print post.id
			#print "PUBLICADO A: ", post.published, "\n"


			#print "############### RESUMO ###################"
			#print summ, "\n"
			#print "############### ARTIGO ################### \n"
			
			h = open('hash_file.txt', 'a+')
			r = open('hash_file.txt', 'r') 
			t = open('title_file.txt', 'a+')
			t2 = open('title_file.txt', 'r')
		#	for digSha in h:
				#shalist = re.split('\W+', digSha)
		#		listHash.append(digSha.strip())

			t2read = t2.readlines()

			if len(t2read) == 0:
				j = 0
			else:
				tline = t2read[len(t2read)-1]
				titleSplit = re.compile("([\W+])", re.UNICODE).split(unicode(tline, 'utf-8'))
				j = int(titleSplit[0]) + 1
				

			if sha in r.read():
				print "ARTIGO JA EXISTENTE", "\n"
			else:
				if artigo == None:										#Verficacao se o artigo esta vazio
					print "Artigo Vazio", "\n"
					h.write(sha + '\n')	
				else:
					f.write(str(j) + " - " + str(artigo.div.contents[0]) + "\n")  #ESCREVER O ARTIGO PARA O FICHEIRO
					t.write(str(j) + " - " + post.title + "\n") 
					h.write(sha + '\n')
					sentiments.sentimentos(j, post.title, str(artigo.div.contents[0]), lexiDic, list_personalities, opinionDic)
			j = j + 1
					#print artigo.div.contents, "\n"

			#print listHash			
			h.close()
			r.close()
			t.close()	
			t2.close()

	index.index("feeds.txt")				#Executa a funcao de indexacao do ficheiro com os artigos


