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
