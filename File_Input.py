import os
import sys
import itertools
from Comp import COMP


def FILE_INPUT(input_file):
    # Program to read in a given input file. Adds information given in the input file
    # into the appropriate dictionary.

    def Find_Molsim():
        # Find the location of the molsimplify folder. 
        # Necessary to add cores, ligands, or modifications

        for root, dir, files in os.walk(os.path.expanduser('~')):
            if 'cores.dict' in files:
                return str(root)[:-5]

    def CheckInt(val, line, line_num):
        # Check to see if given value(s) is an integer
        
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
        # Check to see if file exsists. 
        # Necessary to add cores, ligands, or modifications

        if os.path.exists(check_file):
            pass
        else:
            print ("FILE %s ON LINE %s NOT FOUND" %(check_file, line_num))
            sys.exit()

    def Input():
        # Sanitizes the user input by removing leading and trailing spaces
        # and removes multiple spaces

        x = input(" > ").lower()

        while x == '':
            x = str(input("\033[A > ")).lower()
        while x.endswith(" ") == True:
            x = x[:-1]
        while x.startswith(" ") == True:
            x = x[1:]
        return x


    core_dict   = {}
    ligand_dict = {}
    mod_dict    = {}
    param_dict  = {}

    # Find molsimplify folder, read in input, and remove commented lines

    molsim = Find_Molsim()

    with open(input_file) as f:
        ff = f.readlines()

    for j in ff:
        if j.startswith("#"):
            ff.remove(j)

    # Sanitize the input information by removing newline characters (\n), 
    # leading and trailing spaces, and any extra spaces

    count = 0
    for j in ff:
        temp = list(j)
        if '\n' in temp and temp != ['\n']:
            temp.remove('\n')
        while temp[0] == ' ' or temp[0] == '':
            temp = temp[1:]
        if temp != ['\n']:
            while temp[-1] == ' ' or temp[-1] == '':
                temp = temp[:-1]
        ff[count] = ''.join(temp)
        while '  ' in ff[count]:
            ff[count] = ff[count].replace("  ", " ")

        count += 1

    # Iterate through input list and then check if line starts with "%" which denotes a 
    # core, ligand, modificaiton, or parameter block

    for j in range(len(ff)):
        line = str(ff[j])

        if line.startswith("%"):
            item = str(line)[1:].lower()

            if item.startswith('core'):
                count = 1
                temp = []

                core = item.lower().split(" ")[1:][0]

                core_dict[core] = {}

                while ff[j+count].startswith('end') == False:

                    temp.append(str(ff[j+count]))

                    count += 1

                # Used to add cores

                CORE_FILE, CON_ATOM, MAX_DENT = False, False, False

                for jj in temp:
                    temp_ = list(jj)
                    while temp_[-1] == ' ':
                        temp_ = temp_[:-1]
                    sep = ''
                    jj = sep.join(temp_)

                    j_low = jj.lower()

                    # Determine the value of the specific line.
                    # If that value is a list, then it is handled differently

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
                        CheckInt(j_val, jj, ff.index(jj))
                        core_dict[core]['Symmetric Hs'] = j_val

                    elif j_low.startswith("nonsymmetric"):
                        CheckInt(j_val, jj, ff.index(jj))
                        core_dict[core]['Non-Symmetric Hs'] = j_val

                    elif j_low.startswith('all'):
                        CheckInt(j_val, jj, ff.index(jj))
                        core_dict[core]['All Hs'] = j_val

                    elif j_low.startswith('add_core'):
                        add_core_file = jj.split(" ")[1:][0]
                        CORE_FILE = True
                        CheckFile(add_core_file, jj, ff.index(jj))

                    elif j_low.startswith('add_con_atom'):
                        CheckInt(j_val, jj, ff.index(jj))

                        add_con_atom = ""
                        for j in j_val:
                            add_con_atom += j + " "
                        add_con_atom = str(add_con_atom)[:-1]
                        CON_ATOM = True

                    elif j_low.startswith('add_max_dent'):
                        CheckInt(j_val, jj, ff.index(jj))
                        add_max_dent = j_val[0]
                        MAX_DENT = True

                    else:
                        print ("UNRECOGNIZED VALUE IN LINE %s - %s" %(ff.index(jj), jj))
                        sys.exit()

                if CORE_FILE == True and CON_ATOM == True and MAX_DENT == True:
                    # All checks have passed to add a core to the molsimplify program 
                    # Copy the xyz/mol file to the Cores folder, 
                    # Check to see if core information is already in cores.dict file


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

                # Checks to see hydrogen lists have been created/populated

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

                if allH == True and symH == True:
                    # Removes instances from 'All Hs' if already in 'Symmetric Hs' or 'Non-Symmetric Hs'

                    for i in list(itertools.chain(*core_dict[core]['Symmetric Hs'])):
                        if i in core_dict[core]['All Hs']:
                            core_dict[core]['All Hs'].remove(i)

                    for i in core_dict[core]['All Hs']:
                        if i not in core_dict[core]['Non-Symmetric Hs']:
                            core_dict[core]['Non-Symmetric Hs'].append(i)

                    del core_dict[core]['All Hs']

                # Add lists if not given from input
                # Necessary for down the line

                elif symH == True and nonsymH == False:
                    core_dict[core]['Non-Symmetric Hs'] = []

                elif  symH == False and nonsymH == True:
                    core_dict[core]['Symmetric Hs'] = []

                elif symH == False and nonsymH == False:
                    core_dict[core]['Symmetric Hs'] = []
                    core_dict[core]['Non-Symmetric Hs'] = []

                if symH == True and len(list(itertools.chain(*core_dict[core]['Symmetric Hs']))) == 1:
                    print (" There must be more than one symmetric substitution sites for cores. \
                          \n Moving to non-symmeric dictionary")

                    temp = list(itertools.chain(*core_dict[core]['Symmetric Hs']))
                    for jj in temp:
                        core_dict[core]['Non-Symmetric Hs'].append(jj)

                    core_dict[core]['Symmetric Hs'] = []

            elif item.startswith('ligand'):

                count = 1
                temp  = []

                ligand = item.lower().split(" ")[1:][0]

                temp_lig_dict = {}
                temp_lig_dict[ligand] = {}

                while ff[j+count].startswith('end') == False:

                    temp.append(str(ff[j+count]))

                    count += 1

                # Used to add ligands

                ADD_LIG, CON_ATOM = False, False

                for jj in temp:
                    j_low = jj.lower()

                    # Determine the value of the specific line.
                    # If that value is a list, then it is handled differently

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
                        CheckInt(j_val, jj, ff.index(jj))
                        temp_lig_dict[ligand]['Symmetric Hs'] = j_val

                    elif j_low.startswith("nonsymmetric"):
                        CheckInt(j_val, jj, ff.index(jj))
                        temp_lig_dict[ligand]['Non-Symmetric Hs'] = j_val

                    elif j_low.startswith('all'):
                        CheckInt(j_val, jj, ff.index(jj))
                        temp_lig_dict[ligand]['All Hs'] = j_val

                    elif j_low.startswith('ligocc'):
                        CheckInt(j_val, jj, ff.index(jj))
                        temp_lig_dict[ligand]['Ligand Frequency'] = int(j_val[0])

                    elif j_low.startswith('add_lig'):
                        add_lig_file = jj.split(" ")[1:][0]
                        ADD_LIG = True
                        CheckFile(add_lig_file, jj, ff.index(jj))

                    elif j_low.startswith("add_con_atom"):
                        CheckInt(j_val, jj, ff.index(jj))
                        add_con_atom = "["
                        for j in j_val:
                            add_con_atom += j + ","
                        add_con_atom = str(add_con_atom)[:-1] + "]"
                        CON_ATOM = True

                    elif j_low.startswith("environment"):
                        CheckInt(j_val, jj, ff.index(jj))
                        lig_envir = int(j_val[0])
                    
                    else:
                        print ("UNRECOGNIZED VALUE IN LINE %s - %s" %(ff.index(jj), jj))
                        sys.exit()

                try:
                    temp_lig_dict[ligand]['Ligand Frequency']
                except:
                    temp_lig_dict[ligand]['Ligand Frequency'] = 1

                if ADD_LIG == True and CON_ATOM == True:
                    # All checks have passed to add a ligand to the molsimplify program
                    # Copy the xyz/mol file to the ligand folder,
                    # and run the molsimplify 'ligadd' command to add the ligand

                    os.system("molsimplify -ligadd " + add_lig_file + " -ligname " + ligand + " -ligcon " + add_con_atom )
                    os.system("cp " + add_lig_file + " " + molsim + "Ligands/" + add_lig_file)

                    print ("\n\nLigand added successfully. Use at your own risk")

                # Checks to see hydrogen lists have been created/populated

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
                    # Removes instances from 'All Hs' if already in 'Symmetric Hs' or 'Non-Symmetric Hs'

                    for i in list(itertools.chain(*temp_lig_dict[ligand]['Symmetric Hs'])):
                        if i in temp_lig_dict[ligand]['All Hs']:
                            temp_lig_dict[ligand]['All Hs'].remove(i)

                    for i in temp_lig_dict[ligand]['All Hs']:
                        if i not in temp_lig_dict[ligand]['Non-Symmetric Hs']:
                            temp_lig_dict[ligand]['Non-Symmetric Hs'].append(i)

                    del temp_lig_dict[ligand]['All Hs']

                # Add lists if not given from input
                # Necessary for down the line

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
                    
                    temp = list(itertools.chain(*temp_lig_dict[ligand]['Symmetric Hs']))
                    for jj in temp:
                        temp_lig_dict[ligand]['Non-Symmetric Hs'].append(jj)

                    temp_lig_dict[ligand]['Symmetric Hs'] = []

                try:
                    # Check to see if ligand environment value is given in the input
                    # Program quits if not given for all ligands

                    lig_envir
                except:
                    print ("Input file read unsucessfully")
                    print ("Must Specify the environment for each ligand")
                    sys.exit()

                try:
                    # Check to see if ligand environemnt already in ligand dictionary.
                    # If not, then an empty list is created for the environment. 
                    # The temporary ligand information is then appended to that environment

                    ligand_dict[lig_envir]
                except:
                    ligand_dict[lig_envir] = []

                ligand_dict[lig_envir].append(temp_lig_dict)

            elif item == 'mod':
                count = 1
                temp = []
                perm = []

                add_mod_file = []
                add_con_atom = []

                while ff[j+count].startswith('end') == False:
                    jj = ff[j+count]

                    if ff[j+count].lower().startswith('numsub'):
                        subs = str(jj).split(" ")[1:]
                        mod_dict['Number of Substitutions'] = subs
                        CheckInt(subs, jj, ff.index(jj))

                    elif ff[j+count].lower().startswith("add_mod"):
                        CheckFile(str(jj).split(" ")[1:][0], jj, ff.index(jj))
                        add_mod_file.append(str(ff[j+count]).split(" ")[1:][0])

                    elif ff[j+count].lower().startswith("add_con_atom"):
                        CheckInt(str(jj).split(" ")[1:][0], jj, ff.index(jj))
                        temp_ = "["
                        for k in jj.lower().split(" ")[1:]:
                            temp_ += k + ","
                        add_con_atom.append(str(temp_) + "]")

                    elif ff[j+count].lower().startswith("_"):
                        mod_ = jj[1:].split(" ")
                        perm.append(mod_)

                    else:
                        temp.append(jj)
                    count += 1

                    if len(add_mod_file) != len(add_con_atom):
                        length = min(len(add_mod_file), len(add_con_atom))

                        add_mod_file = add_mod_file[:length]
                        add_con_atom = add_con_atom[:length]

                mod_dict['Modifications'] = temp
                mod_dict['Permanent']     = perm

                for jj in range(len(add_mod_file)):
                    add_mod  = add_mod_file[jj]
                    con_atom = add_con_atom[jj]

                    mod = add_mod.split(".")[0]

                    os.system("molsimplify -ligadd " + add_mod + " -ligname " + mod + " -ligcon " + add_con)
                    os.system("cp " + add_mod + " " + molsim + "Ligands/" + add_mod)

                    print ("\n\nLigand added successfully. Use at your own risk")


            elif item == 'param':
                count = 1

                while ff[j+count].startswith('end') == False:
                    temp = ff[j+count].split(" ")
                    param_dict[temp[0]] = str(temp[1])

                    count += 1


    print ("\n\n Input file read successfully.")
    print (" Would you like to [compile] or [print] the necessary dictionaries?\n")
    
    choice = Input()

    if choice == 'compile':
        COMP(ligand_dict, core_dict, mod_dict, param_dict)

    elif choice == 'print':

        print ("\n\n")

        print (" ________________________")
        print (" Cores:\n")
        for k, v in core_dict.items():
            print (" ", k, v)

        print (" ________________________")
        print (" Ligand Environments:\n")
        for k, v in ligand_dict.items():
            print (" ", k)
            print ()
            for j in v:
                for kk, vv in j.items():
                    print (" ", kk, vv)
                print ()
            print ()

        print (" ________________________")
        print (" Modifications:\n")
        for k, v in mod_dict.items():
            print (" ", k, v)

        print (" ________________________")
        print (" Molsimplify Parameters:\n")
        for k, v in param_dict.items():
            print (" ", k, v)
        print ()

        return

    return


if __name__ == "__main__":

    if len(sys.argv[1:]) > 0:
        if sys.argv[1] == '-f':
            FILE_INPUT(sys.argv[2])

        else:
            print ("Must supply an appropriate input file preceded by '-f'")

    else:
        print ("Must supply an appropriate input file preceded by '-f'")

