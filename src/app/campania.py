from repositorio_de_mensajes import RepositorioDeMensajes

class Campania:
  def __init__(self, unNombre, unaFechaInicio, unaFechaFinal):
    self._nombre = unNombre
    self._fechaInicio = unaFechaInicio
    self._fechaFinal = unaFechaFinal
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


class Eficacia:
    def __init__(self, unCriterio, unaMedicion):
      self._criterio = unCriterio
      self._medicion = unaMedicion

    def compararCon(self, unResultado):
      raise NotImplementedError()

    def criterio(self, unCriterio = None):
      if unCriterio is None:
        return self._criterio
      else:
        self._criterio = unCriterio

    def medicion(self, unaMedicion = None):
      if unaMedicion is None:
        return self._medicion
      else:
        self._medicion = unaMedicion

class PorcentajeDeAprobacion(Eficacia):
  def __init__(self, unCriterio, unaMedicion):
    super().__init__(unCriterio, unaMedicion)

  def compararCon(self, unResultado):
    if type(unResultado) != type(self):
      raise TypeError()

    if self._medicion > unResultado._medicion:
      return 1
    elif self._medicion == unResultado._medicion:
      return 0
    else:
      return -1

class CantidadDeDesaprobados(Eficacia):
  def __init__(self, unCriterio, unaMedicion):
    super().__init__(unCriterio, unaMedicion)
  def compararCon(self, unResultado):
    if type(unResultado) != type(self):
      raise TypeError()

    if self._medicion < unResultado._medicion:
      return 1
    elif self._medicion == unResultado._medicion:
      return 0
    else:
      return -1