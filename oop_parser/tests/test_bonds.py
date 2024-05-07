import sys
sys.path.append("/Users/jhome/code/praktikum/helpers/oop_parser")


import unittest
from unittest.mock import Mock,MagicMock, patch
# from state_transition_manager import StateTransitionManager
# from config import Config

import pandas as pd
from pandas.testing import assert_frame_equal
import re

from parser import Parser
from bonds_node import BondsNode
from section_node import SectionNode

from generate_dummy_data import (print_section_to_console, 
                                 remove_formatting_characters,
                                 generate_dummy_data
                                 )



# %%% dummy data modelling
# !!! check module "generate_dummy_data" for instructions and description
# !!! of data generation process


data_generation_mode = True

if data_generation_mode:
    section_lines = print_section_to_console("BONDS", "ANGLES")
  


   
# results from dummy data generation for bonds section
representative_lines = [
    'BONDS\n',
    '!-------------------------------------GCFF-bv----------------------------------------------------------\n',
    'CG2R51   OG312    525.00   1.2600   !   bv-pfr-c   ,   from   CG2R61   OG312,   PENALTY=   45\n',
    'OG311    CG2O2    800.00   1.3550   !   ras-chim   ,   from   CG321   NG321,   penalty=   4\n',
    '!C        NG321    370.000  1.3450 ! ALLOW   PEP POL ARO\n',
    "                ! Alanine Dipeptide ab initio calc's (LK)\n",
    '!CG2O2    NH1       370.000     1.3450 ! ALLOW   PEP POL ARO\n',
    'CG2O2    NH1     370.000    1.3450 ! ALLOW   PEP POL ARO\n',
    'CG311    HGA1    309.00     1.1110 ! PROT alkane update, adm jr., 3/2/92\n',
    '\n',
    '\n']


representative_data_lines = [
    'CG2R51   OG312    525.00   1.2600   !   bv-pfr-c   ,   from   CG2R61   OG312,   PENALTY=   45\n',
    'OG311    CG2O2    800.00   1.3550   !   ras-chim   ,   from   CG321   NG321,   penalty=   4\n',
    'CG2O2    NH1     370.000    1.3450 ! ALLOW   PEP POL ARO\n',
    'CG311    HGA1    309.00     1.1110 ! PROT alkane update, adm jr., 3/2/92\n',
    ]

if data_generation_mode:
    row_lists = remove_formatting_characters("BONDS", representative_data_lines)


row_lists = [
    ['CG2R51', 'OG312', '525.00', '1.2600', '! bv-pfr-c , from CG2R61 OG312, PENALTY= 45'],
['OG311', 'CG2O2', '800.00', '1.3550', '! ras-chim , from CG321 NG321, penalty= 4'],
['CG2O2', 'NH1', '370.000', '1.3450', '! ALLOW PEP POL ARO'],
['CG311', 'HGA1', '309.00', '1.1110', '! PROT alkane update, adm jr., 3/2/92']
] 



# %%% Test Section

class TestBondsNode(unittest.TestCase):
    
    
    def setUp(self):
        """
        Override setup with additional variables required to test the classes.
        """
        
        super().setUp()
        
        self.mock_parser = Mock(Parser)  # Create a mock Parser object
        
        self.mock_parser.state = MagicMock(return_value="some state")
        
        self.mock_parser.state_transition_manager = MagicMock(return_value="stm")
        
        (self.bonds_section_lines, 
          self.representative_lines, 
          self.representative_data_lines, self.row_lists,
          self.bonds_df) =  generate_dummy_data("BONDS")
        
        
    def test_process_removes_line(self):
        
        node = BondsNode()

        lines =     ['!CG2O2    NH1       370.000     1.3450 ! ALLOW   PEP POL ARO\n',
            'CG2O2    NH1     370.000    1.3450 ! ALLOW   PEP POL ARO\n']
        
        remaining_lines = node.process(self.mock_parser, lines)
        
        # self.mock_parser.process.assert_called_once_with(node, lines)
        
        self.assertEqual(remaining_lines, 
                      ['CG2O2    NH1     370.000    1.3450 ! ALLOW   PEP POL ARO\n']) 
        


if __name__ == '__main__':
    unittest.main()