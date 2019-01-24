#!/usr/bin/env python
# -*- coding: utf-8 -*-

def bruteforce(seq,pattern):
    matchcount = 0
    for i in range(len(seq)):
        if(i+len(pattern) <= len(seq)):
            if (seq[i : i+len(pattern)] == pattern):
                matchcount +=1
                print("Match Found at ",i)


    print ("###### NUMBER OF MATCH : ",matchcount," ######")
###########################KMP RESEARCH Algorithm#####################################
def MP_precalc(pattern):
    doc = list(range(0,len(pattern)))
    doc[0] = 0
    j = 0
    for i in range(1,len(pattern)):
        while (j>0 and pattern[i]!=pattern[j]):
            j = doc[j-1]
        if(pattern[i]==pattern[j]):
            j = j+1
        doc[i]=j

    return doc


def MP_algo(seq,pattern):
    matchcount = 0
    table = MP_precalc(pattern)
    j=0
    for i in range(len(seq)):
        while(j>0 and seq[i] != pattern[j]):
            j = table[j]
        if (seq[i]==pattern[j]):
            j+=1
        if (j == len(pattern)):
            #if (seq[i : i+len(pattern)] == pattern):
            matchcount+=1
            print("Match Found at ",i-len(pattern)+1)
            j = table[j-1]

    print ("###### NUMBER OF MATCH : ",matchcount," ######")

###########################BW RESEARCH Algorithm#####################################


def creerAlphabet(texte):
    liste = []
    for t in texte:
        if (t not in liste):
            liste.append(t) #ajout d'un cractere non present dans l'alphabet
    return liste

#Création de la table du mauvais caractère
#Cas ou la derniere lettre ne correspond pas
def mauvaisCaractere(motif, m, alphabet, asize):
    bmBc = {}
    for i in range(asize):
        bmBc[alphabet[i]] = m #Initialisation de la table, chaque caractère = taille motif
    for i in range(m):
        bmBc[motif[i]] = m - i - 1 #
        #chaque caractère est = au petit indice de ce caractère en partant de la fin du motif (et !=0)
    print("bmBc :",bmBc)
    return bmBc

def suffixes(motif, m):
    suffixe = [0] * m
    suffixe[m - 1] = m
    g = m - 1
    previous_i = 0 #sauvegarde de l'indice i du tour de boucle précédent
    for i in range(m - 2, -1, -1):
        if (i > g and suffixe[i + m - 1 - previous_i] < i - g): #la valeur est deja dans la table
            suffixe[i] = suffixe[i + m - 1 - previous_i]
        else:
            if i < g:
                g = i
            previous_i = i
            while (g >= 0 and motif[g] == motif[g + m - 1 - previous_i]):
                g -= 1 #g est decremente tant que les lettres sont identiques 2 a 2
            suffixe[i] = previous_i - g
    return suffixe


#Fonction de remplissage de la  table bonSuffixe
def bonSuffixe(motif, m):
    suffixe = suffixes(motif, m)
    bmGs = [0] * m
    for i in range(m):
        bmGs[i] = m
    for i in range(m-1, -1, -1):
        if suffixe[i] == i+1: #si il existe un suffixe dans le motif
            for j in range(m - 1 - i):
                if (bmGs[j] == m):
                    bmGs[j] = m - 1 - i #la valeur de saut est changee pour correspondre au suffixe
    for i in range(m - 1):
        bmGs[m - 1 - suffixe[i]] = m - 1 - i #utilisation de la table de suffixe
    print("bmGs :",bmGs)
    return bmGs

def BM_search(seq,pattern):
    matchcount = 0
    i=0
    j=0
    patternlength = len(pattern)
    seqlength = len(seq)
    alphabet = creerAlphabet(seq)
    badchar = mauvaisCaractere(pattern,patternlength,alphabet,len(alphabet))
    goodsuffix = bonSuffixe(pattern,patternlength)
    while(i<=seqlength-patternlength):
        j = patternlength-1
        while(j>=0 and seq[i+j] == pattern[j]):
            j = j-1
        if (j < 0):
            print("Match Found at ",i)
            matchcount+=1
            i = i+goodsuffix[0]
        else:
            i = i+ max(goodsuffix[j],(badchar[seq[i+j]] - patternlength + 1 + j))
    print ("###### NUMBER OF MATCH : ",matchcount," ######")
"""
#####TEMP MAIN
seq = "ATGGCGATGGACAGCATGTTAGTCAGTGACAGATCGTGCAGCAGAT"
pattern = "AGAT"
print("########Naive Algorithm############")
bruteforce(seq,pattern)
print("########MP Algorithm############")
MP_algo(seq,pattern)
"""


import sys
seq = ""
pattern = ""
if len(sys.argv)==1:
    print("This is the example version \n regular usage : script_td1.py [naive/MP/BW] [Pattern] [Sequence file name]")
    seq = "ATGGCGATGGACAGCATGTTAGTCAGTGACAGATCGTGCAGCAGAT"
    pattern = "AGAT"
    print("Sequence = ",seq)
    print("Pattern = ",pattern)
    print("########Naive Algorithm############")
    bruteforce(seq,pattern)
    print("########MP Algorithm############")
    MP_algo(seq,pattern)
    print("########BW Algorithm############")
    BM_search(seq,pattern)

elif len(sys.argv)<4:
    print ("Wrong input \nUsage : script_td1.py [naive/MP/BW] [Pattern] [Sequence file name]")
else:
    method = sys.argv[1]
    pattern = sys.argv[2]
    filename = sys.argv[3]
    file = open(filename)
    seq = file.readline()
    if method == "naive" :
        print("########Naive Algorithm############")
        bruteforce(seq,pattern)
    if method == "MP" :
        print("########MP Algorithm############")
        MP_algo(seq,pattern)
    if method == "BW" :
        print("########BW Algorithm############")
        BM_search(seq,pattern)
