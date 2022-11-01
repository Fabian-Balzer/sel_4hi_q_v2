"""Some functions needed for the matching"""
from .custom_classes import Region
from .custom_paths import get_directory, get_filepath, get_lephare_directory
from .file_io import read_table_from_backup, write_table_as_backup
from .load_and_clean_tables import (load_and_clean_opt_agn_shu,
                                    load_and_clean_sweep, load_and_clean_vhs)
from .matching import (match_shu_with_sweep, match_vhs_to_table,
                       match_with_galex_and_clean_it)
from .pre_processing import (process_for_lephare, process_galex_columns,
                             process_sweep_columns, process_vhs_columns,
                             split_table_by_sourcetype)
from .util import ask_file_overwrite, generate_all_filepaths
