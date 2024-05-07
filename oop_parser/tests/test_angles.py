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
from angles_node import AnglesNode
from section_node import SectionNode

from generate_dummy_data import (print_section_to_console, 
                                 remove_formatting_characters,
                                 generate_dummy_data
                                 )



# %%% dummy data modelling
# !!! check module "generate_dummy_data" for instructions and description
# !!! of data generation process


section_name = "ANGLES"

# !!! switch to True for data generation
data_generation_mode = False

if data_generation_mode:
    # !!! change section headlines depending on section to test
    # section_lines = print_section_to_console("ANGLES", "DIHEDRALS",
    #                                          print_half=1)
    section_lines = print_section_to_console("ANGLES", "DIHEDRALS")
  


   
# results from dummy data generation for angles section
representative_lines = [
    'ANGLES\n' ,
    '!-----------------------------GCFFbv´\n' ,
    'CG2DC1   CG251O   CGCPY4   40.00    119.00   !   bv-pfr-c   ,   from   CG2DC3   CG251O   CG2R53,   PENALTY=   6.5\n' ,
    'CGCPY4   CG321    CG321    58.35    114.00   !   INCA   model   for   D3R,   xxwy;   updated   to   match   yxu   par   in   na_rna_modified.prm\n' ,
    '!---------------------------------Ring-D-------------------------------------------------------------------------\n' ,
    'CG2DC3   CG251O   CG2R51   60.00    127.95 ! RDV , from CG2DC3 CG251O CG2R53, penalty= 3,  equilibrium value MP2/6-31Gd\n' ,
    'CG311    CG2O2    OG2D1    70.00    125.00   20.00   2.44200 ! PROT adm jr. 5/02/91, acetic acid pure solvent; LIPID methyl acetate\n' ,
    '\n' ,
    '\n' ,
    ]


representative_data_lines = [
  'CG2DC1   CG251O   CGCPY4   40.00    119.00   !   bv-pfr-c   ,   from   CG2DC3   CG251O   CG2R53,   PENALTY=   6.5\n' ,
  'CGCPY4   CG321    CG321    58.35    114.00   !   INCA   model   for   D3R,   xxwy;   updated   to   match   yxu   par   in   na_rna_modified.prm\n' ,
  'CG2DC3   CG251O   CG2R51   60.00    127.95 ! RDV , from CG2DC3 CG251O CG2R53, penalty= 3,  equilibrium value MP2/6-31Gd\n' ,
  'CG311    CG2O2    OG2D1    70.00    125.00   20.00   2.44200 ! PROT adm jr. 5/02/91, acetic acid pure solvent; LIPID methyl acetate\n'
    ]

if data_generation_mode:
    row_lists = remove_formatting_characters(section_name, representative_data_lines)


row_lists = [
['CG2DC1', 'CG251O', 'CGCPY4', '40.00', '119.00', '! bv-pfr-c , from CG2DC3 CG251O CG2R53, PENALTY= 6.5'] ,
['CGCPY4', 'CG321', 'CG321', '58.35', '114.00', '! INCA model for D3R, xxwy; updated to match yxu par in na_rna_modified.prm'] ,
['CG2DC3', 'CG251O', 'CG2R51', '60.00', '127.95', '! RDV , from CG2DC3 CG251O CG2R53, penalty= 3, equilibrium value MP2/6-31Gd'] ,
['CG311', 'CG2O2', 'OG2D1', '70.00', '125.00', '20.00', '2.44200', '! PROT adm jr. 5/02/91, acetic acid pure solvent; LIPID methyl acetate']
]



# %%% Test Section

class TestAnglesNode(unittest.TestCase):
    
    
    def setUp(self):
        """
        Override setup with additional variables required to test the classes.
        """
        
        super().setUp()
        
        self.mock_parser = Mock(Parser)  # Create a mock Parser object
        
        self.mock_parser.state = MagicMock(return_value="some state")
        
        self.mock_parser.state_transition_manager = MagicMock(return_value="stm")
        
        self.COL_LABELS_AND_DTYPES = {"atom1": str, 
                                          "atom2": str, 
                                          "atom3": str, 
                                          "ktheta": float, 
                                          "theta0": float, 
                                          "comment": str
                                          }
            
        self.COL_LABELS_AND_DTYPES_urey_bradley = {"atom1": str, 
                                          "atom2": str, 
                                          "atom3": str, 
                                          "ktheta": float, 
                                          "theta0": float, 
                                          "kub": float,
                                          "s0": float,
                                          "comment": str
                                          }
        
        (self.angles_section_lines, 
          self.representative_lines, 
          self.representative_data_lines, self.row_lists,
          self.angles_df) =  generate_dummy_data(section_name)
        
        
    def test_process_line(self):
        """
        Test if process method of node prunes remaining lines by 
        processed line.
        """
        
        node = AnglesNode()

        lines =     ['CG2DC1   CG251O   CGCPY4   40.00    119.00   !   bv-pfr-c   ,   from   CG2DC3   CG251O   CG2R53,   PENALTY=   6.5\n' ,
                'CGCPY4   CG321    CG321    58.35    114.00   !   INCA   model   for   D3R,   xxwy;   updated   to   match   yxu   par   in   na_rna_modified.prm\n'
                ]
        
        remaining_lines = node.process(self.mock_parser, lines)
        
        # self.mock_parser.process.assert_called_once_with(node, lines)
        
        self.assertEqual(remaining_lines, 
                      ['CGCPY4   CG321    CG321    58.35    114.00   !   INCA   model   for   D3R,   xxwy;   updated   to   match   yxu   par   in   na_rna_modified.prm\n']) 
        
        

    def test_extract_column_values_6_cols(self):
        """
        Process line without info on urey bradley params.
        """
        
        #!!! parameterizeb with the following:
             
                # basic_case_line = 'CG2DC1   CG251O   CGCPY4   40.00    119.00   !   bv-pfr-c   ,   from   CG2DC3   CG251O   CG2R53,   PENALTY=   6.5\n'
                
                # row_list = ['CG2DC1', 'CG251O', 'CGCPY4', '40.00', '119.00', '! bv-pfr-c , from CG2DC3 CG251O CG2R53, PENALTY= 6.5']
                
        
        node = AnglesNode()
        
        # set up input line for extract_column_values method
        basic_case_line = 'CG2DC3   CG251O   CG2R51   60.00    127.95 ! RDV , from CG2DC3 CG251O CG2R53, penalty= 3,  equilibrium value MP2/6-31Gd\n'
        
        # hardcode expected row of df as list
        row_list = ['CG2DC3', 'CG251O', 'CG2R51', '60.00', '127.95', '! RDV , from CG2DC3 CG251O CG2R53, penalty= 3, equilibrium value MP2/6-31Gd']
        
        # extract df row from test line
        test_row = node.extract_column_values(basic_case_line, self.mock_parser)

        # assign expected df row
        target_row = pd.DataFrame([row_list],
                                  columns=self.COL_LABELS_AND_DTYPES)
        
        # validate test row
        assert_frame_equal(test_row, target_row)
        
        # print(f"test_extract_column_values_6_cols: {target_row}, {test_row}")



    def test_extract_column_values_8_cols(self):
        """
        Process line with info on urey bradley params in form of 2 additional 
        values.
        """
        
        node = AnglesNode()
        
        # set up input line for extract_column_values method
        urey_bradley_line = 'CG311    CG2O2    OG2D1    70.00    125.00   20.00   2.44200 ! PROT adm jr. 5/02/91, acetic acid pure solvent; LIPID methyl acetate\n'
        
        # hardcode expected row of df as list
        row_list = ['CG311', 'CG2O2', 'OG2D1', '70.00', '125.00', '20.00', '2.44200', '! PROT adm jr. 5/02/91, acetic acid pure solvent; LIPID methyl acetate']
        
        # extract df row from test line
        test_row = node.extract_column_values(urey_bradley_line, self.mock_parser)
                
        # assign expected df row
        target_row = pd.DataFrame([row_list],
                                  columns=node.COL_LABELS_AND_DTYPES)
        
        # validate test row
        assert_frame_equal(test_row, target_row)
        
        
    # def test_validate_datatypes_6_cols(self):
    #     node = AnglesNode()

        
    #     test_row = pd.DataFrame([['CG2DC1', 'CG251O', 'CGCPY4', '40.00', '119.00', '! bv-pfr-c , from CG2DC3 CG251O CG2R53, PENALTY= 6.5'] ,
    #                                  ], columns=node.COL_LABELS_AND_DTYPES_optional)

    #     target_row = pd.DataFrame([row_list],
    #                                       columns=node.COL_LABELS_AND_DTYPES_optional)
                
    
    # def test_validate_datatypes_6_cols(self):
        
    #     node = AnglesNode()
        
    #     urey_bradley_line = 'CG311    CG2O2    OG2D1    70.00    125.00   20.00   2.44200 ! PROT adm jr. 5/02/91, acetic acid pure solvent; LIPID methyl acetate\n'


    #     row_list = ['CG311', 'CG2O2', 'OG2D1', '70.00', '125.00', '20.00', '2.44200', '! PROT adm jr. 5/02/91, acetic acid pure solvent; LIPID methyl acetate']
        
    #     test_row = node.extract_column_values(urey_bradley_line, self.mock_parser)
                
    #     target_row = pd.DataFrame([row_list],
    #                               columns=node.COL_LABELS_AND_DTYPES_optional)
        
    #     assert_frame_equal(test_row, target_row)
        
        
        
        
        
        
        
        
        

if __name__ == '__main__':
    unittest.main()