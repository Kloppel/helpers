import sys
import os

# Get the directory of the current module (test_oop_parser.py)
current_dir = os.path.dirname(__file__)
# assuming oop_parser is one level up
relative_path = os.path.join(current_dir, "..", "oop_parser")
sys.path.append(relative_path)

import unittest
from unittest.mock import patch
import pandas as pd
import numpy as np
from pathlib import Path

from pandas.testing import assert_frame_equal

from state_transition_manager import StateTransitionManager
from config import Config

from parser import Parser

# from prm_test_setup_mixin import ParamParserTestSetup

class TestParser(unittest.TestCase):
    
    def setUp(self):
        pass
    
    def tearDown(self):
        pass
    
    
    # @patch.object(Config, 'select_strategy_by_filetype', autospec=True)
    # def test_file_suffix_extraction(self):
        
    #     path_str = "/Users/jhome/code/praktikum/helpers/oop_parser/files_to_parse/par_bv.prm"

    #     p = Path(path_str)
        
    #     Parser.select_config_strategy()
        
    #     print(type(p))
        











if __name__ == "__main__":
    unittest.main()