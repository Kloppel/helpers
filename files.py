class files():
    def __init__(self):
        return self

    def read_file(pdb_file):
        """
        files.readfile() reads a .pdb file using the readlines method. It also filters out all lines containing the keywords
        REMARK, TER, TITLE, CRYST1, SCALE
        and returns the list containing the lines (strings)
        """
        lines = open(pdb_file, 'r').readlines()
        lines = [k for k in lines if "REMARK" not in k]
        lines = [k for k in lines if "TER" not in k]
        lines = [k for k in lines if "TITLE" not in k]
        lines = [k for k in lines if "CRYST1" not in k]
        lines = [k for k in lines if "SCALE" not in k]
        #lines = [k.replace("\n", '') for k in lines]
        return lines
    
    def write_file(file, lines):
        """
        files.writefile takes a list of strings, e.g. from a read file like with the files.readfile function and opens a writer. 
        Using this write method, files.writefile writes the lines into a file that is saved, and closes the write-method. 
        It returns nothing.
        """
        f = open(file, mode="w", encoding="utf-8")
        f.writelines(lines)
        f.close()
        return 