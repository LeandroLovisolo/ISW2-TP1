#!/usr/bin/env python2
# coding: utf-8

from flask import Flask, request, redirect, url_for, render_template
from datetime import datetime, timedelta
from app.evento import Evento, RepositorioDeEventos
from app.campania import Campania
from app.mensaje import Mensaje, RepositorioDeMensajes
from app.alumno import Alumno, RepositorioDeAlumnos
from app.emisor_de_mensajes import EmisorDeMensajes

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
    return redirect(url_for('mensajes', id=str(campania)))

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
def mensajes(id):
  lista_de_mensajes = []
  nombre_campania = None
  repositorio_de_mensajes = RepositorioDeMensajes.obtenerInstancia()
  repositorio_de_eventos = RepositorioDeEventos.obtenerInstancia()
  for evento in repositorio_de_eventos.eventos():
    for campania in evento.campanias():
      if str(campania) == id:
        nombre_campania = campania.nombre()

  for mensaje in repositorio_de_mensajes.mensajes():
    if str(mensaje.campania()) == id:
      lista_de_mensajes += [{'fecha' : mensaje.fecha(),
                            'contenido' : mensaje.contenido()}]

  return render_template('mensajes.html', mensajes=lista_de_mensajes, id=id, 
    nombre_campania=nombre_campania)

@app.route('/campanias/<id>/mensajes/crear', methods=['GET', 'POST'])
def crear_mensaje(id):
  # Mostrar formulario
  if request.method == 'GET':
    return render_template('crear_mensaje.html', idCampania=id)

  # Guardar nuevo mensaje
  else:
    # Obtener campaña correspondiente
    campania = None
    for evento in RepositorioDeEventos.obtenerInstancia().eventos():
      for _campania in evento.campanias():
        if str(_campania) == request.form['idCampania']:
          campania = _campania
          break

    if campania is None:
        raise Exception('Campaña inexistente')

    # Crear nuevo mensaje
    mensaje = Mensaje(campania,
                      request.form['fecha'],
                      request.form['contenido'])
    RepositorioDeMensajes.obtenerInstancia().agregarMensaje(mensaje)

    return redirect(url_for('mensajes', id=str(campania)))

################################################################################
# Bootstrap de la aplicación                                                   #
################################################################################

def cargarDatosDePrueba():
  # Alumnos
  a1 = Alumno(11111111, 'Juancito', '15-0000-0000')
  a2 = Alumno(22222222, 'Pepito',   '15-1111-1111')
  RepositorioDeAlumnos.obtenerInstancia().agregarAlumno(a1)
  RepositorioDeAlumnos.obtenerInstancia().agregarAlumno(a2)
  RepositorioDeAlumnos.obtenerInstancia().agregarAlumno(
      Alumno(33333333, 'Anita', '15-0303-456'))

  # Eventos
  e = Evento('Prueba de historia')
  RepositorioDeEventos.obtenerInstancia().agregarEvento(e)
  RepositorioDeEventos.obtenerInstancia().agregarEvento(
      Evento(u'Excursión a museo'))

  # Campañas
  c = Campania('Recordatorios v1', '2015-05-01', '2015-06-01')
  c.agregarAlumno(a1)
  c.agregarAlumno(a2)
  e.agregarCampania(c)
  e.agregarCampania(Campania('Recordatorios v2', '2015-05-01', '2015-06-01'))

  # Mensajes
  RepositorioDeMensajes.obtenerInstancia().agregarMensaje(
      Mensaje(c, datetime.now() + timedelta(seconds=5), 'Primer mensaje'))
  RepositorioDeMensajes.obtenerInstancia().agregarMensaje(
      Mensaje(c, datetime.now() + timedelta(seconds=10), 'Segundo mensaje'))
  RepositorioDeMensajes.obtenerInstancia().agregarMensaje(
      Mensaje(c, datetime.now() + timedelta(seconds=15), 'Tercer mensaje'))

def lanzarWebapp():
  app.run()

if __name__ == '__main__':
  cargarDatosDePrueba()
  EmisorDeMensajes.obtenerInstancia() # Se crea tras la primera solicitud
  lanzarWebapp()
