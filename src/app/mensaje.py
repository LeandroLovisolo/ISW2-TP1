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
