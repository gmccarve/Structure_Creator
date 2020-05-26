import sys
import os
from itertools import combinations_with_replacement
from itertools import product
from collections import Counter

#TODO Add option to have constant modification (CF3 on a beta arm)

def LIGMOD(core, ligand_dict, mod_dict, param_dict, compile_structures, size):

    numsub = mod_dict['Number of Substitutions']
    mods   = mod_dict['Modifications']

    temp = []
    for j in numsub:
        temp.append(int(j))

    numsub = temp

    for envir_num, lig_envir in ligand_dict.items():

        sub_counts = [0 for i in range(max(numsub))]

        structure_count = 0

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
                    if kkk == 'Ligand Frequency':
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
                for jjj in range(len(ligands)):
                    try:
                        temp = h_s[jj][jjj] 
                    except:
                        temp = []
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

            ind_perm = list(combinations_with_replacement(record, i))

            if size == 'large':
                mod_perm = list(product(mods, repeat=i))

            elif size == 'small':
                mod_perm = list(combinations_with_replacement(mods, i))

            temp = []
            for j in ind_perm:
                if j not in temp:
                    temp.append(j)

            ind_perm = []

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


                temp = []
                for jj in ind:
                    temp.append(jj[0])

                temp_ = {}
                for jj in temp:
                    temp_[jj] = temp.count(jj)

                temp = temp_

                sub_for_file = []
                ind_for_file = []

                sub_counter = 0
                for k, v in temp.items():
                    temp_ = []
                    for jj in range(v):
                        temp_.append(sub[sub_counter:sub_counter+v][jj])
                    sub_for_file.append(temp_)
                    sub_counter += v

                temp_ = []
                for jj in range(i):
                    temp_.append(ind[jj][1])

                for jj in range(len(temp_)):
                    jj_ind_min = min(jj+1, len(temp_[jj]))-1

                    ind_for_file.append(temp_[jj][jj_ind_min])

                temp = []
                jj_counter = 0
                for jj in range(len(sub_for_file)):
                    jj_len = len(sub_for_file[jj])
                    temp.append(ind_for_file[jj_counter:jj_len+jj_counter])
                    jj_counter += jj_len

                ind_for_file = temp


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


                    f.write(str(structure_count) + " - " + mod_txt + "\tfor ligands " + lig_txt + "\ton sites " + sub_txt + "\n")

                with open(core + "/" + str(envir_num) + "/mol_files/" + str(structure_count) + ".mol", "w") as f:

                    f.write("-core "   + core + "\n")
                    f.write("-rundir " + core + "/" + str(envir_num) + "/runs/\n")

                    f.write("-lig ")

                    for jj in range(len(lig_for_file)):
                        if lig_for_file[jj] != '':
                            f.write(lig_for_file[jj] + " ")

                    for jj in range(len(lig_for_file)):
                        if lig_for_file[jj] == '':
                            f.write(ligands[jj] + " ")

                    f.write("\n")

                    f.write("-ligocc ")

                    for jj in range(len(num_for_file)):
                        if num_for_file[jj] != '':
                            f.write(str(num_for_file[jj]) + " ")

                    for jj in range(len(num_for_file)):
                        if num_for_file[jj] == '':
                            f.write(str(ligoccu[jj]) + " ")

                    f.write("\n")

                    f.write("-decoration ")

                    for jj in range(len(sub_for_file)):
                        if len(sub_for_file[jj]) == 1:
                            f.write("[" + sub_for_file[jj][0] + "] ")
                        else:
                            string =  "["
                            for jjj in range(len(sub_for_file[jj])):
                                string += sub_for_file[jj][jjj]
                                string += ","
                            string = string[:-1]
                            f.write(string + "] ")

                    f.write("\n")

                    f.write("-decoration_index ")

                    for jj in range(len(ind_for_file)):
                        if len(ind_for_file[jj]) == 1:
                            f.write("[" + str(ind_for_file[jj][0]) + "] ")
                        else:
                            string =  "["
                            for jjj in range(len(ind_for_file[jj])):
                                string += str(ind_for_file[jj][jjj])
                                string += ","
                            string = string[:-1]
                            f.write(string + "] ")

                    f.write("\n")

                    for k, v in param_dict.items():
                        f.write("-" + str(k) + " " + str(v) + "\n")


                if compile_structures == True:

                    os.system("molsimplify -i " + core + "/" + str(envir_num) + "/mol_files/" + str(structure_count) + ".mol")
                    os.system("cp " + core + "/" +  str(envir_num) + "/runs/*/*/*.xyz" + \
                              " " + core + "/" + str(envir_num) + "/xyz/" + str(structure_count) + ".xyz")
                    os.system("rm -r " + core + "/" + str(envir_num) + "/runs/*")
                

                structure_count += 1
                sub_count += 1

            
            sub_counts[i-1] = sub_count

            with open(core + "/" + str(envir_num) + "/Structures", "a+") as f:
                f.write("\n%s structures created using %s substitutions" %(sub_count, i))
                f.write("\n\n")

    print ("CORE :", core)
    for j in numsub:
        print ("%s \ttotal structures generated with %s substitutions" %(sub_counts[j-1], j))

    print ("%s \ttotal structures generated" %(structure_count))

    if compile_structures == True:
        sys.exit()

    else:
        return




if __name__ == "__main__":


    if sys.argv[1] == 'long':
        ligand_dict = {0:
                      [{'acac': {'Ligand Frequency': '1', 'Symmetric Hs': [[8, 9, 10], [11, 12, 13]], 'Non-Symmetric Hs': [14]},
                        'no3': {'Ligand Frequency': '2'}}],
                       1:
                      [{'acac': {'Ligand Frequency': '2', 'Symmetric Hs': [[8, 9, 10], [11, 12, 13]], 'Non-Symmetric Hs': [14]},
                        'no3': {'Ligand Frequency': '1'}}],
                       2:
                      [{'acac': {'Ligand Frequency': '3', 'Symmetric Hs': [[8, 9, 10], [11, 12, 13]], 'Non-Symmetric Hs': [14]}}]
                  }
    elif sys.argv[1] == 'short':
        ligand_dict = {0:
                [{'acac': {'Ligand Frequency': 1, 'Non-Symmetric Hs':[8, 9]}}]}



    core        = 'la'

    mod_dict    = {'Modifications': ['f', 'cl', 'br'], 'Number of Substitutions': [2]}

    param_dict = {'geometry': 'tpl'}

    if not os.path.exists(core):
            os.mkdir(core)

    LIGMOD(core, ligand_dict, mod_dict, param_dict, False, 'small')
