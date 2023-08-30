import unittest
import pdb_tools
from abc import ABC, abstractmethod




class TestPDBreadLong(unittest.TestCase):
    def setUp(self):
        self.pdbFiles=["tests/bigTest/3hb3_ooxox.pdb"]
        return 

    def test_readPDB(self):
        for pdbFile in self.pdbFiles:
            parsedFileName=pdbFile[:-4]+"_parsed.pdb"
            original_lines=pdb_tools.files.read_file(pdbFile)
            line_dicts=pdb_tools.files.read_long_file(pdbFile, keep_serial=True)
            pdb_tools.files.write_long_file(parsedFileName,line_dicts)
            parsed_lines=pdb_tools.files.read_file(parsedFileName)
            self.assertEqual(len(original_lines),len(parsed_lines), 
                             f"Number of lines in parsed file is not the same as in original file {pdbFile}.")
            for index, o_line in enumerate(original_lines):
                p_line=parsed_lines[index]
                self.assertEqual(o_line.strip(),p_line.strip(),
                                 f"Line {index} in parsed file is not the same as in original file {pdbFile}.")
        return

if __name__=="__main__":
    unittest.main()
