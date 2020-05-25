import sys
import os
from itertools import combinations_with_replacement
from itertools import product
from collections import Counter

"""

    To Do:
    1 - add flag for too many substitutions and too few total sites - Do in Comp.py

"""


def COREMOD(core, core_mod, mod_dict, param_dict, compile_structures, size):

    structure_count = 0

    numsub = mod_dict['Number of Substitutions']
    mods   = mod_dict['Modifications']

    for j in range(len(numsub)):
        numsub[j] = int(numsub[j])
    
    sub_counts = [0 for i in range(max(numsub))]

    if 'replig' not in param_dict:
        param_dict['replig'] = 'true'
    if 'ffoption' not in param_dict:
        param_dict['ffoption'] = 'no'

    if not os.path.exists(core + "/" + "/xyz"):
        os.mkdir(core + "/" + "/xyz")
    if not os.path.exists(core + "/" + "/mol_files"):
        os.mkdir(core + "/" + "/mol_files")
    if not os.path.exists(core + "/" + "/runs"):
        os.mkdir(core + "/" + "/runs")

    sym_H, nonsym_H, all_H = [], [], []

    for k, v in core_mod.items():

        if k == 'Symmetric Hs':
            sym_H.append(v)
        if k == 'Non-Symmetric Hs':
            nonsym_H.append(v)
        if k == 'All Hs':
            all_H.append(v)
    
    h_s = []
    h_s.append(all_H)
    h_s.append(sym_H)
    h_s.append(nonsym_H)

    if os.path.exists(core + "/" + "/Structures"):
        os.system("rm " + core + "/" + "/Structures")

    for i in numsub:
        i = int(i)
        sub_count = 0

        with open(core + "/" + "/Structures", "a+") as f:
            f.write("Numer of Substitutions - " + str(i) + "\n\n")

        record = []

        for j in range(3):
            temp = h_s[j]
            if temp != []:
                for jj in temp:
                    if type(jj) == list:
                        if any(isinstance(el, list) for el in jj):
                            for k in jj:
                                if i ==1:
                                    record.append(k[:i])
                                else:
                                    for kk in range(min(i, len(k))):
                                        record.append(k[:i])
                        else:
                            for k in jj:
                                record.append([k])
                    else:
                        record.append([jj])


        mod_perm = list(combinations_with_replacement(mods, i))
        ind_perm = list(combinations_with_replacement(record, i))

        if size == 'large':
            mod_perm = list(product(mods, repeat=i))

        elif size == 'small':
            mod_perm = list(combinations_with_replacement(mods, i))

        temp = []
        for j in ind_perm:
            if j not in temp:
                flag = True
                for jj in j:
                    if len(jj) < j.count(jj):
                        flag = False
                if flag == True:
                    temp.append(j)

        ind_perm = temp

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

            temp = [''] * i
            for j in range(i):
                if len(ind[j]) == 1:
                    temp[j] = int(ind[j][0])
                else:
                    trim = False
                    jj = j
                    while trim == False:
                        try:
                            temp[j] = int(ind[j][jj])
                            trim = True
                        except:
                            jj -= 1

            ind = temp

            with open(core + "/" + "/Structures", "a+") as f:

                sub_txt = ''
                ind_txt = ''

                for jj in range(i):
                    sub_txt += str(sub[jj]) + " "
                    ind_txt += str(ind[jj]) + " "

                f.write(sub_txt + "\tsubstitutions on sites " + ind_txt + "\n")

            with open(core + "/" + "/mol_files/" + str(structure_count) + ".mol", "w") as f:

                f.write("-core " + core + "\n")
                f.write("-rundir " + core + "/runs/\n")

                f.write("-lig ")
                for j in sub:
                    f.write(j + " ")
                f.write("\n")

                f.write("-ligocc ")
                for j in range(i):
                    f.write("1" + " ")
                f.write("\n")

                f.write("-ccatoms ")
                temp = ''
                for j in ind:
                    temp += (str(j) + ",")
                f.write(temp[:-1])
                f.write("\n")

                for k, v in param_dict.items():
                    f.write("-" + str(k) + " " + str(v) + "\n")

            if compile_structures == True:
                os.system("molsimplify -i " + core + "/" + "/mol_files/" + str(structure_count) + ".mol")
                os.system("cp " + core + "/" + "/runs/*/*/*.xyz" + \
                          " " + core + "/" + "/xyz/" + str(structure_count) + ".xyz")
                os.system("rm -r " + core + "/" + "/runs/*")



            structure_count += 1
            sub_count += 1
        
        sub_counts[i-1] = sub_count

        with open(core + "/" + "/Structures", "a+") as f:
            f.write("\n%s structures created using %s substitutions" %(sub_count, i))
            f.write("\n\n")

    for j in numsub:
        print ("%s \ttotal structures generated with %s substitutions" %(sub_counts[j-1], j))
    print ("%s \ttotal structures generated" %(structure_count))


    if compile_structures == True:
        sys.exit()
    else:
        return


if __name__ == "__main__":

    core_dict   = {
                   'nickelporphyrin1': {'All Hs': [9, 10, 17, 18, 24, 25, 30, 31]},
                   'nickelporphyrin2': {'Symmetric Hs': [[9, 10], [17, 18], [24, 25]], 'Non-Symmetric Hs': [30, 31]}
                   }

    mod_dict    = {'Modifications': ['f', 'cl', 'br', 'i'], 'Number of Substitutions': [1]}

    param_dict = {'geometry': 'sqp'}

    for core, core_mod in core_dict.items():

        if not os.path.exists(core):
            os.mkdir(core)

        COREMOD(core, core_mod, mod_dict, param_dict)







