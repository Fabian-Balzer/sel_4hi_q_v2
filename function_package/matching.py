"""All functions concerning the matching of different tables."""
import logging

import astropy.units as u
import numpy as np
from astropy.coordinates import SkyCoord
from astropy.table import Table, hstack, join
from astroquery.xmatch import XMatch

from .load_and_clean_tables import clean_galex_matched_table


def match_shu_with_sweep(sweep_table: Table, shu_table: Table, match_radius: float = 0.1) -> Table:
    """Perform the match of the given agn table with the sweep table, applying the given
    match radius.
    Returns the subset of the sweep table with matches found in the agn table, and
    also reports on the number of sources 'lost'.

    Parameters
    ----------
    sweep_table : Table
        The table containing the sweep sources in the given region
    shu_table : Table
        The table containing ra and dec information of possible agn sources
    match_radius : float, optional
        The maximum radius accepted for a match in arcsec, by default 0.1
    Returns
    -------
    Table
        A subset of the sweep table with counterparts found.
    """
    ra_1 = np.array(sweep_table["ra"])
    dec_1 = np.array(sweep_table["dec"])
    ra_2 = np.array(shu_table["ra"])
    dec_2 = np.array(shu_table["dec"])
    coords_1 = SkyCoord(ra=ra_1, dec=dec_1, unit="deg")
    coords_2 = SkyCoord(ra=ra_2, dec=dec_2, unit="deg")
    indices, distances = coords_2.match_to_catalog_sky(coords_1)[:2]
    # Select only the sources within the matching radius
    sel = (distances <= match_radius * u.arcsec)
    indices = indices[sel]
    distances = distances[sel]
    distances = Table([distances], names=["sep_dist_to_sweep"])
    match = hstack([distances, sweep_table[indices], shu_table[sel]],
                   table_names=["", "sweep", "shu"])
    match.rename_columns(["ra_sweep", "dec_sweep"], ["ra", "dec"])
    num_of_unmatched_sources = len(shu_table) - len(indices)
    logging.info("Match of agn to sweep successful for %s sources;\nFor %d of the %d sources in the agn table, no match was found within the given radius.",
                 len(match), num_of_unmatched_sources, len(shu_table))
    logging.info(
        "From now on, the ra and dec columns refer to the sweep ra and dec.")
    return match


def match_vhs_to_table(table_to_keep: Table, table_to_match_against: Table,
                       match_table_name="vhs", match_radius: float = 0.5) -> Table:
    """Adds the members of the `table_to_match_against` to the `table_to_keep` and returns
    the left-joined match.


    Parameters
    ----------
    table_to_keep : Table
        The table whose columns are kept, expected to contain `ra` and `dec` columns,
        expected to be in degrees.
    table_to_match_against : Table
        The other table to search for positional counterparts in, expected to
        contain `ra` and `dec` columns, expected to be in degrees.
        The match will contain all of its columns with entries wherever matches are found.
    match_table_name : str, optional
        The name of the other table, by default "other"
    match_radius : float, optional
        The maximum matching radius in arcsec.
        All sources of `table_to_match_against` with higher distances are ditched, by default 1

    Returns
    -------
    Table
        The left-joined table including columns for the other one.
        The row count should be the same, with values added whereever counterparts were
        found.
    """
    ra_1 = np.array(table_to_keep["ra"])
    dec_1 = np.array(table_to_keep["dec"])
    ra_2 = np.array(table_to_match_against["ra"])
    dec_2 = np.array(table_to_match_against["dec"])
    coords_1 = SkyCoord(ra=ra_1, dec=dec_1, unit="deg")
    coords_2 = SkyCoord(ra=ra_2, dec=dec_2, unit="deg")
    indices, distances = coords_2.match_to_catalog_sky(coords_1)[:2]
    # Select only the sources within the matching radius
    sel = (distances <= match_radius * u.arcsec)
    indices = indices[sel]
    distances = distances[sel]
    distances = Table([distances], names=[f"sep_dist_to_{match_table_name}"])
    logging.info(
        "Found %d matching vhs sources within the prescribed radius.", len(distances))
    match = hstack([distances, table_to_match_against[sel],
                   table_to_keep[indices]["sweep_id"]])
    match = join(table_to_keep, match, table_names=[
                 "sweep", match_table_name], join_type="left", keys="sweep_id")
    match.rename_columns(["ra_sweep", "dec_sweep"], ["ra", "dec"])
    return match


def match_with_galex_and_clean_it(table_base: Table, match_radius: float = 3.5) -> Table:
    """Perform a cds-side cross-match to the GALEX source table on their servers to
    obtain FUV and NUV information.

    Parameters
    ----------
    table_base : Table
        The table to match the galex sources against.
    match_radius : float, optional
        The maximally allowed distance to sources in the galex table, by default 3.5

    Returns
    -------
    Table
        The matched and joined table_base, including galex columns with values
        wherever matches inside of the radius were found.
    """
    ref_table = table_base[["ra", "dec", "sweep_id"]]
    galex_table_id = "II/335/galex_ais"
    match = XMatch.query(cat1=ref_table,
                         cat2=f"vizier:{galex_table_id}",
                         max_distance=match_radius * u.arcsec, colRA1='ra',
                         colDec1='dec')
    match = clean_galex_matched_table(match)
    table_base["sweep_id_galex"] = np.int64(table_base["sweep_id"])
    logging.info(
        "Found %d matching galex sources within the prescribed radius.", len(match))
    # Join the matched sources to the base table via the sweep_id column
    match = join(table_base, match, table_names=[
                 "sweep", "galex"], join_type="left", keys="sweep_id_galex")

    return match
