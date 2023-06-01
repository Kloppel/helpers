import unittest
import pdb_tools

class TestLineOperations(unittest.TestCase):
   
    def setUp(self):
        self.test_line="ATOM      1  N   GLN A  29      33.508  16.306   8.974  1.00 41.94           N  "
        self.test_line_dict= {'atom': 'ATOM  ',
            'serial_no': '    1',
            'atom_name': ' N  ',
            'resname': 'GLN ',
            'chainID': 'A',
            'resi_no': '  29',
            'ins_code': ' ',
            'x_coord': ' 33.508',
            'y_coord': ' 16.306',
            'z_coord': '  8.974',
            'occupancy': ' 1.00',
            'temp_fac': ' 41.94',
            'segment': '    ',
            'elem_symb': 'N'}
        self.Line_operations=pdb_tools.line_operations()

        return
    def test_read_write(self):
        """
        Tests to see if the read->write process is correct
        """
        self.assertEqual(self.Line_operations.create_line(self.Line_operations.read_pdb_line(self.test_line)), self.line)

    def test_write_read(self):
        """
        Tests to see if the write->read process is correct
        """
        self.assertEqual(self.Line_operations.read_pdb_line(self.Line_operations))
    
    def test_types(self):
        line_dict=self.Line_operations.read_pdb_line(self.test_line)
        self.assertEqual(line_dict["atom"].strip(), "ATOM", " The atom key is not correct. String other than ATOM.")
        self.assertEqual(line_dict["serial_no"].strip().isnumeric(), True, " The serial number is not an integer.")
        self.assertEqual(line_dict["atom_name"].strip().isalpha(), True, " The atom name does not contain only letters.")
        self.assertEqual(line_dict["resname"].strip().isalpha(), True, " The residue name does not contain only letters.")
        if line_dict["ins_code"].strip()!="":
            self.assertEqual( line_dict["ins_code"].strip().isnumeric(), True, " The insertion code is not an integer.")
        self.assertEqual(line_dict["x_coord"].strip())


if __name__=="__main__":
    unittest.main()
    

