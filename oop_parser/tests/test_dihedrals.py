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
from dihedrals_node import DihedralsNode
from section_node import SectionNode

from generate_dummy_data import (print_section_to_console, 
                                 remove_formatting_characters,
                                 generate_dummy_data
                                 )



# %%% dummy data modelling
# !!! check module "generate_dummy_data" for instructions and description
# !!! of data generation process


section_name = "DIHEDRALS"

# !!! switch to True for data generation
data_generation_mode = False

if data_generation_mode:
    # !!! change section headlines depending on section to test
    # section_lines = print_section_to_console("ANGLES", "DIHEDRALS",
    #                                          print_half=1)
    section_lines = print_section_to_console("DIHEDRALS", "IMPROPER")
  


   
# results from dummy data generation for angles section
# !!! first time I encounter a line without comment in a prm line
    # edge case lines include:
        # section heading
        # comment lines (starting with !)
        # empty lines (\n)
        # line without comment field value
        # tab'ed comment line (           !...)
        
representative_lines = [
'DIHEDRALS\n' ,
'!------------------------------------------------------------------------------\n' ,
'! Added by Ronald, BV parameters\n' ,
'!-------------------------propB-C---------------------------------------------!\n' ,
'\n' ,
'OG311    CG2O2    CG321    CG321    0.0500   6   180.00 ! From X    CT2  CC   X\n' ,
'!-------------------------------------CGCPY1--------------------------------------------------------------------------------------------\n' ,
'CGCPY3   CG252O   CGCPY1   CG2DC1   0.2000   2   180.00   !   bv-pfr-c   ,   from   CG2DC3   CG251O   CG2R53   NG2R53,   PENALTY=   152.5\n' ,
'\n' ,
'!-------------------------------------CGCPY2--------------------------------------------------------------------------------------------\n' ,
'CG2R51   CG251O   CGCPY2   HGA4     3.9000   2   180.00   !   bv-pfr-c   ,   from   CG2R53   CG251O   CG2DC3   HGA5,   PENALTY=   33\n' ,
'HGA4     CG2DC1   CG321    SG311    0.2000   3     0.00   !   bv-pfr-c   ,   from   HGA4   CG2DC1   CG321   OG3R60,   PENALTY=   122.2\n' ,
'CG2DC3   CG2DC1   CGCPY6   CGCPY5   1.13     2   180.00\n' ,
'                                 ! Revised to adjust NMA cis/trans energy difference. (LK)\n' ,
'HB1      CT1      C        NG321      0.0000  1     0.00 !   ALLOW PEP\n' ,
'CG2O2    CG311    CG321    HGA2       0.2000  3     0.00 ! AMGA, Alpha Methyl Glu Acid CDCA\n' ,
    ]


representative_data_lines = [
'OG311    CG2O2    CG321    CG321    0.0500   6   180.00 ! From X    CT2  CC   X\n' ,
'CGCPY3   CG252O   CGCPY1   CG2DC1   0.2000   2   180.00   !   bv-pfr-c   ,   from   CG2DC3   CG251O   CG2R53   NG2R53,   PENALTY=   152.5\n' ,
'CG2R51   CG251O   CGCPY2   HGA4     3.9000   2   180.00   !   bv-pfr-c   ,   from   CG2R53   CG251O   CG2DC3   HGA5,   PENALTY=   33\n' ,
'HGA4     CG2DC1   CG321    SG311    0.2000   3     0.00   !   bv-pfr-c   ,   from   HGA4   CG2DC1   CG321   OG3R60,   PENALTY=   122.2\n' ,
'CG2DC3   CG2DC1   CGCPY6   CGCPY5   1.13     2   180.00\n' ,
'HB1      CT1      C        NG321      0.0000  1     0.00 !   ALLOW PEP\n' ,
'CG2O2    CG311    CG321    HGA2       0.2000  3     0.00 ! AMGA, Alpha Methyl Glu Acid CDCA\n' ,
    ]

if data_generation_mode:
    row_lists = remove_formatting_characters(section_name, representative_data_lines)


row_lists = [ 
['OG311', 'CG2O2', 'CG321', 'CG321', '0.0500', '6', '180.00', '! From X CT2 CC X'] ,
['CGCPY3', 'CG252O', 'CGCPY1', 'CG2DC1', '0.2000', '2', '180.00', '! bv-pfr-c , from CG2DC3 CG251O CG2R53 NG2R53, PENALTY= 152.5'] ,
['CG2R51', 'CG251O', 'CGCPY2', 'HGA4', '3.9000', '2', '180.00', '! bv-pfr-c , from CG2R53 CG251O CG2DC3 HGA5, PENALTY= 33'] ,
['HGA4', 'CG2DC1', 'CG321', 'SG311', '0.2000', '3', '0.00', '! bv-pfr-c , from HGA4 CG2DC1 CG321 OG3R60, PENALTY= 122.2'] ,
['CG2DC3', 'CG2DC1', 'CGCPY6', 'CGCPY5', '1.13', '2', '180.00', ''] ,
['HB1', 'CT1', 'C', 'NG321', '0.0000', '1', '0.00', '! ALLOW PEP'] ,
['CG2O2', 'CG311', 'CG321', 'HGA2', '0.2000', '3', '0.00', '! AMGA, Alpha Methyl Glu Acid CDCA']
]



# %%% Test Section

class TestDihedralsNode(unittest.TestCase):
    
    
    def setUp(self):
        """
        Override setup with additional variables required to test the classes.
        """
        
        super().setUp()
        
        self.mock_parser = Mock(Parser)  # Create a mock Parser object
        
        self.mock_parser.state = MagicMock(return_value="some state")
        
        self.mock_parser.state_transition_manager = MagicMock(return_value="stm")
        

        
        (self.dihedrals_section_lines, 
          self.representative_lines, 
          self.representative_data_lines, self.row_lists,
          self.dihedrals_df) =  generate_dummy_data(section_name)
        
        
    def test_process_line(self):
        
        node = DihedralsNode()

        lines =     ['CGCPY3   CG252O   CGCPY1   CG2DC1   0.2000   2   180.00   !   bv-pfr-c   ,   from   CG2DC3   CG251O   CG2R53   NG2R53,   PENALTY=   152.5\n' ,
        'CG2R51   CG251O   CGCPY2   HGA4     3.9000   2   180.00   !   bv-pfr-c   ,   from   CG2R53   CG251O   CG2DC3   HGA5,   PENALTY=   33\n'
                    ]
        
        remaining_lines = node.process(self.mock_parser, lines)
        
        # self.mock_parser.process.assert_called_once_with(node, lines)
        
        self.assertEqual(remaining_lines, 
                      [ 'CG2R51   CG251O   CGCPY2   HGA4     3.9000   2   180.00   !   bv-pfr-c   ,   from   CG2R53   CG251O   CG2DC3   HGA5,   PENALTY=   33\n']) 
        
        

    def test_extract_column_values(self):
        """
        Extract values from regular line.
        """
        
        node = DihedralsNode()
        
        basic_case_line = 'HGA4     CG2DC1   CG321    SG311    0.2000   3     0.00   !   bv-pfr-c   ,   from   HGA4   CG2DC1   CG321   OG3R60,   PENALTY=   122.2\n'
        
        row_list = ['HGA4', 'CG2DC1', 'CG321', 'SG311', '0.2000', '3', '0.00', '! bv-pfr-c , from HGA4 CG2DC1 CG321 OG3R60, PENALTY= 122.2']
        
        test_row = node.extract_column_values(basic_case_line, self.mock_parser)

        target_row = pd.DataFrame([row_list],
                                  columns=node.COL_LABELS_AND_DTYPES)
        
        assert_frame_equal(test_row, target_row)
        
        
    def test_extract_column_values_no_comment_value(self):
        """
        Extract values from line without value in comment field.
        """
        
        node = DihedralsNode()
        
        no_comment_line = 'CG2DC3   CG2DC1   CGCPY6   CGCPY5   1.13     2   180.00\n'
        
        row_list = ['CG2DC3', 'CG2DC1', 'CGCPY6', 'CGCPY5', '1.13', '2', '180.00', '']
        
        test_row = node.extract_column_values(no_comment_line, self.mock_parser)

        target_row = pd.DataFrame([row_list],
                                  columns=node.COL_LABELS_AND_DTYPES)
        
        assert_frame_equal(test_row, target_row)

        
        
        
        
        
        

if __name__ == '__main__':
    unittest.main()