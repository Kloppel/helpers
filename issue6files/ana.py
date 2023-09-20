def cco_rmsd(state, universe):
    import os
    import pandas as pd
    import matplotlib.pyplot as plt
    import numpy as np
    import MDAnalysis as mda
    if not os.path.exists(f"{state}/coords/analysis/"):
        os.mkdir(f"{state}/coords/analysis/")
    from MDAnalysis.analysis import rms
    rmsd = rms.RMSD(universe, select='backbone', groupselections=['name CA', 'protein', 'segid EHEM', 'segid GHEM', 'segid META']).run();
    rmsd_df = pd.DataFrame(rmsd.results.rmsd[:, 2:], columns=['Backbone', 'C-alphas', 'Protein', 'Heme a3', 'Heme a', 'Metals'], index=rmsd.results.rmsd[:, 1])
    rmsd_df.index.name='Time (ps)'
    print("RMSD results numpy-array shape (timesteps, variables): " + str(rmsd.results.rmsd.shape))
    fig, axes = plt.subplots(figsize=(8,4))
    rmsd_df.plot.line(ax=axes)
    fig.savefig(f"{state}/coords/analysis/3hb3_{state}_unaligned.png")

    from MDAnalysis.analysis import align
    crystal_struct = mda.Universe(f"{state}/coords/3hb3_{state}.psf", f"{state}/coords/3hb3_{state}.crd")
    aligner = align.AlignTraj(universe, crystal_struct, select='backbone', filename=f'{state}/coords/analysis/{state}_aligned.dcd').run();
    aligned_universe = mda.Universe(f'{state}/coords/3hb3_{state}.psf', f'{state}/coords/3hb3_{state}.crd', f'{state}/coords/analysis/{state}_aligned.dcd')
    rmsd_aligned = rms.RMSD(aligned_universe, select='backbone', groupselections=['name CA', 'protein', 'segid EHEM', 'segid GHEM', 'segid META']).run();
    print("RMSD results numpy-array shape (timesteps, variables): " + str(rmsd_aligned.results.rmsd.shape))
    rmsd_aligned_df = pd.DataFrame(rmsd_aligned.results.rmsd[:,2:], columns=['Backbone', 'C-alphas', 'Protein', 'EHEM', 'GHEM', 'Metals'], index=rmsd_aligned.results.rmsd[:,1])
    rmsd_aligned_df.index.name='Time (ps)'
    fig, axes = plt.subplots(figsize=(8,4))
    rmsd_aligned_df.plot.line(ax=axes)
    fig.savefig(f"{state}/coords/analysis/3hb3_{state}_aligned.png")
    return

def hydrogen_bonds_hemes(universe, filename):
    import pandas as pd
    import MDAnalysis as mda
    import numpy as np
    from MDAnalysis.analysis.hydrogenbonds.hbond_analysis import HydrogenBondAnalysis as HBA
    hbonds = HBA(universe=universe, between=["around 5 segid EHEM or around 5 segid GHEM", "resname TIP3"])

    protein_hydrogens_sel = hbonds.guess_hydrogens("protein")
    protein_acceptors_sel = hbonds.guess_acceptors("protein")

    water_hydrogens_sel = "resname TIP3 and name H1 H2"
    water_acceptors_sel = "resname TIP3 and name OH2"

    hbonds.hydrogens_sel = f"({protein_hydrogens_sel}) or ({water_hydrogens_sel} and around 10 not resname TIP3 and not segid MEMB)"
    hbonds.acceptors_sel = f"({protein_acceptors_sel}) or ({water_acceptors_sel} and around 10 not resname TIP3 and not segid MEMB)"

    hbonds.run()
    np.save(filename, hbonds.results.hbonds)
    print("H-bond analysis bonds numpy array looks like: ")
    print(hbonds.results.hbonds)
    hbonds = pd.DataFrame(hbonds.results.hbonds)
    hbonds.to_csv("hbonds_ooxox.csv")
    return
