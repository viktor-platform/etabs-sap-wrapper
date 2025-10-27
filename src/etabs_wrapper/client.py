"""
Client classes for ETABS and SAP2000.

Provides high-level interfaces for interacting with both CSI applications.
"""

from etabs_wrapper.core.base_client import BaseCSIClient
from etabs_wrapper.core.connection import close_etabs_instance
from etabs_wrapper.core.connection import close_sap2000_instance
from etabs_wrapper.core.connection import connect_to_etabs
from etabs_wrapper.core.connection import connect_to_sap2000
from etabs_wrapper.core.connection import start_etabs
from etabs_wrapper.core.connection import start_sap2000


class ETABSClient(BaseCSIClient):
    """
    Client for interacting with ETABS.

    This class provides a high-level interface to ETABS functionality.
    Organized into submodules:
    - results: Retrieve analysis results (tables, forces, displacements)
    - analysis: Run analysis and manage load cases (future)
    - model: Model manipulation and properties (future)

    Attributes:
        results: Results retrieval operations
            - tables: TableResults instance for retrieving table data
    """

    def __init__(self, sap_model):
        """
        Initialize ETABSClient with a SapModel object.

        Args:
            sap_model: ETABS SapModel COM object

        Note:
            Typically you won't call this directly. Use class methods
            `from_running_instance()` or `start_new_instance()` instead.
        """
        super().__init__(sap_model, "ETABS")

    @classmethod
    def from_running_instance(cls) -> "ETABSClient":
        """
        Connect to a currently running ETABS instance.

        Returns:
            ETABSClient connected to running instance

        Raises:
            ETABSConnectionError: If connection fails

        Example:
            >>> client = ETABSClient.from_running_instance()
            >>> df = client.results.tables.element_forces_frames(load_cases=["DEAD"])
        """
        model = connect_to_etabs()
        return cls(model)

    @classmethod
    def start_new_instance(cls) -> "ETABSClient":
        """
        Start a new ETABS instance.

        Returns:
            ETABSClient with new ETABS instance

        Raises:
            ETABSConnectionError: If ETABS cannot be started

        Example:
            >>> client = ETABSClient.start_new_instance()
            >>> # Load a model, run analysis, etc.
        """
        model = start_etabs()
        return cls(model)

    @classmethod
    def close_etabs(cls) -> None:
        """
        Close the ETABS instance.

        Returns:
            None
        """
        close_etabs_instance()


class SAPClient(BaseCSIClient):
    """
    Client for interacting with SAP2000.

    This class provides a high-level interface to SAP2000 functionality.
    Organized into submodules:
    - results: Retrieve analysis results (tables, forces, displacements)
    - analysis: Run analysis and manage load cases (future)
    - model: Model manipulation and properties (future)

    Attributes:
        results: Results retrieval operations
            - tables: TableResults instance for retrieving table data

    Note:
        SAP2000 uses the same COM API as ETABS, so all table methods
        and result retrieval work identically.
    """

    def __init__(self, sap_model):
        """
        Initialize SAPClient with a SapModel object.

        Args:
            sap_model: SAP2000 SapModel COM object

        Note:
            Typically you won't call this directly. Use class methods
            `from_running_instance()` or `start_new_instance()` instead.
        """
        super().__init__(sap_model, "SAP2000")

    @classmethod
    def from_running_instance(cls) -> "SAPClient":
        """
        Connect to a currently running SAP2000 instance.

        Returns:
            SAPClient connected to running instance

        Raises:
            SAP2000ConnectionError: If connection fails

        Example:
            >>> client = SAPClient.from_running_instance()
            >>> df = client.results.tables.element_forces_frames(load_cases=["DEAD"])
        """
        model = connect_to_sap2000()
        return cls(model)

    @classmethod
    def start_new_instance(cls) -> "SAPClient":
        """
        Start a new SAP2000 instance.

        Returns:
            SAPClient with new SAP2000 instance

        Raises:
            SAP2000ConnectionError: If SAP2000 cannot be started

        Example:
            >>> client = SAPClient.start_new_instance()
            >>> # Load a model, run analysis, etc.
        """
        model = start_sap2000()
        return cls(model)

    @classmethod
    def close_sap2000(cls) -> None:
        """
        Close the SAP2000 instance.

        Returns:
            None
        """
        close_sap2000_instance()
