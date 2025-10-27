"""
ETABS/SAP2000 Wrapper - A Python wrapper for the CSI API.

Simplified interface for interacting with ETABS and SAP2000 via COM, focused on
retrieving table results for structural analysis.

Package Structure:
    - core: Connection management and base functionality
    - results: Analysis results retrieval (tables, forces, displacements)
    - analysis: Analysis operations (future)
    - model: Model manipulation (future)

Supported Applications:
    - ETABS: Use ETABSClient
    - SAP2000: Use SAPClient
"""

from etabs_wrapper.client import ETABSClient
from etabs_wrapper.client import SAPClient
from etabs_wrapper.core import CSIConnectionError
from etabs_wrapper.core import ETABSConnectionError
from etabs_wrapper.core import SAP2000ConnectionError
from etabs_wrapper.core import connect_to_etabs
from etabs_wrapper.core import connect_to_instance
from etabs_wrapper.core import connect_to_sap2000
from etabs_wrapper.core import start_etabs
from etabs_wrapper.core import start_new_instance
from etabs_wrapper.core import start_sap2000

__version__ = "0.1.0"
__all__ = [
    # Clients
    "ETABSClient",
    "SAPClient",
    # Connection functions
    "connect_to_etabs",
    "connect_to_sap2000",
    "start_etabs",
    "start_sap2000",
    # Backward compatibility aliases
    "connect_to_instance",  # Alias for connect_to_etabs
    "start_new_instance",  # Alias for start_etabs
    # Exceptions
    "ETABSConnectionError",
    "SAP2000ConnectionError",
    "CSIConnectionError",
]
