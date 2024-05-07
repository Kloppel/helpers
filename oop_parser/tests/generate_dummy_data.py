import pandas as pd
import re


test_file_p = "/Users/jhome/code/praktikum/helpers/oop_parser/files_to_parse/par_bv.prm"

#%%% Section formats and properties

def set_section_format() -> dict:
    """
    Function to associate names of sections with corresponding column labels.
    
    Encapsulation of formatting information.

    Returns
    -------
    section_formats : dict[str, dict[str, type]]
        Dict of "section name": "column labels" key:value pairs.
        Used to store required formatting information in one container for easy
        and obvious retrieval.

    """
    section_names = ["ATOMS", "BONDS", "ANGLES", "DIHEDRALS", "IMPROPER", 
                     "NONBONDED"]

    atoms_col_labels_and_dtypes = {"mass": str,
                       "number": int,
                       "atomtype": str,
                       "mass_value": float,
                       "comment": str
                       }
    
    bonds_col_labels_and_dtypes = {"atom1": str, 
                       "atom2": str, 
                       "kb": float, 
                       "b0": float, 
                       "comment": str}
    
    
    angles_col_labels_and_dtypes = {"atom1": str, 
                            "atom2": str, 
                            "atom3": str, 
                            "ktheta": float, 
                            "theta0": float, 
                            "comment": str}
    
    dihedrals_col_labels_and_dtypes = {"atom1": str, 
                           "atom2": str, 
                           "atom3": str, 
                           "atom4": str, 
                           "kchi": float, 
                           "n": int, 
                           "delta": float, 
                           "comment": str}

    # ignored: float, < 0
    nonbonded_col_labels_and_dtypes = { 
                                    "atom": str, 
                                    "ignored": float, 
                                    "epsilon": float, 
                                    "rminhalf": float, 
                                    "ignored_1_4": float,
                                    "epsilon_1_4": float,
                                    "rminhalf_1_4": float,
                                    "comment": str}
    

    improper_col_labels_and_dtypes = {"atom1": str, 
                                  "atom2": str, 
                                  "atom3": str, 
                                  "atom4": str, 
                                  "kpsi": float,
                                  "0": int,
                                  "psi0": float,
                                  "comment": str}

    col_labels_and_dtypes = [atoms_col_labels_and_dtypes, 
              bonds_col_labels_and_dtypes, 
              angles_col_labels_and_dtypes,
              dihedrals_col_labels_and_dtypes,
              improper_col_labels_and_dtypes,
              nonbonded_col_labels_and_dtypes
              ]
    
    
    section_formats = {
        i:k for i, k in zip(section_names, col_labels_and_dtypes)
        }
    
    return section_formats




#%%% Step 1: print section lines to console for easy copy/paste
    
def print_section_to_console(section_start_specifier, 
                     section_end_specifier,
                     absolute_file_path=test_file_p,
                     print_half=False):
    # "par_bv.prm"
    """
    Generate dummy data for prm section.
    Set generation_mode to True to execute print statements and use function
    for data generation.
    """

    
    # read prm file
    with open(absolute_file_path) as f:
        # read lines as raw strings
        pmf_lines = f.readlines()
        

    # get idx of atom section headline
    # !!! purposefully use for loop instead of list comprehension for clarity
    for idx, line in enumerate(pmf_lines):
        if section_start_specifier in line.strip():
            section_start_line_idx = idx
            
    # confirm idx manually
    
    print(f" Index: {section_start_line_idx}\n\
          Line: {pmf_lines[section_start_line_idx]}")
          
    # get idx of next section headline
    # !!! purposefully use for loop instead of list comprehension for clarity
    for idx, line in enumerate(pmf_lines):
        if section_end_specifier in line.strip():
            section_end_line_idx = idx
    
    # confirm idx manually
    
    print(f" Index: {section_end_line_idx}\n\
          Line: {pmf_lines[section_end_line_idx]}")

    # slice atoms section
    
    section_lines = pmf_lines[
                    section_start_line_idx:section_end_line_idx]
    
    # # save number of lines for raw atom section
    # number_of_lines_in_atom_section = len(section_lines)
    
    if print_half:
        half = int(len(section_lines)/2)
        print(half)
        if print_half == 1:
            for line in section_lines[:half]:
                # print out raw representation of string
                print(repr(line), ",")
                # elaborate on lines that shouldn't count as data row:
                    # formatting/supplementary information: lines starting with '!'
                    # completely empty lines: newlines ('\n')
        
        if print_half == 2:
            for line in section_lines[half:]:
                # print out raw representation of string
                print(repr(line), ",")
        
    else:
        for line in section_lines:
            # print out raw representation of string
            print(repr(line), ",")
            # elaborate on lines that shouldn't count as data row:
                # formatting/supplementary information: lines starting with '!'
                # completely empty lines: newlines ('\n')
                
    return section_lines

#%%% Step 2: manually extract representative lines from console output

    # copy/paste some lines that make good dummy data
    # (containing all different types of formatting lines, comments, etc.)
    # remove very last commata
    # surround paste by [] to define a list "representative_lines"
    
section_lines = []

#!!! insert lines here
representative_lines = []

# example for atoms section
# [
#   '! added by Ronald\n', 
#   'MASS  -1  CGCPY1    12.01100   ! analogy to CA / allow for BV ring A\n',
#   'MASS  -1  CGCPY2    12.01100   ! analogy to CPM / allow for BV methine bridge ring C-D\n',
#   'MASS  -1  CGCPY3    12.01100   ! analogy to CPM / allow for BV methine bridge ring A-B\n',
#   'MASS  -1  CGCPY4    12.01100   ! analogy to CPM / allow for BV ring C\n',
#   '\n',
#   '!carbons\n',
#   'MASS  -1  CG1T2     12.01100   ! terminal alkyne H-C#C\n',
#   'MASS  -1  CG1N1     12.01100   ! C for cyano  group\n',
#   '! Patch for ring-a-cys\n',
#   '!MASS  -1  C         12.01100 ! carbonyl C, peptide backbone\n',
#   '!MASS  -1  CT1       12.01100 ! aliphatic sp3 C for CH\n',
#   '!MASS  -1  O         15.99900 ! carbonyl oxygen\n',
#   '!MASS  -1  H          1.00800 ! polar H\n',
#   '!MASS  -1  NH1       14.00700 ! peptide nitrogen\n',
#   '\n']

#%%% Step 3: manually remove formatting lines

    # delete formatting lines manually
    # make sure only valid data lines remain

representative_data_lines = []

# example for atoms section

# [
#  'MASS  -1  CGCPY1    12.01100   ! analogy to CA / allow for BV ring A\n',
#  'MASS  -1  CGCPY2    12.01100   ! analogy to CPM / allow for BV methine bridge ring C-D\n',
#  'MASS  -1  CGCPY3    12.01100   ! analogy to CPM / allow for BV methine bridge ring A-B\n',
#  'MASS  -1  CGCPY4    12.01100   ! analogy to CPM / allow for BV ring C\n',
#  'MASS  -1  CG1T2     12.01100   ! terminal alkyne H-C#C\n',
#  'MASS  -1  CG1N1     12.01100   ! C for cyano  group\n'
#  ]


#%%% Step 4: automatically remove formatting characters to prepare df creation

# make sure each value is clean


def remove_formatting_characters(section_name,
                                 representative_data_lines=representative_data_lines):
    """
    # remove newline character from comment
    # remove any leading or trailing spaces
    """
    
    # dict: section label: {col name: type}
    section_formats = set_section_format()


    # access section column labels
    column_labels = list(section_formats[section_name])

    # # regex pattern for the field/value delimiter: 2 or 3 space characters
    # pattern = r" {1,4}"
    
    # # split values upon 2 or 3 subsequent space characters
    # row_lists = [re.split(pattern, i) for i in representative_data_lines]
    
    # # remove newline character from comment
    # # remove any leading or trailing spaces

    # for row_list in row_lists:
    #     # access comment value and strip newline char
    #     row_list[-1] = row_list[-1].rstrip("\n")
    #     print(row_list)
        
    # assign index of "comment" label
    comment_column_index = len(column_labels) - 1
        
    # save row lines
    row_lines = []
        
    for line in representative_data_lines:        
        # split line by whitespace
        # additionally removes newline character from comment
        values = line.split()
    
        # join comment fragments    
        comment = " ".join(values[comment_column_index:])
        
        # slice of values containing actual data
        data_values = values[:comment_column_index]
    
        # append comment value to data_values
        data_values.append(comment)
        
        print(data_values, ",")
        
        row_lines.append(data_values)


    return row_lines
     
# copy row_list from console and paste to variable
# check if comment value was splitted properly + correct manually if needed
row_lists = []

# example for atoms section:
# row_lists = [['MASS', '-1', 'CGCPY1', '12.01100', '! analogy to CA / allow for BV ring A'],
# ['MASS', '-1', 'CGCPY2', '12.01100', '! analogy to CPM / allow for BV methine bridge ring C-D'],
# ['MASS', '-1', 'CGCPY3', '12.01100', '! analogy to CPM / allow for BV methine bridge ring A-B'],
# ['MASS', '-1', 'CGCPY4', '12.01100', '! analogy to CPM / allow for BV ring C'],
# ['MASS', '-1', 'CG1T2', '12.01100', '! terminal alkyne H-C#C'],
# ['MASS', '-1', 'CG1N1', '12.01100', '! C for cyano group']]


def generate_dummy_data(section_name,
                        row_lists=row_lists):
    
    # dict: section label: {col name: type}
    section_formats = set_section_format()


    # access section column labels
    column_labels = list(section_formats[section_name])
    
    df = pd.DataFrame(row_lists, 
                      columns=column_labels)
    
    
    # Security check: make sure values really contain no unwanted spaces
    # container for erroneous rows
    erroneous_rows = []
    # exclude comment values since they are supposed to have a space
    for col_label in column_labels[:-1]:
        err_lines = df.loc[df[col_label].apply(lambda val: " " in val)]
        if not err_lines.empty:
            erroneous_rows.append(err_lines)
    
    if erroneous_rows:
        raise ValueError("some data values have space characters")
    
      
    return (section_lines, representative_lines, representative_data_lines,
            row_lists, df)


if __name__ == "__main__":
    section_lines = print_section_to_console("ATOMS",
                             "BONDS")
    
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
    
    representative_data_lines = [
     'MASS  -1  CGCPY1    12.01100   ! analogy to CA / allow for BV ring A\n',
     'MASS  -1  CGCPY2    12.01100   ! analogy to CPM / allow for BV methine bridge ring C-D\n',
     'MASS  -1  CGCPY3    12.01100   ! analogy to CPM / allow for BV methine bridge ring A-B\n',
     'MASS  -1  CGCPY4    12.01100   ! analogy to CPM / allow for BV ring C\n',
     'MASS  -1  CG1T2     12.01100   ! terminal alkyne H-C#C\n',
     'MASS  -1  CG1N1     12.01100   ! C for cyano  group\n'
     ]

    row_lists = remove_formatting_characters("ATOMS", representative_data_lines)  

    row_lists = [['MASS', '-1', 'CGCPY1', '12.01100', '! analogy to CA / allow for BV ring A'],
       ['MASS', '-1', 'CGCPY2', '12.01100', '! analogy to CPM / allow for BV methine bridge ring C-D'],
       ['MASS', '-1', 'CGCPY3', '12.01100', '! analogy to CPM / allow for BV methine bridge ring A-B'],
       ['MASS', '-1', 'CGCPY4', '12.01100', '! analogy to CPM / allow for BV ring C'],
       ['MASS', '-1', 'CG1T2', '12.01100', '! terminal alkyne H-C#C'],
       ['MASS', '-1', 'CG1N1', '12.01100', '! C for cyano group']]    

    (atom_section_lines, 
      representative_lines, 
      representative_data_lines, row_lists,
      atoms_df) = generate_dummy_data("ATOMS")
