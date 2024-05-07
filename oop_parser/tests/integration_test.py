import sys

sys.path.append("/Users/jhome/code/praktikum/helpers/oop_parser")

import unittest
import pandas as pd
import numpy as np

from pandas.testing import assert_frame_equal

from state_transition_manager import StateTransitionManager
from config import Config

from parser import Parser

from prm_test_setup_mixin import ParamParserTestSetup



test_file_p = "/Users/jhome/code/praktikum/helpers/oop_parser/files_to_parse/par_bv.prm"

def model_dummy_data(absolute_file_path, 
                     section_start_specifier, 
                     section_end_specifier,
                     generation_mode=False):
    """
    Generate dummy data for atom section.
    
    Set generation_mode to True to execute print statements and use function
    for data generation.
    
    Read comments for detailed explanation/instructions.
    """
    section_names = ["ATOMS", "BONDS", "ANGLES", "IMPROPER", 
                          "DIHEDRALS", "NONBONDED"]
    
    # read prm file
    with open(absolute_file_path) as f:
        # read lines as raw strings
        pmf_lines = f.readlines()
        

    # get idx of atom section headline
    # !!! purposefully use for loop instead of list comprehension for clarity
    for idx, line in enumerate(pmf_lines):
        if line.strip() == section_start_specifier:
            atom_section_start_line_idx = idx
            
    # confirm idx manually
    if generation_mode:
        print(f" Index: {atom_section_start_line_idx}\n\
              Line: {pmf_lines[atom_section_start_line_idx]}")
              
    # get idx of atom section headline
    # !!! purposefully use for loop instead of list comprehension for clarity
    for idx, line in enumerate(pmf_lines):
        if line.strip() == section_end_specifier:
            bonds_section_start_line_idx = idx
    
    # confirm idx manually
    if generation_mode:
        print(f" Index: {bonds_section_start_line_idx}\n\
              Line: {pmf_lines[bonds_section_start_line_idx]}")

    # slice atoms section
    
    atom_section_lines = pmf_lines[
                    atom_section_start_line_idx:bonds_section_start_line_idx]
    
    # # save number of lines for raw atom section
    # number_of_lines_in_atom_section = len(atom_section_lines)
    
    if generation_mode:
    
        for line in atom_section_lines:
            # print out raw representation of string
            print(repr(line))
            # elaborate on lines that shouldn't count as data row:
                # formatting/supplementary information: lines starting with '!'
                # completely empty lines: newlines ('\n')
    
    
    # copy/paste some lines that make good dummy data
    # (containing all different types of formatting lines, etc.)
    
    # contains
    representative_lines_bonds = [
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


# !!! uncomment and adjust args for dummy data printouts to console
# model_dummy_data(test_file_p,"ANGLES", "IMPROPER", True)








# %%% Integration Tests


class IntegrationTest(ParamParserTestSetup, unittest.TestCase):
    """
    ParamParserTestSetup:
        Inherits from that mixin class to instantiate setUp method:
            instantiates multiple variables used in testcases within 
            this TestCase class.
         
    1) Tests correct parser initializations.
            
    2) Tests correctness of dataframes for parsed sections EXPLICITLY!
            
        Explicit test scenarios include a realistic model sequence representing 
        a .prm file, i.e. it includes the same shape and structure:
            - intro lines
            - newline characters
            - all possible forms of lines for section under test
            - comments
            - headline for subsequent section to specify section end
            - file end specifier (END)
    
    """
    
    def setUp(self):
        """
        Override setup with additional variables required to test the classes.
        
        # !!! Explanation for Nereu:
            I try to reduce duplicate code by assigning vars used in multiple
            test methods to "self.var_name". 
            
            In contrast, test method vars unique to the method don't have 
            "self." as prefix.
        
        """
        
        super().setUp()
        
        self.config = Config()
        
        self.stm = StateTransitionManager()
    
        self.parser = Parser(filepath=self.prm_file_path, 
                    config=self.config,
                    StateTransitionManager=StateTransitionManager)
        
        
            
    def test_parser_initilization(self):
        """
        Test if instantiation of the parser object initializes properly:
            setting the current state to the StateTransitionManager.

        """
        
        # instantiate parser
        p = Parser(filepath=self.prm_file_path, 
                    config=self.config,
                    StateTransitionManager=StateTransitionManager)
        
        # assert state
        self.assertEqual(p.state, p.state_transition_manager)


    def test_param_sets_config_filetype(self):
        """
        Test if instantiation of the parser object initializes properly:
            setting the config file type.
        """
        
        p = Parser(filepath=self.prm_file_path, 
                    config=self.config,
                    StateTransitionManager=StateTransitionManager)
        
        self.assertEqual(p.config.file_type, "prm")

        
        
    def test_stm_bond_recognition(self):
        """
        If "BONDS" is found in line, does STM do the following:
            - initiate bonds node?
            - changes parser state to it?
            
        tested via type validation of parsers current state    
        """
        
        # process a line that resembles BONDS section headline
        self.parser.state_transition_manager.process(self.parser, ['BONDS\n'])

        # assert parser state was set to the "Bonds Node" state
        self.assertTrue(isinstance(self.parser.state, Config.PRM_SECTION_NODE_CLASSES["Bonds Node"]))
        
        
        
    def test_atoms_section_df(self):
        """
        Test if atoms section is parsed correctly.
        
        See TestCase Docstring 2) for more details.

        """
        
        representative_lines = [
'*some intro line\n',
'\n',
'ATOMS\n'
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
'\n',
'BONDS\n',
'!-------------------------------------GCFF-bv----------------------------------------------------------\n',
'CG2R51   OG312    525.00   1.2600   !   bv-pfr-c   ,   from   CG2R61   OG312,   PENALTY=   45\n',
'\n',
'END'
            ]
        
        # assign lines to parser
        self.parser.lines = representative_lines
        
        # start parsing
        self.parser.start()
        
        # access atoms node object
        atoms_node = self.parser.nodes["Atoms Node"][0]
        
        # access atoms column labels and datatypes container
        atoms_column_labels = atoms_node.COL_LABELS_AND_DTYPES
        
        # access section dataframe we want to test
        test_df = atoms_node.section_dataframe

        # hardcode the expected dataframe as a result from our input lines
        target_df = pd.DataFrame(
        [
        ['MASS', '-1', 'CGCPY1', '12.01100', '! analogy to CA / allow for BV ring A'],
        ['MASS', '-1', 'CGCPY2', '12.01100', '! analogy to CPM / allow for BV methine bridge ring C-D'],
        ['MASS', '-1', 'CGCPY3', '12.01100', '! analogy to CPM / allow for BV methine bridge ring A-B'],
        ['MASS', '-1', 'CGCPY4', '12.01100', '! analogy to CPM / allow for BV ring C'],
        ['MASS', '-1', 'CG1T2', '12.01100', '! terminal alkyne H-C#C'],
        ['MASS', '-1', 'CG1N1', '12.01100', '! C for cyano group']
        ], 
                                 columns=atoms_column_labels)
                     
        # assert correctness of dataframes
        assert_frame_equal(target_df, test_df)
        
        
        
    def test_bonds_section_df(self):
        """
        Test if bonds section is parsed correctly.
        
        See TestCase Docstring 2) for more details.

        """
        
    
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
        
        self.parser.lines = representative_lines
        self.parser.start()
        
        bonds_node = self.parser.nodes["Bonds Node"][0]
        
        bonds_column_labels = bonds_node.COL_LABELS_AND_DTYPES
        
        test_df = self.parser.nodes["Bonds Node"][0].section_dataframe
        
        target_df = pd.DataFrame([
            ['CG2R51', 'OG312', '525.00', '1.2600', '! bv-pfr-c , from CG2R61 OG312, PENALTY= 45'],
        ['OG311', 'CG2O2', '800.00', '1.3550', '! ras-chim , from CG321 NG321, penalty= 4'],
        ['CG2O2', 'NH1', '370.000', '1.3450', '! ALLOW PEP POL ARO'],
        ['CG311', 'HGA1', '309.00', '1.1110', '! PROT alkane update, adm jr., 3/2/92']
        ] , columns=bonds_column_labels)
                     
        assert_frame_equal(target_df, test_df)
        
       
    def test_angles_section_df(self):
        """
        Test if angles section is parsed correctly.
        
        See TestCase Docstring 2) for more details.

        """
    
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
        
        self.parser.lines = representative_lines
        self.parser.start()
        
        angles_node = self.parser.nodes["Angles Node"][0]
        
        angles_column_labels = angles_node.COL_LABELS_AND_DTYPES
        
        test_df = self.parser.nodes["Angles Node"][0].section_dataframe
        
        # rows without urey bradly values have NaN values instead
        target_df = pd.DataFrame([
        ['CG2DC1', 'CG251O', 'CGCPY4', '40.00', '119.00', np.nan, np.nan, '! bv-pfr-c , from CG2DC3 CG251O CG2R53, PENALTY= 6.5'] ,
        ['CGCPY4', 'CG321', 'CG321', '58.35', '114.00', np.nan, np.nan, '! INCA model for D3R, xxwy; updated to match yxu par in na_rna_modified.prm'] ,
        ['CG2DC3', 'CG251O', 'CG2R51', '60.00', '127.95', np.nan, np.nan,'! RDV , from CG2DC3 CG251O CG2R53, penalty= 3, equilibrium value MP2/6-31Gd'] ,
        ['CG311', 'CG2O2', 'OG2D1', '70.00', '125.00', '20.00', '2.44200', '! PROT adm jr. 5/02/91, acetic acid pure solvent; LIPID methyl acetate']
        ] , columns=angles_column_labels)
                             
        assert_frame_equal(target_df, test_df)
        
        
    def test_dihedrals_section_df(self):
        """
        Test if dihedrals section is parsed correctly.
        
        See TestCase Docstring 2) for more details.

        """

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
        
        self.parser.lines = representative_lines
        self.parser.start()
        
        dihedrals_node = self.parser.nodes["Dihedrals Node"][0]
        
        dihedrals_column_labels = dihedrals_node.COL_LABELS_AND_DTYPES
        
        test_df = self.parser.nodes["Dihedrals Node"][0].section_dataframe
        
        # rows without urey bradly values have NaN values instead
        target_df = pd.DataFrame([ 
                ['OG311', 'CG2O2', 'CG321', 'CG321', '0.0500', '6', '180.00', '! From X CT2 CC X'] ,
                ['CGCPY3', 'CG252O', 'CGCPY1', 'CG2DC1', '0.2000', '2', '180.00', '! bv-pfr-c , from CG2DC3 CG251O CG2R53 NG2R53, PENALTY= 152.5'] ,
                ['CG2R51', 'CG251O', 'CGCPY2', 'HGA4', '3.9000', '2', '180.00', '! bv-pfr-c , from CG2R53 CG251O CG2DC3 HGA5, PENALTY= 33'] ,
                ['HGA4', 'CG2DC1', 'CG321', 'SG311', '0.2000', '3', '0.00', '! bv-pfr-c , from HGA4 CG2DC1 CG321 OG3R60, PENALTY= 122.2'] ,
                ['CG2DC3', 'CG2DC1', 'CGCPY6', 'CGCPY5', '1.13', '2', '180.00', ''] ,
                ['HB1', 'CT1', 'C', 'NG321', '0.0000', '1', '0.00', '! ALLOW PEP'] ,
                ['CG2O2', 'CG311', 'CG321', 'HGA2', '0.2000', '3', '0.00', '! AMGA, Alpha Methyl Glu Acid CDCA']
                ] , columns=dihedrals_column_labels)
                             
        assert_frame_equal(target_df, test_df)
        

    def test_improper_section_df(self):
        """
        Test if improper section is parsed correctly.
        
        See TestCase Docstring 2) for more details.

        """
        
        representative_lines = [
        'IMPROPER\n' ,
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
        
        self.parser.lines = representative_lines
        self.parser.start()
        
        improper_node = self.parser.nodes["Improper Node"][0]
        
        improper_column_labels = improper_node.COL_LABELS_AND_DTYPES
        
        test_df = self.parser.nodes["Improper Node"][0].section_dataframe
        
        # rows without urey bradly values have NaN values instead
        target_df = pd.DataFrame([
        ['CG2DC1', 'CG251O', 'CG2R51', 'HGA4', '3.0000', '0', '0.0000', '! for ethene, yin/adm jr., 12/95 ! see param HE2 HE2 CE2 CE2'] ,
        ['CG2R53', 'CG3C51', 'NG2R53', 'OG2D1', '90.0000', '0', '0.00', '! bv-pfr-c , from CG2R53 CG3C52 NG2R53 OG2D1, PENALTY= 0.4'] ,
        ['CG2O2', 'CG311', 'NH1', 'OG2D1', '120.0000', '0', '0.0000', '! ALLOW PEP POL ARO'] ,
        ['CGCPY1', 'CG3C51', 'CG252O', 'CG2DC1', '140.0000', '0', '0.0000', '! ALLOW HEM !'] ,
        ['CG2DC3', 'CG2DC1', 'HGA5', 'HGA5', '3.0000', '0', '0.00', ''] ,
        ['NG2R51', 'CG2R51', 'CG2R51', 'HGP1', '0.010', '0', '0.0000', '! ALLOW ARO']
        ] , columns=improper_column_labels)
                             
        assert_frame_equal(target_df, test_df)
        
        
        
    def test_nonbonded_section_df(self):
        """
        Test if nonbonded section is parsed correctly.
        
        See TestCase Docstring 2) for more details.
    
        Model lines contain both possible cases for row lengths:
            1) 5 total values (without 1_4 values)
            2) 8 total values (containing 1_4 values):
                                    "ignored_1_4": float,
                                    "epsilon_1_4": float,
                                    "rminhalf_1_4": float,
        """
        
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
        
        self.parser.lines = representative_lines
        self.parser.start()
        
        nonbonded_node = self.parser.nodes["Nonbonded Node"][0]
        
        nonbonded_column_labels = nonbonded_node.COL_LABELS_AND_DTYPES
        
        test_df = self.parser.nodes["Nonbonded Node"][0].section_dataframe
                
        # rows without urey bradly values have NaN values instead
        target_df = pd.DataFrame([
        ['HGA1', '0.0', '-0.0450', '1.3400', np.nan, np.nan, np.nan, '! alkane, igor, 6/05'] ,
        ['CG1T2', '0.0', '-0.1032', '1.9925', np.nan, np.nan, np.nan, '! PRPY, propyne, rima & kevo'] ,
        ['CG311', '0.0', '-0.0320', '2.0000', '0.0', '-0.01', '1.9', '! alkane (CT1), isobutane, 6/05 viv'],
        ['CG3AM1', '0.0', '-0.0780', '1.9800', np.nan, np.nan, np.nan,  '! aliphatic amines'] ,
        ['CGCPY1', '0.0', '-0.0680', '2.0900', np.nan, np.nan, np.nan,  '! same as CG2DC1 but in 5-membered ring with exocyclic double bond'] ,
        ['CGCPY6', '0.0', '-0.0500', '2.1000', np.nan, np.nan, np.nan,  '! INDO/TRP; bulk solvent of 10 maybridge cmpds (kevo)']
        ] , columns=nonbonded_column_labels)
                             
        assert_frame_equal(target_df, test_df)
                
        

        
        
        
if __name__ == "__main__":
    unittest.main()
                   
        
        