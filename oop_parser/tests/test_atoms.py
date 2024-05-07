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
from atoms_node import AtomsNode
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
    section_lines = print_section_to_console("ATOMS", "BONDS")

   
# results from dummy data generation for atoms section
representative_lines = [
  '! added by Ronald\n', 
  'MASS  -1  CGCPY1    12.01100   ! analogy to CA / allow for BV ring A\n',
  'MASS  -1  CGCPY2    12.01100   ! analogy to CPM / allow for BV methine bridge ring C-D\n',
  'MASS  -1  CGCPY3    12.01100   ! analogy to CPM / allow for BV methine bridge ring A-B\n',
  'MASS  -1  CGCPY4    12.01100   ! analogy to CPM / allow for BV ring C\n',
  '\n',
  '!carbons\n',
  'MASS  -1  CG1T2     12.01100   ! terminal alkyne H-C#C\n',
  'MASS  -1  CG1N1     12.01100   ! C for cyano  group\n',
  '! Patch for ring-a-cys\n',
  '!MASS  -1  C         12.01100 ! carbonyl C, peptide backbone\n',
  '!MASS  -1  CT1       12.01100 ! aliphatic sp3 C for CH\n',
  '!MASS  -1  O         15.99900 ! carbonyl oxygen\n',
  '!MASS  -1  H          1.00800 ! polar H\n',
  '!MASS  -1  NH1       14.00700 ! peptide nitrogen\n',
  '\n']
    
# 
representative_data_lines = [
 'MASS  -1  CGCPY1    12.01100   ! analogy to CA / allow for BV ring A\n',
 'MASS  -1  CGCPY2    12.01100   ! analogy to CPM / allow for BV methine bridge ring C-D\n',
 'MASS  -1  CGCPY3    12.01100   ! analogy to CPM / allow for BV methine bridge ring A-B\n',
 'MASS  -1  CGCPY4    12.01100   ! analogy to CPM / allow for BV ring C\n',
 'MASS  -1  CG1T2     12.01100   ! terminal alkyne H-C#C\n',
 'MASS  -1  CG1N1     12.01100   ! C for cyano  group\n'
 ]

if data_generation_mode:
    remove_formatting_characters("ATOMS",representative_data_lines)  

row_lists = [['MASS', '-1', 'CGCPY1', '12.01100', '! analogy to CA / allow for BV ring A'],
   ['MASS', '-1', 'CGCPY2', '12.01100', '! analogy to CPM / allow for BV methine bridge ring C-D'],
   ['MASS', '-1', 'CGCPY3', '12.01100', '! analogy to CPM / allow for BV methine bridge ring A-B'],
   ['MASS', '-1', 'CGCPY4', '12.01100', '! analogy to CPM / allow for BV ring C'],
   ['MASS', '-1', 'CG1T2', '12.01100', '! terminal alkyne H-C#C'],
   ['MASS', '-1', 'CG1N1', '12.01100', '! C for cyano group']] 



# %%% Test Atoms Section

class TestAtomsNode(unittest.TestCase):
    
    
    def setUp(self):
        """
        Override setup with additional variables required to test the classes.
        """
        
        super().setUp()
        
        self.mock_parser = Mock(Parser)  # Create a mock Parser object
        
        self.mock_parser.state = MagicMock(return_value="some state")
        
        self.mock_parser.state_transition_manager = MagicMock(return_value="stm")
        
        (self.atom_section_lines, 
          self.representative_lines, 
          self.representative_data_lines, self.row_lists,
          self.atoms_df) =  generate_dummy_data("ATOMS")
        
    def test_process_removes_line(self):
        
        node = AtomsNode()

        lines = [
            'MASS  -1  CGCPY1    12.01100   ! analogy to CA / allow for BV ring A\n',
            'MASS  -1  CGCPY2    12.01100   ! analogy to CPM / allow for BV methine bridge ring C-D\n'
            ]
        
        remaining_lines = node.process(self.mock_parser, lines)
        
        # self.mock_parser.process.assert_called_once_with(node, lines)
        
        self.assertEqual(remaining_lines, 
                      ['MASS  -1  CGCPY2    12.01100   ! analogy to CPM / allow for BV methine bridge ring C-D\n']) 
        


if __name__ == '__main__':
    unittest.main()