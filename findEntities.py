#!/usr/bin/python
# -*- coding: latin-1 -*-

import nltk
import re
    
def personalidadesTratamento(list_personalities):
    print "personalidadesTratamento"
    with open("personalities.txt") as file:
       dic_words = eval(file.read())
       for t in dic_words['listPersonalities'].keys():  #Estamos a passar directamente a leitura dos nomes do ficheiro
           t = re.sub(" de ",' ', t)
           t = re.sub(" da ",' ', t)
           t = re.sub(' do ',' ', t)
           t = re.sub(' dos ',' ', t)
           t = re.sub(' das ',' ', t)
           list_personalities.append(t)
    list_personalities.append("Cavaco Silva")
    list_personalities.append("Passos Coelho")
    list_personalities.append("António Seguro")
    
    return

def _SearchEntities(news, list_personalities): 
    print "_SearchEntities"                   
    try:
        performers_list = []
        news = re.sub(r'\W+\d+\s+.,\'"&', '', news)
        
        ######################################################
        # Para ja substituimos os de/da/do em todo o ficheiro#
        #  Mas o ideal sera so tirar quando esta entre dois  #
        #                      Entidades                     #
        ######################################################

        news = re.sub(" de ",' ', news)
        news = re.sub(" da ",' ', news)
        news = re.sub(' do ',' ',news)
        news = re.sub(' dos ',' ', news)
        news = re.sub(' das ',' ',news)

        
        for sentence in nltk.sent_tokenize(news):
           
        ######################################################
        # Atention: ele ainda distingue passos coelho sendo   #
        # Uma pessoa diferente, arranjar uma tecnica que faz #
        # com que ele perceba que sao a mesma pessoa         #
        ######################################################
            for chunk in nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(sentence))):
                if hasattr(chunk, 'node'): #verifica se eh um node
                    if chunk.node == "PERSON":
                        performer = ' '.join(c[0] for c in chunk.leaves())
                        if performer in list_personalities:
                            performers_list.append(performer)                 
        return performers_list
    except:
        print " ERROR: Couldn't perform named entity recognition on this text"
        return      
