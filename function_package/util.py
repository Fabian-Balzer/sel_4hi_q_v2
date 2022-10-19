"""Utility functions for smoothing things out"""
import os

import numpy as np
from astropy.table import Table

from .custom_paths import ALL_PATHS


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


def generate_all_filepaths():
    """Generate the paths that are expected for the application to run.
    WARNING: This might create lots of paths relative to your current working
    directory, so make sure you know what you're doing!
    """
    for path in ALL_PATHS:
        os.makedirs(path, exist_ok=True)
