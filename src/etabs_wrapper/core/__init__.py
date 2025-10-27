"""
Core functionality for ETABS/SAP2000 wrapper.

Contains connection management and base client classes.
"""

from etabs_wrapper.core.base_client import BaseCSIClient
from etabs_wrapper.core.connection import CSIConnectionError
from etabs_wrapper.core.connection import ETABSConnectionError
from etabs_wrapper.core.connection import SAP2000ConnectionError
from etabs_wrapper.core.connection import connect_to_etabs
from etabs_wrapper.core.connection import connect_to_instance
from etabs_wrapper.core.connection import connect_to_sap2000
from etabs_wrapper.core.connection import start_etabs
from etabs_wrapper.core.connection import start_new_instance
from etabs_wrapper.core.connection import start_sap2000

__all__ = [
    "BaseCSIClient",
    "connect_to_etabs",
    "connect_to_sap2000",
    "start_etabs",
    "start_sap2000",
    "connect_to_instance",  # Alias for connect_to_etabs
    "start_new_instance",  # Alias for start_etabs
    "ETABSConnectionError",
    "SAP2000ConnectionError",
    "CSIConnectionError",
]
