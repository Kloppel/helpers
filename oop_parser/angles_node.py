from optional_columns_processor import OptionalColumnsProcessor


class AnglesNode(OptionalColumnsProcessor):
    """
    Template Pattern Child Class of 'OptionalColumnsProcessor'.
    OptionalColumnsProcessor is Child Class of SectionNode.
    """
    
    START_SPECIFIER = "ANGLES"
    
    END_SPECIFIER = "DIHEDRALS"
    
    # specify labels and datatypes for section values
    COL_LABELS_AND_DTYPES = {"atom1": str, 
                                  "atom2": str, 
                                  "atom3": str, 
                                  "ktheta": float, 
                                  "theta0": float, 
                                  "kub": float,
                                  "s0": float,
                                  "comment": str
                                  }
    
    # columns for lines without urey_bradley values
    COL_LABELS_AND_DTYPES_optional = {"atom1": str, 
                                  "atom2": str, 
                                  "atom3": str, 
                                  "ktheta": float, 
                                  "theta0": float, 
                                  "comment": str
                                  }

    def __init__(self):
        super().__init__()


    def extract_column_values(self, line,
                              parser):
        """
        Abstract method to enable extraction of values from rows with variable
        length.
        
        Assumption:
            Edge cases for rows:
                1) got 4 float values (full length line)
                2) got 2 float values (optional line)
        """

        # optional line has 2 floating point values
        amount_floating_point_values = 2

        # pass optional line specifier to parent method
        return super().extract_column_values(line,
                                             parser,
                                             self.COL_LABELS_AND_DTYPES_optional,
                                             amount_floating_point_values)


        
    def validate_datatypes(self, row):
     
        return super().validate_datatypes(row)

       
       