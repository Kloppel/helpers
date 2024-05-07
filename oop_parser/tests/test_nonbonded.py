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
from nonbonded_node import NonbondedNode
from section_node import SectionNode

from generate_dummy_data import (print_section_to_console, 
                                 remove_formatting_characters,
                                 generate_dummy_data
                                 )



# %%% dummy data modelling
# !!! check module "generate_dummy_data" for instructions and description
# !!! of data generation process


section_name = "NONBONDED"

# !!! switch to True for data generation
data_generation_mode = False

if data_generation_mode:
    # !!! change section headlines depending on section to test
    # section_lines = print_section_to_console("ANGLES", "NONBONDED",
    #                                          print_half=1)
    section_lines = print_section_to_console("NONBONDED", "END")
  


   
# results from dummy data generation for nonbonded section
    # edge case lines include:
        # section heading
        # comment lines (starting with !)
        # empty lines (\n)
        # line without comment field value
        # tab'ed comment line (           !...)
        
representative_lines = [
    'NONBONDED nbxmod  5 atom cdiel fshift vatom vdistance vfswitch -\n' ,
    'cutnb 14.0 ctofnb 12.0 ctonnb 10.0 eps 1.0 e14fac 1.0 wmin 1.5\n' ,
    '!hydrogens\n' ,
    'HGA1     0.0       -0.0450     1.3400 ! alkane, igor, 6/05\n' ,
    '!carbons\n' ,
    'CG1T2    0.0       -0.1032     1.9925 ! PRPY, propyne, rima & kevo\n' ,
    "! THESE ARE IGOR'S ALKANE AND THF PARAMS\n" ,
    'CG311    0.0       -0.0320     2.0000   0.0 -0.01 1.9 ! alkane (CT1), isobutane, 6/05 viv\n' ,
    '! "highly specialized amine parameters"\n' ,
    'CG3AM1   0.0       -0.0780     1.9800 ! aliphatic amines\n' ,
    '\n' ,
    '!--------------------------------------------BV-parameters-------------------------------------------\n' ,
    'CGCPY1   0.0       -0.0680     2.0900 ! same as CG2DC1 but in 5-membered ring with exocyclic double bond\n',
    'CGCPY6   0.0       -0.0500     2.1000 ! INDO/TRP; bulk solvent of 10 maybridge cmpds (kevo)\n' ,
    '!-----------------------------------------------------------------------------------------------------\n'
]


representative_data_lines = [
    'HGA1     0.0       -0.0450     1.3400 ! alkane, igor, 6/05\n' ,
    'CG1T2    0.0       -0.1032     1.9925 ! PRPY, propyne, rima & kevo\n' ,
    'CG311    0.0       -0.0320     2.0000   0.0 -0.01 1.9 ! alkane (CT1), isobutane, 6/05 viv\n' ,
    'CG3AM1   0.0       -0.0780     1.9800 ! aliphatic amines\n' ,
    'CGCPY1   0.0       -0.0680     2.0900 ! same as CG2DC1 but in 5-membered ring with exocyclic double bond\n',
    'CGCPY6   0.0       -0.0500     2.1000 ! INDO/TRP; bulk solvent of 10 maybridge cmpds (kevo)\n' 
]


if data_generation_mode:
    row_lists = remove_formatting_characters(section_name, representative_data_lines)


row_lists = [
['HGA1', '0.0', '-0.0450', '1.3400', '! alkane, igor, 6/05'] ,
['CG1T2', '0.0', '-0.1032', '1.9925', '! PRPY, propyne, rima & kevo'] ,
['CG311', '0.0', '-0.0320', '2.0000', '0.0', '-0.01', '1.9', '! alkane (CT1), isobutane, 6/05 viv'],
['CG3AM1', '0.0', '-0.0780', '1.9800', '! aliphatic amines'] ,
['CGCPY1', '0.0', '-0.0680', '2.0900', '! same as CG2DC1 but in 5-membered ring with exocyclic double bond'] ,
['CGCPY6', '0.0', '-0.0500', '2.1000', '! INDO/TRP; bulk solvent of 10 maybridge cmpds (kevo)']
]


# %%% Test Section

class TestNonbondedNode(unittest.TestCase):
    
    
    def setUp(self):
        """
        Override setup with additional variables required to test the classes.
        """
        
        super().setUp()
        
        self.mock_parser = Mock(Parser)  # Create a mock Parser object
        
        self.mock_parser.state = MagicMock(return_value="some state")
        
        self.mock_parser.state_transition_manager = MagicMock(return_value="stm")
        

        
        (self.nonbonded_section_lines, 
          self.representative_lines, 
          self.representative_data_lines, self.row_lists,
          self.nonbonded_df) =  generate_dummy_data(section_name)
        
        
    def test_process_line(self):
        """
        Test if process method of nonbonded node prunes remaining lines by 
        processed line.
        """
        
        node = NonbondedNode()

        lines =     [
'CGCPY1   0.0       -0.0680     2.0900 ! same as CG2DC1 but in 5-membered ring with exocyclic double bond\n',
'CGCPY6   0.0       -0.0500     2.1000 ! INDO/TRP; bulk solvent of 10 maybridge cmpds (kevo)\n'
          ]
        
        # call process method and add a magic mock object as parser
        remaining_lines = node.process(self.mock_parser, lines)
        
        # self.mock_parser.process.assert_called_once_with(node, lines)
        
        # assert sequence was pruned by processed line
        self.assertEqual(remaining_lines, 
                      ['CGCPY6   0.0       -0.0500     2.1000 ! INDO/TRP; bulk solvent of 10 maybridge cmpds (kevo)\n']) 
        
        

    def test_extract_column_values_regular_optional_line(self):
        """
        Extract values from regular line without 1_4 values.
        """
        
        # instantiate node
        node = NonbondedNode()
        
        # set up input line for extract_column_values method
        basic_case_line = 'CGCPY1   0.0       -0.0680     2.0900 ! same as CG2DC1 but in 5-membered ring with exocyclic double bond\n'
        
        # hardcode expected row of df as list
        row_list = ['CGCPY1', '0.0', '-0.0680', '2.0900', '! same as CG2DC1 but in 5-membered ring with exocyclic double bond']
        
        # extract df row from test line
        test_row = node.extract_column_values(basic_case_line, self.mock_parser)

        # assign expected df row
        target_row = pd.DataFrame([row_list],
                                  columns=node.COL_LABELS_AND_DTYPES_optional)
        
        # validate test row
        assert_frame_equal(test_row, target_row)
        


    def test_extract_column_values_regular_full_length_line(self):
        """
        Extract values from regular full length line.
        """
        
        # instantiate node
        node = NonbondedNode()
        
        # set up input line for extract_column_values method
        basic_case_line = 'CG311    0.0       -0.0320     2.0000   0.0 -0.01 1.9 ! alkane (CT1), isobutane, 6/05 viv\n'
        
        # hardcode expected row of df as list
        row_list = ['CG311', '0.0', '-0.0320', '2.0000', '0.0', '-0.01', '1.9', '! alkane (CT1), isobutane, 6/05 viv']
        
        # extract df row from test line
        test_row = node.extract_column_values(basic_case_line, self.mock_parser)
        
        # assign expected df row
        target_row = pd.DataFrame([row_list],
                                  columns=node.COL_LABELS_AND_DTYPES)
        
        # validate test row
        assert_frame_equal(test_row, target_row)
        
        
        
    def test_extract_column_values_no_comment_value(self):
        """
        Extract values from line without value in comment field.
        """
        
        # instantiate node
        node = NonbondedNode()
        
        # set up input line for extract_column_values method
        no_comment_line = 'CG2DC3    CG2DC1   HGA5     HGA5        3.0000 0        0.00\n'
        
        # hardcode expected row of df as list
        row_list = ['CG2DC3', 'CG2DC1', 'HGA5', 'HGA5', '3.0000', '0', '0.00', '']

        # extract df row from test line
        test_row = node.extract_column_values(no_comment_line, self.mock_parser)

        # assign expected df row
        target_row = pd.DataFrame([row_list],
                                  columns=node.COL_LABELS_AND_DTYPES)
        
        # validate test row
        assert_frame_equal(test_row, target_row)

        
        
        
        
        
        

if __name__ == '__main__':
    unittest.main()