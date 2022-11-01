"""Functions to perform the processing needed in preparation for LePhare."""
import logging
from typing import Sequence, Tuple

import numpy as np
from astropy.table import Table

from .custom_constants import (ALL_BANDS, ALL_GALEX_BANDS, ALL_SWEEP_BANDS,
                               ALL_VHS_BANDS, VEGA_AB_DICT)
from .custom_types import (Band, TableExtended, TablePointlike, TableSplit,
                           TableType)


def _process_single_sweep_column(table: Table, band: Band) -> Table:
    """Add a column to the table correcting the sweep fluxes for the MW_TRANSMISSION.
    Errors are calculated by taking the inverse variance.
    Convert from nanomaggie to erg/cm**2/Hz/s by multiplying with 3631*10**(-23)*10**(-9).
    """
    table[f"c_flux_{band}"] = table[f"flux_{band}"] / \
        table[f"mw_transmission_{band}"] * 3.631 * 1e-29
    table[f"c_flux_err_{band}"] = 1 / np.sqrt(
        table[f"flux_ivar_{band}"]) / table[f"mw_transmission_{band}"] * 3.631 * 1e-29
    return table


def process_sweep_columns(table: Table, bands: Sequence[Band] = ALL_SWEEP_BANDS) -> Table:
    """Correct the sweep columns (assumed to be of the form `flux_{band}` and `flux_ivar_{band}`)
    for the transmission values that are provided in the `mw_transmission_{band}` column.

    Parameters
    ----------
    table : Table
        The input table with the uncorrected fluxes
    bands : Sequence[str], optional
        The bands to convert, by default ALL_SWEEP_BANDS

    Returns
    -------
    Table
        The table with the value-added columns
    """
    for band in bands:
        table = _process_single_sweep_column(table, band)
    return table


def _process_single_galex_column(table: Table, band: Band) -> Table:
    """Corrects the GALEX NUV and FUV fluxes by using the suggested prescription of
    A_FUV = 8.06 * EBV_Galex and A_NUV = 7.95 * EBV_Galex as correction magnitudes, giving
    a flux correction of 
        F_real = F_mes*10**(A_band/2.5).
    As the flux is given in 10**(-6)Jy, we multiply it by 10**(-29)."""
    correction_factors = {"fuv": 8.06, "nuv": 7.95}
    corr_factor = correction_factors[band]
    table[f"c_flux_{band}"] = table[f"flux_{band}"] * \
        10**(corr_factor * table["galex_ebv"] / 2.5) * 1e-29
    table[f"c_flux_err_{band}"] = table[f"flux_err_{band}"] * \
        10**(corr_factor * table["galex_ebv"] / 2.5) * 1e-29
    return table


def process_galex_columns(table: Table, bands: Sequence[Band] = ALL_GALEX_BANDS) -> Table:
    """Correct the galex columns (assumed to be of the form `flux_{band}` and `flux_err_{band}`)
    for the EBV values that are provided in the `galex_ebv` column.

    Parameters
    ----------
    table : Table
        The input table with the uncorrected fluxes
    bands : Sequence[Band], optional
        The bands to convert, by default ALL_GALEX_BANDS

    Returns
    -------
    Table
        The table with the value-added columns
    """
    for band in bands:
        table = _process_single_galex_column(table, band)
    return table


def _delete_all_apermag_cols(table: TableSplit, ttype: TableType) -> Table:
    """Delete all column names containing `apermag{suffix}` from the given table.
    Suffix should be "4" or "6".
    """
    num_cols_before = len(table.colnames)
    rm_suffix = "4" if ttype == "extended" else "6"
    cols_to_keep = [
        col for col in table.colnames if not f"apermag{rm_suffix}" in col]
    table = table[cols_to_keep]
    num_cols_lost = num_cols_before - len(cols_to_keep)
    logging.debug("Found and removed %d apermag%s columns.",
                  num_cols_lost, rm_suffix)
    rename_suffix = "6" if ttype == "extended" else "4"
    oldnames = [
        col for col in table.colnames if f"apermag{rename_suffix}" in col]
    newnames = ["mag_" + col.replace(f"apermag{rename_suffix}", "")
                for col in oldnames]
    table.rename_columns(oldnames, newnames)
    return table


def split_table_by_sourcetype(table: Table) -> Tuple[TablePointlike, TableExtended]:
    """Splits the given table into two subsets of point-like and extended sources and
    deletes irrelevant (vhs) columns, as 2''8 (apermag4) photometry is used for pointlike
    and apermag6 is used for extended sources

    Parameters
    ----------
    table : Table
        The input table containing the matches

    Returns
    -------
    tuple[Table, Table]

    TablePointlike : Table
        The pointlike table
    TableExtended : Table
        The extended table
    """
    mask = table["sweep_type"] == "PSF"
    pointlike = table[mask]
    pointlike = _delete_all_apermag_cols(pointlike, "pointlike")
    extended = table[~mask]
    extended = _delete_all_apermag_cols(extended, "extended")
    return pointlike, extended


def _process_single_vhs_column(table: TableSplit, band: Band) -> Table:
    """Coming from a column with name magcolname, convert its values from the vega
    to AB system and add a column with the corresponding flux (and errors) in ergs/(cm**2*Hz*s)"""
    ab_corr = VEGA_AB_DICT[band]
    # Correct the magnitude for dust and convert it from vega to ab:
    table[f"c_mag_{band}"] = table[f"mag_{band}"] + \
        table[f"a{band}"] + ab_corr
    table[f"c_mag_err_{band}"] = table[f"mag_{band}err"] + \
        table[f"a{band}"] + ab_corr
    # Convert the magnitude to flux:
    table[f"c_flux_{band}"] = 10**(-(table[f"c_mag_{band}"] + 48.6) / 2.5)
    table[f"c_flux_err_{band}"] = 10**(-(table[f"c_mag_{band}"] + 48.6) / 2.5) * \
        table[f"c_mag_err_{band}"] * np.log(10) / 2.5
    return table


def process_vhs_columns(table: TableSplit, bands: Sequence[str] = ALL_VHS_BANDS) -> Table:
    """Convert the vhs columns (assumed to be of the form `mag_{band}` and `mag_{band}err`)
    from their VEGA magnitudes to flux columns

    Parameters
    ----------
    table : Table
        A `pointlike` or `extended` table instance
    bands : Sequence[str], optional
        The bands to convert, by default ALL_VHS_BANDS

    Returns
    -------
    Table
        The table with the value-added columns
    """
    for band in bands:
        table = _process_single_vhs_column(table, band)
    return table


def process_for_lephare(table: TableSplit, bands: Sequence[Band] = ALL_BANDS) -> TableSplit:
    """Returns a table only containing SWEEP ra and dec and then, in
    alternating fashion, flux and flux error for each of the requested bands
    (in the order given by BAND_LIST), followed by the ZSPEC column.
    """
    col_list = ["sweep_id"]
    new_colnames = ["IDENT"]
    if "zspec" not in table.colnames:
        table["zspec"] = -99.
    for band in bands:
        col_list.append("c_flux_" + band)
        col_list.append("c_flux_err_" + band)
        new_colnames.append(band)
        new_colnames.append(band + "_err")
    for infocol in ["CONTEXT", "zspec", "String"]:
        col_list.append(infocol)
        new_colnames.append(infocol)
    table["CONTEXT"] = "-1"
    table["String"] = ""
    table = table[col_list]
    table.rename_columns(col_list, new_colnames)
    for col in new_colnames:
        if col not in ["IDENT", "CONTEXT", "STRING"]:
            # We need to try/except since astropy doesn't like filling columns that
            # do not have any nan values
            try:
                table[col] = table[col].filled(-99.)
            except AttributeError:
                pass
    # Replace any null values with -99. as they otherwise cause problems for LePhare:
    # for colname in new_colnames:
    return table
