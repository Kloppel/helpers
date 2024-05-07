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
from improper_node import ImproperNode
from section_node import SectionNode

from generate_dummy_data import (print_section_to_console, 
                                 remove_formatting_characters,
                                 generate_dummy_data
                                 )



# %%% dummy data modelling
# !!! check module "generate_dummy_data" for instructions and description
# !!! of data generation process


section_name = "IMPROPER"

# !!! switch to True for data generation
data_generation_mode = False

if data_generation_mode:
    # !!! change section headlines depending on section to test
    # section_lines = print_section_to_console("ANGLES", "IMPROPER",
    #                                          print_half=1)
    section_lines = print_section_to_console("IMPROPER", "NONBONDED")
  


   
# results from dummy data generation for improper section
    # edge case lines include:
        # section heading
        # comment lines (starting with !)
        # empty lines (\n)
        # line without comment field value
        # tab'ed comment line (           !...)
        
representative_lines = ['IMPROPER\n' ,
'!------------------------------BV-parameters--added by Ronald--------------------------------------------------\n' ,
'CG2DC1   CG251O   CG2R51   HGA4     3.0000   0     0.0000 ! for ethene, yin/adm jr., 12/95  ! see param  HE2  HE2  CE2  CE2\n' ,
'\n' ,
'!-Ring-A----------------------------------------------------\n' ,
'CG2R53   CG3C51   NG2R53   OG2D1    90.0000  0     0.00   !   bv-pfr-c   ,  from   CG2R53   CG3C52   NG2R53   OG2D1,   PENALTY=   0.4\n' ,
'CG2O2     CG311    NH1      OG2D1   120.0000  0      0.0000 ! ALLOW   PEP POL ARO\n' ,
'                              ! NMA Vibrational Modes (LK)\n' ,
'!----------------------------------------------------------------------------------------------------------------\n' ,
'CGCPY1    CG3C51   CG252O   CG2DC1   140.0000  0      0.0000 ! ALLOW HEM  !\n' ,
'CG2DC3    CG2DC1   HGA5     HGA5        3.0000 0        0.00\n' ,
'NG2R51    CG2R51   CG2R51   HGP1         0.010 0      0.0000 ! ALLOW ARO\n' ,
'\n'
]


representative_data_lines = [
    'CG2DC1   CG251O   CG2R51   HGA4     3.0000   0     0.0000 ! for ethene, yin/adm jr., 12/95  ! see param  HE2  HE2  CE2  CE2\n' ,
'CG2R53   CG3C51   NG2R53   OG2D1    90.0000  0     0.00   !   bv-pfr-c   ,  from   CG2R53   CG3C52   NG2R53   OG2D1,   PENALTY=   0.4\n' ,
'CG2O2     CG311    NH1      OG2D1   120.0000  0      0.0000 ! ALLOW   PEP POL ARO\n' ,
'CGCPY1    CG3C51   CG252O   CG2DC1   140.0000  0      0.0000 ! ALLOW HEM  !\n' ,
'CG2DC3    CG2DC1   HGA5     HGA5        3.0000 0        0.00\n' ,
'NG2R51    CG2R51   CG2R51   HGP1         0.010 0      0.0000 ! ALLOW ARO\n'
]


if data_generation_mode:
    row_lists = remove_formatting_characters(section_name, representative_data_lines)


row_lists = [
['CG2DC1', 'CG251O', 'CG2R51', 'HGA4', '3.0000', '0', '0.0000', '! for ethene, yin/adm jr., 12/95 ! see param HE2 HE2 CE2 CE2'] ,
['CG2R53', 'CG3C51', 'NG2R53', 'OG2D1', '90.0000', '0', '0.00', '! bv-pfr-c , from CG2R53 CG3C52 NG2R53 OG2D1, PENALTY= 0.4'] ,
['CG2O2', 'CG311', 'NH1', 'OG2D1', '120.0000', '0', '0.0000', '! ALLOW PEP POL ARO'] ,
['CGCPY1', 'CG3C51', 'CG252O', 'CG2DC1', '140.0000', '0', '0.0000', '! ALLOW HEM !'] ,
['CG2DC3', 'CG2DC1', 'HGA5', 'HGA5', '3.0000', '0', '0.00', ''] ,
['NG2R51', 'CG2R51', 'CG2R51', 'HGP1', '0.010', '0', '0.0000', '! ALLOW ARO']
]


# %%% Test Section

class TestImproperNode(unittest.TestCase):
    
    
    def setUp(self):
        """
        Override setup with additional variables required to test the classes.
        """
        
        super().setUp()
        
        self.mock_parser = Mock(Parser)  # Create a mock Parser object
        
        self.mock_parser.state = MagicMock(return_value="some state")
        
        self.mock_parser.state_transition_manager = MagicMock(return_value="stm")
        

        
        (self.improper_section_lines, 
          self.representative_lines, 
          self.representative_data_lines, self.row_lists,
          self.improper_df) =  generate_dummy_data(section_name)
        
        
    def test_process_line(self):
        
        node = ImproperNode()

        lines =     [
            'CG2R53   CG3C51   NG2R53   OG2D1    90.0000  0     0.00   !   bv-pfr-c   ,  from   CG2R53   CG3C52   NG2R53   OG2D1,   PENALTY=   0.4\n' ,
'CG2O2     CG311    NH1      OG2D1   120.0000  0      0.0000 ! ALLOW   PEP POL ARO\n'
                    ]
        
        remaining_lines = node.process(self.mock_parser, lines)
        
        # self.mock_parser.process.assert_called_once_with(node, lines)
        
        self.assertEqual(remaining_lines, 
                      ['CG2O2     CG311    NH1      OG2D1   120.0000  0      0.0000 ! ALLOW   PEP POL ARO\n']) 
        
        

    def test_extract_column_values(self):
        """
        Extract values from regular line.
        """
        
        node = ImproperNode()
        
        basic_case_line = 'CG2DC1   CG251O   CG2R51   HGA4     3.0000   0     0.0000 ! for ethene, yin/adm jr., 12/95  ! see param  HE2  HE2  CE2  CE2\n'
        
        row_list = ['CG2DC1', 'CG251O', 'CG2R51', 'HGA4', '3.0000', '0', '0.0000', '! for ethene, yin/adm jr., 12/95 ! see param HE2 HE2 CE2 CE2']
        
        test_row = node.extract_column_values(basic_case_line, self.mock_parser)

        target_row = pd.DataFrame([row_list],
                                  columns=node.COL_LABELS_AND_DTYPES)
        
        assert_frame_equal(test_row, target_row)
        
        
    def test_extract_column_values_no_comment_value(self):
        """
        Extract values from line without value in comment field.
        """
        
        node = ImproperNode()
        
        no_comment_line = 'CG2DC3    CG2DC1   HGA5     HGA5        3.0000 0        0.00\n'
        
        row_list = ['CG2DC3', 'CG2DC1', 'HGA5', 'HGA5', '3.0000', '0', '0.00', '']

        
        test_row = node.extract_column_values(no_comment_line, self.mock_parser)

        target_row = pd.DataFrame([row_list],
                                  columns=node.COL_LABELS_AND_DTYPES)
        
        assert_frame_equal(test_row, target_row)

        
        
        
        
        
        

if __name__ == '__main__':
    unittest.main()