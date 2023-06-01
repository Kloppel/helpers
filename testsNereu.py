import unittest
import pdb_tools
from abc import ABC

class TestLineOperations(unittest.TestCase):
   
    def setUp(self):
        self.test_line="ATOM      1  N   GLY    17     -29.474   4.513 -19.989  1.00101.81      ACHA     \n"
        self.test_line_dict= {'atom': 'ATOM  ',
            'serial_no': '    1',
            'atom_name': ' N  ',
            'resname': 'GLY ',
            'chainID': ' ',
            'resi_no': '  17',
            'ins_code': ' ',
            'x_coord': '-29.474',
            'y_coord': '  4.513',
            'z_coord': '-19.989',
            'occupancy': ' 1.00',
            'temp_fac': '101.81',
            'segment': 'ACHA',
            'elem_symb': '  ',
            "charge": "  "}
        self.Line_operations=pdb_tools.line_operations

        return
    def test_read_write(self):
        """
        Tests to see if the read->write process is correct
        """
        self.assertEqual(self.Line_operations.create_line(self.Line_operations.read_pdb_line(self.test_line)), self.test_line,
                         "The conversion read->write for a single line is not clean. In other words reading and writting a line does not return the original.")

    def test_write_read(self):
        """
        Tests to see if the write->read process is correct
        """
        self.assertEqual(self.Line_operations.read_pdb_line(self.Line_operations.create_line(self.test_line_dict)),self.test_line_dict,
                         "The conversion write->read for a single line dictionary is not clean. In other words writting and then reading a line does not return the same dictionary.")
    
    def notready_test_types(self):
        line_dict=self.Line_operations.read_pdb_line(self.test_line)
        self.assertEqual(line_dict["atom"].strip(), "ATOM", " The atom key is not correct. String other than ATOM.")
        self.assertEqual(line_dict["serial_no"].strip().isnumeric(), True, " The serial number is not an integer.")
        self.assertEqual(line_dict["atom_name"].strip().isalpha(), True, " The atom name does not contain only letters.")
        self.assertEqual(line_dict["resname"].strip().isalpha(), True, " The residue name does not contain only letters.")
        if line_dict["ins_code"].strip()!="":
            self.assertEqual( line_dict["ins_code"].strip().isnumeric(), True, " The insertion code is not an integer.")
        #TO-DO add the rest of the test in the afternoon from the flashdrive at home
    
    @unittest.skip
    class general_fill_function(ABC, unittest.TestCase):
        def __init__(self):
                self.maximum
                self.type
                self.test_number
                self.wrongType
                self.wrongMessage
                self.fill_function
        def test_wrongType(self):
            for wrong in enumerate(self.wrongType):
                with self.assertRaises(TypeError, f"The input is taken although {wrong} is not the right type.") as error:
                    self.fill_function(self.test_number)
                
                    
                
                


if __name__=="__main__":
    unittest.main()
    

