#!/bin/sh

echo
echo -----------------------------[Python] - A inciar a execucao. Aguarde pff.----------------------------- 
echo

rm -f feeds.txt
rm -f hash_file.txt
rm -f title_file.txt

echo
echo ------------------------------ Exemplos de feeds: http://feeds.dn.pt/DN-Politica ----------------------------- 
echo ------------------------------------------------- http://feeds.jn.pt/JN-Politica -----------------------------
echo

python scriptInicial.py

echo
echo ------------------------------ Done! -----------------------------
echo

cd plots/

echo
echo ----------------------------- [GNUPLOT] - A gerar graficos. Aguarde pff.-----------------------------
echo

#Linhas para a execucao do Gnuplot com a configuracoes dos ficheiros de plot.
gnuplot plotBM25.gp
gnuplot plotSentimentos.gp

echo
echo ----------------------------- [GNUPLOT] - Done! -----------------------------
echo ----------------------------- [GNUPLOT] - Os graficos gerados encontram-se na pasta /graficos.-----------------------------
echo

cd ..
cd graficos/

echo
echo ----------------------------- [Analise] - A abrir os graficos. -----------------------------
echo

open BM25.eps
open sentiments.eps
