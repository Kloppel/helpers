

from section_node import SectionNode

class DihedralsNode(SectionNode):
    """
    Template Pattern Child Class of 'SectionNode'.
    """
    
    
    START_SPECIFIER = "DIHEDRALS"
    
    END_SPECIFIER = "IMPROPER"
    
    COL_LABELS_AND_DTYPES = {"atom1": str, 
                                  "atom2": str, 
                                  "atom3": str, 
                                  "atom4": str, 
                                  "kchi": float, 
                                  "n": int, 
                                  "delta": float, 
                                  "comment": str}

    def __init__(self):
        super().__init__()
        
        

       
       
       
