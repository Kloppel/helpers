import itertools

class files():
    def __init__(self):
        return self

    def read_file(pdb_file):
        """
        files.readfile() reads a .pdb file using the readlines method. It also filters out all lines containing the keywords
        REMARK, TER, TITLE, CRYST1, SCALE
        and returns the list containing the lines (strings)
        """
        f=open(pdb_file, 'r')
        lines = f.readlines()
        f.close()
        lines = [k for k in lines if "HEADER" not in k]
        lines = [k for k in lines if "TITLE" not in k]
        lines = [k for k in lines if "CRYST1" not in k]
        lines = [k for k in lines if "REMARK" not in k]
        lines = [k for k in lines if "SCALE" not in k]
        lines = [k for k in lines if "MODEL" not in k]
        lines = [k for k in lines if "ENDMDL" not in k]
        lines = [k for k in lines if "TER" not in k]
        lines = [k for k in lines if "END" not in k]
        #lines = [k.replace("\n", '') for k in lines]
        return lines

    def write_file(file, lines):
        """
        files.writefile takes a list of strings, e.g. from a read file like with the files.readfile function and opens a writer.
        Using this write method, files.writefile writes the lines into a file that is saved, and closes the write-method.
        It returns nothing.
        """
        #lines_ = line_operations.add_terminus(lines=lines)
        #if "END" not in lines_[-1]:
        #    lines.append("END")
        lines_ = line_operations.add_ending(lines=lines)
        f = open(file, mode="w", encoding="utf-8")
        f.writelines(lines_)
        f.close()
        return

class line_operations():
    """
    The class lines contains all the functions that operate on a line, which are iterated over in the operations functions.
    It relies on being handed a single line or line_dict object as input.
    """
    def __init__(self):
        return None

    def read_pdb_lineold(line):
        """
        line_operations.read_pdb_line() creates a dictionary (line_dict) which is filled with the content of the line it is given based on
        string indexing. Based on the typical .pdb format, line_dict then knows:
        atom, serial_no, atom_name, resname, chainID, resi_no, x_coord, y_coord, z_coord, occupancy,
        temp_fac, segment, element_symbol.
        line_operations.read_pdb_line() returns the dictionary line_dict.
        """
        line_dict = {
            "atom": line[0:6],
            "serial_no": line[6:11],
            "atom_name": line[12:16],
            "resname": line[17:21],
            "chainID": line[21],
            "resi_no": line[22:26],
            "ins_code": line[26],
            "x_coord": line[31:38],
            "y_coord": line[39:46],
            "z_coord": line[47:54],
            "occupancy": line[55:60],
            "temp_fac": line[60:66],
            "segment": line[72:76],
            "elem_symb": line[77:79],
            "charge": line[79:81]
        }
        if "\n" in line_dict["elem_symb"]:
            line_dict["elem_symb"] = line_dict["elem_symb"].replace("\n", "")
        line_dict["elem_symb"] = line_dict["elem_symb"].strip()
        if line_dict["elem_symb"] == "":
            line_dict["elem_symb"] = "  "
        if "\n" in line_dict["charge"]:
            line_dict["charge"] = line_dict["elem_symb"].replace("\n", "")
        if line_dict["charge"]=="":
            line_dict["charge"]="  "
        return line_dict
    
    def read_pdb_lines(lines):
        """
        line_operations.read_pdb_lines() takes a list of strings (lines) and iterates over them, calling the line_operations.read_pdb_line()
        function on each line. It returns a list of dictionaries (line_dicts) that contain the information of each line.

        This function keeps track of the serial and residue numbers even when they exceed 5 digits. However when written into a file they
        should be written as 5 asterisks "*****" as the .pdb format does not allow for more than 5 digits.
        """
        line_dicts=[]
        counter_serial=1
        counter_resi=1
        segment=None; residue=None
        for line in lines:
            line_dict=line_operations.read_pdb_line(line=line)
            if residue!=line_dict["resname"]:
                counter_resi+=1
            if segment!=line_dict["segment"]:
                counter_resi=1; counter_serial=1
                segment=line_dict["segment"]
            line_dict["serial_no"]=f"{counter_serial}"
            line_dict["resi_no"]=f"{counter_resi}"
            line_dicts.append(line_dict)
            counter_serial+=1
        return line_dicts

    
    
    def read_pdb_line(line):
        """
        This function takes a line (string) and returns a dictionary containing the information in the line.

        This function should ignore any errors in column placement, as it does not see white spaces.
        The algorithm used is as follows:
        1. Split the line into words
        2. Iterate over the words, and check if the word is shorter than the expected length of the key.
        3.      If it is shorter, add it to the dictionary and take the next dictionary key.
        4.      If it is longer, check if the next word could be made up of concatenated words (check condition maximum_concatenated_length-wordlength<maximumkeylength).
        

        """
        words=line.split()
        dict_keys=["atom", "serial_no", "atom_name",
                "resname", "chainID", "resi_no",
                "ins_code", "x_coord", "y_coord",
                "z_coord", "occupancy", "temp_fac",
                "segment","elem_symb", "charge"]
        key_sizes=[6,5,4,
                3,1,4,
                1,7,7,
                7,5,6,
                4,2,2]
        output_dict={
            "atom":None,
            "serial_no":None,
            "atom_name":None,
            "resname":None,
            "chainID":None,
            "resi_no":None,
            "ins_code":None,
            "x_coord":None,
            "y_coord":None,
            "z_coord":None,
            "occupancy":None,
            "temp_fac":None,
            "segment": None,
            "elem_symb":None,
            "charge":None
        }
        dict_types={
            "atom":str,
            "serial_no":str,
            "atom_name":str,
            "resname":str,
            "chainID":str,
            "resi_no":int,
            "ins_code":str,
            "x_coord":float,
            "y_coord":float,
            "z_coord":float,
            "occupancy":float,
            "temp_fac":float,
            "segment": str,
            "elem_symb":str,
            "charge":str
        }
        

        count=0; word_count=0
        while word_count<len(words) and count<len(key_sizes):
            word=words[word_count]
            if len(word)<=key_sizes[count]:
                try:
                    dict_types[dict_keys[count]](word)
                    output_dict[dict_keys[count]]=word
                    count+=1
                except:
                    word_count-=1
                    count+=1
            #check if it can
            elif len(word)>key_sizes[count] and count+1<len(key_sizes):
                count2=count+1
                expected=key_sizes[count]+key_sizes[count2]
                while len(word)>expected and count2<len(key_sizes)-1:
                    count2+=1
                    expected+=key_sizes[count2]
                if expected-len(word)<=key_sizes[count]:  
                    ccount2=count2
                    word2=word[::-1]
                    olddict=output_dict.copy()
                    validType=True
                    while count2>count:
                        try:
                            dict_types[dict_keys[count2]](word2[:key_sizes[count2]][::-1])
                            #sometimes people use chainID to expand the resi_no
                            #therefore one has to check if the chainID is numeric
                            if dict_keys[count2]=="ins_code":
                                if word2[:key_sizes[count2]][::-1].isnumeric():
                                    try:
                                        dict_types["resi_no"](word2[:5][::-1])
                                        output_dict["resi_no"]=word2[:5][::-1]
                                        word2=word2[5:]
                                        count2-=2
                                    except:
                                        output_dict=olddict.copy()
                                        validType=False
                                        break
                                else:
                                    output_dict[dict_keys[count2]]=word2[:key_sizes[count2]][::-1]
                                    word2=word2[key_sizes[count2]:]
                                    count2-=1 
                            else:
                                output_dict[dict_keys[count2]]=word2[:key_sizes[count2]][::-1]
                                word2=word2[key_sizes[count2]:]
                                count2-=1
                        except:
                            output_dict=olddict.copy()
                            validType=False
                            break
                    if validType:     
                        try:
                            dict_types[dict_keys[count2]](word2[::-1])
                            output_dict[dict_keys[count2]]=word2[::-1]
                            count=ccount2+1
                        except:
                            output_dict=olddict.copy()
                            word_count-=1
                            count+=1
                    else:
                        word_count-=1
                        count+=1    
                else:
                    word_count-=1
                    count+=1
                    
            word_count+=1

        for indx,key in enumerate(output_dict.keys()):
            if output_dict[key]==None:
                output_dict[key]=" "*key_sizes[indx]
            #atom key is left justified
            elif key=="atom":
                output_dict[key]=output_dict[key].ljust(key_sizes[indx])
            elif key=="atom_name":
                if len(output_dict[key])<2:
                    output_dict[key]=output_dict[key].rjust(2)+" "*2
                else:
                    output_dict[key]=output_dict[key].ljust(key_sizes[indx])
            elif key=="resname":
                output_dict[key]=output_dict[key].rjust(3)+" "*1
            elif key=="resi_no":
                if len(output_dict[key])<4:
                    output_dict[key]=output_dict[key].rjust(4)
            else:
                output_dict[key]=output_dict[key].rjust(key_sizes[indx])

        return output_dict

    def correct_dict_formatting(line_dict):
        """
        line_operations.correct_dict_formatting() takes a line_dict and corrects the formatting of the line_dict so that it is
        in the correct format for the .pdb file. It returns the corrected line_dict.
        """
        key_sizes=[6,5,4,
                3,1,4,
                1,7,7,
                7,5,6,
                4,2,2]
        for indx,key in enumerate(line_dict.keys()):
            if line_dict[key]==None:
                line_dict[key]=" "*key_sizes[indx]
            #atom key is left justified
            elif key=="atom":
                line_dict[key]=line_dict[key].ljust(key_sizes[indx])
            elif key=="atom_name":
                if len(line_dict[key])<2:
                    line_dict[key]=line_dict[key].rjust(2)+" "*2
                else:
                    line_dict[key]=line_dict[key].ljust(key_sizes[indx])
            elif key=="resname":
                line_dict[key]=line_dict[key].rjust(3)+" "*1
            elif key=="resi_no":
                if len(line_dict[key])<4:
                    line_dict[key]=line_dict[key].rjust(4)
            else:
                line_dict[key]=line_dict[key].rjust(key_sizes[indx])
        return line_dict


    def create_line(line_dict):
        """
        line_operations.create_line() takes a line_dict and creates the PDB-style line with the information contained in the dictionary.
        It returns "line", an object containing the string that was produced.

        If the serial number has more than 5 digits (i.e >99.999) it will output ******
        """
        if len(str(int(line_dict["resi_no"])))>=5:
            line_dict["serial_no"]="*****"
        if len(str(int(line_dict["serial_no"])))>=5:
            line_dict["serial_no"]="*****"
        line = f'{line_dict["atom"]}{line_dict["serial_no"]} {line_dict["atom_name"]} {line_dict["resname"]}{line_dict["chainID"]}{line_dict["resi_no"]}{line_dict["ins_code"]}    {line_dict["x_coord"]} {line_dict["y_coord"]} {line_dict["z_coord"]} {line_dict["occupancy"]}{line_dict["temp_fac"]}      {line_dict["segment"]} {line_dict["elem_symb"]}      '
        #line = f'{line_dict["atom"]}{line_dict["serial_no"]} {line_dict["atom_name"]} {line_dict["resname"]}{line_dict["chainID"]}{line_dict["resi_no"]}{line_dict["ins_code"]}   {line_dict["x_coord"]} {line_dict["y_coord"]} {line_dict["z_coord"]} {line_dict["occupancy"]} {line_dict["temp_fac"]}       {line_dict["segment"]} {line_dict["elem_symb"]}{line_dict["charge"]}\n'
        if len(line) > 82:
            line=line.strip()
        if len(line) < 82:
            line=f"{line: <82}"
        line = line + "\n"
        return line

    def fill_serial(serial_no: int, line_dict: dict):
        """
        line_operations.fill_serial() takes a serial number (serial_no) and a line_dict and creates line_dict["serial_no"] objects with
        the appropriate number of spaces inserted in front, so that the serial number is inserted at the place the .pdb-format
        dictates. It returns the line_dict with the appropriate serial_no.
        """
        if isinstance(serial_no, int):
            if serial_no >= 1e5:
                raise ValueError("Only serial numbers until 99.999 allowed. ")
            line_dict["serial_no"] = f"{serial_no: >5}"
        else:
            raise TypeError(f"The serial number {serial_no} is not an integer !!")
        return line_dict

    def fill_resi_no(resi_no, line_dict):
        """
        line_operations.fill_resi_no() takes a residue number (resi_no) and a line_dict and creates a line_dict with the serial
        number and the appropriate number of spaces inserted into line_dict["resi_no"]. It returns the line_dict.
        """
        if isinstance(resi_no, int):
            if resi_no >= 1e4:
                raise ValueError("Only residue numbers until 9.999 allowed. ")
            line_dict["resi_no"] = f"{resi_no: >4}"
        else:
            raise TypeError(f"The residue number {resi_no} is not an integer !!")
        return line_dict

    def add_terminus(lines):
        """
        line_operations.add_terminus() takes a list of strings (lines) and adds the string "TER" as the very last string in the list.
        """
        if lines[-1] != "TER":
            lines.append("TER")
        return lines

    def add_ending(lines):
        """
        line_operations.add_terminus() takes a list of strings (lines) and adds the string "TER" as the very last string in the list.
        """
        if lines[-1] != "END":
            lines.append("END")
        return lines

    def exchange_segment(line_dict, segment):
        """
        line_operations.exchange_segment() takes a line_dict and a segment name; then exchanges the previous segment name with the new
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
        line_operations.exchange_chainID() takes a line_dict and a name for a chainID (maximum of 1 character) and exchanges the previous
        chainID with the new chainID. It then returns the line_dict with the updated chainID.
        """
        if len(chainID) > 1:
            raise ValueError("chainID value given is longer than 1. ")
        line_dict["chainID"] = chainID
        return line_dict

class operations():
    def __init__(self):
        return 

    def _filter_segment(lines, segname):
        lines=[k for k in lines if segname in k]
        return lines

    def _split_segment(pdb_file, segname, pdb_id):
        """
        operations.split_segment() takes a pdb_file, a segname, and a pdb_id; then reads the file and drops all instances that
        do not have the segname within them. It writes the file as "coords/{pdb_id}_{segname}.pdb. Not having a folder "coords"
        will produce an error until the writefile function checks if the folder exists.
        """
        lines=files.read_file(pdb_file=pdb_file)
        lines=operations._filter_segment(lines=lines, segname=segname)
        files.write_file(file=f'coords/{pdb_id}_{segname}.pdb', lines=lines)
        return

    def split_segments(pdb_file, segnames, pdb_id):
        """
        operations.split_segments() takes a pdb_file and a list of segname strings (segnames) and a pdb_id; then for each
        instance in segnames calls the operations.split_segment() function, producing a single file that contains only the
        lines in the pdb that had the segname in them.
        """
        for segname in segnames:
            operations._split_segment(pdb_file=pdb_file, segname=segname, pdb_id=pdb_id)
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
        calls the line_operations.exchange_segment() function to exchange the segment identifier in the line_dict. In the end it
        writes the file based on pdb_file_output.
        """
        lines=files.read_file(pdb_file=pdb_file)
        lines_ = []
        serial_no=1
        for line in lines:
            line_dict=line_operations.read_pdb_line(line=line)
            line_dict=line_operations.exchange_segment(line_dict=line_dict, segment=segment)
            line_=line_operations.create_line(line_dict=line_dict)
            lines_.append(line_)
            serial_no+=1
        files.write_file(file=pdb_file_output, lines=lines_)
        return

    def add_chainID(pdb_file, pdb_file_output, chainID):
        """
        operations.add_chainID() takes a pdb_file and a output name pdb_file_output and a segment name; then iterates over
        all lines in the PDB file changing the chainID. In the end it saves the new file according to pdb_file_output.
        """
        lines=files.read_file(pdb_file=pdb_file)
        lines_ = []
        for line in lines:
            line_dict=line_operations.read_pdb_line(line=line)
            line_dict=line_operations.exchange_chainID(line_dict=line_dict, chainID=chainID)
            line_=line_operations.create_line(line_dict=line_dict)
            lines_.append(line_)
        files.write_file(file=pdb_file_output, lines=lines_)
        return

    def change_temp_factors(pdb_file, restraints_file, temp_dict=None, default="  1.00"):
        """
        operations.change_temp_factors() takes a pdb_file and a name for a restraints_file; then it
        creates a restraints file based on the specifications of CHARMM-GUIs NAMD constraint files.

        The function takes a dictionary temp_dict that contains the atom names as keys and the temp_factors as values.
        It also takes a default value to set to the other atoms.
            
            IMPORTANT: The temp_factors can overwrite each other. For example, if you set the temp_factor for "C" to 1.00 but
            also set the temp_factor for "CA" to 0.50, then all atoms that start with "C" will have a temp_factor of 1.00 except
            for the ones that start with "CA" which will have a temp_factor of 0.50. If "CA" is not in the dictionary then it will have the "C" value.
        
        Default settings are:
            H-atoms will recieve the temp_fac 0.00
            All C-atoms but CA (C-alphas) will recieve temp_fac 0.50
            All other atoms will recieve temp_fac 1.00.
        """
        lines=files.read_file(pdb_file=pdb_file)
        lines_ = []
        if temp_dict==None:
            temp_dict={
                "H": "  0.00",
                "C": "  0.50",
                "CA": "  1.00",
            }
        def convert_temp_fact(temp_fact, key=None):
            """
            Inner function to check and convert the temperature factor appropriately.
            """
            try:
                temp_fact=float(temp_fact)
            except:
                raise ValueError(f"{key} temperature factor {temp_fact} is not a float. ")
            temp_fact=f"{temp_fact:.2f}" .rjust(6, " ")
            if len(temp_fact)>6:
                raise ValueError(f"{key} temperature factor {temp_fact} is longer than 6 characters. ")
            return temp_fact
        
        #First check that the temp factors are valid
        for key in temp_dict.keys():
            temp_dict[key]=convert_temp_fact(temp_fact=temp_dict[key], key=key)
        default=convert_temp_fact(temp_fact=default, key="default")
        #Sort the keys by length
        ordered_keys=list(temp_dict.keys())
        ordered_keys.sort(key=len)
        

        for line in lines:
            line_dict=line_operations.read_pdb_line(line)
            is_default=True
            for key in ordered_keys:
                if line_dict["atom_name"].startswith(key):
                    line_dict["temp_fac"]=temp_dict[key]
                    is_default=False
            if is_default:
                line_dict["temp_fac"]=default
            line_ = line_operations.create_line(line_dict=line_dict)
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
        so it will raise a ValueError, if not it will use the line_operations.fill_serial() method to renumber the atoms starting at 1. In
        the end it will write a file based on pdb_file_output.
        """
        lines=files.read_file(pdb_file=pdb_file)
        if len(lines) > 99999:
            raise ValueError("len(lines)>99999. Try again with less atoms.")
        lines_ = []
        serial_no=1
        for line in lines:
            line_dict=line_operations.read_pdb_line(line=line)
            line_dict=line_operations.fill_serial(serial_no=serial_no, line_dict=line_dict)
            line_=line_operations.create_line(line_dict=line_dict)
            lines_.append(line_)
            serial_no+=1
        files.write_file(file=pdb_file_output, lines=lines_)
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
            line_dict=line_operations.read_pdb_line(line=line)
            line_dict=line_operations.fill_serial(serial_no=serial_no, line_dict=line_dict)
            resi_no=((serial_no-1)//3)+1
            line_operations.fill_resi_no(resi_no=resi_no, line_dict=line_dict)
            line_dict["segment"] = segment
            line_=line_operations.create_line(line_dict=line_dict)
            lines_.append(line_)
            serial_no+=1
        files.write_file(file=pdb_file_output, lines=lines_)
        return