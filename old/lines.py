class lines():
    """
    The class lines contains all the functions that operate on a line, which are iterated over in the operations functions.
    It relies on being handed a single line or line_dict object as input.
    """
    def __init__(self):
        return self

    def read_pdb_line(line):
        """
        lines.read_pdb_line() creates a dictionary (line_dict) which is filled with the content of the line it is given based on
        string indexing. Based on the typical .pdb format, line_dict then knows:
        atom, serial_no, atom_name, resname, chainID, resi_sequence_no, x_coord, y_coord, z_coord, occupancy, 
        temp_fac, segment, element_symbol. 
        lines.read_pdb_line() returns the dictionary line_dict.
        """
        line_dict = {
            "atom": line[0:6],
            "serial_no": line[6:12],
            "atom_name": line[12:16],
            "resname": line[17:21],
            "chainID": line[21],
            "resi_sequence_no": line[22:27],
            "x_coord": line[31:38],
            "y_coord": line[39:46],
            "z_coord": line[47:54],
            "occupancy": line[55:60],
            "temp_fac": line[60:66],
            "segment": line[72:76],
            "element_symbol": line[77:78],
        }
        return line_dict

    def create_line(line_dict):
        """
        lines.create_line() takes a line_dict and creates the PDB-style line with the information contained in the dictionary. 
        It returns "line", an object containing the string that was produced. 
        """
        line = f'{line_dict["atom"]}{line_dict["serial_no"]} {line_dict["atom_name"]} {line_dict["resname"]}{line_dict["chainID"]}{line_dict["resi_sequence_no"]}    {line_dict["x_coord"]} {line_dict["y_coord"]} {line_dict["z_coord"]} {line_dict["occupancy"]}{line_dict["temp_fac"]}      {line_dict["segment"]} {line_dict["element_symbol"]}  \n'
        return line

    def fill_serial(serial_no, line_dict):
        """
        lines.fill_serial() takes a serial number (serial_no) and a line_dict and creates line_dict["serial_no"] objects with
        the appropriate number of spaces inserted in front, so that the serial number is inserted at the place the .pdb-format 
        dictates. It returns the line_dict with the appropriate serial_no. 
        """
        if serial_no < 10:
            line_dict["serial_no"] = f"    {serial_no}"
        if serial_no < 100 and serial_no >= 10:
            line_dict["serial_no"] = f"   {serial_no}"
        if serial_no < 1000 and serial_no >= 100:
            line_dict["serial_no"] = f"  {serial_no}"
        if serial_no < 10000 and serial_no >= 1000:
            line_dict["serial_no"] = f" {serial_no}"
        if serial_no >= 10000:
            line_dict["serial_no"] = f"{serial_no}"
        return line_dict
    
    def fill_resi_sequence_no(resi_no, line_dict):
        """
        lines.fill_resi_sequence_no() takes a residue number (resi_no) and a line_dict and creates a line_dict with the serial 
        number and the appropriate number of spaces inserted into line_dict["resi_sequence_no"]. It returns the line_dict. 
        """
        if resi_no < 10:
            line_dict["resi_sequence_no"] = f"   {resi_no} "
        if resi_no < 100 and resi_no >= 10:
            line_dict["resi_sequence_no"] = f"  {resi_no} "
        if resi_no < 1000 and resi_no >= 100:
            line_dict["resi_sequence_no"] = f" {resi_no} "
        if resi_no <= 9999 and resi_no >=1000:
            line_dict["resi_sequence_no"] = f"{resi_no} "
        return line_dict
    
    def add_terminus(lines):
        """
        lines.add_terminus() takes a list of strings (lines) and adds the string "TER" as the very last string in the list.
        """
        if lines[-1] != "TER":
            lines.append("TER")
        return lines

    def exchange_segment(line_dict, segment):
        """
        lines.exchange_segment() takes a line_dict and a segment name; then exchanges the previous segment name with the new 
        name and returns the line_dict with updated segment name. If the given segment name is too long, it will raise a 
        ValueError. If the given segment name is too short, it will start filling them up with whitespaces from the left
        until the desired length of 4 characters is reached. 
        """
        if len(segment) > 4:
            raise ValueError("segment value given is longer than 4. ")
        if len(segment) < 4:
            whitespaces=" "*(4-len(segment))
            segment=f'{whitespaces}{segment}'
        line_dict["segment"] = segment
        return line_dict
    
    def exchange_chainID(line_dict, chainID):
        """
        lines.exchange_chainID() takes a line_dict and a name for a chainID (maximum of 1 character) and exchanges the previous
        chainID with the new chainID. It then returns the line_dict with the updated chainID. 
        """
        if len(chainID) > 1:
            raise ValueError("chainID value given is longer than 1. ")
        line_dict["chainID"] = chainID
        return line_dict