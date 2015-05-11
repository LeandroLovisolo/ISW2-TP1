#!/usr/bin/env python2
# coding: utf-8

from flask import Flask, request, redirect, url_for, render_template
from app.evento import Evento, RepositorioDeEventos
from app.campania import Campania
from app.mensaje import Mensaje, RepositorioDeMensajes
from app.alumno import Alumno, RepositorioDeAlumnos

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
                            'evento' : evento.nombre(),
                            'criterioEficacia' : campania.eficacia().criterio(),
                            'medicionEficacia' : campania.eficacia().medicion()}]

  return render_template('campanias.html', campanias=lista_de_campanias)

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
    return render_template('crear_campania.html', eventos=eventosStr, 
      alumnos=lista_de_alumnos)

  # Guardar nueva campaña
  else:
    campania = Campania(request.form['nombre'],
                        request.form['fechaInicio'],
                        request.form['fechaFinal'])
    eficacia = campania.eficacia()
    eficacia.criterio(request.form['criterio'])
    eficacia.medicion(0)

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
          eficacia = campania.eficacia()
          eficacia.criterio(request.form['criterio'])
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
                        'alumnos' : idAlumnosCampania}
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
    mensaje = Mensaje(campania,
                      request.form['fecha'],
                      request.form['contenido'])
    RepositorioDeMensajes.obtenerInstancia().agregarMensaje(mensaje)

    return redirect(url_for('mensajes', id=str(campania)))

def cargarDatosDePrueba():
  # Alumnos
  r = RepositorioDeAlumnos.obtenerInstancia()
  r.agregarAlumno(Alumno(11111111, 'Juancito', '15-0000-0000'))
  r.agregarAlumno(Alumno(22222222, 'Pepito',   '15-1111-1111'))
  r.agregarAlumno(Alumno(33333333, 'Anita',    '15-0303-456'))

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
