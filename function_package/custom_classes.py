"""Some custom classes that might be necessary"""
from math import ceil, floor

from astropy.table import Table

from .custom_types import Brickstring, Regionstring


class Region:
    """A rectangular region in the sky that is used to constrain the matching routines.
    Also offers possibilities to provide the correct sweep tables.
    """

    def __init__(self, ra_min: float, ra_max: float, dec_min: float, dec_max: float):
        """Initialise a rectangular region with the specified dimensions.

        Parameters
        ----------
        ra_min : float
            The minimum ra in deg
        ra_max : float
            The maximum ra in deg
        dec_min : float
            The minimum dec in deg
        dec_max : float
            The maximum dec in deg
        """
        assert ra_max > ra_min, "The maximum ra has to be higher than the minimum ra"
        assert dec_max > dec_min, "The maximum dec has to be higher than the minimum dec"
        self.ra_min = ra_min
        self.ra_max = ra_max
        self.dec_min = dec_min
        self.dec_max = dec_max

        self.ra_dist = ra_max - ra_min
        self.dec_dist = dec_max - dec_min
        self.linear_size = self.ra_dist * self.dec_dist

    def __str__(self):
        return (f"Region constrained to {self.ra_min:.4f} <= RA <= {self.ra_max:.4f} "
                f"and {self.dec_min:.4f} <= DEC <= {self.dec_max:.4f}.\n"
                f"This corresponds to a linear (!) size of {self.linear_size} deg^2")

    def constrain_to_region(self, table: Table) -> Table:
        """Constrains the given table to the region

        Parameters
        ----------
        table : Table
            The table that needs to be constrained.
            Expected to contain "ra" and "dec" columns in degrees.

        Returns
        -------
        Table
            The table, reduced to the given region.
        """
        colnames = table.colnames
        assert "ra" in colnames and "dec" in colnames, "Could not find ra or dec column. Make sure they are lowercased."
        mask = (table["ra"] >= self.ra_min) & (table["ra"] <= self.ra_max)
        mask *= (table["dec"] >= self.dec_min) & (table["dec"] <= self.dec_max)
        return table[mask]

    def _get_sweep_sgn_str(self, dec: float) -> str:
        """Returns 'p' if dec is positive, 'm' if it's negative."""
        return "p" if dec >= 0 else "m"

    def _get_sweep_region_string(self, ra: int, dec: int) -> Regionstring:
        """Returns a string conforming to the naming convention of the SWEEP
        catalogues following the <AAA>c<BBB> pattern where AAA is the ra, c 
        the p or m for the sign of dec and BBB is the dec."""
        return f"{ra:03}{self._get_sweep_sgn_str(dec)}{abs(dec):03}"

    def get_included_sweep_bricks(self) -> list[Brickstring]:
        """Retrieve the relevant SWEEP bricks for this region.

        Returns
        -------
        list[str]
            A list of sweep brickstrings
        """
        brick_strings = []
        # Right ascension is taken in steps of 10, declination in steps of five
        ra_min = 10 * floor(self.ra_min / 10)
        ra_max = 10 * ceil(self.ra_max / 10)
        dec_min = 5 * floor(self.dec_min / 5)
        dec_max = 5 * ceil(self.dec_max / 5)
        for ra in range(ra_min, ra_max, 10):
            for dec in range(dec_min, dec_max, 5):
                reg_min = self._get_sweep_region_string(ra, dec)
                reg_max = self._get_sweep_region_string(ra + 10, dec + 5)
                brick_strings.append(f"{reg_min}-{reg_max}")
        return brick_strings
