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

es= Elasticsearch(HOST="http://localhost", PORT=9200)


baseURL='https://api.thingspeak.com/update?api_key=RC2OVKUXZYRZNUSC'

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

global historico
historico=[]
global j
j=0

app = Flask(__name__)

@app.route('/')
def home():
    global flag
    global j
    global historico
    fecha=0
    hora=0
    auxiliar=0
    j=j+1
    auxa = 1
    flag = 1
   
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
    return render_template('home.html', titulo=auxiliar, fecha=fecha)
   
  
@app.route('/about', methods=['POST','GET'])
def about():
    global umbral
    flag=0
    aux=0
    aux2=0
    encontrado2=0
    global historico
    noticias=[]
    noticias2=[]
    acierto=[]
    bandera=0
    if request.method == 'POST':
           if request.form['intr'] == 'Enviar':
                flag = 1
		umbral = float(request.form['dato'])
                length=len(historico)-1
                for encontrado in range(length):
                        encontrado2=encontrado+1
			if historico[encontrado2]> umbral:
				acierto.append([encontrado2])
                                aux=es.get(index="valores",doc_type="numero",id=encontrado2)
                                aux2=str(aux['_source'])
                                noticias2.append(aux2)
           elif request.form['intr'] == 'Next':
                flag = 5
                noticias = 10
    else:
	    noticias = 0

    flag=len(noticias2)    
    noticias=noticias2[(flag-5):flag]

    if len(noticias) > 5:
	bandera=5
    else: 
	bandera=len(noticias)
    print(acierto)
    return render_template('about.html', valor=noticias, bandera = bandera, umbrale = umbral)

@app.route('/about1', methods=['POST','GET'])
def about1():
    global umbral
    global flag
    global aux
    if request.method == 'POST':
           if request.form['intr'] == 'Enviar':
                flag = 1
		umbral = float(request.form['dato'])
		noticias = 10
    
    else:
	    noticias = 0
    return render_template('about1.html', valor=noticias, bandera = flag, umbrale = umbral)	

@app.route('/medio')
def medio():
    global j
    auxiliar=0
    auxiliar2=0
    auxiliar3 = 0
    mediam = 0
    mediabe=0
    index=j-1
    print(index)

    for encontrado in range(index):
        print(encontrado)
	encontrado=encontrado+1
	auxiliar=es.get(index="valores",doc_type="numero",id=encontrado)
        auxiliar2=str(auxiliar['_source'])
        auxiliar=float(auxiliar2[(12):(20)])
        print(auxiliar)
    	mediam = mediam + auxiliar

    conn = urllib2.urlopen("https://api.thingspeak.com/channels/933069/feeds/last.json?api_key=0S2B51J76IAAT3UF") 
    response = conn.read()
    data=json.loads(response)
    print data['field1'] 
    
    conn.close()
    auxiliar3 = float(data['field1'])
    mediam = mediam/index
    print(index)
    if index > 4:
    	mediabe = (mediabe+auxiliar3)/2
    else:
	mediabe= auxiliar3

    #print(auxiliar3)

    return render_template('medio.html', media = mediam, mediab = mediabe)

@app.route('/extra')
def extra():
    return render_template('extra.html')

if __name__ == '__main__':
        global flag
        global umbral
        umbral = 0
        flag = 1
        app.debug = True
        app.run(host ='0.0.0.0', port=5000) 
     

