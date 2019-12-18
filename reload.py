#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib,json, urllib2
import re 
import time
import sys
reload (sys)

from flask import Flask, render_template, url_for
from flask import request

from elasticsearch import Elasticsearch
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

global historico
historico=[]
global j
j=0

def twominutes():
	global historico
	global j
	historico=[]
	fecha=0
        hora=0
        auxiliar=0
        j=j+1
        auxa = 1
        flag = 1

	es= Elasticsearch(HOST="http://localhost", PORT=9200)


	baseURL='https://api.thingspeak.com/update?api_key=RC2OVKUXZYRZNUSC'



	web = urllib.urlopen("https://quotes.wsj.com/index/DJIA")   
	web_m = str(web.read())

	texto = "quote_val" 
	lista = re.finditer(texto, web_m)
	 
	texto1 = "quote_dateTime" 
	lista1 = re.finditer(texto1, web_m)

	noticiasi = ['']
	noticiasf = ['']

	for encontrado in lista:
		x = (encontrado.start())
		noticiasi.append(x)

	for encontrado in lista1:
		y = (encontrado.start())
		noticiasf.append(y)

        i=1
	fecha = web_m[(noticiasf[i]+16):(noticiasf[i]+37)]
	tituloa= {"dato": web_m[(noticiasi[i]+11):(noticiasi[i]+19)]}
	titulo = {"dato": web_m[(noticiasi[i]+11):(noticiasi[i]+19)], "fecha" : fecha}
	auxiliar=float(web_m[(noticiasi[i]+11):(noticiasi[i]+19)])
	historico.append(auxiliar)
	#es.index(index="valores",doc_type="numero",id=j, body=titulo)

	#auxa = es.count(index="valores",doc_type="numero")
	es.index(index="valores",doc_type="numero",id = j , body=titulo)
	#res=es.get(index="valores",doc_type="numero",id=1)
	res=es.search(index="valores",body={"query": {"match": {"content": "dato"}}})  
	print(historico)
		
	#fecha= str(time.strftime("%x"))
	hora= time.strftime("%X")
	conn=urllib2.urlopen(baseURL + '&field1=%s' %auxiliar)
	conn.close()
	time.sleep(10)

while True:
	twominutes()


    
