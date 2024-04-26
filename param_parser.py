import pandas as pd
import re



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
    section_names = ["ATOMS", "BONDS", "ANGLES", "IMPROPER", 
                     "DIHEDRALS", "NONBONDED"]

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
    nonbonded_col_labels_and_dtypes = {"atom": str, 
                           "ignored": float, 
                           "epsilon": float, 
                           "rminhalf": float, 
                           "comment": str}
    
    # object required to distinguish "IMPROPER" section from data sections 
    # downstream
    improper_col_labels_and_dtypes = {"None": None}

    col_labels_and_dtypes = [atoms_col_labels_and_dtypes, 
              bonds_col_labels_and_dtypes, 
              angles_col_labels_and_dtypes, 
              improper_col_labels_and_dtypes,
              dihedrals_col_labels_and_dtypes, 
              nonbonded_col_labels_and_dtypes
              ]
    
    
    section_formats = {
        i:k for i, k in zip(section_names, col_labels_and_dtypes)
        }
    
    return section_formats


def read_prm_file(filepath: str) -> list:
    """
    Opens and closes a file, reads lines into a list and returns the list.
    File must be located in the same directory as the parser.

    Parameters
    ----------
    filepath : str
        Path to prm file.

    Returns
    -------
    lines : list
        List containing each line of prm as an item (string).

    """
    try:
        with open(filepath, "r") as file:
            lines = file.readlines()
    except FileNotFoundError:
        raise FileNotFoundError(
              "Give absolute path of file or place file in parser directory!")
        
    return lines


def group_lines_by_sections(list_of_lines: list, section_names: dict) -> dict:
    """
    Takes all lines of prm file and section names to associate both.
    
    Parameters
    ----------
    list_of_lines : list
        List containing lines of prm file (strings) as items.
    section_names : dict
        Dict with "section name": "section column labels" pairs.

    Returns
    -------
    sections : dict
        Contains key:value pairs of "Name of section": "List of section lines"

    """
    
    section_names_and_lines = {}
    
    current_section_name = ""
    # To store the current section lines
    current_section_lines = []
    
    for line in list_of_lines:
        # check if line of prm file is a headline for a new section
        if any(section_name in line for section_name in section_names):
            # finish section by appending sublist to dict and make new sublist 
            if current_section_name:
                # Append the current sublist
                section_names_and_lines[current_section_name] = current_section_lines  
            # Start a new sublist
            current_section_name = line.strip()
            # assign nonbonded name manually since line contains additional words
            if "NONBONDED" in current_section_name:
                current_section_name = "NONBONDED"

            current_section_lines = []
        
        # if line is no section formatter, add row to current section sublist
        else:
            # Add the item to the current sublist
            current_section_lines.append(line)  
    
    # append last name and line
    section_names_and_lines[current_section_name] = current_section_lines
    
    return section_names_and_lines


def remove_non_data_lines(section_lines: list) -> list:
    """
    Remove lines containing no relevant data.
    
    E.g. residual formatting characters, supplementary information.

    Parameters
    ----------
    section_lines : list
        List of string items corresponding to one row of section-specific data.

    Returns
    -------
    section_lines : list
        Contains rows of relevant section data.

    """
    
    # remove lines starting with newline characters
    section_lines = [k for k in section_lines if not k.startswith("\n")]
    
    # remove descriptive lines
    section_lines = [k for k in section_lines if not k.strip().startswith("!")]
    
    # remove empty lines
    section_lines = [k for k in section_lines if not k.strip()==""]
    
    # remove formatter for end of file
    section_lines = [k for k in section_lines if not k.startswith("END")]
    
    # remove line with irrelevant information from "NONBONDED" section
    section_lines = [k for k in section_lines if not k.startswith("cutnb ")]
    
    return section_lines
    

def extract_column_values(line: str, column_labels: list) -> pd.DataFrame:
    """
    Transforms a section line of a prm file into a pandas DataFrame (df) with
    appropriate column labels.

    Parameters
    ----------
    line : str
        Line of prm file containing data for multiple fields of a section.
    column_labels : list
        List with strings of section column labels.

    Returns
    -------
    row_df : pandas DataFrame
        Single row of a df with proper column labels.

    """
    
    # assign index of "comment" label
    comment_column_index = len(column_labels) - 1
    
    # split line by whitespace
    # additionally removes newline character from comment
    values = line.split()

    # join comment fragments    
    comment = " ".join(values[comment_column_index:])
    
    # slice of values containing actual data
    data_values = values[:comment_column_index]

    # append comment value to data_values
    data_values.append(comment)
    
    # transform values to dataframe representing one row    
    row_df = pd.DataFrame([data_values], columns=column_labels)

    return row_df

    
    
def create_df(column_labels: list, lines: list) -> pd.DataFrame:
    """
    Takes section-specific column labels and lines and creates a pandas
    DataFrame with all data of a prm section.

    Parameters
    ----------
    column_labels : list
        Labels for the columns of a section.
    lines : list
        Lines (str) of prm file containing data for multiple fields of a section.

    Returns
    -------
    section_df : pandas DataFrame
    Table of data corresponding to all data from one section of a prm file.    

    """
    
    # remove any line which is not a row of data
    data_lines = remove_non_data_lines(lines)
    
    # instantiate df with appropriate column labels
    section_df = pd.DataFrame(columns=column_labels)
    
    # extract data of line, put it in a df row and append to section dataframe
    for line in data_lines:
        row_df = extract_column_values(line, column_labels)
        section_df = pd.concat([section_df, row_df], ignore_index=True)
    
    return section_df
        

def validate_datatypes(df: pd.DataFrame, section_name: str, 
                       section_formats: dict) -> pd.DataFrame:
    """
    Takes table of data + information on value formats and transforms values
    to correct datatypes.

    Parameters
    ----------
    df : pandas DataFrame
        df containing data of a pmf file section
    section_name : str
        name of pmf file section
    section_formats : dict
        dict of "str:dict" pairs associating section names with their column 
        labels and column datatypes.

    Raises
    ------
    ValueError
        If a value got parsed incorrectly, i.e. datatype cannot be confirmed.

    Returns
    -------
    df with correct datatypes.

    """
    
  
    col_labels_and_dtypes = section_formats[section_name]
    
    for label, dtype in col_labels_and_dtypes.items():
        try:
            df[label] = df[label].astype(dtype)
        except ValueError:
            raise ValueError(f"Column {label} contains values of invalid\
                              dtype")
    
    return df
    
    
def main(filepath: str):
    """
    

    Parameters
    ----------
    filepath : TYPE
        DESCRIPTION.

    Returns
    -------
    atom_df : TYPE
        DESCRIPTION.

    """
    
    # read prm file and save lines in list
    list_of_lines = read_prm_file(filepath)
    
    # define section names and corresponding column labels and datatypes
    section_formats = set_section_format()
        
    #!!! remove?! redundant; part of section formats
    # section_names = ["ATOMS", "BONDS", "ANGLES", "DIHEDRALS", "IMPROPER", "NONBONDED"]
    
    # map section_names to section_lines
    section_names_and_lines = group_lines_by_sections(list_of_lines, 
                                                      list(section_formats))
    
    # generate atom section df
    atom_df_raw = create_df(list(section_formats["ATOMS"]), 
                            section_names_and_lines["ATOMS"])
    
    # validate and transform datatypes 
    atom_df = validate_datatypes(atom_df_raw, "ATOMS", section_formats)

    bonds_df_raw = create_df(list(section_formats["BONDS"]), 
                             section_names_and_lines["BONDS"])
    
    bonds_df = validate_datatypes(bonds_df_raw, "BONDS", section_formats)
    
    
    dihedrals_df_raw = create_df(list(section_formats["DIHEDRALS"]), 
                                 section_names_and_lines["DIHEDRALS"])
    
    dihedrals_df = validate_datatypes(dihedrals_df_raw, "DIHEDRALS", 
                                      section_formats)
    
    
    angles_df_raw = create_df(list(section_formats["ANGLES"]), section_names_and_lines["ANGLES"])
    
    angles_df = validate_datatypes(angles_df_raw, "ANGLES", section_formats)
    
    
    nonbonded_df_raw = create_df(list(section_formats["NONBONDED"]), section_names_and_lines["NONBONDED"])
    
    nonbonded_df = validate_datatypes(nonbonded_df_raw, "NONBONDED", section_formats)
    

        
    return atom_df, bonds_df, dihedrals_df, angles_df, nonbonded_df
    
if __name__ == "__main__":
    atoms, bonds, dihedrals, angles_df, nonbonded_df = main("par_bv.prm")
