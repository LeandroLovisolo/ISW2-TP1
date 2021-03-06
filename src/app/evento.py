from campania import Campania

class Evento:
  def __init__(self, unNombre):
    self._nombre = unNombre
    self._campanias = list()

  def nombre(self, unNombre = None):
    if unNombre == None:
      return self._nombre
    else:
      self._nombre = unNombre

  def agregarCampania(self, unaCampania):
    self._campanias.append(unaCampania)

  def quitarCampania(self, unaCampania):
    self._campanias.remove(unaCampania)

  def campanias(self):
    return self._campanias

class RepositorioDeEventos:
  _instancia = None

  @classmethod
  def obtenerInstancia(cls):
    if cls._instancia == None:
      cls._instancia = RepositorioDeEventos()
    return cls._instancia

  def __init__(self):
    self._eventos = []

  def eventos(self):
    return self._eventos

  def agregarEvento(self, unEvento):
    self._eventos.append(unEvento)

  def quitarEvento(self, unEvento):
    self._eventos.remove(unEvento)
