# coding: utf-8

from datetime import datetime

class Mensaje:
  def __init__(self, unaCampania, unaFecha, unContenido):
    self._campania = unaCampania
    self._fecha = unaFecha
    self._contenido = unContenido
    self._estado = MensajeNoEnviado(self)

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

  def marcarComoEnviado(self):
    self._estado = MensajeEnviado(self)

  def aceptar(self, unVisitadorDeMensajes):
    self._estado.aceptar(unVisitadorDeMensajes)

################################################################################

class VisitadorDeMensajesAEnviarAhora:
  def __init__(self):
    self._mensajes = []

  def visitarMensajeNoEnviado(self, unMensajeNoEnviado):
    if unMensajeNoEnviado.fecha() < datetime.now():
      self._mensajes.append(unMensajeNoEnviado)

  def visitarMensajeEnviado(self, unMensajeEnviado):
    # No me interesan los mensajes enviados, así que no hago nada
    pass

  def mensajesAEnviarAhora(self):
    return self._mensajes

################################################################################

class EstadoDeMensaje:
  def __init__(self, unMensaje):
    self._mensaje = unMensaje

  def aceptar(self, unVisitadorDeMensajes):
    raise NotImplementedError()

class MensajeNoEnviado(EstadoDeMensaje):
  def aceptar(self, unVisitadorDeMensajes):
    unVisitadorDeMensajes.visitarMensajeNoEnviado(self._mensaje)

class MensajeEnviado(EstadoDeMensaje):
  def aceptar(self, unVisitadorDeMensajes):
    unVisitadorDeMensajes.visitarMensajeEnviado(self._mensaje)

################################################################################

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

  def mensajesAEnviarAhora(self):
    visitador = VisitadorDeMensajesAEnviarAhora()
    for mensaje in self._mensajes:
      mensaje.aceptar(visitador)
    return visitador.mensajesAEnviarAhora()

  def agregarMensaje(self, unMensaje):
    self._mensajes.append(unMensaje)

  def quitarMensaje(self, unMensaje):
    self._mensajes.remove(unMensaje)
