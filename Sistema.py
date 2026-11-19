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
