#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import sys
import os

#abreviaturas es un fichero con las abreviaturas de los aminoácidos:
f = open("abreviaturas", "r")

#Cada elemento de lista contendrá la abreviatura de un aminoácido:
lista = f.read().splitlines()

for i in lista:
	#babel es un comando del software openbabel para transformar ficheros
	comando = r'babel ' + i + r'.sdf ' + i + r'.pdb' 
	os.system(comando) 
	

f.close()


