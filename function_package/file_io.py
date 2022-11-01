"""Functions concerning reading and writing files"""
import logging
import warnings
from typing import Optional

from astropy.table import Table
from astropy.units import UnitsWarning

from .custom_paths import get_filepath
from .custom_types import TableType


def write_table_as_backup(table: Table, path_type: str, ttype: Optional[TableType] = None,
                          stem: str = "base", overwrite: bool = False):
    """Writes the given table as a backup to the corresponding path

    Parameters
    ----------
    table : Table
        The table to save on disk
    path_type : str
        The path_type describing the type of table and therefore the filepath
    ttype : Optional[TableType], optional
        In case it's needed, specify whether the table is extended or pointlike, by default None
    stem : str, optional
        The stem to describe the run by, by default "base"
    overwrite : bool, optional
        Whether to directly overwrite an existing backup table of that name, by default False
    """
    fpath = get_filepath(path_type, ttype, stem)
    file_format = fpath.split(".")[-1]
    file_format = "ascii" if file_format in ["in", "out"] else file_format
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", UnitsWarning)
        table.write(fpath, format=file_format, overwrite=overwrite)
    logging.info(
        "Successfully written a %s file at %s.", path_type, fpath)


def read_table_from_backup(path_type: str, ttype: Optional[TableType] = None,
                           stem: str = "base") -> Table:
    """Read a table from backup, expecting it to be found at the corresponding path.

    Parameters
    ----------
    path_type : str
        The path_type describing the type of table and therefore the filepath
    ttype : Optional[TableType], optional
        In case it's needed, specify whether the table is extended or pointlike, by default None
    stem : str, optional
        The stem to describe the run by, by default "base"

    Returns
    -------
    Table
        The table found at the path.
    """
    fpath = get_filepath(path_type, ttype, stem)
    file_format = fpath.split(".")[-1]
    file_format = "ascii" if file_format in ["in", "out"] else file_format
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", UnitsWarning)
        table = Table.read(fpath, format=file_format)
    return table
