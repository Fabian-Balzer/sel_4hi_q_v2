"""Utility functions for smoothing things out"""
from astropy.table import Table
import numpy as np


def rename_columns_to_lowercase(table: Table) -> Table:
    """Renames all columns of a given table to their lowercase versions

    Parameters
    ----------
    table : Table
        The table with the dirty colnames

    Returns
    -------
    Table
        The table with the clean colnames
    """
    old_colnames = table.colnames
    new_colnames = [colname.lower() for colname in old_colnames]
    table.rename_columns(old_colnames, new_colnames)
    return table


def convert_rad_to_deg(table: Table) -> Table:
    """Converts the ra and dec columns of the given table to degree

    Parameters
    ----------
    table : Table
        The table to convert the columns for

    Returns
    -------
    Table
        The table with the converted columns
    """
    for col in ["ra", "dec"]:
        table[col] = table[col] * 180 / np.pi
        table[col].info.unit = "deg"
    return table
