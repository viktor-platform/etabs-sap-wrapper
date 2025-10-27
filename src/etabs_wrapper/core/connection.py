"""
Connection management for CSI applications (ETABS and SAP2000) COM interface.

Handles connecting to running instances or starting new instances of both applications.
"""

from typing import Any

import comtypes.client


class ETABSConnectionError(Exception):
    """Raised when connection to ETABS fails."""

    pass


class SAP2000ConnectionError(Exception):
    """Raised when connection to SAP2000 fails."""

    pass


# Alias for backward compatibility and general use
CSIConnectionError = ETABSConnectionError


def _get_etabs_helper():
    """
    Get the ETABS COM API helper object.

    Returns:
        ETABS helper object for creating/attaching to instances

    Raises:
        ETABSConnectionError: If helper object cannot be created
    """
    try:
        helper = comtypes.client.CreateObject("ETABSv1.Helper")
        helper = helper.QueryInterface(comtypes.gen.ETABSv1.cHelper)
        return helper
    except (OSError, comtypes.COMError) as e:
        raise ETABSConnectionError(f"Failed to create ETABS helper object: {e}") from e


def _get_sap2000_helper():
    """
    Get the SAP2000 COM API helper object.

    Returns:
        SAP2000 helper object for creating/attaching to instances

    Raises:
        SAP2000ConnectionError: If helper object cannot be created
    """
    try:
        helper = comtypes.client.CreateObject("SAP2000v1.Helper")
        helper = helper.QueryInterface(comtypes.gen.SAP2000v1.cHelper)
        return helper
    except (OSError, comtypes.COMError) as e:
        raise SAP2000ConnectionError(f"Failed to create SAP2000 helper object: {e}") from e


def connect_to_etabs() -> Any:
    """
    Connect to a currently running ETABS instance.

    Returns:
        ETABS SapModel object

    Raises:
        ETABSConnectionError: If no running instance found or connection fails

    Example:
        >>> model = connect_to_etabs()
        >>> # Use model for API calls
    """
    helper = _get_etabs_helper()

    try:
        etabs_object = helper.GetObject("CSI.ETABS.API.ETABSObject")
    except (OSError, comtypes.COMError) as e:
        raise ETABSConnectionError(
            "Could not connect to running ETABS instance. "
            "Please ensure ETABS is running and a model is open."
        ) from e

    if etabs_object is None:
        raise ETABSConnectionError(
            "Could not get connection to running ETABS instance. " "ETABS may not be running or no model is open."
        )

    return etabs_object.SapModel


def connect_to_sap2000() -> Any:
    """
    Connect to a currently running SAP2000 instance.

    Returns:
        SAP2000 SapModel object

    Raises:
        SAP2000ConnectionError: If no running instance found or connection fails

    Example:
        >>> model = connect_to_sap2000()
        >>> # Use model for API calls
    """
    helper = _get_sap2000_helper()

    try:
        sap_object = helper.GetObject("CSI.SAP2000.API.SapObject")
    except (OSError, comtypes.COMError) as e:
        raise SAP2000ConnectionError(
            "Could not connect to running SAP2000 instance. "
            "Please ensure SAP2000 is running and a model is open."
        ) from e

    if sap_object is None:
        raise SAP2000ConnectionError(
            "Could not get connection to running SAP2000 instance. " "SAP2000 may not be running or no model is open."
        )

    return sap_object.SapModel


def start_etabs() -> Any:
    """
    Start a new ETABS instance.

    Returns:
        ETABS SapModel object

    Raises:
        ETABSConnectionError: If ETABS cannot be started

    Example:
        >>> model = start_etabs()
        >>> # Use model for API calls
    """
    helper = _get_etabs_helper()

    try:
        etabs_object = helper.CreateObjectProgID("CSI.ETABS.API.ETABSObject")
        etabs_object.ApplicationStart()
    except (OSError, comtypes.COMError) as e:
        raise ETABSConnectionError(f"Could not start ETABS instance: {e}") from e

    return etabs_object.SapModel


def start_sap2000() -> Any:
    """
    Start a new SAP2000 instance.

    Returns:
        SAP2000 SapModel object

    Raises:
        SAP2000ConnectionError: If SAP2000 cannot be started

    Example:
        >>> model = start_sap2000()
        >>> # Use model for API calls
    """
    helper = _get_sap2000_helper()

    try:
        sap_object = helper.CreateObjectProgID("CSI.SAP2000.API.SapObject")
        sap_object.ApplicationStart()
    except (OSError, comtypes.COMError) as e:
        raise SAP2000ConnectionError(f"Could not start SAP2000 instance: {e}") from e

    return sap_object.SapModel


def close_sap2000_instance() -> None:
    """
    Close the SAP2000 instance.

    Returns:
        None
    """
    helper = _get_sap2000_helper()

    try:
        sap_object = helper.GetObject("CSI.SAP2000.API.SapObject")
    except (OSError, comtypes.COMError) as e:
        raise SAP2000ConnectionError(
            "Could not connect to running SAP2000 instance. "
            "Please ensure SAP2000 is running and a model is open."
        ) from e

    if sap_object is None:
        raise SAP2000ConnectionError(
            "Could not get connection to running SAP2000 instance. " "SAP2000 may not be running or no model is open."
        )
    sap_object.ApplicationExit(False)


def close_etabs_instance() -> None:
    """
    Close the ETABS instance.

    Returns:
        None
    """
    helper = _get_etabs_helper()

    try:
        etabs_object = helper.GetObject("CSI.ETABS.API.ETABSObject")
    except (OSError, comtypes.COMError) as e:
        raise ETABSConnectionError(
            "Could not connect to running ETABS instance. "
            "Please ensure ETABS is running and a model is open."
        ) from e

    if etabs_object is None:
        raise ETABSConnectionError(
            "Could not get connection to running ETABS instance. " "ETABS may not be running or no model is open."
        )
    etabs_object.ApplicationExit(False)


# Backward compatibility aliases
connect_to_instance = connect_to_etabs
start_new_instance = start_etabs
