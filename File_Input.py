import os
import sys
import itertools


#TODO Check for correct types


def FILE_INPUT(input_file):

    def Find_Molsim():
        for root, dir, files in os.walk(os.path.expanduser('~')):
            if 'cores.dict' in files:
                return str(root)[:-5]

    def CheckInt(val, line, line_num):
        if type(val) == list:
            if any(isinstance(el, list) for el in val):
                val = list(itertools.chain(*val))
        for j in val:
            try:
                int(j)
            except:
                print ("INCORRECT DATATYPE ON LINE %s - %s" %(str(line_num+1), line))
                sys.exit()

    def CheckFile(check_file, line, line_num):
        if os.path.exists(check_file):
            pass
        else:
            print ("FILE %s ON LINE %s NOT FOUND" %(check_file, line_num))
            sys.exit()



    core_dict   = {}
    ligand_dict = {}
    mod_dict    = {}
    param_dict  = {}

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
        while line.startswith(" "):
            line = line[1:]
        while line.endswith("\n") or line.endswith(" "):
            line = line[:-1]

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

                for jj in temp:
                    j_low = jj.lower()

                    if "[" not in j_low or "]" not in j_low:
                        j_val = jj.lower().split(" ")[1:]
                    else:
                        j_val = jj[9:]
                        while j_val.startswith(" "):
                            j_val = j_val[1:]
                        while j_val.endswith(" "):
                            j_val = j_val[:1]
                        j_val = j_val.split("] [")
                        j_val[0] = j_val[0][1:]
                        j_val[-1] = j_val[-1][:-1]
                        for jjj in range(len(j_val)):
                            j_val[jjj] = j_val[jjj].split(" ")

                    if j_low.startswith("symmetric"):
                        #CheckInt(j_val, jj, ff.index(str(j_low)+"\n"))
                        core_dict[core]['Symmetric Hs'] = j_val

                    elif j_low.startswith("nonsymmetric"):
                        CheckInt(j_val, jj, ff.index(jj+"\n"))
                        core_dict[core]['Non-Symmetric Hs'] = j_val

                    elif j_low.startswith('all'):
                        CheckInt(j_val, jj, ff.index(jj+"\n"))
                        core_dict[core]['All Hs'] = j_val

                    elif j_low.startswith('add_core'):
                        add_core_file = jj.split(" ")[1:][0]
                        CORE_FILE = True
                        CheckFile(add_core_file, jj, ff.index(jj+"\n"))

                    elif j_low.startswith('add_con_atom'):
                        CheckInt(j_val, jj, ff.index(jj+"\n"))
                        add_con_atom = ""
                        for j in j_val:
                            add_con_atom += j + " "
                        add_con_atom = str(add_con_atom)[:-1]
                        CON_ATOM = True

                    elif j_low.startswith('add_max_dent'):
                        CheckInt(j_val, jj, ff.index(jj+"\n"))
                        add_max_dent = j_val[0]
                        MAX_DENT = True

                    else:
                        print ("UNRECOGNIZED VALUE IN LINE %s - %s" %(ff.index(jj+"\n"), jj))
                        sys.exit()

                if CORE_FILE == True and CON_ATOM == True and MAX_DENT == True:

                    if os.path.exists(molsim + "Cores/" + add_core_file):
                        pass
                    else:
                        os.system("cp " + add_core_file + " " + molsim + "Cores/" + add_core_file)
                    
                    CORE_FILE_EXISTS = False
                    with open(molsim + "Cores/cores.dict", "r") as fle:
                        fle = fle.readlines()
                    
                    for line_ in fle:
                        if (core.lower() + ":") in line_:
                            CORE_FILE_EXISTS = True

                    if CORE_FILE_EXISTS == False:
                        with open(molsim + "Cores/cores.dict", "a") as fle:
                            fle.write(core + ":" + add_core_file + "," + add_con_atom + "," + add_max_dent + "\n")
                            print ("\n\nCore %s added successfully. Use at your own risk." %core)

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

                if symH == True and len(list(itertools.chain(*core_dict[core]['Symmetric Hs']))) == 1:
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
                temp  = []

                ligand = item.lower().split(" ")[1:][0]

                temp_lig_dict = {}
                temp_lig_dict[ligand] = {}

                while ff[j+count].startswith('end') == False:

                    temp.append(str(ff[j+count])[:-1])

                    count += 1

                ADD_LIG, CON_ATOM = False, False

                for jj in temp:
                    j_low = jj.lower()
                    if "[" not in j_low or "]" not in j_low:
                        j_val = jj.lower().split(" ")[1:]
                    else:
                        j_val = j_low[9:]
                        while j_val.startswith(" "):
                            j_val = j_val[1:]
                        while j_val.endswith(" "):
                            j_val = j_val[:1]
                        j_val = j_val.split("] [")
                        j_val[0] = j_val[0][1:]
                        j_val[-1] = j_val[-1][:-1]
                        for jjj in range(len(j_val)):
                            j_val[jjj] = j_val[jjj].split(" ")

                    if j_low.startswith("symmetric"):
                        CheckInt(j_val, jj, ff.index(str(j_low)+"\n"))
                        temp_lig_dict[ligand]['Symmetric Hs'] = j_val

                    elif j_low.startswith("nonsymmetric"):
                        CheckInt(j_val, jj, ff.index(jj+"\n"))
                        temp_lig_dict[ligand]['Non-Symmetric Hs'] = j_val

                    elif j_low.startswith('all'):
                        CheckInt(j_val, jj, ff.index(jj+"\n"))
                        temp_lig_dict[ligand]['All Hs'] = j_val

                    elif j_low.startswith('ligocc'):
                        CheckInt(j_val, jj, ff.index(jj+"\n"))
                        temp_lig_dict[ligand]['Ligand Frequency'] = int(j_val[0])

                    elif j_low.startswith('add_lig'):
                        add_lig_file = jj.split(" ")[1:][0]
                        ADD_LIG = True
                        CheckFile(add_lig_file, jj, ff.index(jj+"\n"))

                    elif j_low.startswith("add_con_atom"):
                        CheckInt(j_val, jj, ff.index(jj+"\n"))
                        add_con_atom = "["
                        for j in j_val:
                            add_con_atom += j + ","
                        add_con_atom = str(add_con_atom)[:-1] + "]"
                        CON_ATOM = True

                    elif j_low.startswith("environment"):
                        CheckInt(j_val, jj, ff.index(jj+"\n"))
                        lig_envir = int(j_val[0])
                    
                    else:
                        print ("UNRECOGNIZED VALUE IN LINE %s - %s" %(ff.index(jj+"\n"), jj))
                        sys.exit()

                try:
                    temp_lig_dict[ligand]['Ligand Frequency']
                except:
                    temp_lig_dict[ligand]['Ligand Frequency'] = 1

                if ADD_LIG == True and CON_ATOM == True:

                    os.system("molsimplify -ligadd " + add_lig_file + " -ligname " + ligand + " -ligcon " + add_con_atom )
                    os.system("cp " + add_lig_file + " " + molsim + "Ligands/" + add_lig_file)

                    print ("\n\nLigand added successfully. Use at your own risk")

                try:
                    temp_lig_dict[ligand]['All Hs']
                    allH = True
                except:
                    allH = False

                try:
                    temp_lig_dict[ligand]['Symmetric Hs']
                    symH = True
                except:
                    symH = False

                try:
                    temp_lig_dict[ligand]['Non-Symmetric Hs']
                    nonsymH = True
                except:
                    nonsymH = False

                if allH == True and symH == True:

                    for i in temp_lig_dict[ligand]['Symmetric Hs']:
                        if i in temp_lig_dict[ligand]['All Hs']:
                            temp_lig_dict[ligand]['All Hs'].remove(i)

                    temp_lig_dict[ligand]['Non-Symmetric Hs'] = temp_lig_dict[ligand]['All Hs']
                    del temp_lig_dict[ligand]['All Hs']

                elif symH == True and nonsymH == False:
                    temp_lig_dict[ligand]['Non-Symmetric Hs'] = []

                elif  symH == False and nonsymH == True:
                    temp_lig_dict[ligand]['Symmetric Hs'] = []

                elif symH == False and nonsymH == False:
                    temp_lig_dict[ligand]['Symmetric Hs'] = []
                    temp_lig_dict[ligand]['Non-Symmetric Hs'] = []

                if symH == True and len(list(itertools.chain(*temp_lig_dict[ligand]['Symmetric Hs']))) == 1:
                    print ("There must be more than one symmetric substitution sites for ligands. \
                            \nMoving to non-symmeric dictionary")
                    
                    temp = []
                    for jj in temp_lig_dict[ligand]['Symmetric Hs']:
                        temp.append(jj)

                    if len(temp_lig_dict[ligand]['Non-Symmetric Hs']) != 0:
                        for jj in temp_lig_dict[ligand]['Non-Symmetric Hs']:
                            temp.append(jj)

                    temp_lig_dict[ligand]['Non-Symmetric Hs']  = temp
                    temp_lig_dict[ligand]['Symmetric Hs'] = []

                try:
                    lig_envir
                except:
                    print ("Input file read unsucessfully")
                    print ("Must Specify the environment for each ligand")
                    sys.exit()

                try:
                    ligand_dict[lig_envir]
                except:
                    ligand_dict[lig_envir] = []

                ligand_dict[lig_envir].append(temp_lig_dict)

            elif item == 'mod':
                count = 1
                temp = []

                ADD_MOD, CON_ATOM = False, False

                while ff[j+count].startswith('end') == False:

                    if ff[j+count].lower().startswith('numsub'):
                        subs = str(ff[j+count])[:-1].split(" ")[1:]
                        mod_dict['Number of Substitutions'] = subs
                        CheckInt(subs, jj, ff.index(jj+"\n"))

                    elif ff[j+count].lower().startswith("add_mod"):
                        add_mod_file = str(ff[j+count])[:-1].split(" ")[1:][0]
                        ADD_MOD = True
                        CheckFile(add_mod_file, jj, ff.index(jj+"\n"))

                    elif ff[j+count].lower().startswith("add_con_atom"):
                        add_con_atom = "["
                        for k in ff[j+count].lower().split(" ")[1:]:
                            add_con_atom += k + ","
                        add_con_atom = str(add_con_atom)[:-1] + "]"
                        CON_ATOM = True
                        CheckInt(list(add_con_atom), jj, ff.index(jj+"\n"))

                    else:
                        temp.append(str(ff[j+count])[:-1])
                    count += 1

                mod_dict['Modifications'] = temp


                if ADD_MOD == True and CON_ATOM == True:
                    mod = add_mod_file.split(".")[0]

                    os.system("molsimplify -ligadd " + add_mod_file + " -ligname " + mod + " -ligcon " + add_con_atom )
                    os.system("cp " + add_mod_file + " " + molsim + "Ligands/" + add_mod_file)

                    print ("\n\nLigand added successfully. Use at your own risk")


            elif item == 'param':
                count = 1

                while ff[j+count].startswith('end') == False:
                    temp = ff[j+count].split(" ")
                    param_dict[temp[0]] = str(temp[1])[:-1]

                    count += 1



    print ("\n\nInput file read successfully.")
    print ("Would you like to [compile] or [print] the necessary dictionaries?\n")
    choice = input(" > ")

    if choice.lower() == 'compile':
        return ligand_dict, core_dict, mod_dict, param_dict
        COMP(ligand_dict, core_dict, mod_dict, param_dict)

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
            for j in v:
                for kk, vv in j.items():
                    print (kk, vv)
                print ()
            print ()

        print ("________________________")
        print ("Modifications:\n")
        for k, v in mod_dict.items():
            print (k, v)

        print ("________________________")
        print ("Molsimplify Parameters:\n")
        for k, v in param_dict.items():
            print (k, v)
        print ()

    return


if __name__ == "__main__":

    if len(sys.argv[1:]) > 0:
        if sys.argv[1] == '-f':
            FILE_INPUT(sys.argv[2])

        else:
            print ("Must supply an appropriate input file preceded by '-f'")

    else:
        print ("Must supply an appropriate input file preceded by '-f'")

