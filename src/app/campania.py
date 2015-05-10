from repositorio_de_mensajes import RepositorioDeMensajes

class Campania:
  def __init__(self, unNombre, unaFechaInicio, unaFechaFinal):
    self._nombre = unNombre
    self._fechaInicio = unaFechaInicio
    self._fechaFinal = unaFechaFinal

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
