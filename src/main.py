#!/usr/bin/env python2
# coding: utf-8

from flask import Flask, request
from flask import render_template
from app.campania import Campania
from app.evento import Evento
from app.repositorio_de_eventos import RepositorioDeEventos

app = Flask(__name__)

@app.route('/')
def home():
  return render_template('home.html')

@app.route('/campaigns')
def campaigns():
  repositorio_de_eventos = RepositorioDeEventos.obtenerInstancia()
  lista_de_campanias = []
  for evento in repositorio_de_eventos.eventos():
    for campania in evento.campanias():
      lista_de_campanias += [{'nombre' : campania.nombre(), 
                            'fechaInicio' : campania.fechaInicio(),
                            'fechaFinal' : campania.fechaFinal(),
                            'codificacion' : str(campania)}]
  
  return render_template('campaigns.html', campanias=lista_de_campanias)

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
  # Mostrar formulario
  if request.method == 'GET':
    eventos = RepositorioDeEventos.obtenerInstancia().eventos()
    eventosStr = []
    for evento in eventos:
      eventosStr.append({'nombre': evento.nombre(), 'id': str(evento)})
    return render_template('campaign_add.html', eventos=eventosStr)

  # Guardar nueva campaña
  else:
    campania = Campania(request.form['nombre'],
                        request.form['fechaInicio'],
                        request.form['fechaFinal'])

    for evento in RepositorioDeEventos.obtenerInstancia().eventos():
      if str(evento) == request.form['idEvento']:
        evento.agregarCampania(campania)
    return 'Campaña creada'

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

@app.route('/campaigns/<campaign_number>/messages/<message_number>', 
  methods=['GET', 'POST'])
def message_edit(campaign_number, message_number):
  if request.method == 'POST':
    #Pedir el mensaje del repositorio y editarlo
    return 'Mensaje editado'
  else:
    #Pasar datos del mensaje
    return render_template('message_edit.html')

def cargarDatosDePrueba():
  # Eventos y campañas
  e = Evento('Prueba de historia')
  RepositorioDeEventos.obtenerInstancia().agregarEvento(e)
  e.agregarCampania(Campania('Recordatorios v1', '2015-05-01', '2015-06-01'))
  e.agregarCampania(Campania('Recordatorios v2', '2015-05-01', '2015-06-01'))
  RepositorioDeEventos.obtenerInstancia().agregarEvento(
      Evento(u'Excursión a museo'))

def lanzarWebapp():
  app.debug = True
  app.run()

if __name__ == '__main__':
  cargarDatosDePrueba()
  lanzarWebapp()
