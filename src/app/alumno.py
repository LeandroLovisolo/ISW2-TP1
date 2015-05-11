class Alumno:
  def __init__(self, unDni, unNombre, unTelefono):
    self._dni = unDni
    self._nombre = unNombre
    self._telefono = unTelefono

  def dni(self, unDni = None):
    if unDni is None:
      return self._dni
    else:
      self._dni = unDni

  def nombre(self, unNombre = None):
    if unNombre is None:
      return _nombre
    else:
      self._nombre = unNombre

  def telefono(self, unTelefono = None):
    if unTelefono is None:
      return self._telefono
    else:
      self._telefono = unTelefono

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
