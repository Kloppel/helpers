import unittest
import pdb_tools
from Bio.PDB import PDBList
import pandas as pd
import numpy as np
import sys
import os

# Disable
def blockPrint():
    sys.stdout = open(os.devnull, 'w')

# Restore
def enablePrint():
    sys.stdout.close()
    sys.stdout = sys.__stdout__


class TestPDBreadLong(unittest.TestCase):
    def setUp(self):
        data=pd.read_csv("pyDISH_data.csv", sep=",")
        pdbIDs=data["# PDB"]
        self.testSize=self.read_config()
        self.pdbFiles=[]
        for i in range(self.testSize):
            pdbID=pdbIDs[i]
            pdbl = PDBList()
            blockPrint()
            pdbl.retrieve_pdb_file(pdbID, pdir="tests/bigTest", file_format="pdb", )
            enablePrint()
            print(f"\rDownloading... {i/self.testSize*100:.2f}%", end=" ")
            self.pdbFiles.append(f"tests/bigTest/pdb{pdbID}.ent")
        print("\rDownloading completed!", end="\n")
        self.pdbFiles.append("tests/bigTest/3hb3_ooxox.pdb")
        self.pdbFiles=np.array(self.pdbFiles)
        return

    def read_config(self):
        testSize=-1
        f=open("tests/bigTest/_config.txt","r") 
        lines=f.readlines()
        for line in lines:
            if line.startswith("#"):
                continue
            elif line.startswith("SIZE"):
                testSize=int(line.split(":")[1])
        f.close()
        if testSize<0:
            raise ValueError("Test size not set in _config.txt")
        return testSize

    def test_readPDB(self):
        print(f"Will test {self.testSize+1} PDB files.")
        i=0; N=len(self.pdbFiles)
        for pdbFile in self.pdbFiles:
            print("\rTesting file:"+f"{pdbFile} ({i/N*100:.2f}%)", end=" ")
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
            i+=1
        print("\rTesting completed!                                       ", end="\n")
        return

if __name__=="__main__":
    unittest.main()
