from campania import Campania

class Evento():
  def __init__(self, unNombre, unAutor):
    self._nombre = unNombre
    self._autor = unAutor
    self._campanias = list()

  def nombre():
    return self._nombre

  def nombre(unNombre):
    self._nombre = unNombre

  def agregarCampania(unaCampania):
    self._campanias.append(unaCampania)

  def quitarCampania(unaCampania):
    self._campanias.remove(unaCampania)

  def campanias():
    return self._campanias