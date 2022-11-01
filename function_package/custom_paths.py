"""The definition of some important paths."""
import os
from typing import Literal, Optional

from .custom_types import Dirpath, Filepath, TableType

STEM = "base"  # The stem can be changed in case you want to differentiate between


def get_lephare_directory(lephare_type: Literal["input", "output", "filters", "parameters",
                                                "templates", "main", "work", "dir"]) -> Dirpath:
    """Retrieve the given LePhare directory.

    Parameters
    ----------
    lephare_type : str
        The type of directory requested

    Returns
    -------
    Dirpath
        The path of the lephare directory, including a trailing backslash
    """
    main_path = get_directory("lephare")
    dirpath_dict = {"main": main_path}
    for path_type in ["input", "output", "filters", "parameters", "templates"]:
        dirpath_dict[path_type] = main_path + path_type + "/"
    if lephare_type == "work":
        assert "LEPHAREWORK" in os.environ, "Please set up the LEPHAREWORK environment variable on your system"
        return os.environ["LEPHAREWORK"] + "/"
    if lephare_type == "dir":
        assert "LEPHAREDIR" in os.environ, "Please set up the LEPHAREDIR environment variable on your system"
        return os.environ["LEPHAREDIR"] + "/"
    assert lephare_type in dirpath_dict, f"The type of directory ({lephare_type}) you have specified does not exist, please use one of the following: {', '.join(dirpath_dict)}"
    return dirpath_dict[lephare_type]


def get_directory(dir_type: Literal["data", "catalogues", "regions",
                                    "match_backups", "lephare", "sweep"]) -> Dirpath:
    """Returns the directory path of the directory in question

    Parameters
    ----------
    dir_type : str
        The directory type requested
    lephare_type : str, optional, by default None
        If the dir type

    Returns
    -------
    Dirpath
        The path of the requested directory, including a trailing backslash
    """
    datapath = os.getcwd() + "/data/"
    catpath = os.getcwd() + "catalogues/"
    dir_dict = {"data": datapath, "catalogues": catpath}
    for path_type in ["regions", "match_backups", "lephare"]:
        dir_dict[path_type] = datapath + path_type + "/"
    dir_dict["sweep"] = catpath + "sweep/"
    assert dir_type in dir_dict, f"The type of directory ({dir_type}) you have specified does not exist, please use one of the following: {', '.join(dir_dict)}"
    return dir_dict[dir_type]


def get_filepath(path_type: Literal["region_backup", "match_backup", "processed_backup",
                                    "lephare_in", "lephare_out", "para_in", "para_out",
                                    "filter"],
                 ttype: Optional[TableType] = None, stem="base") -> Filepath:
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
    filepath_dict = {"region_backup": f"{get_directory('data')}/regions/{stem}_backup.json",
                     "match_backup": f"{get_directory('match_backups')}{stem}_full_match.fits",
                     "processed_backup": f"{get_directory('match_backups')}{stem}_processed_{ttype}.fits",
                     "lephare_in": f"{get_lephare_directory('input')}{stem}_input_{ttype}.in",
                     "lephare_out": f"{get_lephare_directory('output')}{stem}_output_{ttype}.out",
                     "para_in": f"{get_lephare_directory('parameters')}{stem}_input.para",
                     "para_out": f"{get_lephare_directory('parameters')}{stem}_output.para",
                     "filter": f"{get_lephare_directory('filters')}{stem}.filt"}
    assert path_type in filepath_dict, f"The type of file you have specified does not exist, please use one of the following: {', '.join(filepath_dict)}"
    # The path_types that do not make use of ttype:
    need_ttype = ["processed_backup", "lephare_in", "lephare_out"]
    assert path_type not in need_ttype or ttype is not None, "Please specify a table type for this kind of path."
    fpath = filepath_dict[path_type]

    return fpath
