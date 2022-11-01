# Quasar selection for the 4HI-Q project (version 2)

The code supplied here is capable of processing the data provided by the different catalogues and to perform the photometric redshift fitting via LePhare.
In addition to that, various plotting routines are provided to perform analysis of the joint input catalogue and the output coming from LePhare.

## Requirements

To be able to run this, the following requirements need to be met:

- A `python 3.10` environment, including the `astropy`, `astroquery`, `scipy` and standard modules
- The `function package` and the `catalogues` in the same directory as this script.
- For the LePhare part, the ``LEPHAREDIR`` and ``LEPHAREWORK`` environment variable should be set up along with a working LePhare installation (for which the setup instructions are provided [here](https://gitlab.lam.fr/Galaxies/LEPHARE)).

## Structure

The code is structured into three main jupyter notebooks to keep it cleaner.\
All of the functions used for these notebooks can either be found directly in them or in the `function_package` directory.

### Matching the tables

In this part of the code, the input catalogue data is assembled.\
More information is provided in the header of the notebook, see `match_tables.ipynb`.

### Running LePhare

In this part of the code, the LePhare routines are provided and briefly explained.\
More information is provided in the header of the notebook, see ``run_lephare.ipynb``.

### Analysing the results

The notebook ``catalogue_analysis.ipynb`` provides several ways to plot the data.\
(STILL **TODO**)

> **Note**:
> It is important that these routines are called one after another for each region.

## Citations

- Please see `other/citations.md` for any citations/acknowledgements that might be required when using this script.

## License

This project is distributed using the BSD 3-Clause License, see the ``License`` file.
