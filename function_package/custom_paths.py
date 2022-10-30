"""The definition of some important paths."""
import os
from typing import Literal, Optional

from .custom_types import Filepath, TableType

CATPATH = os.getcwd() + "/catalogues/"
DATAPATH = os.getcwd() + "/data/"
MATCHPATH = DATAPATH + "match_backups/"
LEPHARE_PATH = DATAPATH + "lephare/"
LEPHARE_IN_PATH = LEPHARE_PATH + "input/"
LEPHARE_OUT_PATH = LEPHARE_PATH + "output/"
LEPHARE_FILT_PATH = LEPHARE_PATH + "filters/"
LEPHARE_PARA_PATH = LEPHARE_PATH + "parameters/"
LEPHARE_TEMP_PATH = LEPHARE_PATH + "templates/"


ALL_PATHS = [CATPATH, DATAPATH, MATCHPATH, LEPHARE_FILT_PATH, LEPHARE_PARA_PATH,
             LEPHARE_IN_PATH, LEPHARE_OUT_PATH, LEPHARE_TEMP_PATH, LEPHARE_PATH]

STEM = "base"  # The stem can be changed in case you want to differentiate between


def get_filepath(path_type: Literal["region_backup", "match_backup", "processed_backup",
                                    "lephare_in", "lephare_out", "para_in", "para_out",
                                    "filter"], ttype: Optional[TableType] = None, stem="base") -> Filepath:
    """Get the unified filepath string for a given filepath type.
    Via the stem argument, the filenames can be altered.

    Parameters
    ----------
    path_type : str
        One of the supported path types
    ttype : Optional[TableType], optional
        If the path type refers to extended or pointlike,
        you need to specify it here, by default None
    stem : str, optional
        The filestem, by default "base"

    Returns
    -------
    Filepath
        The path used to store path_type files in.
    """
    filepath_dict = {"region_backup": f"{DATAPATH}/regions/{stem}_backup.json",
                     "match_backup": f"{MATCHPATH}{stem}_full_match.fits",
                     "processed_backup": f"{MATCHPATH}{stem}_processed_{ttype}.fits",
                     "lephare_in": f"{LEPHARE_IN_PATH}{stem}_input_{ttype}.in",
                     "lephare_out": f"{LEPHARE_OUT_PATH}{stem}_output_{ttype}.out",
                     "para_in": f"{LEPHARE_PARA_PATH}{stem}_input.para",
                     "para_out": f"{LEPHARE_PARA_PATH}{stem}_output.para",
                     "filter": f"{LEPHARE_FILT_PATH}{stem}.filt"}
    assert path_type in filepath_dict, f"The type of file you have specified does not exist, please use one of the following: {', '.join(filepath_dict)}"
    # The path_types that do not make use of ttype:
    no_ttype = ["match_backup", "region_backup"]
    assert path_type in no_ttype or ttype is not None, "Please specify a table type for this kind of path."
    fpath = filepath_dict[path_type]
    return fpath
