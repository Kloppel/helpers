from section_node import SectionNode

class BondsNode(SectionNode):
    """
    Template Pattern Child Class of 'SectionNode'.
    """
    
    START_SPECIFIER = "BONDS"
    
    END_SPECIFIER = "ANGLES"
    
    COL_LABELS_AND_DTYPES = {"atom1": str, 
                                  "atom2": str, 
                                  "kb": float, 
                                  "b0": float, 
                                  "comment": str}

    def __init__(self):
        super().__init__()
        

            
    
    
    
 