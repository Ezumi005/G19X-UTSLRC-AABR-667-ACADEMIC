"""Capa de adaptadores: traducen fuentes externas al contrato interno V1.

El nucleo del sistema solo conoce la interfaz BaseAdapter y el contrato
(src/contracts); nunca el formato nativo de las fuentes externas.
"""

from src.adapters.base import AdapterReport, AdapterResult, BaseAdapter, Incident
from src.adapters.simulated_crm_adapter import SimulatedCRMAdapter

__all__ = [
    "AdapterReport",
    "AdapterResult",
    "BaseAdapter",
    "Incident",
    "SimulatedCRMAdapter",
]
