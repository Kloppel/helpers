import re

from optional_columns_processor import OptionalColumnsProcessor

import pandas as pd

class NonbondedNode(OptionalColumnsProcessor):
    """
    Template Pattern Child Class of 'SectionNode'.
    
    Inherits
    """
    
    START_SPECIFIER = "NONBONDED"
    
    END_SPECIFIER = "END"
    
    # specify labels and datatypes for full-length section values
    COL_LABELS_AND_DTYPES = { 
                                    "atom": str, 
                                    "ignored": float, 
                                    "epsilon": float, 
                                    "rminhalf": float, 
                                    "ignored_1_4": float,
                                    "epsilon_1_4": float,
                                    "rminhalf_1_4": float,
                                    "comment": str}
    
    # columns for lines without 1_4 data
    COL_LABELS_AND_DTYPES_optional  = { 
                                    "atom": str, 
                                    "ignored": float, 
                                    "epsilon": float, 
                                    "rminhalf": float, 
                                    "comment": str}

    def __init__(self):
        super().__init__()
        
        
    def remove_non_data_line(self, line, 
                             specific_non_data_condition=False):
        """
        Override method to add section-specific condition rendering a line 
        as non-data line.
        """
        
        # is True if condition holds true
        # triggers removal of line in process method
        specific_non_data_condition = line.strip().startswith("cutnb")
        
        return super().remove_non_data_line(line,
                        specific_non_data_condition)




    def extract_column_values(self, 
                              line,
                              parser):
        """
        Abstract method to enable extraction of values from rows with variable
        length.
        
        Assumption:
            Edge cases for rows:
                1) got 6 float values (full length line)
                2) got 3 float values (optional line)
        """
        
        
        # optional line has 3 floating point values
        amount_floating_point_values = 3

        # specified number of floating point values is used by 
        # columns process parent method to determine if line needs optional
        # column/dtype values
        return super().extract_column_values(line,
                                             parser,
                                             self.COL_LABELS_AND_DTYPES_optional,
                                             amount_floating_point_values)


        
    def validate_datatypes(self, row):
     
        return super().validate_datatypes(row)

       
       