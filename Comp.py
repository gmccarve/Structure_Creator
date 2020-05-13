import os
import sys
from LigMod import LIGMOD


def COMP(ligand_dict, core_dict, mod_dict, extra_dict):

    def No_Inp(x):
        while x == '':
            x = str(input("\033[A > ")).lower()
        return x

    def clear():
        os.system('clear')


    try:
        ligand_dict[0]
    except:
        ligand_dict[0] = {}

    try:
        mod_dict['Number of Substitutions']
    except:
        mod_dict['Number of Substitutions'] = []

    try:
        mod_dict['Modifications']
        if mod_dict['Number of Substitutions'] == []:
            mod_dict['Number of Substitutions'] = [1]
    except:
        mod_dict['Modifications'] = []


    num_atoms = 0
    for k, v in ligand_dict.items():
        for kk, vv in v.items():
            for kkk, vvv in vv.items():
                if kkk == 'Non-Symmetric Hs' or kkk == 'Symmetric Hs':
                    num_atoms += len(vvv)

    for k, v in core_dict.items():
        for kk, vv in v.items():
            if kk == 'Non-Symmetric Hs' or kk == 'Symmetric Hs':
                num_atoms += len(vv)

    try:
        FAIL = 0
        mod_dict['Number of Substitutions']

        if len(mod_dict['Number of Substitutions']) > num_atoms:
            print ("\n\n ERROR. Too many substitutions and not enough atoms to modify")
            FAIL = 1

    except:
        FAIL = 0

    if FAIL == 1:
        sys.exit()


    for core, core_mod in core_dict.items():

        if not os.path.exists(core):
            os.mkdir(core)

        for k, v in ligand_dict.items():

            lig_count = 0
            for kk, vv in v.items():
                for kkk, vvv in vv.items():
                    if kkk != 'Number of Ligands':
                        lig_count += len(vvv)
        
        core_count = 0
        for k, v in core_mod.items():
            core_count += len(v)

        if lig_count == 0:
            COREMOD(core, core_mod, ligand_dict, mod_dict)

        elif core_count == 0:
            LIGMOD(core, ligand_dict, mod_dict)

        else:
            FULLMOD(core, core_mod, ligand_dict, mod_dict)



    sys.exit()


if __name__ == '__main__':


    ligand_dict = {0:
                  {'acac': {'Number of Ligands': '1', 'Symmetric Hs': [7, 8], 'Non-Symmetric Hs': [14]}, 
                   'no3': {'Number of Ligands': '2'}}}
    
    core_dict   = {'la': {'Symmetric Hs': [], 'Non-Symmetric Hs': []},
                   'gd': {'Symmetric Hs': [], 'Non-Symmetric Hs': []},
                   'lu': {'Symmetric Hs': [], 'Non-Symmetric Hs': []}}


    mod_dict    = {'Modifications': ['f', 'cl', 'br'], 'Number of Substitutions': [1]}

    COMP(ligand_dict, core_dict, mod_dict)


