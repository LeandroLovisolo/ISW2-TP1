# coding: utf-8

import time
import signal
import sys
from threading import Thread
from mensaje import RepositorioDeMensajes
from emisor_de_sms import EmisorDeSms

class EmisorDeMensajes:
  _instancia = None

  @classmethod
  def obtenerInstancia(cls):
    if cls._instancia == None:
      cls._instancia = EmisorDeMensajes()
    return cls._instancia

  def __init__(self):
    self._lanzarThread()
    self._capturarSigInt()

  def _lanzarThread(self):
    emisorDeMensajes = self
    class worker(Thread):
      def __init__(self):
        Thread.__init__(self)
        self.activo = True
      def run(self):
        while self.activo:
          time.sleep(1)
          emisorDeMensajes.enviarMensajes()
    self._worker = worker()
    self._worker.start()

  def _capturarSigInt(self):
    def handler(signal, frame):
      self._worker.activo = False
      sys.exit(0)
    signal.signal(signal.SIGINT, handler)

  def enviarMensajes(self):
    mensajes = RepositorioDeMensajes.obtenerInstancia().mensajesAEnviarAhora()
    for mensaje in mensajes:
      mensaje.marcarComoEnviado()
      for alumno in mensaje.campania().alumnos():
        EmisorDeSms.obtenerInstancia().enviarSms(alumno.telefono(),
                                                 mensaje.contenido())
