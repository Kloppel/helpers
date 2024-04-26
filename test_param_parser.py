import pandas as pd
import re
import unittest
from pandas.testing import assert_frame_equal

from param_parser import (read_prm_file,
                          set_section_format, 
                          group_lines_by_sections,
                          remove_non_data_lines,
                          extract_column_values,
                          create_df,
                          validate_datatypes,
                          main)




def model_dummy_data(relative_file_path, generation_mode=False):
    # "par_bv.prm"
    """
    Generate dummy data for atom section.
    Set generation_mode to True to execute print statements and use function
    for data generation.
    """
    section_names = ["ATOMS", "BONDS", "ANGLES", "IMPROPER", 
                          "DIHEDRALS", "NONBONDED"]
    
    # read prm file
    with open(relative_file_path) as f:
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



    
    


class TestParamParser(unittest.TestCase):
    
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
                   {'None': None}, 
               'DIHEDRALS': 
                   {'atom1': str, 'atom2': str, 'atom3': str, 'atom4': str, 'kchi': float, 'n': int, 'delta': float, 'comment': str}, 
               'NONBONDED': 
                   {'atom': str, 'ignored': float, 'epsilon': float, 'rminhalf': float, 'comment': str}}
        
        # read prm file
        with open("par_bv.prm") as f:
            # read lines as raw strings
            self.pmf_lines = f.readlines()
            
        (self.atom_section_lines, 
         self.representative_lines, 
         self.representative_data_lines, self.row_lists,
         self.atoms_df) =  model_dummy_data("par_bv.prm")
            

    def test_read_prm_file_relative_path(self):
        """
        Positive control:
            Test if relative import works by providing just the filename.
            
        Dependency:
            "par_bv.prm" must exist within directory where parser is located.
        """
        
        lines = read_prm_file("par_bv.prm")
        
        self.assertTrue(lines)
        
    
    def test_read_prm_file_nonexistent(self):
        """
        Negative control:
            Test if error is raised when no such file is present in parser dir.
        """
        
        self.assertRaises(FileNotFoundError, read_prm_file, 
                          "this_file_definitely_does_not_exist.prm")
        
        
    def test_read_prm_file_absolute_path(self):
        """
        Incorporate in future version via mock object.
        """
        pass
                

    def test_set_section_format(self):
        """
        Test if format dict is generate correctly.
        """
        
        test_dict = set_section_format()
                
        self.assertEqual(test_dict, self.section_formats_dict)

    
    def test_group_lines_by_sections_confirm_section_names(self):
        """
        Test correct naming of sections.
        """
        

            
        names_and_lines = group_lines_by_sections(self.pmf_lines, self.section_names)
        
        self.assertEqual(sorted(self.section_names), sorted(
                                                        list(names_and_lines)))


    def test_remove_non_data_lines(self):
        """
        Test if function returns list where each line represents a row of data.
        """
        
        # section snippet including formatting lines
        raw_lines = self.representative_lines
        # data-containing section snippet lines
        target = self.representative_data_lines
        
        test_data_lines = remove_non_data_lines(raw_lines)
        
        self.assertEqual(test_data_lines, target)


    def test_extract_column_values_properly_formatted_line(self):
        """
        Tests if function works with a properly formatted line.
        
        I.e. all delimiters consist of 2 spaces, no subsequent spaces separate
        words in comment value, etc.
        """
        
        # select properly formatted line from dummy data already
        # consisting of comma-separated string values
        target_line = self.row_lists[0]
        
        # create target row df
        target_df = pd.DataFrame([target_line], 
                                 columns=self.atoms_column_labels)
        
        # target_dfs = []
        # for row in self.row_lists:
        #     target_dfs.append(pd.DataFrame([row], 
        #                                    columns=self.atoms_column_labels))
        
        
        # select properly formatted raw line from dummy data
        test_line = self.representative_data_lines[0]
        
        # create test row df
        test_df = extract_column_values(test_line, self.atoms_column_labels)
        
        assert_frame_equal(target_df, test_df)
        
        
    def test_extract_column_values_subsequent_spaces(self):
        """
        Edge Case: test if function works with a line containing 
        a formatting error.
        
        Here, the error consists of 2 subsequent spaces in the comment value.
        """
        
        # select line where 2 subsequent spaces in comment value are already
        # fixed
        target_line = self.row_lists[-1]
        
        # create target row df
        target_df = pd.DataFrame([target_line], 
                                 columns=self.atoms_column_labels)
        
        
        # select line with 2 subsequent spaces in comment value
        test_line = self.representative_data_lines[-1]
        
        # create test row df
        test_df = extract_column_values(test_line, self.atoms_column_labels)
        
        assert_frame_equal(target_df, test_df)


    
       
    def test_extract_column_values_additional_delimiter_space(self):
        """
        Edge Case: test if function works with a line containing 
        a formatting error.
        
        Here, the error consists of an additional (delimiting) space character 
        between "atomtype" and "mass" values.
        """
        
        # select line were additional delimiting space was already removed
        target_line = self.row_lists[-2]
        
        # create target row df
        target_df = pd.DataFrame([target_line], 
                                 columns=self.atoms_column_labels)
        
        
        # select line with additional delimiting space
        test_line = self.representative_data_lines[-2]
        
        # create test row df
        test_df = extract_column_values(test_line, self.atoms_column_labels)
        
        assert_frame_equal(target_df, test_df)


    def test_create_df(self):
        """
        Macroscopic test:
            Test if lines with errors are parsed correctly and result in 
            desired df.
            
        Dependency exists: on "extract_column_values"
        """
    
        target_df = self.atoms_df
        
        test_df = create_df(self.atoms_column_labels, 
                            self.representative_data_lines)
        
        assert_frame_equal(target_df, test_df)
        

    def test_validate_datatypes_float_values(self):
        """
        Positive control:
            Test if values are indeed of type float.
        """
        
        # omitt atomtype value and introduce random value to keep correct 
        # shape of row
        df = pd.DataFrame(
            [['MASS', '-1', 'CGCPY2', '12.01100',
              '! analogy to CPM / allow for BV methine bridge ring C-D']], 
            columns=self.atoms_column_labels)
        
        df = validate_datatypes(df, "ATOMS", 
                                self.section_formats_dict)
        
        self.assertTrue(isinstance(df.mass_value.values[0], float))
            

    def test_validate_datatypes_omitted_field(self):
        """
        Edge case: 
            Test if erroneous field values (e.g. swapped due to delimiter error)
            are detected.
        """
        
        # omitt atomtype value and introduce random value to keep correct 
        # shape of row
        erroneous_df = pd.DataFrame(
            [['MASS', '-1', '12.01100', 
              '! analogy to CPM / allow for BV methine bridge ring C-D', 
              'random string']], 
            columns=self.atoms_column_labels)
        
        with self.assertRaises(ValueError) as e:
            df = validate_datatypes(erroneous_df, "ATOMS", 
                                self.section_formats_dict)
        
        
        

if __name__ == "__main__":
    unittest.main()