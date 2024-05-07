import re

from section_node import SectionNode

import pandas as pd


class OptionalColumnsProcessor(SectionNode):
    """
                    ...::: MIXIN CLASS :::...
                    
    Implementing abstract methods that are common in only 
    a subset of base node child classes.
    
    Enables child classes with two sets of possible column labels to properly
    override the base class methods for
    a) extraction of column values from a prm file line
    b) validation of these values' datatypes
    """

    COL_LABELS_AND_DTYPES_optional: dict = NotImplemented

    def __init__(self):
        super().__init__()


    def extract_column_values(self, 
                              line, 
                              parser, 
                              optional_column_labels_and_dtypes,
                              amount_floating_point_values):
        """
        Abstract method to enable extraction of values from rows with variable
        columns.
        Uses optional labels/dtypes if condition for that is detected.
        
        
        amount_floating_point_values: int
            number of floats in line rendering it the optional case;
                specified and passed by child method.
        
        Assumption for conditional:
            Edge cases for rows before splitting the line can be detected via
            variable number of float values in line.
        """
        
        
        # remove comment part due to interference with correct number of floats
        # required for downstream conditional 
        # (yields error if a floating point value is found in the comment part)
        line_without_comment = line.split("!")[0]
        
        # pattern for the floating point values found in line
        pattern = r"\d+\.\d+"
        
        # extract number of floating point values in line
        number_of_floats = len(re.findall(pattern, line_without_comment))
        
        # print(f"number of floats: {number_of_floats}")
        
        # set appropriate column labels for line
        if number_of_floats == amount_floating_point_values:
            optional_column_labels_and_dtypes = self.COL_LABELS_AND_DTYPES_optional
            return super().extract_column_values(
                                        line,
                                        parser,
                                        optional_column_labels_and_dtypes)

        return super().extract_column_values(line,
                                             parser)

        
    def validate_datatypes(self, row):
        """
        Abstract method to enable extraction of values from rows with variable
        columns.
        """
        
        # if row length differs from default length, use optional labels/dtypes
        if len(list(row)) != len(list(self.COL_LABELS_AND_DTYPES)):
            return super().validate_datatypes(
                            row, 
                            self.COL_LABELS_AND_DTYPES_optional)
        
        return super().validate_datatypes(row)

       
       