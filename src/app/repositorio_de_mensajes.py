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
