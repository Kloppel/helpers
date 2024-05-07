import unittest
import re
import pandas as pd

def model_dummy_data(absolute_file_path, generation_mode=False):
    # "par_bv.prm"
    """
    Generate dummy data for atom section.
    Set generation_mode to True to execute print statements and use function
    for data generation.
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
        if line.strip() == "ATOMS":
            atom_section_start_line_idx = idx
    
    
    # confirm idx manually
    if generation_mode:
        print(f" Index: {atom_section_start_line_idx}\n\
              Line: {pmf_lines[atom_section_start_line_idx]}")
              
    # get idx of atom section headline
    # !!! purposefully use for loop instead of list comprehension for clarity
    for idx, line in enumerate(pmf_lines):
        if line.strip() == "BONDS":
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
    
    # manually introduced an error in last line:
        # two spaces separate the words "cyano" and "group"
    # penultimate line contains file-intrinsic error:
        # atomtype and mass value are separated by an additional space
    representative_data_lines = [
     'MASS  -1  CGCPY1    12.01100   ! analogy to CA / allow for BV ring A\n',
     'MASS  -1  CGCPY2    12.01100   ! analogy to CPM / allow for BV methine bridge ring C-D\n',
     'MASS  -1  CGCPY3    12.01100   ! analogy to CPM / allow for BV methine bridge ring A-B\n',
     'MASS  -1  CGCPY4    12.01100   ! analogy to CPM / allow for BV ring C\n',
     'MASS  -1  CG1T2     12.01100   ! terminal alkyne H-C#C\n',
     'MASS  -1  CG1N1     12.01100   ! C for cyano  group\n'
     ]

    # regex pattern: 2 or 3 space characters
    pattern = r" {2,4}"
    
    # split values upon 2 or 3 subsequent space characters
    row_lists = [re.split(pattern, i) for i in representative_data_lines]
    
    # remove newline character from comment
    # remove any leading or trailing spaces
    if generation_mode:
        for row_list in row_lists:
            # access comment value and strip newline char
            row_list[-1] = row_list[-1].rstrip("\n")
            print(row_list)
        
    row_lists = [['MASS', '-1', 'CGCPY1', '12.01100', '! analogy to CA / allow for BV ring A'],
    ['MASS', '-1', 'CGCPY2', '12.01100', '! analogy to CPM / allow for BV methine bridge ring C-D'],
    ['MASS', '-1', 'CGCPY3', '12.01100', '! analogy to CPM / allow for BV methine bridge ring A-B'],
    ['MASS', '-1', 'CGCPY4', '12.01100', '! analogy to CPM / allow for BV ring C'],
    ['MASS', '-1', 'CG1T2', '12.01100', '! terminal alkyne H-C#C'],
    ['MASS', '-1', 'CG1N1', '12.01100', '! C for cyano group']]
    
    # print(row_lists)    
    
    atoms_column_labels = ["mass", "number", "atomtype", "mass_value", "comment"]
    
    atoms_df = pd.DataFrame(row_lists, 
                      columns=atoms_column_labels)
    
    
    # Security check: make sure values really contain no unwanted spaces
    # container for erroneous rows
    erroneous_rows = []
    for col_label in ["mass", "number", "atomtype", "mass_value"]:
        err_lines = atoms_df.loc[atoms_df[col_label].apply(lambda val: " " in val)]
        if not err_lines.empty:
            erroneous_rows.append(err_lines)
    
    if erroneous_rows:
        raise ValueError("some data values have space characters")
    
      
    return (atom_section_lines, representative_lines, representative_data_lines,
            row_lists, atoms_df)


# %%% Testcase class

class ParamParserTestSetup(unittest.TestCase):
    
    def setUp(self):
        
        self.section_names = ["ATOMS", "BONDS", "ANGLES", "IMPROPER", 
                              "DIHEDRALS", "NONBONDED"]
        
        self.atoms_column_labels = ["mass", "number", "atomtype", "mass_value", 
                               "comment"]
        
        self.section_formats_dict = {
               'ATOMS': 
                   {'mass': str, 'number': int, 'atomtype': str, 'mass_value': float, 'comment': str},
               'BONDS': 
                   {'atom1': str, 'atom2': str, 'kb': float, 'b0': float, 'comment': str}, 
               'ANGLES': 
                   {'atom1': str, 'atom2': str, 'atom3': str, 'ktheta': float, 'theta0': float, 'comment': str}, 
               'IMPROPER': 
                   {"atom1": str, 
                                                 "atom2": str, 
                                                 "atom3": str, 
                                                 "atom4": str, 
                                                 "kpsi": float,
                                                 "0": int,
                                                 "psi0": float,
                                                 "comment": str}, 
               'DIHEDRALS': 
                   {'atom1': str, 'atom2': str, 'atom3': str, 'atom4': str, 'kchi': float, 'n': int, 'delta': float, 'comment': str}, 
               'NONBONDED': 
                   { 
                                                   "atom": str, 
                                                   "ignored": float, 
                                                   "epsilon": float, 
                                                   "rminhalf": float, 
                                                   "ignored_1_4": float,
                                                   "epsilon_1_4": float,
                                                   "rminhalf_1_4": float,
                                                   "comment": str}
        }
            
         
                  
        self.prm_file_path = "/Users/jhome/code/praktikum/helpers/oop_parser/files_to_parse/par_bv.prm"
        # read prm file
        with open(self.prm_file_path) as f:
            # read lines as raw strings
            self.pmf_lines = f.readlines()
            
        (self.atom_section_lines, 
         self.representative_lines, 
         self.representative_data_lines, self.row_lists,
         self.atoms_df) =  model_dummy_data(self.prm_file_path)
            
        
        