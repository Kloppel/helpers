import files
import lines
import itertools

class operations():

    def __init__(self):
        return self

    def split_segment(pdb_file, segname, pdb_id):
        """
        operations.split_segment() takes a pdb_file, a segname, and a pdb_id; then reads the file and drops all instances that
        do not have the segname within them. It writes the file as "coords/{pdb_id}_{segname}.pdb. Not having a folder "coords"
        will produce an error until the writefile function checks if the folder exists. 
        """
        lines=files.read_file(pdb_file=pdb_file)
        lines=[k for k in lines if segname in k]
        #lines=lines.add_terminus(lines)
        files.write_file(file=f'coords/{pdb_id}_{segname}.pdb', lines=lines)
        return
    
    def split_segments(pdb_file, segnames, pdb_id):
        """
        operations.split_segments() takes a pdb_file and a list of segname strings (segnames) and a pdb_id; then for each 
        instance in segnames calls the operations.split_segment() function, producing a single file that contains only the 
        lines in the pdb that had the segname in them. 
        """
        for segname in segnames:
            operations.split_segment(pdb_file=pdb_file, segname=segname, pdb_id=pdb_id)
        return

    def split_waterchains(pdb_file, output_name):
        """
        operations.split_waterchains() takes a pdb_file and an output_name; first it reads the file (which should only contain
        H2O molecules in the pdb format and TIP3 water model/other water model that has EXACTLY three atoms in the water) and 
        splits them into chains of 10.000 water molecules each. It writes the files based on the operations.renumber_tip3 method.
        """
        lines=files.read_file(pdb_file=pdb_file)
        length, counter, filenames=len(lines), 0, []
        while counter < length:
            lines_=lines[0:29997]
            lines_=lines.add_terminus(lines=lines_)
            filename="coords/"+output_name+f"{counter//29997}.pdb"
            filenames.append(filename)
            files.write_file(file=filename, lines=lines_)
            lines=lines[29997:]
            counter +=29997
        for filename in filenames:
            operations.renumber_tip3(pdb_file=filename, pdb_file_output=filename, segment=filename[12:16])
        return

    def fuse_segments(pdb_files, pdb_output):
        """
        operations.fuse_segments() takes a list of strings that point to .pdb files and a name for a pdb_output; then it
        appends all the files into one, removing potential "TER" lines, and writes a single fused file. 
        """
        lines_=[]
        for pdb_file in pdb_files:
            lines=files.read_file(pdb_file=pdb_file)
            lines_.append(lines)
            lines=[]
        lines_ = list(itertools.chain(*lines_))
        files.write_file(file=pdb_output, lines=lines_)
        return

    def add_segment(pdb_file, pdb_file_output, segment):
        """
        operations.add_segment() takes a pdb_file, the name of a pdb_file_output, and a segment name (segment); then it 
        calls the lines.exchange_segment() function to exchange the segment identifier in the line_dict. In the end it 
        writes the file based on pdb_file_output. 
        """
        lines=files.read_file(pdb_file=pdb_file)
        lines_ = []
        serial_no=1
        for line in lines:
            line_dict=lines.read_pdb_line(line=line)
            line_dict=lines.exchange_segment(line_dict=line_dict, segment=segment)
            line_=lines.create_line(line_dict=line_dict)
            lines_.append(line_)
            serial_no+=1
        lines=lines.add_terminus(lines=lines_)
        files.write_file(file=pdb_file_output, lines=lines)
        return 

    def add_chainID(pdb_file, pdb_file_output, segment):
        """
        operations.add_chainID() takes a pdb_file and a output name pdb_file_output and a segment name; then iterates over
        all lines in the PDB file changing the chainID. In the end it saves the new file according to pdb_file_output. 
        """
        lines=files.read_file(pdb_file=pdb_file)
        lines_ = []
        serial_no=1
        for line in lines:
            line_dict=lines.read_pdb_line(line=line)
            line_dict=lines.exchange_chainID(line_dict=line_dict, segment=segment)
            line_=lines.create_line(line_dict=line_dict)
            lines_.append(line_)
            serial_no+=1
        lines=lines.add_terminus(lines=lines_)
        files.write_file(file=pdb_file_output, lines=lines)
        return

    def change_temp_factors(pdb_file, restraints_file):
        """
        operations.change_temp_factors() takes a pdb_file and a name for a restraints_file; then it creates a restraints file 
        based on the specifications of CHARMM-GUIs NAMD constraint files. 
        H-atoms will recieve the temp_fac 0.00
        All C-atoms but CA (C-alphas) will recieve temp_fac 0.50
        All other atoms will recieve temp_fac 1.00.
        """
        lines=files.read_file(pdb_file=pdb_file)
        lines_ = []
        for line in lines:
            line_dict=lines.read_pdb_line(line)
            if line_dict["atom_name"].startswith("H"):
                line_dict["temp_fac"] = "  0.00"
            else: 
                if line_dict["atom_name"].startswith("C") and not line_dict["atom_name"].startswith("CA"):
                    line_dict["temp_fac"] = "  0.50"
                else:
                    line_dict["temp_fac"] = "  1.00"
            line_ = lines.create_line(line_dict=line_dict)
            lines_.append(line_)
            if line.startswith("TER"):
                line_ = line
                lines_.append("line_")
        files.write_file(file=restraints_file, lines=lines_)
        lines=lines_
        return
    
    def renumber(pdb_file, pdb_file_output):
        """
        operations.renumber() takes a pdb_file and a pdb_file_output name; then it checks if there are more than 99.999 atoms. If
        so it will raise a ValueError, if not it will use the lines.fill_serial() method to renumber the atoms starting at 1. In 
        the end it will write a file based on pdb_file_output. 
        """
        lines=files.read_file(pdb_file=pdb_file)
        if len(lines) > 99999:
            raise ValueError("len(lines)>99999. Try again with less atoms.")
        lines_ = []
        serial_no=1
        for line in lines:
            line_dict=lines.read_pdb_line(line=line)
            line_dict=lines.fill_serial(serial_no=serial_no, line_dict=line_dict)
            line_=lines.create_line(line_dict=line_dict)
            lines_.append(line_)
            serial_no+=1
        lines=lines.add_terminus(lines=lines_)
        files.write_file(file=pdb_file_output, lines=lines)
        return

    def renumber_tip3(pdb_file, pdb_file_output, segment):
        """
        operations.renumber_tip3() takes a pdb_file, a pdb_file_output and a segment name; then it will read the file and 
        check if there are more than 99.999 atoms in the current file. If so it will raise a ValueError, if not it will 
        not only renumber the serial numbers of all atoms but also the residue numbers. This only works with a water model
        that has exactly three atoms per water molecule. In the end it writes a file based on the pdb_file_output specifications.
        """
        lines=files.read_file(pdb_file=pdb_file)
        if len(lines) > 99999:
            raise ValueError("len(lines)>99999. Try again with less atoms.")
        lines_ = []
        serial_no=1
        for line in lines:
            line_dict=lines.read_pdb_line(line=line)
            line_dict=lines.fill_serial(serial_no=serial_no, line_dict=line_dict)
            resi_no=((serial_no-1)//3)+1
            lines.fill_resi_sequence_no(resi_no=resi_no, line_dict=line_dict)
            line_dict["segment"] = segment
            line_=lines.create_line(line_dict=line_dict)
            lines_.append(line_)
            serial_no+=1
        lines=lines.add_terminus(lines=lines_)
        files.write_file(file=pdb_file_output, lines=lines)
        return 