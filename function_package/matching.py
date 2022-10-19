"""All functions concerning the matching of different tables."""
import astropy.units as u
from astropy.coordinates import SkyCoord
from astropy.table import Table, hstack


def crossmatch_tables(t1: Table, t2: Table, match_radius: float, join="left") -> Table:
    ra1, ra2 = t1["ra"], t2["ra"]
    dec1, dec2 = t1["dec"], t2["dec"]
    c1 = SkyCoord(ra1, dec1, unit="deg")
    c2 = SkyCoord(ra2, dec2, unit="deg")
    if join == "left":
        index, distances, _ = c1.match_to_catalog_sky(c2)
        selection = (distances <= match_radius * u.deg)
        index = index[selection]
        distances = distances[selection]
        print(len(index), len(t1), len(t2))
        t1 = t1[index]
    if join == "right":
        index, distances, _ = c2.match_to_catalog_sky(c1)
        selection = (distances <= match_radius * u.deg)
        index = index[selection]
        distances = distances[selection]
    if join == "inner":
        index, distances, _ = c1.match_to_catalog_sky(c2)
        selection = (distances <= match_radius * u.deg)
        index = index[selection]
        distances = distances[selection]
        index, distances, _ = c2.match_to_catalog_sky(c1)
        selection = (distances <= match_radius * u.deg)
        index = index[selection]
        distances = distances[selection]
    table = hstack([distances, t1, t2])
    return table


def match_with_sweep(table_base: Table, table_sweep: Table, match_radius: float = 1e-5) -> Table:
    return crossmatch_tables(table_base, table_sweep, match_radius)
