"""
Table results retrieval from ETABS.

Provides methods to retrieve various analysis results as pandas DataFrames.
"""

from typing import Any

import numpy as np
import pandas as pd


class TableResults:
    """
    Handle retrieval of ETABS database tables.

    This class provides methods to retrieve various analysis results from ETABS,
    including element forces, joint displacements, base reactions, etc.
    """

    def __init__(self, sap_model: Any):
        """
        Initialize TableResults with ETABS model.

        Args:
            sap_model: ETABS SapModel COM object
        """
        self._model = sap_model

    def _retrieve_table_data(self, table_key: str, group_name: str = "") -> pd.DataFrame:
        """
        Internal method to retrieve table data from ETABS.

        Args:
            table_key: Name of the table to retrieve (e.g., "Element Forces - Frames")
            group_name: Optional group name to filter results (default: all)

        Returns:
            pandas DataFrame with table data

        Raises:
            RuntimeError: If table retrieval fails
        """
        try:
            no_tables, table_keys, *_ = self._model.DatabaseTables.GetAvailableTables()

            if no_tables == 0:
                raise RuntimeError("No tables were found in the open model.")

            if table_key not in table_keys:
                raise RuntimeError(f"Failed to retrieve '{table_key}'. It was not found amongst the {no_tables} tables.")

            table = self._model.DatabaseTables.GetTableForDisplayArray(TableKey=table_key, GroupName=group_name)

            # table returns: (ret, FieldKeyList, TableVersion, FieldsKeysIncluded, NumberRecords, TableData)
            cols = table[2]  # Column names
            no_of_rows = table[3]  # Number of records

            if no_of_rows <= 0:
                return pd.DataFrame()

            vals = np.array_split(table[4], no_of_rows)  # Split flat array into rows

            df = pd.DataFrame(vals, columns=cols)
            return df

        except Exception as e:
            raise RuntimeError(f"Failed to retrieve table '{table_key}': {e}") from e

    def get_table(self, table_key: str, group_name: str = "") -> pd.DataFrame:
        """
        Retrieve any ETABS table by name.

        Generic method to retrieve any table from ETABS database.

        Args:
            table_key: Name of the table (e.g., "Element Forces - Frames")
            group_name: Optional group name to filter results

        Returns:
            pandas DataFrame with table data

        Example:
            >>> df = tables.get_table("Joint Displacements", group_name="Floor1")
        """
        return self._retrieve_table_data(table_key, group_name)

    def element_forces_frames(
        self, load_cases: list[str] | None = None, load_combinations: list[str] | None = None, group_name: str = ""
    ) -> pd.DataFrame:
        """
        Retrieve frame element forces.

        Args:
            load_cases: List of load case names to display (None for all)
            load_combinations: List of load combination names to display (None for all)
            group_name: Optional group name to filter results

        Returns:
            DataFrame with columns: Frame, OutputCase, StepType, P, V2, V3, T, M2, M3, etc.
            - Frame: Element ID (int)
            - P: Axial force (float)
            - V2, V3: Shear forces (float)
            - M2, M3: Bending moments (float)

        Example:
            >>> df = tables.element_forces_frames(
            ...     load_cases=["DEAD", "LIVE"],
            ...     load_combinations=["COMB1"],
            ...     group_name="Columns"
            ... )
        """
        self._model.Results.Setup.DeselectAllCasesAndCombosForOutput()

        if load_cases:
            self._model.DatabaseTables.SetLoadCasesSelectedForDisplay(load_cases)
        if load_combinations:
            self._model.DatabaseTables.SetLoadCombinationsSelectedForDisplay(load_combinations)

        table_key = "Element Forces - Frames"
        df = self._retrieve_table_data(table_key, group_name)

        # Convert numeric columns to appropriate types
        if "Frame" in df.columns:
            df["Frame"] = pd.to_numeric(df["Frame"], errors="coerce").fillna(0).astype(int)
        for col in ["P", "V2", "V3", "T", "M2", "M3"]:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(float)

        return df

    def joint_displacements(
        self, load_cases: list[str] | None = None, load_combinations: list[str] | None = None, group_name: str = ""
    ) -> pd.DataFrame:
        """
        Retrieve joint displacements.

        Args:
            load_cases: List of load case names to display (None for all)
            load_combinations: List of load combination names to display (None for all)
            group_name: Optional group name to filter results

        Returns:
            DataFrame with columns: Joint, OutputCase, U1, U2, U3, R1, R2, R3
            - Joint: Joint ID (int)
            - U1, U2, U3: Translational displacements (float)
            - R1, R2, R3: Rotational displacements (float)

        Example:
            >>> df = tables.joint_displacements(load_cases=["DEAD"], group_name="ALL")
        """
        self._model.Results.Setup.DeselectAllCasesAndCombosForOutput()

        if load_cases:
            self._model.DatabaseTables.SetLoadCasesSelectedForDisplay(load_cases)
        if load_combinations:
            self._model.DatabaseTables.SetLoadCombinationsSelectedForDisplay(load_combinations)

        table_key = "Joint Displacements"
        df = self._retrieve_table_data(table_key, group_name)

        # Convert numeric columns
        if "Joint" in df.columns:
            df["Joint"] = pd.to_numeric(df["Joint"], errors="coerce").fillna(0).astype(int)
        for col in ["U1", "U2", "U3", "R1", "R2", "R3"]:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(float)

        return df

    def base_reactions(
        self, load_cases: list[str] | None = None, load_combinations: list[str] | None = None, group_name: str = ""
    ) -> pd.DataFrame:
        """
        Retrieve base reactions.

        Args:
            load_cases: List of load case names to display (None for all)
            load_combinations: List of load combination names to display (None for all)
            group_name: Optional group name to filter results

        Returns:
            DataFrame with columns: OutputCase, FX, FY, FZ, MX, MY, MZ
            - FX, FY, FZ: Base reaction forces (float)
            - MX, MY, MZ: Base reaction moments (float)

        Example:
            >>> df = tables.base_reactions(load_combinations=["COMB1", "COMB2"])
        """
        self._model.Results.Setup.DeselectAllCasesAndCombosForOutput()

        if load_cases:
            self._model.DatabaseTables.SetLoadCasesSelectedForDisplay(load_cases)
        if load_combinations:
            self._model.DatabaseTables.SetLoadCombinationsSelectedForDisplay(load_combinations)

        table_key = "Base Reactions"
        df = self._retrieve_table_data(table_key, group_name)

        # Convert numeric columns
        for col in ["FX", "FY", "FZ", "MX", "MY", "MZ"]:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(float)

        return df

    def element_forces_beams(
        self, load_cases: list[str] | None = None, load_combinations: list[str] | None = None, group_name: str = ""
    ) -> pd.DataFrame:
        """
        Retrieve beam element forces.

        Args:
            load_cases: List of load case names to display (None for all)
            load_combinations: List of load combination names to display (None for all)
            group_name: Optional group name to filter results

        Returns:
            DataFrame with beam forces data

        Example:
            >>> df = tables.element_forces_beams(load_cases=["DEAD", "LIVE"])
        """
        self._model.Results.Setup.DeselectAllCasesAndCombosForOutput()

        if load_cases:
            self._model.DatabaseTables.SetLoadCasesSelectedForDisplay(load_cases)
        if load_combinations:
            self._model.DatabaseTables.SetLoadCombinationsSelectedForDisplay(load_combinations)

        table_key = "Element Forces - Beams"
        df = self._retrieve_table_data(table_key, group_name)

        return df
