import sys
import os

# Get the directory of the current module (test_oop_parser.py)
current_dir = os.path.dirname(__file__)
# assuming oop_parser is one level up
relative_path = os.path.join(current_dir, "..", "oop_parser")
sys.path.append(relative_path)

from pathlib import Path
import pandas as pd
import numpy as np

import unittest
from unittest.mock import patch
from pandas.testing import assert_frame_equal
from parameterized import parameterized

from main import parse_file

# "/Users/jhome/code/praktikum/helpers/oop_parser/files_to_parse/par_all36_carb.prm",
# "/Users/jhome/code/praktikum/helpers/oop_parser/files_to_parse/par_all36_cgenff.prm",
# "/Users/jhome/code/praktikum/helpers/oop_parser/files_to_parse/par_all36_lipid.prm",
# "/Users/jhome/code/praktikum/helpers/oop_parser/files_to_parse/par_all36_na.prm",
# "/Users/jhome/code/praktikum/helpers/oop_parser/files_to_parse/par_all36m_prot_additions.prm",
# "/Users/jhome/code/praktikum/helpers/oop_parser/files_to_parse/",
# "/Users/jhome/code/praktikum/helpers/oop_parser/files_to_parse/par_bv.prm"

class TestParseMultiplePrmFiles(unittest.TestCase):
    
    def setUp(self):
        # dir with files to pars in same dir as this test module
        self.files_to_parse_dir = Path("files_to_parse")
        
    
    @parameterized.expand([
        # ("par_bv.prm"),
        ("par_all36m_prot.prm"),
        ])
    def test_par_bv(self, filename):
        """
        Successfully parsed files:
            par_bv.prm
            
        Bugs found:
            par_all36m_prot.prm
            
            error msg:
                E
                ======================================================================
                ERROR: test_par_bv_1_par_all36m_prot_copy_prm (__main__.TestParseMultiplePrmFiles)
                ----------------------------------------------------------------------
                Traceback (most recent call last):
                  File "/Users/jhome/opt/anaconda3/envs/my_envs/lib/python3.10/site-packages/parameterized/parameterized.py", line 620, in standalone_func
                    return func(*(a + p.args), **p.kwargs, **kw)
                  File "/Users/jhome/code/praktikum/helpers/oop_parser/tests/test_multiple_prm_files.py", line 44, in test_par_bv
                    parser = parse_file(p)
                  File "/Users/jhome/code/praktikum/helpers/oop_parser/main.py", line 27, in parse_file
                    p.start()
                  File "/Users/jhome/code/praktikum/helpers/oop_parser/parser.py", line 124, in start
                    self.process(self.lines)
                  File "/Users/jhome/code/praktikum/helpers/oop_parser/parser.py", line 112, in process
                    self.process(remaining_lines)
                  File "/Users/jhome/code/praktikum/helpers/oop_parser/parser.py", line 112, in process
                    self.process(remaining_lines)
                  File "/Users/jhome/code/praktikum/helpers/oop_parser/parser.py", line 112, in process
                    self.process(remaining_lines)
                  [Previous line repeated 2925 more times]
                  File "/Users/jhome/code/praktikum/helpers/oop_parser/parser.py", line 101, in process
                    remaining_lines = self.state.process(self, lines)
                  File "/Users/jhome/code/praktikum/helpers/oop_parser/section_node.py", line 94, in process
                    self.section_dataframe = self.append_row_to_df(self.section_dataframe,
                  File "/Users/jhome/code/praktikum/helpers/oop_parser/section_node.py", line 216, in append_row_to_df
                    section_df = pd.concat([section_dataframe, row_df],
                  File "/Users/jhome/opt/anaconda3/envs/my_envs/lib/python3.10/site-packages/pandas/util/_decorators.py", line 331, in wrapper
                    return func(*args, **kwargs)
                  File "/Users/jhome/opt/anaconda3/envs/my_envs/lib/python3.10/site-packages/pandas/core/reshape/concat.py", line 368, in concat
                    op = _Concatenator(
                  File "/Users/jhome/opt/anaconda3/envs/my_envs/lib/python3.10/site-packages/pandas/core/reshape/concat.py", line 563, in __init__
                    self.new_axes = self._get_new_axes()
                  File "/Users/jhome/opt/anaconda3/envs/my_envs/lib/python3.10/site-packages/pandas/core/reshape/concat.py", line 633, in _get_new_axes
                    return [
                  File "/Users/jhome/opt/anaconda3/envs/my_envs/lib/python3.10/site-packages/pandas/core/reshape/concat.py", line 634, in <listcomp>
                    self._get_concat_axis if i == self.bm_axis else self._get_comb_axis(i)
                  File "/Users/jhome/opt/anaconda3/envs/my_envs/lib/python3.10/site-packages/pandas/core/reshape/concat.py", line 640, in _get_comb_axis
                    return get_objs_combined_axis(
                  File "/Users/jhome/opt/anaconda3/envs/my_envs/lib/python3.10/site-packages/pandas/core/indexes/api.py", line 105, in get_objs_combined_axis
                    return _get_combined_index(obs_idxes, intersect=intersect, sort=sort, copy=copy)
                  File "/Users/jhome/opt/anaconda3/envs/my_envs/lib/python3.10/site-packages/pandas/core/indexes/api.py", line 158, in _get_combined_index
                    index = union_indexes(indexes, sort=False)
                  File "/Users/jhome/opt/anaconda3/envs/my_envs/lib/python3.10/site-packages/pandas/core/indexes/api.py", line 316, in union_indexes
                    if not all(index.equals(other) for other in indexes[1:]):
                  File "/Users/jhome/opt/anaconda3/envs/my_envs/lib/python3.10/site-packages/pandas/core/indexes/api.py", line 316, in <genexpr>
                    if not all(index.equals(other) for other in indexes[1:]):
                  File "/Users/jhome/opt/anaconda3/envs/my_envs/lib/python3.10/site-packages/pandas/core/indexes/base.py", line 5572, in equals
                    if is_object_dtype(self.dtype) and not is_object_dtype(other.dtype):
                  File "/Users/jhome/opt/anaconda3/envs/my_envs/lib/python3.10/site-packages/pandas/core/dtypes/common.py", line 189, in is_object_dtype
                    return _is_dtype_type(arr_or_dtype, classes(np.object_))
                  File "/Users/jhome/opt/anaconda3/envs/my_envs/lib/python3.10/site-packages/pandas/core/dtypes/common.py", line 1609, in _is_dtype_type
                    if isinstance(arr_or_dtype, np.dtype):
                RecursionError: maximum recursion depth exceeded while calling a Python object
        
            Ansatz:
                - get line of prm file where error was encountered
                - check concatenation of SectionNode.append_row_to_df()
                
        """
        
        p = Path(self.files_to_parse_dir, filename)
        
        parser = parse_file(p)
        
        # access the first and only df of each section node
        atoms, angles, bonds, dihedrals, improper, nonbonded = (
            parser.nodes[i][0].section_dataframe for i in parser.nodes)
    
        print(atoms)
    
    
    
if __name__ == "__main__":
    unittest.main()