from atoms_node import AtomsNode
from angles_node import AnglesNode
from bonds_node import BondsNode
from dihedrals_node import DihedralsNode
from nonbonded_node import NonbondedNode
from improper_node import ImproperNode

    
class Config:
    """
    System-wide config specifying which types of files can be parsed.
    
    Defines file-specific formats, names and objects required for the 
    parsing process.
    """
    
    ALLOWED_FILE_TYPES = ["str", "prm"]
    
    FILE_END_SPECIFIER = {"prm": "END",
                          "str": NotImplemented}
    
    # specify prm classes
    PRM_SECTION_NODE_CLASSES = {
        "Atoms Node": AtomsNode, 
         "Angles Node": AnglesNode,
         "Bonds Node": BondsNode,
         "Dihedrals Node": DihedralsNode,
         "Improper Node": ImproperNode,
         "Nonbonded Node": NonbondedNode
        }
    
    # tbc
    STR_SECTION_NODE_CLASSES = {}
    
    # container to map required node classes determined by file type
    NODE_CLASSES = {
        "prm": PRM_SECTION_NODE_CLASSES,
        "str": STR_SECTION_NODE_CLASSES
        }
    
    def __init__(self):
        
        self.file_type = None
        

    @property
    def file_type(self):
        return self._file_type
    
    @file_type.setter
    def file_type(self, file_type):
        # allows specified and unspecified file type upon instantiation
        if not file_type or file_type in self.ALLOWED_FILE_TYPES:
            self._file_type = file_type
        
        # raise exception if an invalid filetype is detected
        else:
            raise ValueError("invalid filetype")
            
    
    def select_strategy_by_filetype(self, file_suffix):
        """
        Takes file suffix extracted by parser.
        Sets file_type for current parsing process.
        """
        
        self.file_type = file_suffix
    
    
    def get_node_classes(self):
        """
        Returns node classes required for current parsing.
        """
        
        # return node classes for required strategy
        return self.NODE_CLASSES[self.file_type]
    
    
    def get_file_end_specifier(self):
        """
        Returns specifier representing last line of file type currently parsed.
        """
        return self.FILE_END_SPECIFIER[self.file_type]
    
