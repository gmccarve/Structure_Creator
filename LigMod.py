import sys
import os
import numpy as np
import itertools
from itertools import combinations_with_replacement
from itertools import combinations
from itertools import permutations
from collections import Counter

"""

    To Do:
    1 - Figure out a way to reduce redundancies on say two identical methyl groups
        where a double sub on one methyl is identical to a double sub on the other 
        methyl
    2 - Fix higher substitutions with symmetric centers
        4 subs on ligand with metyl
    
"""

def TEST(lst): 
      
    return list(set([i for i in lst]))


def LIGMOD(core, ligand_dict, mod_dict, param_dict):

    structure_count = []

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
        
        ligands = []
        ligoccu = []
        for k in lig_envir:
            for kk, vv in k.items():
                ligands.append(kk)
                for kkk, vvv in vv.items():
                    if kkk == 'Number of Ligands':
                        ligoccu.append(vvv)


        all_H    = []
        sym_H    = []
        nonsym_H = []

        lig_count = 0
        for j in lig_envir:

            SYM  = False
            nSYM = False
            ALLH = False
            for k, v in j.items():
                if 'Symmetric Hs' in v:
                    SYM = True
                if 'Non-Symmetric Hs' in v:
                    nSYM = True
                if 'All Hs' in v:
                    ALLH = True

                if ALLH == False:
                    all_H += [[]]
                if SYM == False:
                    sym_H += [[]]
                if nSYM == False:
                    nonsym_H += [[]]

                for kk, vv in v.items():

                    if kk == "All Hs":
                        if ALLH == True:
                            all_H = all_H + [vv]
                    elif kk == 'Symmetric Hs':
                        if SYM == True:
                            sym_H = sym_H + [vv]
                    elif kk == 'Non-Symmetric Hs':
                        if nSYM == True:
                            nonsym_H = nonsym_H + [vv]
            lig_count += 1


        h_s = []
        h_s.append(all_H)
        h_s.append(sym_H)
        h_s.append(nonsym_H)

        if os.path.exists(core + "/" + str(envir_num) + "/Structures"):
            os.system("rm " + core + "/" + str(envir_num) + "/Structures")

        for i in numsub:
            i = int(i)
            sub_count = 0

            with open(core + "/" + str(envir_num) + "/Structures", "a+") as f:
                f.write("Numer of Substitutions - " + str(i) + "\n\n")

            record = []

            for jj in range(3):
                for jjj in range(len(all_H)):
                    temp = h_s[jj][jjj] 
                    if temp != []:
                        for k in temp:
                            temp_ = []
                            if type(k) == list:
                                if i == 1:
                                    record.append([jjj, k[:i]])
                                else:
                                    for kk in range(i):
                                        record.append([jjj, k[:i]]) 
                            else:
                                record.append([jjj, [k]])


            mod_perm = list(combinations_with_replacement(mods, i))
            ind_perm = list(combinations_with_replacement(record, i))

            temp = []
            for j in ind_perm:
                if j not in temp:
                    temp.append(j)

            ind_perm = []

            waste = []


            for j in temp:
                subs  = []
                sites = []
                temp2 = []
                for jj in j:
                    if jj not in temp2:
                        temp2.append(jj)
                        subs.append(j.count(jj))

                for jj in range(len(temp2)):
                    sites.append(len(temp2[jj][1]))

                
                if sum(sites) >= i:
                    flag = True
                    for jj in range(len(sites)):
                        if sites[jj] < subs[jj]:
                            flag = False

                    if flag == True:
                        ind_perm.append(j)


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

                lig_for_file = ["" for i in range(len(ligands))]
                num_for_file = ["" for i in range(len(ligands))]

                for jj in ind:
                    lig_for_file[jj[0]] = ligands[jj[0]]
                    num_for_file[jj[0]] = ligoccu[jj[0]]

                test = []
                for jj in range(len(ind)):
                    if ind[jj][0] not in test:
                        test.append(ind[jj][0])

                sub_for_file = list(sub)
                ind_for_file = [[] for i in range(len(test))]
                
                for jj in range(len(test)):
                    ind_for_file[jj] = ind[jj:]

                print (lig_for_file, num_for_file, sub_for_file, ind)
                
                

                

                with open(core + "/" + str(envir_num) + "/Structures", "a+") as f:

                    mod_txt = ''
                    lig_txt = ''
                    sub_txt = ''

                    for jj in range(i):
                        mod_txt += str(sub[jj]) + " "
                        lig_txt += str(ind[jj][0]) + " "
                            
                        if all(elem == ind[0] for elem in ind) and len(ind) != 1:
                            sub_txt += str(ind[jj][1][jj]) + " "
                        else:
                            sub_txt += str(ind[jj][1][0]) + " "


                    f.write(mod_txt + "\tfor ligands " + lig_txt + "\ton sites " + sub_txt + "\n")
                    
        

                with open(core + "/" + str(envir_num) + "/mol_files/" + str(sub_count) + ".mol", "w") as f:

                    f.write("-core "   + core + "\n")
                    f.write("-rundir " + core + "/" + str(envir_num) + "/runs/\n")

                    f.write("-lig ")
                    temp_lig = [''] * len(ligands)
                    for jj in ind:
                        lig_ = ligands[jj[0]]
                        f.write(lig_ + " ")
                        temp_lig[jj[0]] = lig_
                    for jj in range(len(ligands)):
                        if temp_lig[jj] == '':
                            f.write(ligands[jj] + " ")
                    f.write("\n")

                    f.write("-ligocc ")
                    for jj in ligoccu:
                        f.write(str(jj) + " ")
                    f.write("\n")

                    f.write("-decoration ")
                    for jj in sub:
                        f.write("[" + str(jj) + "] ")
                    f.write("\n")

                    f.write("-decoration_index ")
                    if all(elem == ind[0] for elem in ind) and len(ind) != 1:
                        for jj in range(len(ind)):
                            f.write("[" + str(ind[jj][1][jj]) + "] ")
                    else:
                        for jj in ind:
                            f.write("[" + str(jj[1][0]) + "] ")
                    f.write("\n")

                    for k, v in param_dict.items():
                        f.write("-" + str(k) + " " + str(v) + "\n")

                
                #os.system("molsimplify -i " + core + "/" + str(envir_num) + "/mol_files/" + str(structure_count) + ".mol")
                #os.system("cp " + core + "/" +  str(envir_num) + "/runs/*/*/*.xyz" + \
                #                " " + core + "/" + str(envir_num) + "/xyz/" + str(structure_count) + ".xyz")
                #os.system("rm -r " + core + "/" + str(envir_num) + "/runs/*")
                
                #os.system("cat " + core + "/" + str(envir_num) + "/mol_files/" + str(sub_count) + ".mol; echo")

                sub_count += 1

            structure_count.append(sub_count)
    
            with open(core + "/" + str(envir_num) + "/Structures", "a+") as f:
                f.write("\n%s structures created using %s substitutions" %(sub_count, i))
                f.write("\n\n")

        

    print ("%s total structures generated" %(sum(structure_count)))

    
    return




if __name__ == "__main__":


    if sys.argv[1] == 'long':
        ligand_dict = {0:
                     [{'acac': {'Number of Ligands': '1', 'Symmetric Hs': [[8, 9, 10], [11, 12, 13]], 'Non-Symmetric Hs': [14]}},
                      {'acac': {'Number of Ligands': '1', 'Symmetric Hs': [[8, 9, 10], [11, 12, 13]], 'Non-Symmetric Hs': [14]}}, 
                      {'acac': {'Number of Ligands': '1', 'Symmetric Hs': [[8, 9, 10], [11, 12, 13]], 'Non-Symmetric Hs': [14]}}]
                    }

    elif sys.argv[1] == 'short':

        ligand_dict = {0:
                     [{'acac': {'Number of Ligands': '3', 'Symmetric Hs': [[8, 9, 10], [11, 12, 13]], 'Non-Symmetric Hs': [14]}}]
                      }

    elif sys.argv[1] == 'test':

        ligand_dict = {0:
                     [{'acac': {'Number of Ligands': '3', 'All Hs': [8, 9, 10, 11, 12, 13, 14]}}]
                     }


    core        = 'la'

    mod_dict    = {'Modifications': ['f', 'cl'], 'Number of Substitutions': [1, 2]}

    param_dict = {'geometry': 'oct'}

    if not os.path.exists(core):
            os.mkdir(core)

    LIGMOD(core, ligand_dict, mod_dict, param_dict)
