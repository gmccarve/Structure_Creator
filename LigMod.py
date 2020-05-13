import sys
import os
import itertools
from itertools import combinations_with_replacement
from itertools import permutations
from collections import Counter

"""

    To Do:
    
    1 - add mutliple, symmetric sets as [[], []...]


"""


def LIGMOD(core, ligand_dict, mod_dict):

    structure_count = 0

    numsub = mod_dict['Number of Substitutions']
    mods   = mod_dict['Modifications']



    for envir_num, lig_envir in ligand_dict.items():

        if not os.path.exists(core + "/" + str(envir_num)):
            os.mkdir(core + "/" + str(envir_num))
        if not os.path.exists(core + "/" + str(envir_num) + "/xyz"):
            os.mkdir(core + "/" + str(envir_num) + "/xyz")
        if not os.path.exists(core + "/" + str(envir_num) + "/mol_files"):
            os.mkdir(core + "/" + str(envir_num) + "/mol_files")
        if not os.path.exists(core + "/" + str(envir_num) + "/runs"):
            os.mkdir(core + "/" + str(envir_num) + "/runs")
        
        print ("Environment Number: " + str(envir_num))
        print ()


        all_H    = {}
        sym_H    = {}
        nonsym_H = {}

        for lig, lig_info in lig_envir.items():

            if 'All Hs' in lig_info:
                all_H = []
                lig_info['All Hs']
                for k in lig_info['All Hs']:
                    all_H.append(k)
                ALLH = True

            else:
                ALLH = False
                sym_H[lig]    = []
                nonsym_H[lig] = []

                try:
                    lig_info['Symmetric Hs']
                    for k in lig_info['Symmetric Hs']:
                        sym_H[lig].append(k)

                except:
                    pass

                try:
                    lig_info['Non-Symmetric Hs']
                    for k in lig_info['Non-Symmetric Hs']:
                        nonsym_H[lig].append(k)

                except:
                    pass


        for i in numsub:

            if ALLH == False:
                
                front = []
                all_H = []

                for k, v in sym_H.items():

                    if v != []:
                        front = v[:int(i)]
                        all_H.append(front)

                for k, v in nonsym_H.items():

                    if v != []:
                        all_H.append(v)

            all_H = list(itertools.chain.from_iterable(all_H))

            print ("Number of Substitutions: " + i)
            print ()
            mod_perm = list(combinations_with_replacement(mods, int(i)))
            ind_perm = list(permutations(all_H, int(i)))
        
            
            if list(itertools.chain.from_iterable(ind_perm)) == []:

                print ("Congratulations. Somehow you got this far with too many substitutions and too few")
                print ("substitution sites. Don't do that again.")
                print ("Skipping environment #%s." %i)
                print ()
                break



            unique = []

            for j in ind_perm:
                for k in mod_perm:
                    count = list(Counter(k))
                    if len(count) < int(i):
                        jj = sorted(j)
                    else:
                        jj = j
                    k_jj = [k, jj]
                    if k_jj not in unique:
                        unique.append(k_jj)

            for j in unique:
                sub = j[0]
                ind = j[1]

                subs = ''
                for k in sub:
                    subs += str(k) + "_"
                subs = subs[:-1]

                inds = ''
                for k in ind:
                    inds += str(k) + "_"
                inds = inds[:-1]

                with open(core + "/" + str(envir_num) + "/mol_files/" + "%s_%s.mol" %(subs, inds), "w") as f:

                    f.write("-core "   + core + "\n")
                    f.write("-lig ")
                    for lig, lig_info in lig_envir.items():
                        f.write(lig + " ")
                    f.write("\n")
                    f.write("-ligocc ")
                    for lig, lig_info in lig_envir.items():
                        f.write(str(lig_info['Number of Ligands']) + " ")
                    f.write("\n")
                    f.write("-rundir " + core + "/" + str(envir_num) + "/runs/\n")
                    f.write("-geometry oct\n")

                    temp = '-decoration ['
                    for k in sub:
                        temp += str(k) + ','
                    temp = temp[:-1]
                    temp += ']\n'
                    f.write(temp)
                    temp = '-decoration_index ['
                    for k in ind:
                        temp += str(k) + ','
                    temp = temp[:-1]
                    temp += ']\n'
                    f.write(temp)


                os.system("molsimplify -i " + core + "/" + str(envir_num) + "/mol_files/" + "%s_%s.mol" % (subs, inds))
                os.system("cp " + core + "/" +  str(envir_num) + "/runs/*/*/*.xyz" + \
                          " " + core + "/" + str(envir_num) + "/xyz/" + "%s_%s.xyz" % (subs, inds))
                os.system("rm -r " + core + "/" + str(envir_num) + "/runs/*")

                structure_count += 1

    print ("%s total structures generated" %structure_count)

    
    return




if __name__ == "__main__":


    #"""
    ligand_dict = {0:
                  {'acac': {'Number of Ligands': '1', 'Symmetric Hs': [8, 9, 10], 'Non-Symmetric Hs': [14]},
                   'no3': {'Number of Ligands': '2'}}, 
                  1:
                  {'acac': {'Number of Ligands': '2', 'Symmetric Hs': [8, 9, 10], 'Non-Symmetric Hs': [14]},
                   'no3': {'Number of Ligands': '1'}},
                  2:
                  {'acac': {'Number of Ligands': '3', 'Symmetric Hs': [8, 9, 10], 'Non-Symmetric Hs': [14]}}}

    #"""

    #ligand_dict = {0:{'acac':{'Number of Ligands': '3', 'All Hs': [8, 9, 10, 11]}}}

    core        = 'la'

    mod_dict    = {'Modifications': ['f', 'cl', 'br'], 'Number of Substitutions': ['1']}


    LIGMOD(core, ligand_dict, mod_dict)
