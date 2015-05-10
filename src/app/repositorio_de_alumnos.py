class RepositorioDeAlumnos:
  _instancia = None

  @classmethod
  def obtenerInstancia(cls):
    if cls._instancia == None:
      cls._instancia = RepositorioDeAlumnos()
    return cls._instancia

  def __init__(self):
    self._alumnos = []

  def alumnos(self):
    return self._alumnos

  def agregarAlumno(self, unAlumno):
    self._alumnos.append(unAlumno)

  def quitarAlumno(self, unAlumno):
    self._alumnos.remove(unAlumno)
