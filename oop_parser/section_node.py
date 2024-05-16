import pandas as pd

import logging

# import inspect

class SectionNode:
    """
    Design Pattern 'Template Pattern' Base Class:
        Parent for Section Node classes that parse contents of a charmm 
        prm file. 
    """
    
    # assign node-specific class variables that must be provided to system
    # independently of node instantiation
    START_SPECIFIER: str = NotImplemented
        
    END_SPECIFIER: str = NotImplemented
    
    COL_LABELS_AND_DTYPES: dict = NotImplemented


    def __init__(self):
        
        self.section_name: str = None
        
        # container sequence for raw section lines
        self.raw_section_lines = []
        
        # container for lines as rows
        self.section_dataframe = pd.DataFrame(
                        columns=list(self.COL_LABELS_AND_DTYPES))

        self.logger = None
                
        
    def process(self, parser, remaining_lines: list):
        """
        ...::: TEMPLATE METHOD of 'Template Pattern' :::...
        
        Takes parser and lines to process and calls methods constituting 
        the parsing process.
        
        ALGORITHM SKELETON calling abstract methods in order to:
            
            Extract lines to a pandas DataFrame (single-row).
            Validate values of row.
            Concatenate validated row to section dataframe.
            Change parser state to state transition manager.
        
        Returns:
            lines pruned by processed line.
        
        """
        
        # acces ModuleLogging from parser
        # instantiate a logger
        if not self.logger:
            self.logger = parser.ModuleLogging.get_function_logger()

        
        # access current line
        line = remaining_lines[0]
        
        # do not process headline of section
        if self.START_SPECIFIER in line:
            return remaining_lines[1:]

        # append line to section
        self.raw_section_lines.append(line)
            
        # assign None to line if line doesn't contain tabular data
        line = self.remove_non_data_line(line)
        
        # remove non-data line line from remaining lines and break
        if line is None:
            self.logger.warning(
            "line is None => return remaining lines pruned by non data line")
    
            # set state to STM
            parser.state = parser.state_transition_manager
            
            return remaining_lines[1:]
            

        # extract column values of line to a single-row pandas DataFrame
        row_df = self.extract_column_values(line, parser)
        
        # raise error if a value is of wrong datatype
        validated_row_df = self.validate_datatypes(row_df)
        
        # append row to section df
        self.section_dataframe = self.append_row_to_df(self.section_dataframe, 
                                           validated_row_df)
            
        
        self.logger.info(
                    f"return remaining lines pruned by current line:\n {line}")

        # set parser state to state transition manager
        parser.state = parser.state_transition_manager

        # return non-processed lines 
        return remaining_lines[1:]


    
    def remove_non_data_line(self, line, 
                             specific_non_data_condition=False):
        """
        Takes a line.
        Returns line if contents represent data.
        Returns None otherwise.
        
        Kwarg "specific_non_data_condition":
            allows addition of non_data_specifier conditions in child classes.
        """
        
        # actual event call
        self.logger.debug("called")

        
        # list contains True for each condition that is true
        non_data_specifier_booleans = [line.startswith("\n"), 
                                       line.startswith("!"),
                                       line.strip()=="",
                                       line.strip().startswith("!"),
                                       line.startswith("END")]
        
        # allows child class to override method easily
        if specific_non_data_condition:
            non_data_specifier_booleans.append(specific_non_data_condition)

        self.logger.debug(
            f"non_data_specifier booleans: {non_data_specifier_booleans}")
        
        # if specifier detected that renders line a non data line, return None
        if any(non_data_specifier_booleans):
            logging.warning("found non data line specifier and return None")
            return None
        
        self.logger.debug(f"{self.section_name} removes its non-data lines")

        return line
        
    
    
    def extract_column_values(self, 
                              line, 
                              parser, 
                              optional_column_labels_and_dtypes=None):
        """
        Transforms a section line of a prm file into a pandas DataFrame (df) 
        with appropriate column labels.

        Parameters
        ----------
        line : str
            Line of prm file containing data for multiple fields of a section.

        Returns
        -------
        row_df : pandas DataFrame
            Single row of a df with proper column labels.
        """
        
        self.logger.debug(f"{self.section_name} calls extract_column_values")
        
        
        # access column labels
        column_labels = list(self.COL_LABELS_AND_DTYPES)
                
        # allows child classes to set alternative labels and dtypes
        if optional_column_labels_and_dtypes is not None:
            self.logger.warning(
                f"using optional_column_labels_and_dtypes for line:\n {line}")
            column_labels = list(optional_column_labels_and_dtypes)
            
        # assign index of "comment" label
        comment_column_index = len(column_labels) - 1
        
        # split line by whitespace; removes leftover whitespace around value
        values = line.split()

        # join comment fragments    
        comment = " ".join(values[comment_column_index:])
        
        # slice of values containing actual data
        data_values = values[:comment_column_index]

        # append comment value to data_values
        data_values.append(comment)
        
        self.logger.debug(f"split values: {values} ")
        self.logger.debug(f"comment: {comment} ")
        self.logger.debug(f"final row: {data_values} ")
        
        # instantiate single-row dataframe
        try:
            row_df = pd.DataFrame([data_values], columns=column_labels)
            
            self.logger.debug(
                f"successfully extracted data values to df row:\n {row_df}")

            
        # raise value error and print out line that couldn't be extracted
        except ValueError:
            msg = f"Extract vals FAILED!!! --- for line:\n {line}"
            self.logger.critical(f"{msg}")
            raise ValueError(msg)
    

        return row_df
        
        
        
    def append_row_to_df(self, 
                         section_dataframe, 
                         row_df):
        """
        Concatenate row to current section dataframe.
        
        Works also for rows with less values due to outer join concatenation
        mode (as required by some child class implementations).
        """
        
        # concatenate row to section dataframe
        section_df = pd.concat([section_dataframe, row_df], 
                               ignore_index=True, join="outer")
        
        self.logger.warning("successfully concatenated row to section df")

        return section_df
        

        
    def validate_datatypes(self, row, 
                           optional_col_labels_and_dtypes=None):
        """
        Transforms values of row to correct datatypes and returns row.
        Raises Value Error if any value cannot be changed to correct datatype.
        """
        
        self.logger.debug("validate dtypes of df")

            
        # full length column labels
        col_labels_and_dtypes = self.COL_LABELS_AND_DTYPES
        
        # enable abstract method overriding in child classes
        if optional_col_labels_and_dtypes is not None:
            
            self.logger.warning(
                f"using optional_column_labels_and_dtypes for row:\n {row}")
            
            # use optional columns injected by child
            col_labels_and_dtypes = optional_col_labels_and_dtypes
              
        # set dtypes for pd.Series'
        for label, dtype in col_labels_and_dtypes.items():
            try:
                row[label] = row[label].astype(dtype)
                self.logger.debug(
                    f"successfully casted column {label} to {dtype}")
                return row
            
            # raise exception if not possible to cast dtype
            except ValueError:
                msg = f"Column {label} contains values of invalid\
                                  dtype: {row[label].dtype}"
                
                self.logger.critical(msg)
                
                raise ValueError(msg)

        
        
        
        
        