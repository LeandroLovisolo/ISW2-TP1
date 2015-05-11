#!/usr/bin/env python2
# coding: utf-8

from flask import Flask, request, redirect, url_for, render_template
from datetime import datetime, timedelta
from app.evento import Evento, RepositorioDeEventos
from app.campania import Campania, PorcentajeDeAprobacion, CriterioDeEficacia
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
      lista_de_campanias.append({
        'nombre': campania.nombre(),
        'fechaInicio': campania.fechaInicio(),
        'fechaFinal': campania.fechaFinal(),
        'codificacion': str(campania),
        'evento': evento.nombre(),
        'criterioEficacia': campania.criterioDeEficacia()
                                    .__doc__.decode('utf-8'),
        'medicionEficacia': campania.criterioDeEficacia().medicion()})

  return render_template('campanias.html', campanias=lista_de_campanias)

@app.route('/campanias/comparar/<id_una>/<id_otra>', methods=['GET'])
def comparar_campanias(id_una, id_otra):
  una = None
  otra = None

  for evento in RepositorioDeEventos.obtenerInstancia().eventos():
    for campania in evento.campanias():
      if str(campania) == id_una:
        una = campania
      if str(campania) == id_otra:
        otra = campania

  if una is None: return 'La primera campaña no existe.'
  if otra is None: return 'La segunda campaña no existe.'

  try:
    resultado = una.criterioDeEficacia().compararCon(otra.criterioDeEficacia())
  except TypeError:
    return 'Las campañas seleccionadas no se pueden comparar entre sí.'

  if resultado < 0:
    return 'La campaña ' + otra.nombre() + ' es la más eficaz.'
  if resultado == 0:
    return 'Ambas campañas son igual de eficaces.'
  if resultado > 0:
    return 'La campaña ' + una.nombre() + ' es la más eficaz.'

@app.route('/campanias/crear', methods=['GET', 'POST'])
def crear_campania():
  # Mostrar formulario
  if request.method == 'GET':
    alumnos = RepositorioDeAlumnos.obtenerInstancia().alumnos()
    eventos = RepositorioDeEventos.obtenerInstancia().eventos()
    lista_de_alumnos = []
    for alumno in alumnos:
      lista_de_alumnos += [{'nombre' : alumno.nombre(),
                            'id' : str(alumno)}]
    eventosStr = []
    for evento in eventos:
      eventosStr.append({'nombre': evento.nombre(), 'id': str(evento)})

    criteriosStr = []
    subclases = CriterioDeEficacia.__subclasses__()
    for subclase in subclases:
      criteriosStr.append({'nombre' : subclase.__name__.decode('utf-8'), 
        'descripcion' : subclase.__doc__.decode('utf-8')})

    return render_template('crear_campania.html', eventos=eventosStr, 
      alumnos=lista_de_alumnos, criterios=criteriosStr)

  # Guardar nueva campaña
  else:
    subclases = CriterioDeEficacia.__subclasses__()
    for subclase in subclases:
      if subclase.__name__ == request.form['criterio']:
        eficacia = subclase(0)

    campania = Campania(request.form['nombre'],
                        request.form['fechaInicio'],
                        request.form['fechaFinal'],
                        eficacia)

    alumnos = RepositorioDeAlumnos.obtenerInstancia().alumnos()
    select_alumnos = request.form.getlist('alumnos')
    for alumno in alumnos:
      if str(alumno) in select_alumnos:
        campania.agregarAlumno(alumno)

    for evento in RepositorioDeEventos.obtenerInstancia().eventos():
      if str(evento) == request.form['idEvento']:
        evento.agregarCampania(campania)
        break
    return redirect(url_for('mensajes', id=str(campania)))

@app.route('/campanias/<id>', methods=['GET', 'POST'])
def editar_campania(id):
  eventos = RepositorioDeEventos.obtenerInstancia().eventos()
  alumnos = RepositorioDeAlumnos.obtenerInstancia().alumnos()
  if request.method == 'POST':
    for evento in eventos:
      for campania in evento.campanias():
        if str(campania) == id:
          campania.nombre(request.form['nombre'])
          campania.fechaInicio(request.form['fechaInicio'])
          campania.fechaFinal(request.form['fechaFinal'])
          # Quito todos los alumnos
          for alumno in campania.alumnos():
            campania.quitarAlumno(alumno)
          # Agrego todos los alumnos seleccionados
          select_alumnos = request.form.getlist('alumnos')
          for alumno in alumnos:
            if str(alumno) in select_alumnos:
              campania.agregarAlumno(alumno)

          eficacia = campania.criterioDeEficacia()
          eficacia.medicion(request.form['medicion'])

    return redirect(url_for('campanias'))

  else:
    campaniaStr = None
    for evento in eventos:
      for campania in evento.campanias():
        if str(campania) == id:
          idAlumnosCampania = []
          for alumno in campania.alumnos():
            idAlumnosCampania.append(str(alumno))

          campaniaStr = {'nombre' : campania.nombre(),
                        'fechaInicio' : campania.fechaInicio(),
                        'fechaFinal' : campania.fechaFinal(),
                        'nombreEvento' : evento.nombre(),
                        'alumnos' : idAlumnosCampania,
                        'nombreCriterio' : 
                        campania.criterioDeEficacia().__class__.__name__}
          break
    alumnosSrt = []
    alumnos = RepositorioDeAlumnos.obtenerInstancia().alumnos()
    for alumno in alumnos:
      alumnosSrt.append({'id' : str(alumno), 'nombre' : alumno.nombre()})

    return render_template('editar_campania.html',
      campania=campaniaStr, alumnos=alumnosSrt)

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
    try:
      fecha = datetime.strptime(request.form['fecha'], '%Y-%m-%d %H:%M:%S')
    except ValueError:
      return 'Fecha inválida.'
    mensaje = Mensaje(campania, fecha, request.form['contenido'])
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
  c = Campania('Recordatorios v1', '2015-05-01', '2015-06-01',
               PorcentajeDeAprobacion(75))
  c.agregarAlumno(a1)
  c.agregarAlumno(a2)
  e.agregarCampania(c)
  e.agregarCampania(Campania('Recordatorios v2', '2015-05-01', '2015-06-01',
                             PorcentajeDeAprobacion(0)))

  # Mensajes
  RepositorioDeMensajes.obtenerInstancia().agregarMensaje(
      Mensaje(c, datetime.now() + timedelta(seconds=5), 'Primer mensaje'))
  RepositorioDeMensajes.obtenerInstancia().agregarMensaje(
      Mensaje(c, datetime.now() + timedelta(seconds=10), 'Segundo mensaje'))
  RepositorioDeMensajes.obtenerInstancia().agregarMensaje(
      Mensaje(c, datetime.now() + timedelta(seconds=15), 'Tercer mensaje'))

def lanzarWebapp():
  app.run(debug=True, use_debugger=True, use_reloader=False)

if __name__ == '__main__':
  print 'Sistema de recordatorios escolares por SMS'
  cargarDatosDePrueba()
  EmisorDeMensajes.obtenerInstancia() # Se crea tras la primera solicitud
  lanzarWebapp()
