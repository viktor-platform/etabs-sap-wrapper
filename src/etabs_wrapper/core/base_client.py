"""
Base client class for CSI applications (ETABS and SAP2000).

Provides shared functionality for both applications.
"""

from typing import Any

from etabs_wrapper.core.enums import Units
from etabs_wrapper.results.tables import TableResults


class BaseCSIClient:
    """
    Base client for CSI applications (ETABS and SAP2000).

    This class provides common functionality shared between ETABS and SAP2000.
    Both applications use the same COM API structure with identical table methods.

    Attributes:
        results: Results retrieval operations
            - tables: TableResults instance for retrieving table data
    """

    def __init__(self, sap_model: Any, application_name: str):
        """
        Initialize BaseCSIClient with a SapModel object.

        Args:
            sap_model: CSI SapModel COM object (works for both ETABS and SAP2000)
            application_name: Name of the application ("ETABS" or "SAP2000")

        Note:
            Typically you won't call this directly. Use ETABSClient or SAPClient instead.
        """
        self._model = sap_model
        self._app_name = application_name

        # Results operations (shared between both applications)
        self._tables = TableResults(sap_model)

    @property
    def model(self) -> Any:
        """
        Access to underlying CSI SapModel COM object.

        Use this for direct API calls not wrapped by this library.
        The SapModel interface is identical for both ETABS and SAP2000.

        Returns:
            CSI SapModel COM object

        Example:
            >>> client = ETABSClient.from_running_instance()
            >>> # Direct API call
            >>> ret = client.model.Analyze.RunAnalysis()
            >>> ret, filename = client.model.GetModelFilename()
        """
        return self._model

    @property
    def results(self) -> "ResultsManager":
        """
        Access results operations.

        Returns:
            ResultsManager with table access

        Example:
            >>> client = ETABSClient.from_running_instance()
            >>> df = client.results.tables.element_forces_frames(load_cases=["DEAD"])
        """
        return ResultsManager(self._tables)

    @property
    def application_name(self) -> str:
        """
        Get the name of the connected application.

        Returns:
            "ETABS" or "SAP2000"
        """
        return self._app_name

    def new_file(self, units: Units = Units.kN_m_C) -> bool:
        """
        Create a new file in the connected application.

        Args:
            units: Optional units to use for the new file. Default is kN_m_C

        Returns:
            bool if a new file has been created
        """
        ret = self._model.InitializeNewModel(units)
        return True if ret == 0 else False

    def open_file(self, file_path: str, units: Units = Units.kN_m_C) -> bool:
        """
        Open a file in the connected application.

        Args:
            file_path: Path to the file to open. The file name must have an sdb, $2k, s2k, xlsx, xls, or mdb extension
            units: Optional units to use for the new file. Default is kN_m_C. Note: this will override the units in the file.

        Returns:
            bool if the file has been opened succesfully
        """
        self.new_file()
        ret = self._model.File.OpenFile(file_path)

        if ret != 0:
            raise RuntimeError(f"Failed to open file '{file_path}'. Error code: {ret}")

        ret = self._model.SetPresentUnits(units)

        if ret != 0:
            raise RuntimeError(f"Failed to set units for file '{file_path}'. Error code: {ret}")

        return True


    def __enter__(self) -> "BaseCSIClient":
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        # No cleanup needed for COM objects
        pass

    def __repr__(self) -> str:
        """String representation."""
        return f"{self.__class__.__name__}(application={self._app_name}, model={self._model})"


class ResultsManager:
    """
    Manager for results operations.

    Provides organized access to different result types.
    Shared between ETABS and SAP2000 as they use the same table structure.
    """

    def __init__(self, tables: TableResults):
        """
        Initialize ResultsManager.

        Args:
            tables: TableResults instance
        """
        self._tables = tables

    @property
    def tables(self) -> TableResults:
        """
        Access table results.

        Returns:
            TableResults instance for retrieving CSI database tables

        Example:
            >>> df = client.results.tables.element_forces_frames(load_cases=["DEAD"])
        """
        return self._tables
