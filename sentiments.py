#!/usr/bin/python
# -*- coding: latin-1 -*-

import re
import os
from whoosh.qparser import *
from whoosh.query import *
from whoosh.qparser import QueryParser
from whoosh.index import open_dir
import nltk
import findEntities

def sentilexTratamento(lexiDic, tuple):
	print "SentilexTratamento"
	with open("SentiLex-flex-PT02.txt") as f:
		# percorre cada linha do ficheiro
		for line in f:
			entry = re.split(r'\,|\;|\.', line)
			palavras = nltk.word_tokenize(entry[0])
			polaridade = entry[5][7:]
			tuple = (palavras[1:] ,len(palavras[1:]), int(polaridade))

			# verifica se a primeira palavra existe no dicionario se sim faz append senao cria
			if palavras[0] in lexiDic:
				lexiDic[palavras[0]].append(tuple)
			else: 
				lexiDic[palavras[0]] = [tuple]
	return

def sentimentos(id, title, news, lexiDic, list_personalities, opinionDic):
	
	#print "Sentimentos da noticia (",id,"): ",title
	#print lexiDic
	#print news

	politiciansList = findEntities._SearchEntities(news, list_personalities)
	#print politiciansList

	words = nltk.word_tokenize(news)
	sum = 0

	# percorre cada palavra da noticia
	for i, word in enumerate(words):
		p=i
		#verifica se a palavra existe no dicionario, se existe adiciona a lista aux
		if word in lexiDic:
			#print "1 ",word
			listaux=[] # contem a correspondencia so para verificacao
			listaux.append(word)
			
			# verifica se a key e acompanhada por mais frases
			if len(lexiDic[word]) > 1:
				# se for entao percorre cada palavra e faz comparaxao com o nltk
				for j in lexiDic[word]:
					i += 1
					for t, val_word in enumerate(j[0]):
						if words[i] == val_word:
							i += 1
							listaux.append(val_word)
						# se a palavra nao for igual este quebra o ciclo e passa para a outra palavra
						else:
							listaux = []
							listaux.append(word)
							i=p
							break
					t +=1
					if t == len(j[0]):
						t +=1
						if len(listaux) == t:
							if j[2] == -1:
								sum -=1
								#print listaux
							else:
								sum +=1
							listaux=[]
							listaux.append(word)

							break
			else:
				if lexiDic[word][0][2] == -1:
					sum -= 1
				else:
					sum +=1

		opinionDic[str(id)+" - "+title] = (politiciansList, sum)

	return

def analiseSentimentos(opinionDic):
	#print "entrei"
	cwderase = os.getcwd()								##################################
	path = os.path.join(cwderase, "plots")				#	Apagar o ficheiro plotBM25   #
	open(path + "/plotSentimentos.dat", 'w+').close()	##################################

	cwderase2 = os.getcwd()						
	path2 = os.path.join(cwderase2, "plots")												
	open(path2 + "/plotSentimentos.gp", 'w+').close()	####################################
														#	Apagar o ficheiro do gnuplot   #
														####################################
	
	print "---------------------------------------"
				
	cwd = os.getcwd()									###################################################################
	path = os.path.join(cwd, "plots")					#	Indicacao do caminho e abertura do ficheiro plotSentimentos   #
	f = open(path + "/plotSentimentos.dat", 'a+')		###################################################################


	f2 = open(path2 + "/plotSentimentos.gp", 'a+')		#####################################
														#	 abertura do ficheiro gnuplot   #
		

	tupla = ()
	listaTup = []													#####################################	
	politicos = ""
	xtics =""
	for pos in opinionDic:
		val = pos.split()
		id = int(val[0])
		politicos = ""
		if opinionDic[pos][0]:
			politicos ="["
			for i in opinionDic[pos][0]:
				#print "falta -",i
				listi = i.split()
				i = ""
				for p in listi:
					i += p[0]  
				politicos +=  i + ","
			politicos = politicos[0:len(politicos)-2]+ "]"
		tupla = (id, politicos)
		listaTup.append(tupla)

			#print politicos
		f.write(str(id)+" "+str(opinionDic[pos][1])+"\n")
	listaTup.sort(key=lambda tupla: tupla[0])
	listaTup.reverse()

	for tup in listaTup:
		xtics += "\"" + str(tup[0]) + " " + tup[1] + "\"" + " " + str(tup[0]) + ", " 

	xtics = xtics[0:len(xtics)-2]
	#print "xtics: ", xtics

		########################################################################
		#																	   #
		#			Tratamento dos dados, para fazer o gráfico......           #
		#																	   #
		########################################################################


			# for j, e2 in enumerate(dataList[0:30]):
			# 	ylabel += "set label" + "\"" + str(e2[1]) + "\" at " + str(j) + "," + str(int(e2[1])+1) + " rotate by 65" + "\n"
			#-10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10"

	#maxX = max(valueList) + 1
	#ytics = ytics[0:len(ytics)-2]
	#xtics = xtics[0:len(xtics)-2]

	f2.write("set title 'Sentimentos das personalidade em cada Noticia'" + "\n" +		#########################################
		"set style fill solid 0.2" + "\n" +												#										#	
		"set xrange [-1:26]" + "\n" +													#										#
		"set xtics nomirror font \"0.001\"" + "\n" +									#	Escrita do ficheiro .gp 			#
		"set xtics (" + xtics + ")" + " rotate by -45" + "\n" +										#	com as definicoes do graficos 		#
		"set xlabel 'Entidades' textcolor lt 3" + "\n" +								#										#
		"set yrange " + "[" + str(-10) + ":" + str(10) + "]" + "\n" +					#										#
		"set ylabel 'Valor de Sentimento' " + "\n" +																		#										#		#########################################	
		"set boxwidth 0.5"+ "\n" +
		"set terminal postscript eps enhanced color" + "\n" +
		"set output '../graficos/sentiments.eps'" + "\n" +
		"plot 'plotSentimentos.dat' using 1:2 notitle  with boxes axis x1y1 lt 3"
		)
				
			#print dataList
		#dataList[:] = []
		
	f2.close()
	f.close()