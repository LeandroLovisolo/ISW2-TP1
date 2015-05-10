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
      return _telefono
    else:
      self._telefono = unTelefono
