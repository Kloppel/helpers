import unittest
import pdb_tools
from abc import ABC, abstractmethod


class LineOperations(ABC):
    """
    Abstract class with the necessary contents for the tests of line_operations functions
    """
    def contents(self):
        self.test_line="ATOM      1  N   GLY    17     -29.474   4.513 -19.989  1.00101.81      ACHA      \n"
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

class TestLineOperations(unittest.TestCase, LineOperations):

    def setUp(self):
        super().contents()
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
        self.assertEqual(line_dict["atom"].strip(), "ATOM" or "HETATM", " The atom key is not correct. String other than ATOM.")
        self.assertEqual(line_dict["serial_no"].strip().isnumeric(), True, " The serial number is not an integer.")
        self.assertEqual(line_dict["atom_name"].strip().isalpha(), True, " The atom name does not contain only letters.")
        self.assertEqual(line_dict["resname"].strip().isalpha(), True, " The residue name does not contain only letters.")
        if line_dict["ins_code"].strip()!="":
            self.assertEqual( line_dict["ins_code"].strip().isnumeric(), True, " The insertion code is not an integer.")
        #TO-DO add the rest of the tests and double check

    def test_add_terminus(self):
        """
        Tests the add_terminus function from the class line_operations. The test is twofold:
            > Tests that the terminus is correctly appended.
            > Tests that the terminus is not doubled.
        """
        lines=["test0", "test1"]
        updated_lines=self.Line_operations.add_terminus(lines)
        self.assertEqual(updated_lines[-1]=="TER", True, f"Line {updated_lines} did not finish in TER")
        updated_linesRepeat=self.Line_operations.add_terminus(updated_lines)
        self.assertEqual(updated_linesRepeat[-2]!="TER" , True, f"TER was not detected or added two times in {updated_lines}.")
        
    def test_read_pdb_line_size(self):
        """
        Tests that the function read_pdb_line from the class line_operations saves strings with the correct length into the dictionary.
        """
        line_dict=self.Line_operations.read_pdb_line(self.test_line)
        dict_sizes=[6,5,4,4,1,4,1,7,7,7,5,6,4,2,2]
        for indx, key in enumerate(line_dict.keys()):
            self.assertEqual(len(line_dict[key]), dict_sizes[indx], f"The entry {key} is not the correct length.")

    def test_exchange_segment(self):
        """
        This tests the function exchange_segment of the class line_operations. The test is threefold:
            > Test that it accurately raises a ValueError when the segment is too long.
            > Test that the segment has the desired length of 4.
            > Test that the segment is indeed introduced.
        """
        exchange_segment=self.Line_operations.exchange_segment
        line_dict=self.test_line_dict
        with self.assertRaises(ValueError, msg=f"The function does not raise the desired error."):
            exchange_segment(line_dict,"12345")
        updated_line_dict=exchange_segment(line_dict, "12a")
        new_segment=updated_line_dict["segment"]
        self.assertEqual(len(new_segment), 4, f"The new segment {new_segment} does not have the desired length.")
        self.assertEqual(new_segment, " 12a", f"The new segment {new_segment} is not the desired   12a.")

    def test_chainID(self):
        """
        This tests the function exchange_chianID of the class line_operations. The test is twofold:
            > Test that it accurately raises a ValueError when the segment is too long.
            > Test that the segment is indeed introduced.
        """
        exchange_chainID=self.Line_operations.exchange_chainID
        line_dict=self.test_line_dict
        with self.assertRaises(ValueError, msg=f"The function does not raise the desired error."):
            exchange_chainID(line_dict,"12345")
        updated_line_dict=exchange_chainID(line_dict, "1")
        new_chainID=updated_line_dict["chainID"]
        self.assertEqual(new_chainID, "1", f"The new segment {new_chainID} is not the desired 1.")

class general_fill_function(ABC):
    """
    List of attributes:
    self.maximum; self.test_value; self.wrongType;
    self.fill_function; self.dict_key; self.string_length
    """
    def test_wrongType(self):
        """
        Tests that the function recognizes when the type is not correct.
        """
        for wrong in self.wrongType:
            with self.assertRaises(TypeError, msg=f"The value {wrong} is taken although it has a wrong type."):
                self.fill_function(wrong, self.test_line_dict)

    def test_wrongValue(self):
        """
        Test that the value is within range and not over a certain maximum.
        """
        with self.assertRaises(ValueError, msg=f"The value is over the maximum {self.maximum} but no error was raised."):
            self.fill_function(int(self.maximum+1), self.test_line_dict)

    def test_string_length(self):
        """
        Tests that when the new value is introduced into the dictionary it has the correct length.
        """
        new_dict=self.fill_function(self.test_value, self.test_line_dict)
        self.assertEqual(len(new_dict[self.dict_key]), self.string_length, "The method does not fill with the correct number of spaces.")



class test_fill_resno(general_fill_function, LineOperations, unittest.TestCase):
    def setUp(self):
        super().contents()
        self.maximum=1e4; self.test_value=123
        self.wrongType=["error", 12.4]
        self.fill_function=self.Line_operations.fill_resi_no
        self.dict_key="resi_no"; self.string_length=4


class test_fill_serial(general_fill_function, LineOperations, unittest.TestCase):
    def setUp(self):
        super().contents()
        self.maximum=1e5; self.test_value=123
        self.wrongType=["error", 12.4]
        self.fill_function=self.Line_operations.fill_serial
        self.dict_key="serial_no"; self.string_length=5

class test_files(unittest.TestCase):
    def setUp(self):
        self.files=pdb_tools.files
        self.test_pdb_file="tests/3hb3_ooxox.pdb"
        self.test_pdb_file2="tests/8sze.pdb"
        self.test_pdb_id="3hb3_ooxox"
        return
    def test_read_file_dict(self):
        """
        Tests that the function read_file_dict correctly takes note of the serial numbers and residue numbers when asked.
        """
        dict_lines_renumbered=self.files.read_file_dict(self.test_pdb_file, absResNumbering=True)
        dict_lines=self.files.read_file_dict(self.test_pdb_file, absResNumbering=False)
        segment_last=None; resi_last=dict_lines[0]["resi_no"]
        resi_no_indx=0; serial_no_indx=0
        for indx,dict_line in enumerate(dict_lines_renumbered):
            if segment_last!=dict_line["segment"]:
                segment_last=dict_line["segment"]
                resi_last=dict_lines[indx]["resi_no"]
                resi_no_indx=1
            elif resi_last!=dict_lines[indx]["resi_no"]:
                resi_last=dict_lines[indx]["resi_no"]
                resi_no_indx+=1
            serial_no_indx+=1
            self.assertEqual(int(dict_line["resi_no"]), resi_no_indx, f"The residue number in segment {dict_line['segment']} (serial_no {dict_line['serial_no']}) is {dict_line['resi_no']} but should be {resi_no_indx}.")
            self.assertEqual(int(dict_line["serial_no"]), serial_no_indx, f"The serial number in segment {dict_line['segment']} is {dict_line['serial_no']} but should be {serial_no_indx}.")
        return
class test_operations(unittest.TestCase):
    def setUp(self):
        self.test_pdb_file="tests/3hb3_ooxox.pdb"
        self.test_pdb_file2="tests/8sze.pdb"
        self.test_pdb_id="3hb3_ooxox"
        self.operations=pdb_tools.operations
        self.files=pdb_tools.files
        return

    def test__split_segment(self):
        """
        Tests the function _split_segment of the class operations. Looks wether it really filters out the desired segment names.
        """
        segname="MEMB"
        self.operations._split_segment(self.test_pdb_file, segname, self.test_pdb_id)
        lines=self.files.read_file(pdb_file=f"coords/{self.test_pdb_id}_{segname}.pdb")
        for line in lines:
            self.assertIn(segname, line, msg=f"The line {line} does not contain {segname}.")
        return

    def TODO_test_waterchains(self):
        pass

    def TOOLONG_test_fuse_segments(self):
        """
        Tests the fuse_segments function of the class operations. Makes sure that the files are correctly fused.
        """
        test_pdb_files=["tests/8sze.pdb","tests/3hb3_ooxox.pdb"]
        test_pdb_output="tests/test_fused.pdb"
        self.operations.fuse_segments(test_pdb_files, test_pdb_output)
        lines_fused=pdb_tools.files.read_file(test_pdb_output)
        for pdb in test_pdb_files:
            lines_pdb=pdb_tools.files.read_file(pdb)
            for line in lines_pdb:
                self.assertIn(line, lines_fused, msg=f"The line {line} of {pdb} is not in {test_pdb_output}.")

    def test_add_segment(self):
        """
        Tests the function add_segments in pdb_tools.  The test is twofold:
            > Test that the segment is indeed changed
            > Test that the segment insertion is correct.
        """
        test_output="tests/SEG_test.pdb"
        test_segment="SEG"
        self.operations.add_segment(self.test_pdb_file, test_output, test_segment)
        with self.assertRaises(ValueError, msg="The add_segment function has added a residue with more than 4 letters!"):
            self.operations.add_segment(self.test_pdb_file, "tests/SEGMENT_test.pdb", "SEGMENT")
        for line in self.files.read_file(test_output):
            if "ATOM" in line:
                line_dict=pdb_tools.line_operations.read_pdb_line(line)
                self.assertEqual(" SEG", line_dict["segment"], f"The segment  {test_segment} is not in {test_output}.")

    def test_add_chainID(self):
        """
        Tests the function add_segments in pdb_tools.  The test is twofold:
            > Test that the chainID is indeed changed
            > Test that the chainID insertion is correct.
        """
        test_output="tests/T_test.pdb"
        test_chainID="T"
        self.operations.add_chainID(self.test_pdb_file, test_output, test_chainID)
        with self.assertRaises(ValueError, msg="The add_chainID function has added a residue with more than 1 letter!"):
            self.operations.add_chainID(self.test_pdb_file, "tests/NO_test.pdb", "NO")
        for line in self.files.read_file(test_output):
            if "ATOM" in line:
                #Here also the HETATM thing mentioned above JJ
                line_dict=pdb_tools.line_operations.read_pdb_line(line)
                self.assertEqual(test_chainID, line_dict["chainID"], f"The chainID {test_chainID} is not in {line} {test_output}.")

    def test_change_temp_factors(self):
        """
        Tests that the function operations.test_temp_factors, looks that the temperature factors are indeed as desired.
        """
        test_restraints="tests/tests_restraints.pdb"
        self.operations.change_temp_factors(self.test_pdb_file, test_restraints)
        test_temp_fact={
            "H": "0.00",
            "CB":   0.75,
            "C": "  0.50",
            "CA": 1,  
        }
        lines=self.files.read_file(test_restraints)
        #Checks the default values
        for line in lines:
            line_dict=pdb_tools.line_operations.read_pdb_line(line)
            temp_fact=line_dict["temp_fac"]
            atom_name=line_dict["atom_name"]
            if atom_name.startswith("H"):
                self.assertEqual(temp_fact, "  0.00")
            elif atom_name.startswith("C") and not atom_name.startswith("CA"):
                self.assertEqual(temp_fact, "  0.50")
            else:
                self.assertEqual(temp_fact, "  1.00")
        #Checks for wrong values
        wrong_temp_fact=test_temp_fact.copy()
        with self.assertRaises(ValueError, msg="The function did not raise an error when the default temperature factor was not a float."):
            self.operations.change_temp_factors(self.test_pdb_file, test_restraints, default="a")
        with self.assertRaises(ValueError, msg="The function did not raise an error when the default temperature factor was too long."):
            self.operations.change_temp_factors(self.test_pdb_file, test_restraints, default="1234567")
        with self.assertRaises(ValueError, msg="The function did not raise an error when one of the temperature factors was not a float."):       
            wrong_temp_fact["H"]="zz"
            self.operations.change_temp_factors(self.test_pdb_file, test_restraints,wrong_temp_fact)
        with self.assertRaises(ValueError, msg="The function did not raise an error when one of the temperature factors was too long."):       
            wrong_temp_fact["H"]="1234567"
            self.operations.change_temp_factors(self.test_pdb_file, test_restraints,wrong_temp_fact)
        #Test when introducing personalized temperature factors in different formats
        self.operations.change_temp_factors(self.test_pdb_file, test_restraints, test_temp_fact, default="2.00")
        lines=self.files.read_file(test_restraints)
        for line in lines:
            line_dict=pdb_tools.line_operations.read_pdb_line(line)
            temp_fact=line_dict["temp_fac"]
            atom_name=line_dict["atom_name"]
            if atom_name.startswith("H"):
                self.assertEqual(temp_fact, "  0.00")
            elif atom_name.startswith("CB"):
                self.assertEqual(temp_fact, "  0.75")
            elif atom_name.startswith("CA"):
                self.assertEqual(temp_fact, "  1.00")
            elif atom_name.startswith("C"):
                self.assertEqual(temp_fact, "  0.50")
            else:
                self.assertEqual(temp_fact, "  2.00")

    def test_renumber(self):
        """
        Tests the function options.renumber(),
            > Looks that it effectively raises an error for pdb files with too many atoms.
        """
        with self.assertRaises(ValueError, msg="The test_renumber function did not raise an error"):
            self.operations.renumber(self.test_pdb_file, "tests/toomanyatoms.pdb")
        self.operations.renumber(self.test_pdb_file2, "tests/test_renumber.pdb")


    def test_renumber_tip3(self):
        """
        Tests the function options.renumber_tip3(),
            > Looks that it effectively raises an error for pdb files with too many atoms.
        """
        with self.assertRaises(ValueError, msg="The test_renumber_tip3 function did not raise an error"):
            self.operations.renumber_tip3(self.test_pdb_file, "tests/toomanyatoms.pdb", "SEGM")
        self.operations.renumber_tip3(self.test_pdb_file2, "tests/test_renumber_tip3p.pdb", "SEGM")


if __name__=="__main__":
    unittest.main()
