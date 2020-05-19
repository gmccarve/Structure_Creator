import os
import sys
import itertools
from LigMod import LIGMOD
from CoreMod import COREMOD
from FullMod import FULLMOD



def COMP(ligand_dict, core_dict, mod_dict, param_dict):

    try:
        ligand_dict[0]
    except:
        ligand_dict[0] = {}

    try:
        mod_dict['Modifications']
        try:
            mod_dict['Number of Substitutions']
        except:
            mod_dict['Number of Substitutions'] = [1]
    except:
        mod_dict['Modifications'] = []
        mod_dict['Number of Substitutions'] = []

    num_lig_atoms = 0
    for k, v in ligand_dict.items():
        for kk in v:
            for kkk, vvv in kk.items():
                for kkkk, vvvv in vvv.items():
                    if kkkk == 'Non-Symmetric Hs':
                        if vvvv != []:
                            num_lig_atoms += len(vvvv)
                    elif kkkk == 'Symmetric Hs':
                        if vvvv != []:
                            try:
                                num_lig_atoms += len(list(itertools.chain.from_iterable(vvvv)))
                            except:
                                num_lig_atoms += len(vvvv)

    num_core_atoms = 0
    for k, v in core_dict.items():
        for kk, vv in v.items():
            if kk == 'Non-Symmetric Hs' or kk == 'Symmetric Hs':
                if vv != []:
                    num_core_atoms += len(vv)

    num_atoms = num_core_atoms + num_lig_atoms

    if len(mod_dict['Number of Substitutions']) > num_atoms:
        print ("\n\n ERROR. Too many substitutions and not enough atoms to modify\
                  \n Changing number of substitutions to match number of given\
                  \n modifications")
        mod_dict['Number of Substitutions'] = num_atoms
    


    for core, core_mod in core_dict.items():

        if not os.path.exists(core):
            os.mkdir(core)

        
        if num_lig_atoms == 0:
            COREMOD(core, core_mod, ligand_dict, mod_dict, param_dict)
        elif num_core_atoms == 0:
            LIGMOD(core, ligand_dict, mod_dict, param_dict)
        elif num_core_atoms == 0 and num_lig_atoms == 0:
            print ("Nothing to do")
            sys.exit()
        else:
            FULLMOD(core, core_mod, ligand_dict, mod_dict, param_dict)



if __name__ == '__main__':


    ligand_dict = {0: [{'acac': {'Ligand Frequency': '3', 'Symmetric Hs': [[1, 2, 3], [4, 5, 6]], 'Non-Symmetric Hs': [14]}}]}

    core_dict   = {'la': {'Symmetric Hs': [1], 'Non-Symmetric Hs': []},
                   'gd': {'Symmetric Hs': [], 'Non-Symmetric Hs': []},
                   'lu': {'Symmetric Hs': [], 'Non-Symmetric Hs': []}}


    mod_dict    = {'Modifications': ['f', 'cl', 'br'], 'Number of Substitutions': [1]}

    param_dict  = {'geometry': 'oct'}

    COMP(ligand_dict, core_dict, mod_dict, param_dict)


