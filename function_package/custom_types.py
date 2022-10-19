"""Define some useful types for this module"""


Filepath = str  # A full filepath, e. g. my_dir/my_second_dir/my_file.py
Filename = str  # Only the filename (including extension), e. g. my_file.py
Dirpath = str  # The name of the directory, e. g. my_dir/my_second_dir/

# A SWEEP region string used to specify RA and DEC in <AAA>c<BBB> pattern where
# AAA is the RA, c the p or m for the sign of DEC and BBB is the DEC
Regionstring = str
# A SWEEP brick string following the sweep convention of <RA_DEC_min>-<RA_DEC_max>
Brickstring = str
