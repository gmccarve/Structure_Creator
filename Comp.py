import os
import sys
import itertools
from LigMod import LIGMOD
from CoreMod import COREMOD

#TODO check error from too many mods and not enough sites

def COMP(ligand_dict, core_dict, mod_dict, param_dict):

    def Input():

        x = input(" > ").lower()

        while x == '':
            x = str(input("\033[A > ")).lower()
        while x.endswith(" ") == True:
            x = x[:-1]
        while x.startswith(" ") == True:
            x = x[1:]
        return x

    if core_dict == {}:
        print ("\n\nNo cores given and thus nothing to do\n\n")
        return

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
        print ("No modifications given. Quiting program.")
        sys.exit()

    mod_dict['Modifications'] = sorted(mod_dict['Modifications'])

    num_lig_atoms = 0
    for k, v in ligand_dict.items():
        for kk in v:
            for kkk, vvv in kk.items():
                for kkkk, vvvv in vvv.items():
                    if kkkk == 'Non-Symmetric Hs' or kkkk == 'All Hs':
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
            if kk == 'Non-Symmetric Hs' or kk == 'Symmetric Hs' or kk == 'All Hs':
                if vv != []:
                    num_core_atoms += len(vv)

    for j in mod_dict['Number of Substitutions']:
        if int(j) > num_core_atoms and int(j) > num_lig_atoms:  
            print ("\n\n ERROR. Too many substitutions and not enough atoms to modify")
            sys.exit()

    print ("\n\n Do you want to display the number of structures that would be created? (y/n)\n")
    choice = Input()

    if choice == 'y':
        compile_structures = False
    else:
        compile_structures = True

    print ("\n\n Do you want to generate all possible structures or eliminate redundancies?")
    print ("\n 1 - Generate all possible structures\
            \n 2 - Eliminate redundancies to some degree\n")

    choice = Input()

    if choice == '1':
        size = 'large'
    else:
        size = 'small'

    for core, core_mod in core_dict.items():

        if not os.path.exists(core):
            os.mkdir(core)
        if num_lig_atoms == 0:
            COREMOD(core, core_mod, mod_dict, param_dict, compile_structures, size)
        elif num_core_atoms == 0:
            LIGMOD(core, ligand_dict, mod_dict, param_dict, compile_structures, size)
        elif num_core_atoms == 0 and num_lig_atoms == 0:
            print ("Nothing to do")
            sys.exit()

if __name__ == '__main__':


    ligand_dict = {0: [{'acac': {'Ligand Frequency': '3', 'Symmetric Hs': [8, 9, 10], 'Non-Symmetric Hs': [14]}}]}

    core_dict   = {'la': {},
                   'gd': {},
                   'lu': {}}


    mod_dict    = {'Modifications': ['f', 'cl', 'br'], 'Number of Substitutions': [2], 'Permanent': [['cl', 8]]}

    param_dict  = {'geometry': 'oct'}

    COMP(ligand_dict, core_dict, mod_dict, param_dict)


