"""Functions concerning reading and writing files"""
import logging
import warnings

from astropy.units import UnitsWarning

from .custom_paths import LEPHARE_IN_PATH
from .custom_types import Filestem, TableSplit, TableType


def write_lephare_input(table: TableSplit, ttype: TableType, filestem: Filestem = "base",
                        overwrite: bool = False):
    """Write the lephare input table to the input directory

    Parameters
    ----------
    table : TableSplit
        The table to write. Needs to be in the right format!
    ttype : TableType
        extended or pointlike
    filestem : Filestem, optional
        The stem used for this run, by default "base"
    """
    fname = f"{filestem}_input_{ttype}"
    fpath = LEPHARE_IN_PATH + fname
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", UnitsWarning)
        table.write(fpath + ".fits", overwrite=overwrite)
        table.write(fpath + ".in", format="ascii", overwrite=overwrite)
    logging.info(
        "Successfully written a LePhare input file at %s as a .fits and as a .in", fpath)
