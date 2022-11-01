"""Several functions that are called for reading the tables"""
import logging
import os
import warnings
from typing import Optional, Sequence

from astropy.table import Table, vstack
from astropy.units import UnitsWarning

from .custom_classes import Region
from .custom_constants import ALL_SWEEP_BANDS, ALL_VHS_BANDS
from .custom_paths import get_directory
from .custom_types import Dirpath, Filename
from .util import convert_rad_to_deg, rename_columns_to_lowercase


def _sanitise_table(table: Table, region: Optional[Region] = None, name: str = "?") -> Table:
    """Perform standard operations on the given table:
    This includes lowercasing the colnames, reducing it to a region if necessary,
    and logging information about it.

    Parameters
    ----------
    table : Table
        The table to be sanitised
    region : Optional[Region], by default None
        If the table needs to be constrained, the region can be provided.

    Returns
    -------
    Table
        The sanitised table
    """
    table = rename_columns_to_lowercase(table)
    if region:
        table = region.constrain_to_region(table)
        name = "reduced " + name

    logging.info("The %s table provided contains %d sources.",
                 name, len(table))
    return table


def load_and_clean_opt_agn_shu(region: Region, fname: Filename = "optical_agn_shu.fits",
                               dpath: Dirpath = get_directory("catalogues"),
                               rf_prob_cut: float = 0.94) -> Table:
    """Cleans the opt_agn table by selecting only the relevant columns.

    Parameters
    ----------
    region : Region
        The region to constrain the table to
    fname : Filename, optional
        The name of the file that the table is saved at, by default "optical_agn_shu.fits"
    dpath : Dirpath, optional
        The directory where the table is saved, by default CATPATH
    rf_prob_cut : float, optional
        The probability cut to apply for the Random Forest Classifier, by default 0.94

    Returns
    -------
    Table
        The cleaned AGN table
    """
    fpath = dpath + "/" + fname
    assert os.path.isfile(
        fpath), f"Please add a file called {fname} in the catalogues directory to proceed."
    table = Table.read(fpath)
    table = _sanitise_table(table, region, "shu_agn")
    relevant_cols = ["ra", "dec", "phot_z", "prob_rf"]
    table = table[relevant_cols]
    table.rename_columns(["phot_z", "prob_rf"], ["shu_z_phot", "shu_prob_rf"])
    rf_prob_mask = table["shu_prob_rf"] >= rf_prob_cut
    table = table[rf_prob_mask]
    logging.info(
        "After the probability cut at p_rf >= %.3f, %d sources are left in the shu_agn table", rf_prob_cut, len(table))
    return table


def load_and_clean_vhs(region: Region, fname: Filename = "vhs_query_efeds.fits",
                       dpath: Dirpath = get_directory("catalogues"), bands: Sequence[str] = ALL_VHS_BANDS) -> Table:
    """Cleans the vhs table by selecting only the relevant columns.

    Parameters
    ----------
    region : Region
        The region to constrain the table to
    fname : Filename, optional
        The name of the file that the table is saved at, by default "optical_agn_shu.fits"
    dpath : Dirpath, optional
        The directory where the table is saved, by default CATPATH
    bands : Sequence[str], optional
        The bands that the table shall be reduced to

    Returns
    -------
    Table
        The cleaned VHS table
    """
    fpath = dpath + "/" + fname
    assert os.path.isfile(
        fpath), f"Please add a file called {fname} in the catalogues directory to proceed."
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", UnitsWarning)
        table = Table.read(fpath)
    table = _sanitise_table(table, name="vhs")  # Just to convert the colnames
    table = convert_rad_to_deg(table)
    table = _sanitise_table(table, region, "vhs")
    oldnames = ["pstar", "pgalaxy", "ebv"]
    newnames = [f"vhs_{col}" for col in oldnames]
    table.rename_columns(oldnames, newnames)
    relevant_cols = ["ra", "dec"] + newnames
    for suffix in ["apermag6", "apermag6err", "apermag4", "apermag4err"]:
        relevant_cols += [band + suffix for band in bands]
    relevant_cols += ["a" + band for band in bands]
    table = table[relevant_cols]
    return table


def load_and_clean_sweep(region: Region, dpath: Dirpath = get_directory("catalogues"),
                         bands: Sequence[str] = ALL_SWEEP_BANDS) -> Table:
    """Cleans the sweep table by selecting only the relevant columns.

    Parameters
    ----------
    region : Region
        The region to constrain the table to
    fname : Filename, optional
        The name of the file that the table is saved at, by default "optical_agn_shu.fits"
    dpath : Dirpath, optional
        The directory where the table is saved, by default CATPATH
    bands : Sequence[str], optional
        The bands that the table shall be reduced to

    Returns
    -------
    Table
        The cleaned SWEEP table
    """
    sweep_tables = []
    bricks = region.get_included_sweep_bricks()
    logging.info(
        "The following bricks are in the requested region for the sweep table:\n%s", bricks)
    for brick in bricks:
        fname = f"sweep/sweep-{brick}.fits"
        fpath = dpath + "/" + fname
        if not os.path.isfile(fpath):
            logging.warning(
                "The brick %s could NOT be found, but lies in the requested region.", brick)
            continue
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", UnitsWarning)
            sweep_tables.append(Table.read(fpath))
    table = vstack(sweep_tables)
    table = _sanitise_table(table, region, "sweep")
    table["sweep_id"] = [
        f'{row["release"]}_{row["brickid"]}_{row["objid"]}' for row in table]
    oldnames = ["type", "ebv", "maskbits", "fitbits"]
    newnames = [f"sweep_{col}" for col in oldnames]
    table.rename_columns(oldnames, newnames)
    relevant_cols = ["ra", "dec", "sweep_id"] + newnames
    for prefix in ["flux_", "flux_ivar_", "mw_transmission_"]:
        relevant_cols += [prefix + band for band in bands]
    table = table[relevant_cols]
    return table


def clean_galex_matched_table(matched_table: Table) -> Table:
    """Manipulate the column names of a matched galex table.

    Parameters
    ----------
    matched_table : Table
        The galex table

    Returns
    -------
    Table
        The galex table, reduced to the relevant column names.
    """
    relevant_cols = ["angDist", "RAJ2000", "DEJ2000", "sweep_id",
                     "E(B-V)", "Fflux", "Nflux", "e_Fflux", "e_Nflux"]
    new_colnames = ["sep_to_galex", "ra_galex", "dec_galex", "sweep_id_galex",
                    "galex_ebv", "flux_fuv", "flux_nuv", "flux_err_fuv", "flux_err_nuv"]
    matched_table.keep_columns(relevant_cols)
    matched_table.rename_columns(relevant_cols, new_colnames)
    return matched_table
