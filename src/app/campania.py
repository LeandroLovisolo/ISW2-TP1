# coding: utf-8

from repositorio_de_mensajes import RepositorioDeMensajes

class Campania:
  def __init__(self, unNombre, unaFechaInicio, unaFechaFinal,
               unCriterioDeEficacia):
    self._nombre = unNombre
    self._fechaInicio = unaFechaInicio
    self._fechaFinal = unaFechaFinal
    self._criterioDeEficacia = unCriterioDeEficacia
    self._alumnos = []

  def nombre(self, unNombre = None):
    if unNombre is None:
      return self._nombre
    else:
      self._nombre = unNombre

  def fechaInicio(self, unaFechaInicio = None):
    if unaFechaInicio is None:
      return self._fechaInicio
    else:
      self._fechaInicio = unaFechaInicio

  def fechaFinal(self, unaFechaFinal = None):
    if unaFechaFinal is None:
      return self._fechaFinal
    else:
      self._fechaFinal = unaFechaFinal

  def mensajes(self):
    return RepositorioDeMensajes.obtenerInstancia().mensajesAsignadosA(self)

  def alumnos(self):
    return self._alumnos

  def agregarAlumno(self, unAlumno):
    self._alumnos.append(unAlumno)

  def quitarAlumno(self, unAlumno):
    self._alumnos.remove(unAlumno)

  def criterioDeEficacia(self):
    return self._criterioDeEficacia

################################################################################

class CriterioDeEficacia(object):
  def __init__(self, unaMedicion):
    self._medicion = unaMedicion

  def medicion(self, unaMedicion = None):
    if unaMedicion is None:
      return self._medicion
    else:
      self._medicion = unaMedicion

  def compararCon(self, otroCriterio):
    raise NotImplementedError()

class PorcentajeDeAprobacion(CriterioDeEficacia):
  '''Porcentaje de aprobación'''

  def compararCon(self, otroCriterio):
    if not isinstance(otroCriterio, PorcentajeDeAprobacion):
      raise TypeError()

    if self._medicion < otroCriterio.medicion():
      return -1
    if self._medicion == otroCriterio.medicion():
      return 0
    return 1

class CantidadDeDesaprobados(CriterioDeEficacia):
  '''Cantidad de desaprobados'''

  def compararCon(self, otroCriterio):
    if not isinstance(otroCriterio, CantidadDeDesaprobados):
      raise TypeError()

    if self._medicion < otroCriterio.medicion():
      return -1
    if self._medicion == otroCriterio.medicion():
      return 0
    return 1
