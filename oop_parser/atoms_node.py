from section_node import SectionNode


class AtomsNode(SectionNode):
    """
    Template Pattern Child Class of "SectionNode".
    """
    
    START_SPECIFIER = "ATOMS"
    
    END_SPECIFIER = "BONDS"
    
    COL_LABELS_AND_DTYPES = {"mass": str,
                       "number": int,
                       "atomtype": str,
                       "mass_value": float,
                       "comment": str
                       }
    
    def __init__(self):
        super().__init__()

        
        
        
