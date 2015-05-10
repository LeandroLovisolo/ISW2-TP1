class Mensaje:
  def __init__(self, unaCampania, unaFecha, unContenido):
    self._campania = unaCampania
    self._fecha = unaFecha
    self._contenido = unContenido

  def campania(self):
    return self._campania

  def fecha(self, unaFecha = None):
    if unaFecha is None:
      return self._fecha
    else:
      self._fecha = unaFecha

  def contenido(self, unContenido = None):
    if unContenido is None:
      return self._contenido
    else:
      self._contenido = unContenido

class RepositorioDeMensajes:
  _instancia = None

  @classmethod
  def obtenerInstancia(cls):
    if cls._instancia == None:
      cls._instancia = RepositorioDeMensajes()
    return cls._instancia

  def __init__(self):
    self._mensajes = []

  def mensajes(self):
    return self._mensajes

  def mensajesAsignadosA(self, unaCampania):
    return filter(lambda m: m.campania() == unaCampania, self._mensajes)

  def agregarMensaje(self, unMensaje):
    self._mensajes.append(unMensaje)

  def quitarMensaje(self, unMensaje):
    self._mensajes.remove(unMensaje)
