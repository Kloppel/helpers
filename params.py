import pandas as pd

def split_list_by_keywords(input_list, keywords):
    sublists = []  # To store the sublists
    current_sublist = []  # To store the current sublist
    for item in input_list:
        if any(keyword in item for keyword in keywords):
            if current_sublist:
                sublists.append(current_sublist)  # Append the current sublist
            current_sublist = [item]  # Start a new sublist with the current item
        else:
            current_sublist.append(item)  # Add the item to the current sublist
    if current_sublist:
        sublists.append(current_sublist)  # Append the last sublist
    return sublists

def clean(list):
    list = [k for k in list if not k.startswith("ATOMS")]
    list = [k for k in list if not k.startswith("BONDS")]
    list = [k for k in list if not k.startswith("ANGLES")]
    list = [k for k in list if not k.startswith("DIHEDRALS")]
    list = [k for k in list if not k.startswith("IMPROPER")]
    list = [k for k in list if not k.startswith("NONBONDED")]
    list = [k for k in list if not k.startswith("cutnb ")]
    list = [k for k in list if not k.startswith("END")]
    list = [k for k in list if not k.startswith("!")]
    list = [k for k in list if not k.startswith("\n")]
    list = [k for k in list if not k.strip().startswith("!")]
    list = [k for k in list if not k.strip()==""]
    return list

def create_atoms_df(atoms, verbose, writefile):
    atoms_df = pd.DataFrame(columns=["mass", "number", "atomtype", "mass_value", "comment"])
    atoms = clean(atoms)
    for line in atoms:
        parts = line.split()
        if verbose:
            print(parts)
        mass_word = parts[0]
        number = parts[1]
        atomtype = parts[2]
        mass_value = parts[3]
        comment = ' '.join(parts[4:])
        mini_list = [mass_word, number, atomtype, mass_value, comment]
        if verbose:
            print(mini_list)
        mini_df = pd.DataFrame(mini_list)#, columns=["mass", "number", "atomtype", "mass_value", "comment"])
        if verbose:
            print(mini_df)
        mini_df = mini_df.T
        if verbose:
            print(mini_df)
        mini_df.columns=["mass", "number", "atomtype", "mass_value", "comment"]
        atoms_df = pd.concat([atoms_df, mini_df])
    if writefile:
        with open("atoms.prm", 'w') as file:
            file.writelines(atoms)
    return atoms_df

def create_bonds_df(bonds, verbose, writefile):
    bonds_df = pd.DataFrame(columns=["atom1", "atom2", "kb", "b0", "comment"])
    bonds = clean(bonds)
    for line in bonds:
        parts = line.split()
        if verbose:
            print(parts)
        atom1 = parts[0]
        atom2 = parts[1]
        kb = parts[2]
        b0 = parts[3]
        comment = ' '.join(parts[4:])
        mini_list = [atom1, atom2, kb, b0, comment]
        if verbose:
            print(mini_list)
        mini_df = pd.DataFrame(mini_list)
        if verbose:
            print(mini_df)
        mini_df = mini_df.T
        mini_df.columns=["atom1", "atom2", "kb", "b0", "comment"]
        if verbose:
            print(mini_df)
        bonds_df = pd.concat([bonds_df, mini_df])
    if writefile:
        with open("bonds.prm", 'w') as file:
            file.writelines(bonds)
    return bonds_df

def create_angles_df(angles, verbose, writefile):
    angles_df = pd.DataFrame(columns=["atom1", "atom2", "atom3," "ktheta", "theta0", "comment"])
    angles = clean(angles)
    for line in angles:
        parts = line.split()
        if verbose:
            print(parts)
        atom1 = parts[0]
        atom2 = parts[1]
        atom3 = parts[2]
        ktheta = parts[3]
        theta0 = parts[4]
        comment = ' '.join(parts[5:])
        mini_list = [atom1, atom2, atom3, ktheta, theta0, comment]
        if verbose:
            print(mini_list)
        mini_df = pd.DataFrame(mini_list)
        if verbose:
            print(mini_df)
        mini_df = mini_df.T
        if verbose:
            print(mini_df)
        mini_df.columns=["atom1", "atom2", "atom3", "ktheta", "theta0", "comment"]
        if verbose:
            print(mini_df)
        angles_df = pd.concat([angles_df, mini_df])
    if writefile:
        with open("angles.prm", 'w') as file:
            file.writelines(angles)
    return angles_df

def create_dihedrals_df(dihedrals, verbose, writefile):
    dihedrals_df = pd.DataFrame(columns=["atom1", "atom2", "atom3", "atom4", "kchi", "n", "delta", "comment"])
    dihedrals = clean(dihedrals)
    for line in dihedrals:
        parts = line.split()
        if verbose:
            print(parts)
        atom1 = parts[0]
        atom2 = parts[1]
        atom3 = parts[2]
        atom4 = parts[3]
        kchi = parts[4]
        n = parts[5]
        delta = parts[6]
        comment = ' '.join(parts[7:])
        mini_list = [atom1, atom2, atom3, atom4, kchi, n, delta, comment]
        if verbose:
            print(mini_list)
        mini_df = pd.DataFrame(mini_list)
        if verbose:
            print(mini_df)
        mini_df = mini_df.T
        if verbose:
            print(mini_df)
        mini_df.columns=["atom1", "atom2", "atom3", "atom4", "kchi", "n", "delta", "comment"]
        if verbose:
            print(mini_df)
        dihedrals_df = pd.concat([dihedrals_df, mini_df])
    if writefile:
        with open("dihedrals.prm", 'w') as file:
            file.writelines(dihedrals)
    return dihedrals_df

def create_nonbonded_df(nonbonded, verbose, writefile):
    nonbonded_df = pd.DataFrame(columns=["atom", "ignored", "epsilon", "rminhalf", "comment"])
    nonbonded = clean(nonbonded)
    for line in nonbonded:
        parts = line.split()
        if verbose:
            print(parts)
        atom = parts[0]
        ignored = parts[1]
        epsilon = parts[2]
        rminhalf = parts[3]
        comment = ' '.join(parts[4:])
        mini_list = [atom, ignored, epsilon, rminhalf, comment]
        if verbose:
            print(mini_list)
        mini_df = pd.DataFrame(mini_list)
        if verbose:
            print(mini_df)
        mini_df = mini_df.T
        if verbose:
            print(mini_df)
        mini_df.columns=["atom", "ignored", "epsilon", "rminhalf", "comment"]
        if verbose:
            print(mini_df)
        nonbonded_df = pd.concat([nonbonded_df, mini_df])
    if writefile:
        with open("nonbonded.prm", 'w') as file:
            file.writelines(nonbonded)
    return nonbonded_df

def read_charmm_parameters(filename):
    verbose, writefile=False, False
    with open(file="par_bv.prm") as file:
        lines = file.readlines()
    sections = ["ATOMS", "BONDS", "ANGLES", "DIHEDRALS", "IMPROPER", "NONBONDED"]
    sublists = split_list_by_keywords(input_list = lines, keywords=sections)
    intro, atoms, bonds, angles, dihedrals, improper, nonbonded = sublists[0], sublists[1], sublists[2], sublists[3], sublists[4], sublists[5], sublists[6]
    if verbose:
        print("atoms = ")
        print(atoms[:5])
        print("bonds = ")
        print(bonds[:5])
        print("angles = ")
        print(angles[:5])
        print("dihedrals = ")
        print(dihedrals[:5])
        print("improper = ")
        print(improper[:5])
        print("nonbonded = ")
        print(nonbonded[:5])
    atoms_df  = create_atoms_df(atoms=atoms, verbose=verbose, writefile=writefile)
    bonds_df  = create_bonds_df(bonds=bonds, verbose=verbose, writefile=writefile)
    angles_df = create_angles_df(angles=angles, verbose=verbose, writefile=writefile)
    dihedrals_df = create_dihedrals_df(dihedrals=dihedrals, verbose=verbose, writefile=writefile)
    nonbonded_df = create_nonbonded_df(nonbonded=nonbonded, verbose=verbose, writefile=writefile)
    if verbose:
        print(atoms_df.head())
        print(bonds_df.head())
        print(angles_df.head())
        print(dihedrals_df.head())
        print(nonbonded_df.head())
    return atoms_df, bonds_df, angles_df, dihedrals_df, nonbonded_df

if __name__ == "__main__":
    atoms_df_first, bonds_df_first, angles_df_first, dihedrals_df_first, nonbonded_df_first = read_charmm_parameters('par_bv.prm')
    atoms_df_second, bonds_df_second, angles_df_second, dihedrals_df_second, nonbonded_df_second = read_charmm_parameters(XXX) #exchange XXX for other parameter file
    #pd.merge(df1, df2, on=columns_to_compare, how='inner')
    atoms_df = pd.merge(atoms_df_first, atoms_df_second, on=["atomtype"], how="inner")
    bonds_df = pd.merge(bonds_df_first, bonds_df_second, on=["atom1", "atom2"], how="inner")
    angles_df = pd.merge(angles_df_first, angles_df_second, on=["atom1", "atom2", "atom3"], how="inner")
    dihedrals_df = pd.merge(dihedrals_df_first, dihedrals_df_second, on=["atom1", "atom2", "atom3", "atom4"], how="inner")
    nonbonded_df = pd.merge(nonbonded_df_first, nonbonded_df_second, on=["atom"], how="inner")
    atoms_df.to_csv("same_atom_params.csv")
    bonds_df.to_csv("same_bonds_params.csv")
    angles_df.to_csv("same_angles_params.csv")
    dihedrals_df.to_csv("same_dihedrals_params.csv")
    nonbonded_df.to_csv("same_nonbonded_params.csv")