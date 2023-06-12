import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os, re, subprocess, sys, json, glob
from molmod import *
from molmod.io import FCHKFile
from molmod.io.xyz import XYZReader, XYZFile
import requests
import Bio as bio 
from Bio import PDB
import MDAnalysis as mda 
import wts;
import Bio
from Bio.PDB.PDBParser import PDBParser
import pdb_tools

class PDBPrep:
    import pandas as pd
    import MDAnalysis as mda

    def error_catches(self):
        """Returns a ValueError when the column does not contain 4-letter alphanumerals."""
        bad_rows = []
        self.df['PDB str length'] = self.df['# PDB'].str.len()
        for index, row in self.df.iterrows():
            if row['PDB str length'] != 4:
                bad_rows.append(row)
        if bad_rows:
            for row in bad_rows:
                print(row)
            raise ValueError(f"PDB-ID length is not 4 for row_index {index}")

def isolate_heme(filename):
    universe = mda.Universe(filename)
    heme_name_list = ["HEM", "HEA", "HEB", "HEC", "HEO"]
    atom_selection_string = f"resname {heme_name_list[0]} "
    for heme_name in heme_name_list[1:]:
        atom_selection_string += f"or resname {heme_name} "
    heme = universe.select_atoms(atom_selection_string)
    mda.Writer(f"PDB/{pdb_id}_heme.pdb").write(heme) #is pdb a string containing the pdb-id or a number?
    if heme.n_atoms==0:
        print(f"Current heme resnames: {heme_name_list}")
        raise ValueError(f"No atoms have been added to the Universe, because no atoms have been found with the resname identifiers for heme. Please add the identifier you find in the PDB to the heme identifying names. The PDB is {pdb}")
    return heme

def convert_ent_to_pdb(ent_file_path, pdb_file_path):
    parser = PDBParser()
    structure = parser.get_structure('structure', ent_file_path)
    io = Bio.PDB.PDBIO()
    io.set_structure(structure)
    io.save(pdb_file_path)
    os.remove(ent_file_path)
    return pdb_file_path

def HETATM_to_ATM(pdb_id):
    lines = pdb_tools.files.read_file(pdb_file=f"PDB/{pdb_id}_heme.pdb")
    lines_ = ["CRYST1\n"]
    #print(lines)
    for line in lines:
        #print(line)
        line_dict = pdb_tools.line_operations.read_pdb_line(line=line)
        pdb_tools.line_operations.exchange_HETATM_ATOM(line_dict=line_dict)
        line_ = pdb_tools.line_operations.create_line(line_dict=line_dict)
        lines_.append(line_)
    lines_.append("")
    #print(lines_)
    pdb_tools.files.write_file(file=f"PDB/{pdb_id}_heme_ATOM.pdb", lines=lines_)
    return 



if __name__ == "__main__":
    data = pd.read_csv('pyDISH_data.csv')
    data = data.drop('Unnamed: 0', axis=1)
    universes, hemes = {}, {}
    for pdb_id in data['# PDB'].iloc[:10]:
        filename = PDB.PDBList().retrieve_pdb_file(pdb_id, pdir='PDB', file_format='pdb');
        filename = convert_ent_to_pdb(f"PDB/pdb{pdb_id}.ent", f"PDB/{pdb_id}.pdb")
        universes[pdb_id] = mda.Universe(filename)
        hemes[pdb_id] = isolate_heme(filename)
        HETATM_to_ATM(pdb_id=pdb_id)
        molecule = wts.porphyr(f"PDB/{pdb_id}_heme_ATOM.pdb")
        molecule.name = pdb_id
        molecule.set_ordered_xyz()
