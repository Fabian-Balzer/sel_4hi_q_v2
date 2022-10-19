"""The definition of some important paths."""
import os

CATPATH = os.getcwd() + "/catalogues/"
DATAPATH = os.getcwd() + "/data/"
MATCHPATH = DATAPATH + "match_backups/"
LEPHARE_PATH = DATAPATH + "lephare/"
LEPHARE_IN_PATH = LEPHARE_PATH + "input/"
LEPHARE_OUT_PATH = LEPHARE_PATH + "output/"
LEPHARE_FILT_PATH = LEPHARE_PATH + "filters/"
LEPHARE_TEMP_PATH = LEPHARE_PATH + "templates/"


ALL_PATHS = [CATPATH, DATAPATH, MATCHPATH, LEPHARE_FILT_PATH,
             LEPHARE_IN_PATH, LEPHARE_OUT_PATH, LEPHARE_TEMP_PATH, LEPHARE_PATH]
