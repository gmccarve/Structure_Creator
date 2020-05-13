import os
import sys


def FILE_INPUT(input_file):

    def Find_Molsim():
        for root, dir, files in os.walk(os.path.expanduser('~')):
            if 'cores.dict' in files:
                return str(root)[:-5]


    core_dict   = {}
    ligand_dict = {}
    mod_dict    = {}
    extra_dict  = {}

    runcheck = False

    molsim = Find_Molsim()


    with open(input_file) as f:
        ff = f.readlines()

    count = 0
    for j in ff:
        if j.startswith("#"):
            ff.remove(j)
        while '  ' in ff[count]:
            ff[count] = ff[count].replace("  ", " ")

        count += 1

    for j in range(len(ff)):
        line = str(ff[j])[:-1]

        if line.startswith("%"):
            item = str(line)[1:].lower()

            if item.startswith('core'):
                count = 1
                temp = []

                core = item.lower().split(" ")[1:][0]

                core_dict[core] = {}

                while ff[j+count].startswith('end') == False:

                    temp.append(str(ff[j+count])[:-1])

                    count += 1

                CORE_FILE, CON_ATOM, MAX_DENT = False, False, False

                for j in temp:
                    j_low = j.lower()
                    j_val = j.lower().split(" ")[1:]

                    if j_low.startswith("symmetric"):
                        core_dict[core]['Symmetric Hs'] = j_val

                    elif j_low.startswith("nonsymmetric"):
                        core_dict[core]['Non-Symmetric Hs'] = j_val

                    elif j_low.startswith('all'):
                        core_dict[core]['All Hs'] = j_val

                    elif j_low.startswith('add_core'):
                        add_core_file = j.split(" ")[1:][0]
                        CORE_FILE = True

                    elif j_low.startswith('add_con_atom'):
                        add_con_atom = ""
                        for j in j_val:
                            add_con_atom += j + " "
                        add_con_atom = str(add_con_atom)[:-1]
                        CON_ATOM = True

                    elif j_low.startswith('add_max_dent'):
                        add_max_dent = j_val[0]
                        MAX_DENT = True

                if CORE_FILE == True and CON_ATOM == True and MAX_DENT == True:

                    os.system("cp " + add_core_file + " " + molsim + "Cores/" + add_core_file)

                    with open(molsim + "Cores/cores.dict", "a") as f:
                        f.write(core + ":" + add_core_file + "," + add_con_atom + "," + add_max_dent + "\n")

                    print ("\n\nCore added successfully. Use at your own risk.")


                try:
                    core_dict[core]['All Hs']
                    allH = True
                except:
                    allH = False

                try:
                    core_dict[core]['Symmetric Hs']
                    symH = True
                except:
                    symH = False

                try:
                    core_dict[core]['Non-Symmetric Hs']
                    nonsymH = True
                except:
                    nonsymH = False

                if allH == True and symH == True and nonsymH == True or allH == True and symH == True and nonsymH == False:

                    for i in core_dict[core]['Symmetric Hs']:
                        if i in core_dict[core]['All Hs']:
                            core_dict[core]['All Hs'].remove(i)

                    core_dict[core]['Non-Symmetric Hs'] = core_dict[core]['All Hs']
                    del core_dict[core]['All Hs']

                elif symH == True and nonsymH == False:
                    core_dict[core]['Non-Symmetric Hs'] = []

                elif  symH == False and nonsymH == True:
                    core_dict[core]['Symmetric Hs'] = []

                elif symH == False and nonsymH == False:
                    core_dict[core]['Symmetric Hs'] = []
                    core_dict[core]['Non-Symmetric Hs'] = []

                if symH == True and len(core_dict[core]['Symmetric Hs']) == 1:
                    print ("There must be more than one symmetric substitution sites for cores. \nMoving to non-symmeric dictionary")

                    temp = []
                    for jj in core_dict[core]['Symmetric Hs']:
                        temp.append(jj)
                    if len(core_dict[core]['Non-Symmetric Hs']) != 0:
                        for jj in core_dict[core]['Non-Symmetric Hs']:
                            temp.append(jj)

                    core_dict[core]['Non-Symmetric Hs']  = temp
                    core_dict[core]['Symmetric Hs'] = []

            elif item.startswith('ligand'):

                count = 1
                temp = []

                lig_envir = item.lower().split(" ")[1:][0]
                ligand    = item.lower().split(" ")[1:][1]

                try:
                    ligand_dict[lig_envir]
                except:
                    ligand_dict[lig_envir] = {}

                ligand_dict[lig_envir][ligand] = {}

                while ff[j+count].startswith('end') == False:

                    temp.append(str(ff[j+count])[:-1])

                    count += 1

                ADD_LIG, CON_ATOM = False, False

                for j in temp:
                    j_low = j.lower()
                    j_val = j.lower().split(" ")[1:]
                    if j_low.startswith("symmetric"):
                        ligand_dict[lig_envir][ligand]['Symmetric Hs'] = j_val

                    elif j_low.startswith("nonsymmetric"):
                        ligand_dict[lig_envir][ligand]['Non-Symmetric Hs'] = j_val

                    elif j_low.startswith('all'):
                        ligand_dict[lig_envir][ligand]['All Hs'] = j_val

                    elif j_low.startswith('ligocc'):
                        ligand_dict[lig_envir][ligand]['Ligand Frequency'] = j_val

                    elif j_low.startswith('add_lig'):
                        add_lig_file = j.split(" ")[1:][0]
                        ADD_LIG = True

                    elif j_low.startswith("add_con_atom"):
                        add_con_atom = "["
                        for j in j_val:
                            add_con_atom += j + ","
                        add_con_atom = str(add_con_atom)[:-1] + "]"
                        CON_ATOM = True

                if ADD_LIG == True and CON_ATOM == True:

                    os.system("molsimplify -ligadd " + add_lig_file + " -ligname " + ligand + " -ligcon " + add_con_atom )
                    os.system("cp " + add_lig_file + " " + molsim + "Ligands/" + add_lig_file)

                    print ("\n\nLigand added successfully. Use at your own risk")

                try:
                    ligand_dict[lig_envir][ligand]['All Hs']
                    allH = True
                except:
                    allH = False

                try:
                    ligand_dict[lig_envir][ligand]['Symmetric Hs']
                    symH = True
                except:
                    symH = False

                try:
                    ligand_dict[lig_envir][ligand]['Non-Symmetric Hs']
                    nonsymH = True
                except:
                    nonsymH = False

                if allH == True and symH == True:

                    for i in ligand_dict[lig_envir][ligand]['Symmetric Hs']:
                        if i in ligand_dict[lig_envir][ligand]['All Hs']:
                            ligand_dict[lig_envir][ligand]['All Hs'].remove(i)

                    ligand_dict[lig_envir][ligand]['Non-Symmetric Hs'] = ligand_dict[lig_envir][ligand]['All Hs']
                    del ligand_dict[lig_envir][ligand]['All Hs']

                elif symH == True and nonsymH == False:
                    ligand_dict[lig_envir][ligand]['Non-Symmetric Hs'] = []

                elif  symH == False and nonsymH == True:
                    ligand_dict[lig_envir][ligand]['Symmetric Hs'] = []

                elif symH == False and nonsymH == False:
                    ligand_dict[lig_envir][ligand]['Symmetric Hs'] = []
                    ligand_dict[lig_envir][ligand]['Non-Symmetric Hs'] = []

                if symH == True and len(ligand_dict[lig_envir][ligand]['Symmetric Hs']) == 1:
                    print ("There must be more than one symmetric substitution sites for ligands. \nMoving to non-symmeric dictionary")
                    temp = []
                    for jj in ligand_dict[lig_envir][ligand]['Symmetric Hs']:
                        temp.append(jj)

                    if len(ligand_dict[lig_envir][ligand]['Non-Symmetric Hs']) != 0:
                        for jj in ligand_dict[lig_envir][ligand]['Non-Symmetric Hs']:
                            temp.append(jj)

                    ligand_dict[lig_envir][ligand]['Non-Symmetric Hs']  = temp
                    ligand_dict[lig_envir][ligand]['Symmetric Hs'] = []



            elif item == 'mod':
                count = 1
                temp = []

                ADD_MOD, CON_ATOM = False, False

                while ff[j+count].startswith('end') == False:

                    if ff[j+count].lower().startswith('numsub'):
                        subs = str(ff[j+count])[:-1].split(" ")[1:]
                        mod_dict['Number of Substitutions'] = subs

                    elif ff[j+count].lower().startswith("add_mod"):
                        add_mod_file = str(ff[j+count])[:-1].split(" ")[1:][0]
                        ADD_MOD = True

                    elif ff[j+count].lower().startswith("add_con_atom"):
                        add_con_atom = "["
                        for k in ff[j+count].lower().split(" ")[1:]:
                            add_con_atom += k + ","
                        add_con_atom = str(add_con_atom)[:-1] + "]"
                        CON_ATOM = True

                    else:
                        temp.append(str(ff[j+count])[:-1])
                    count += 1

                mod_dict['Modifications'] = temp


                if ADD_MOD == True and CON_ATOM == True:
                    mod = add_mod_file.split(".")[0]

                    os.system("molsimplify -ligadd " + add_mod_file + " -ligname " + mod + " -ligcon " + add_con_atom )
                    os.system("cp " + add_mod_file + " " + molsim + "Ligands/" + add_mod_file)

                    print ("\n\nLigand added successfully. Use at your own risk")


            elif item == 'extra':
                count = 1

                while ff[j+count].startswith('end') == False:
                    temp = ff[j+count].split(" ")
                    extra_dict[temp[0]] = str(temp[1])[:-1]

                    count += 1



    print ("\n\nInput file read successfully.")
    print ("Would you like to [compile] or [print] the necessary dictionaries?")
    choice = input(" > ")

    if choice.lower() == 'compile':
        return ligand_dict, core_dict, mod_dict, extra_dict
        COMP(ligand_dict, core_dict, mod_dict, extra_dict)

    elif choice.lower() == 'print':

        print ("________________________")
        print ("Cores:\n")
        for k, v in core_dict.items():
            print (k, v)

        print ("________________________")
        print ("Ligand Environments:\n")
        for k, v in ligand_dict.items():
            print (k)
            print ()
            for kk, vv in v.items():
                print (kk, vv)
            print ()

        print ("________________________")
        print ("Modifications:\n")
        for k, v in mod_dict.items():
            print (k, v)

        print ("________________________")
        print ("Molsimplify Extras:\n")
        for k, v in extra_dict.items():
            print (k, v)
        print ()

    return


if __name__ == "__main__":

    if len(sys.argv[1:]) > 0:
        if sys.argv[1] == '-f':
            FILE_INPUT()

        else:
            print ("Must supply an appropriate input file preceded by '-f'")

    else:
        print ("Must supply an appropriate input file preceded by '-f'")

