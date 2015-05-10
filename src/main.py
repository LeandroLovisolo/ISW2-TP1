#!/usr/bin/env python2
# coding: utf-8

from flask import Flask, request, redirect, url_for, render_template
from app.campania import Campania
from app.evento import Evento
from app.repositorio_de_eventos import RepositorioDeEventos

app = Flask(__name__)

@app.route('/')
def home():
  return render_template('home.html')

################################################################################
# Campañas                                                                     #
################################################################################

@app.route('/campanias')
def campanias():
  repositorio_de_eventos = RepositorioDeEventos.obtenerInstancia()
  lista_de_campanias = []
  for evento in repositorio_de_eventos.eventos():
    for campania in evento.campanias():
      lista_de_campanias += [{'nombre' : campania.nombre(), 
                            'fechaInicio' : campania.fechaInicio(),
                            'fechaFinal' : campania.fechaFinal(),
                            'codificacion' : str(campania),
                            'evento' : evento.nombre()}]

  return render_template('campanias.html', campanias=lista_de_campanias)

@app.route('/campanias/crear', methods=['GET', 'POST'])
def crear_campania():
  # Mostrar formulario
  if request.method == 'GET':
    eventos = RepositorioDeEventos.obtenerInstancia().eventos()
    eventosStr = []
    for evento in eventos:
      eventosStr.append({'nombre': evento.nombre(), 'id': str(evento)})
    return render_template('crear_campania.html', eventos=eventosStr)

  # Guardar nueva campaña
  else:
    campania = Campania(request.form['nombre'],
                        request.form['fechaInicio'],
                        request.form['fechaFinal'])
    for evento in RepositorioDeEventos.obtenerInstancia().eventos():
      if str(evento) == request.form['idEvento']:
        evento.agregarCampania(campania)
        break
    return redirect(url_for('campanias'))

@app.route('/campanias/<id>', methods=['GET', 'POST'])
def editar_campania(id):
  if request.method == 'POST':
    #Conseguir campaña y editarla
    return 'Campaña editada'
  else:
    #Pasar como parametro campaña
    return render_template('editar_campania.html')

################################################################################
# Mensajes                                                                     #
################################################################################

@app.route('/campanias/<id>/mensajes/')
def messages(id):
  #Conseguir lista de mensajes de la campaña
  #Pasar como parámetro lista de mensajes
  return render_template('mensajes.html')

@app.route('/campanias/<id>/mensajes/crear', methods=['GET', 'POST'])
def messages_add(id):
  if request.method == 'POST':
    #Creo el mensaje y lo agrego al repositorio
    return 'Mensaje agregado'
  else:
    #Le tengo que pasar el número de la campaña
    return render_template('crear_mensaje.html')

@app.route('/campanias/<campania_id>/messages/<mensaje_id>',
           methods=['GET', 'POST'])
def message_edit(campania_id, mensaje_id):
  if request.method == 'POST':
    #Pedir el mensaje del repositorio y editarlo
    return 'Mensaje editado'
  else:
    #Pasar datos del mensaje
    return render_template('editar_mensaje.html')

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
