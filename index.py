#!/usr/bin/python
#-*- coding: latin-1 -*-

####################################################################################################
#								FUNCOES PARA INDEXAR OS FEEDS									   #
####################################################################################################
import re
from whoosh.index import create_in
from whoosh.fields import *

lista = []
schema = Schema(id = NUMERIC(stored=True), content=TEXT)
ix = create_in("indexdir_proj", schema)


def index(fToIndex):

	with open(fToIndex, 'r') as f:

		writer = ix.writer()

		for document, line in enumerate(f):
			#line=line.decode("utf-8")
			#print line
			#wordlist = re.split('\W+', line, flags=re.UNICODE)

			ficheiro = re.sub('<div><p>', '', line)
			ficheiro = re.sub('</p></div>', '', ficheiro)
			ficheiro = re.sub('<p>', '', ficheiro)
			ficheiro = re.sub('</p>', '', ficheiro)
			ficheiro = re.sub('<p></p>', '', ficheiro)


			wordlist = re.compile("([\W+])", re.UNICODE).split(unicode(ficheiro, 'utf-8'))

			writer.add_document(id=document, content=unicode(wordlist))
		writer.commit()