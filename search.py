#!/usr/bin/python
# -*- coding: latin-1 -*-

import re
import os
from whoosh.qparser import *
from whoosh.query import *
from whoosh.qparser import QueryParser
from whoosh.index import open_dir

def search(list_personalities):
	cwderase = os.getcwd()						##################################
	path = os.path.join(cwderase, "plots")		#	Apagar o ficheiro plotBM25   #
	open(path + "/plotBM25.dat", 'w+').close()	##################################

	cwderase2 = os.getcwd()						
	path2 = os.path.join(cwderase2, "plots")												
	open(path2 + "/plotBM25.gp", 'w+').close()	####################################
												#	Apagar o ficheiro do gnuplot   #
												####################################
	resList = []
	dataList = []
	valueList = []
	entiList = []
	fileDic = {}
	ytics = ""
	ylabel = ""
	xtics = ""
	tupla = ()

	ix = open_dir("indexdir_proj")

	with ix.searcher() as searcher:

		with open("personalities.txt") as f:

			word_dic = eval(f.read())

			for t in list_personalities:  #Passamos directamente os nomes lidos do ficheiro
				print unicode(t.decode('utf-8'))
				query = QueryParser("content", ix.schema, group=OrGroup).parse(unicode(t.decode('utf-8')))
				results = searcher.search(query)

				for i, r in enumerate(results):
					resList.append(float(results.score(i)))
					print "Score Doc:", r['id'], "==>", results.score(i)
				sumList = sum(resList)
				lenList = len(resList)

				if lenList == 0:
					avg = 0
				else:
					avg = sumList/lenList
					tupla = (t, float(avg))
					print "Average rank: ", avg
					dataList.append(tupla)



				resList[:] = []	# Apagar a lista result ao fim de cada ciclo para nao acumular infinitamente
				

				print "---------------------------------------"
				
				cwd = os.getcwd()							############################################################
				path = os.path.join(cwd, "plots")			#	Indicacao do caminho e abertura do ficheiro plotBM25   #
				f = open(path + "/plotBM25.dat", 'a+')		############################################################


				f2 = open(path2 + "/plotBM25.gp", 'a+')		#####################################
															#	 abertura do ficheiro gnuplot   #
															#####################################	
			dataList.sort(key=lambda tupla: tupla[1])
			dataList.reverse()
			#print dataList													

			for i, e in enumerate(dataList[0:20]):
				f.write(str(e[1]) + " " + str(e[0]) + "\n") #(str(avg) + "\n")
				valueList.append(int(e[1]))
				ytics += str(e[1]) + ", "
				xtics += "\"" + str(e[0]) + "\" " + str(i) + ", " 

			for j, e2 in enumerate(dataList[0:20]):
				ylabel += "set label" + "\"" + str(e2[1]) + "\" at " + str(j) + "," + str(int(e2[1])+1) + " rotate by 65" + "\n"
			
			maxX = max(valueList) + 1
			ytics = ytics[0:len(ytics)-2]
			xtics = xtics[0:len(xtics)-2]

			f2.write("set title 'BM25 Ranking'" + "\n" +							#########################################
				"set style fill solid 0.2" + "\n" +									#										#	
				"set xrange [-1:21]" + "\n" +										#										#
				"set xtics nomirror font \"0.001\"" + "\n" +						#	Escrita do ficheiro .gp 			#
				"set xtics (" + xtics + ")" + " rotate by -65" + "\n" +				#	com as definicoes do graficos 		#
				"set xlabel 'Entidades' textcolor lt 3" + "\n" +					#										#
				"set yrange " + "[0:" + str(30) + "]" + "\n" +						#										#
				ylabel +															#										#
				"set y2label 'Rank (%)' rotate by -90 textcolor lt 3" + "\n" +		#########################################	
				"set boxwidth 0.5"+ "\n" +
				"set terminal postscript eps enhanced color" + "\n" +
				"set output '../graficos/BM25.eps'" + "\n" +
				"plot 'plotBM25.dat' using :1 notitle  with boxes axis x1y1 lt 3"
				)
						
			#print dataList
		dataList[:] = []
				
	f.close()
	f2.close()