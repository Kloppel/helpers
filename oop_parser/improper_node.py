from section_node import SectionNode

class ImproperNode(SectionNode):
    """
    Template Pattern Child Class of 'SectionNode'.
    """
    
        
    START_SPECIFIER = "IMPROPER"
    
    END_SPECIFIER = "NONBONDED"
    
    COL_LABELS_AND_DTYPES = {"atom1": str, 
                                  "atom2": str, 
                                  "atom3": str, 
                                  "atom4": str, 
                                  "kpsi": float,
                                  "0": int,
                                  "psi0": float,
                                  "comment": str}


    def __init__(self):
        super().__init__()
  
        

       
       