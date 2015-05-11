# coding: utf-8

from datetime import datetime

class EmisorDeSms:
  _instancia = None

  @classmethod
  def obtenerInstancia(cls):
    if cls._instancia == None:
      cls._instancia = EmisorDeSms()
    return cls._instancia

  def enviarSms(self, unTelefono, unContenido):
    print '=================================================='
    print 'Enviando SMS...'
    print 'Fecha y hora: %s' % datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print 'Teléfono:     %s' % unTelefono
    print 'Contenido:'
    print unContenido
    print '=================================================='
    print ''
