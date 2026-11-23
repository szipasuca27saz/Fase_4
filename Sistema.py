SoftwareFJ/
│
├── main.py
├── entidades.py
├── excepciones.py
├── clientes.py
├── servicios.py
├── reservas.py
├── gestor.py
├── logger.py
│
└── logs/
    └── sistema.log

class SoftwareFJError(Exception):
    """Excepción base del sistema."""
    pass


class ClienteInvalidoError(SoftwareFJError):
    """Error relacionado con datos inválidos de clientes."""
    pass


class ClienteNoEncontradoError(SoftwareFJError):
    """El cliente solicitado no existe."""
    pass


class ServicioInvalidoError(SoftwareFJError):
    """Error relacionado con un servicio."""
    pass


class ServicioNoDisponibleError(SoftwareFJError):
    """El servicio no está disponible."""
    pass


class ReservaInvalidaError(SoftwareFJError):
    """Error relacionado con una reserva."""
    pass


class ReservaNoEncontradaError(SoftwareFJError):
    """La reserva no existe."""
    pass


class OperacionNoPermitidaError(SoftwareFJError):
    """La operación solicitada no está permitida."""
    pass


class ParametroFaltanteError(SoftwareFJError):
    """Falta un parámetro requerido."""
    pass

import logging
import os


def configurar_logger():

    os.makedirs("logs", exist_ok=True)

    logging.basicConfig(
        filename="logs/sistema.log",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        encoding="utf-8"
    )


def registrar_evento(mensaje):
    logging.info(mensaje)


def registrar_error(mensaje):
    logging.error(mensaje)

from abc import ABC, abstractmethod


class Entidad(ABC):

    def __init__(self, identificador):
        self.__identificador = identificador

    @property
    def identificador(self):
        return self.__identificador

    @abstractmethod
    def mostrar_informacion(self):
        pass

import re
from entidades import Entidad
from excepciones import ClienteInvalidoError


class Cliente(Entidad):

    def __init__(self, identificador, nombre, documento, correo, telefono):

        super().__init__(identificador)

        if not nombre or not nombre.strip():
            raise ClienteInvalidoError(
                "El nombre del cliente no puede estar vacío."
            )

        if not documento.isdigit():
            raise ClienteInvalidoError(
                "El documento debe contener solamente números."
            )

        patron_correo = r"^[^@]+@[^@]+\.[^@]+$"

        if not re.match(patron_correo, correo):
            raise ClienteInvalidoError(
                "El correo electrónico no tiene un formato válido."
            )

        if not telefono.isdigit():
            raise ClienteInvalidoError(
                "El teléfono debe contener solamente números."
            )

        self.__nombre = nombre
        self.__documento = documento
        self.__correo = correo
        self.__telefono = telefono

    @property
    def nombre(self):
        return self.__nombre

    @property
    def documento(self):
        return self.__documento

    @property
    def correo(self):
        return self.__correo

    @property
    def telefono(self):
        return self.__telefono

    def mostrar_informacion(self):

        return (
            f"Cliente #{self.identificador} | "
            f"Nombre: {self.nombre} | "
            f"Documento: {self.documento} | "
            f"Correo: {self.correo} | "
            f"Teléfono: {self.telefono}"
        )

    def __str__(self):
        return self.mostrar_informacion()

from abc import abstractmethod
from entidades import Entidad
from excepciones import (
    ServicioInvalidoError,
    ParametroFaltanteError
)


class Servicio(Entidad):

    def __init__(self, identificador, nombre, precio_base):

        super().__init__(identificador)

        if not nombre or not nombre.strip():
            raise ServicioInvalidoError(
                "El nombre del servicio es obligatorio."
            )

        if precio_base <= 0:
            raise ServicioInvalidoError(
                "El precio base debe ser mayor que cero."
            )

        self.__nombre = nombre
        self.__precio_base = precio_base
        self.__disponible = True

    @property
    def nombre(self):
        return self.__nombre

    @property
    def precio_base(self):
        return self.__precio_base

    @property
    def disponible(self):
        return self.__disponible

    def cambiar_disponibilidad(self, estado):

        if not isinstance(estado, bool):
            raise ServicioInvalidoError(
                "La disponibilidad debe ser True o False."
            )

        self.__disponible = estado

    @abstractmethod
    def calcular_costo(self, duracion, descuento=0, impuesto=0):
        pass

    @abstractmethod
    def validar_parametros(self, duracion):
        pass

    @abstractmethod
    def describir(self):
        pass

    def mostrar_informacion(self):

        estado = "Disponible" if self.disponible else "No disponible"

        return (
            f"Servicio #{self.identificador} | "
            f"{self.nombre} | "
            f"Precio base: ${self.precio_base:,.2f} | "
            f"Estado: {estado}"
        )


class ReservaSala(Servicio):

    def __init__(
        self,
        identificador,
        nombre,
        precio_base,
        capacidad
    ):

        super().__init__(
            identificador,
            nombre,
            precio_base
        )

        if capacidad <= 0:
            raise ServicioInvalidoError(
                "La capacidad debe ser mayor que cero."
            )

        self.__capacidad = capacidad

    def validar_parametros(self, duracion):

        if duracion <= 0:
            raise ParametroFaltanteError(
                "La duración debe ser mayor que cero."
            )

        return True

    def calcular_costo(
        self,
        duracion,
        descuento=0,
        impuesto=0
    ):

        self.validar_parametros(duracion)

        subtotal = self.precio_base * duracion

        subtotal -= subtotal * (descuento / 100)

        total = subtotal + subtotal * (impuesto / 100)

        return total

    def describir(self):

        return (
            f"Sala para reuniones. "
            f"Capacidad: {self.__capacidad} personas."
        )


class AlquilerEquipo(Servicio):

    def __init__(
        self,
        identificador,
        nombre,
        precio_base,
        tipo_equipo
    ):

        super().__init__(
            identificador,
            nombre,
            precio_base
        )

        if not tipo_equipo:
            raise ServicioInvalidoError(
                "Debe especificarse el tipo de equipo."
            )

        self.__tipo_equipo = tipo_equipo

    def validar_parametros(self, duracion):

        if duracion <= 0:
            raise ParametroFaltanteError(
                "Las horas de alquiler deben ser mayores que cero."
            )

        return True

    def calcular_costo(
        self,
        duracion,
        descuento=0,
        impuesto=0
    ):

        self.validar_parametros(duracion)

        subtotal = self.precio_base * duracion

        # Descuento adicional para alquileres prolongados
        if duracion >= 8:
            subtotal *= 0.90

        subtotal -= subtotal * (descuento / 100)

        total = subtotal + subtotal * (impuesto / 100)

        return total

    def describir(self):

        return (
            f"Alquiler de equipo tecnológico. "
            f"Tipo: {self.__tipo_equipo}."
        )


class AsesoriaEspecializada(Servicio):

    def __init__(
        self,
        identificador,
        nombre,
        precio_base,
        especialidad
    ):

        super().__init__(
            identificador,
            nombre,
            precio_base
        )

        if not especialidad:
            raise ServicioInvalidoError(
                "La especialidad es obligatoria."
            )

        self.__especialidad = especialidad

    def validar_parametros(self, duracion):

        if duracion <= 0:
            raise ParametroFaltanteError(
                "La duración de la asesoría debe ser mayor que cero."
            )

        return True

    def calcular_costo(
        self,
        duracion,
        descuento=0,
        impuesto=0
    ):

        self.validar_parametros(duracion)

        # Las asesorías tienen tarifa diferente
        subtotal = self.precio_base * duracion

        subtotal -= subtotal * (descuento / 100)

        total = subtotal + subtotal * (impuesto / 100)

        return total

    def describir(self):

        return (
            f"Asesoría especializada en "
            f"{self.__especialidad}."
        )

from excepciones import (
    ReservaInvalidaError,
    ServicioNoDisponibleError,
    OperacionNoPermitidaError
)


class Reserva:

    ESTADOS_VALIDOS = [
        "PENDIENTE",
        "CONFIRMADA",
        "CANCELADA",
        "FINALIZADA"
    ]

    def __init__(
        self,
        identificador,
        cliente,
        servicio,
        duracion
    ):

        if cliente is None:
            raise ReservaInvalidaError(
                "La reserva necesita un cliente."
            )

        if servicio is None:
            raise ReservaInvalidaError(
                "La reserva necesita un servicio."
            )

        if duracion <= 0:
            raise ReservaInvalidaError(
                "La duración debe ser mayor que cero."
            )

        if not servicio.disponible:
            raise ServicioNoDisponibleError(
                "El servicio seleccionado no está disponible."
            )

        self.__identificador = identificador
        self.__cliente = cliente
        self.__servicio = servicio
        self.__duracion = duracion
        self.__estado = "PENDIENTE"
        self.__costo = 0

    @property
    def identificador(self):
        return self.__identificador

    @property
    def cliente(self):
        return self.__cliente

    @property
    def servicio(self):
        return self.__servicio

    @property
    def duracion(self):
        return self.__duracion

    @property
    def estado(self):
        return self.__estado

    @property
    def costo(self):
        return self.__costo

    def confirmar(self):

        if self.__estado != "PENDIENTE":
            raise OperacionNoPermitidaError(
                "Solo se pueden confirmar reservas pendientes."
            )

        self.__estado = "CONFIRMADA"

    def cancelar(self):

        if self.__estado == "FINALIZADA":
            raise OperacionNoPermitidaError(
                "No se puede cancelar una reserva finalizada."
            )

        if self.__estado == "CANCELADA":
            raise OperacionNoPermitidaError(
                "La reserva ya está cancelada."
            )

        self.__estado = "CANCELADA"

    def procesar(self, descuento=0, impuesto=19):

        if self.__estado != "CONFIRMADA":
            raise OperacionNoPermitidaError(
                "La reserva debe estar confirmada antes de procesarse."
            )

        try:

            self.__costo = self.__servicio.calcular_costo(
                self.__duracion,
                descuento,
                impuesto
            )

        except Exception as error:

            raise ReservaInvalidaError(
                "No fue posible calcular el costo de la reserva."
            ) from error

        self.__estado = "FINALIZADA"

        return self.__costo

    def mostrar_informacion(self):

        return (
            f"Reserva #{self.identificador} | "
            f"Cliente: {self.cliente.nombre} | "
            f"Servicio: {self.servicio.nombre} | "
            f"Duración: {self.duracion} | "
            f"Estado: {self.estado} | "
            f"Costo: ${self.costo:,.2f}"
        )

    def __str__(self):
        return self.mostrar_informacion()
