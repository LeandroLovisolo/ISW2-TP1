class Campania:
  def __init__(self, unNombre, unaFechaInicio, unaFechaFinal):
    self._nombre = unNombre
    self._fechaInicio = unaFechaInicio
    self._fechaFinal = unaFechaFinal

  def nombre(self):
    return self._nombre

  def fechaInicio(self):
    return self._fechaInicio

  def fechaFinal(self):
    return self._fechaFinal
