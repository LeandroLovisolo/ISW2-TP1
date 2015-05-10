class Mensajes:
	def __init__(self, unaCampania, unaFecha, unContenido):
		self._campania = unaCampania
		self._fecha = unaFecha
		self._contenido = unContenido

	def campania(self):
		return self._campania

	def fecha(self, unaFecha = None):
		if unaFecha == None:
			return self._fecha
		else:
			_fecha = unaFecha

	def contenido(self, unContenido = None):
		if unContenido == None:
			return _contenido
		else:
			_contenido = unContenido