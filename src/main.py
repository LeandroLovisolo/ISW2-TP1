#!/usr/bin/env python2
# coding: utf-8
from flask import Flask
from flask import render_template
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/campaigns')
def campaigns():
	#Conseguir lista de campañas
	#Pasar como parámetro lista de campañas
    return render_template('campaings.html')

@app.route('/campaigns/<campaign_number>', methods=['GET', 'POST'])
def campaign_edit(campaign_number):
	if request.method == 'POST':
		#Conseguir campaña y editarla
		return 'Campaña editada'
	else:
		#Pasar como parametro campaña
	    return render_template('campaing_edit.html')

@app.route('/campaigns/add', methods=['GET', 'POST'])
def campaign_add():
	if request.method == 'POST':
		#Crear campaña poniendolé su autor
		#Agregar campaña al repositorio
		return 'Campaña creada'
	else:
		#Pasar como parametro el maestro? o nombre del maestro o algo?
	    return render_template('campaing_add.html')

@app.route('/campaigns/<campaign_number>/messages/')
def messages(campaign_number):
	#Conseguir lista de mensajes de la campaña
	#Pasar como parámetro lista de mensajes
    return render_template('messages.html')

@app.route('/campaigns/<campaign_number>/messages/add', methods=['GET', 'POST'])
def messages_add(campaign_number):
	if request.method == 'POST':
		#Creo el mensaje y lo agrego al repositorio
		return 'Mensaje agregado'
	else:
		#Le tengo que pasar el número de la campaña
		return render_template('message_add.html')

@app.route('/campaigns/<campaign_number>/messages/<message_number>', methods=['GET', 'POST'])
def message_edit(campaign_number, message_number):
	if request.method == 'POST':
		#Pedir el mensaje del repositorio y editarlo
		return 'Mensaje editado'
	else:
		#Pasar datos del mensaje
		return render_template('message_edit.html')

if __name__ == '__main__':
	app.debug = True
	app.run()
