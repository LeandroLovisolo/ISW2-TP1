from campania import Campania

class Evento:
  def __init__(self, unNombre):
    self._nombre = unNombre
    self._campanias = list()

  def nombre(self):
    return self._nombre

  def nombre(self, unNombre):
    self._nombre = unNombre

  def agregarCampania(self, unaCampania):
    self._campanias.append(unaCampania)

  def quitarCampania(self, unaCampania):
    self._campanias.remove(unaCampania)

  def campanias(self):
    return self._campanias
