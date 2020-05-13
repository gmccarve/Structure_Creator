import os

""" 

    To Do:

    1 - add ability to remove ligand from ligand environemnt
    2 - add ability for multiples of the same ligand in an environment
        {1:[{acac1}, {acac2}, ...]}
    3 - add ability for multiple symmetric lists [[], []]


"""

def LIGAND(ligand_dict):

    def Input():

        x = input(" > ").lower()

        while x == '':
            x = str(input("\033[A > ")).lower()
        while x.endswith(" ") == True:
            x = x[:-1]
        while x.startswith(" ") == True:
            x = x[1:]
        return x

    def load_ligands():
        for root, dir, files in os.walk(os.path.expanduser('~')):
            if 'ligands.dict' in files:
                ligand_file = os.path.join(root, 'ligands.dict')
                return str(root)[:-7], ligand_file


    def check_ligand(ligand, ligand_file):
        with open(ligand_file) as f:
            LIG = False
            for line in f:
                if line[:len(ligand)+1].lower() == (str(ligand)  + ":").lower():
                    print ()
                    print (" " + line)
                    temp = [True, line]
                    return temp
            if LIG != True:
                temp = [False, 0]
                return temp
        return

    def ADD(ligand_dict, ligand):
        print ("\n\n Which atoms (if any) would you like to modify for this ligand?")
        print (" Type 'all' to modify all hydrogens, \
                        \n      'none' to modify no hydrogens, or\
                        \n      'manual' to add hydrogens by index\n\n")

        ligand_mod = Input()

        if ligand_mod == 'all':

            ligand_dict[envir][ligand]['All Hs'] = []
            with open(MolSim + "Ligands/" + ligand_location) as f:
                lines = f.readlines()
                count = 0

                if END == '.mol':
                    temp_ = str(lines[3])
                    while temp_.startswith(" "):
                        temp_ = temp_[1:]
                    Num_atoms = int(temp_.split(" ")[0])
                    del lines[:4]
                elif END == '.xyz':
                    Num_atoms = int(lines[1])
                    del lines[:2]
                for line in lines:
                    if count < Num_atoms:
                        for j in line.split(" "):
                            if j.lower() == 'h':
                                ligand_dict[envir][ligand]['All Hs'].append(count+1)
                        count += 1

            return

        elif ligand_mod == 'none':
            return

        elif ligand_mod == 'manual':
            print ("\n Type the indices of any symmetric hydrogens or 'skip' to skip\n\n")
            
            symmetric_hs = Input()

            if symmetric_hs != 'skip':

                symmetric_hs = symmetric_hs.split(" ")
            
                for j in range(len(symmetric_hs)):
                    symmetric_hs[j] = int(symmetric_hs[j])

                ligand_dict[envir][ligand]['Symmetric Hs'] = symmetric_hs


            print ("\n Type the indices of any non-symmetric hydrogens or 'skip' to skip\n\n")

            nonsymmetric_hs = Input()

            if nonsymmetric_hs != 'skip':

                nonsymmetric_hs = nonsymmetric_hs.split(" ")

                for j in range(len(nonsymmetric_hs)):
                    nonsymmetric_hs[j] = int(nonsymmetric_hs[j])

                ligand_dict[envir][ligand]['Non-Symmetric Hs'] = nonsymmetric_hs

        return


    def Add_Envir(ligand_dict):

        print ("\n List of Ligand Environments")
        print (" ____________________________")
        for k, v in ligand_dict.items():
            print ("\n Ligand Environment : " + str(k))
            print (" \n List of added ligands: \n\n")
            for kk, vv in v.items():
                print (" ", kk, " - ", vv)
                print ()

        print ("\n Which environment would you like to add this ligand to?")
        print ("\n Or type 'new' to add a new environment\n")

        envir = Input()

        return envir




    MolSim, ligand_file = load_ligands()

    choice = ''

    while choice != 'end':

        print ("\n What would you like to do?")
        print ("\n 1 - Add/modify ligand environment\
                \n 2 - Show list of added ligands\
                \n 3 - Show data from ligand file\
                \n 4 - Show available ligands\
                \n 5 - Remove a ligand environment\
                \n 6 - Go Back \n\n")

        choice = Input()

        if choice == '1':

            if ligand_dict == {}:
                envir = 0

                ligand_dict[envir] = {}

                print ("\n Adding ligands to the first environment")

            else:

                envir_test = Add_Envir(ligand_dict)

                try:
                    envir_test = int(envir_test)
                    if envir_test in ligand_dict:
                        envir = int(envir_test)

                    elif envir_test == [max(k) for k, v in ligand_dict.items()] + 1:
                        envir = max(ligand_dict.items()) + 1

                    else:
                        print ("\n Not a valid option. Adding to new environment")
                        envir = len(ligand_dict)
                        ligand_dict[envir] = {}

                except:
                    envir_test = str(envir_test)

                    if envir_test == 'new':
                        envir = len(ligand_dict)
                        ligand_dict[envir] = {}

                    else:
                        print ("\n Not a valid option. Adding to new environment")
                        envir = len(ligand_dict)
                        ligand_dict[envir] = {}


            print ("\n Which ligand would you like to add? \n")

            ligand = Input()
            
            print ("\n How many of this ligand would you like to add? \n")
            
            num_lig = Input()
            
            temp = check_ligand(ligand, ligand_file)

            if temp[0] == True:
                print (" Ligand found\n")
                try:
                    ligand_dict[envir][ligand]
                except:
                    ligand_dict[envir][ligand] = {}
                ligand_dict[envir][ligand] = {}
                ligand_dict[envir][ligand]['Ligand Frequency'] = num_lig
                ligand_location = str(temp[1].split(",")[0].split(":")[1])
                END = ligand_location[-4:]

            
            else:
                y_n = input("\n Ligand not found. \
                        \n Would you like to supply a .mol or .xyz file for this ligand (y/n)? \n\n > ").lower()

                if y_n == 'y':
                    print ("\n Enter location of file \n\n")

                    ligand_location = Input

                    add_ligand_file = ligand_location.split("/")[-1]

                    print ("\n Enter connection atom(s) index separated by commas\n\n")

                    con_atom = str("[" + Input() + "]")

                    try:
                
                        os.system("molsimplify -ligadd " + ligand_location + " -ligname " + ligand + " -ligcon " + con_atom )
                        os.system("cp " + ligand_location + " " + MolSim + "Ligands/" + add_ligand_file)

                        print ("\n\n Ligand added but use at your own risk")
                        
                        ligand_dict[envir] = {}
                        ligand_dict[envir][ligand] = {}
                        ligand_dict[envir][ligand]['Ligand frequency'] = num_lig
                        END = ligand_file[-4:]

                    except:

                        print ("\n\n Ligand unable to be added")

                else:
                    pass

            try:
                with open(MolSim + "Ligands/" + ligand_location) as f:
                    for i, l in enumerate(f):
                        pass
                    ligand_len = i
            except:
                ligand_len = 0


            if ligand_len > 2:

                print("\n What would you like to do?")
                print (" 1 - Display the ligand file\
                      \n 2 - Choose which atoms to modify\
                      \n 3 - Skip")
                
                show_mod = Input()


                if show_mod == '1':
                    with open(MolSim + "Ligands/" + ligand_location) as f:
                        for line in f:
                            print (str(line)[:-1])

                    ADD(ligand_dict, ligand)


                elif show_mod == '2':

                    ADD(ligand_dict, ligand)

                elif show_mod == '3':

                    temp = 0

        
        elif choice == '2':
            if ligand_dict == {}:
                print ("\n No ligands added yet")
            else:
                print ("\n List of Ligand Environments")
                print (" ____________________________")
                for k, v in ligand_dict.items():
                    print ("\n Ligand Environment : " + str(k))
                    print (" \n List of added ligands: \n\n")
                    for kk, vv in v.items():
                        print (" ", kk, " - ", vv)
                        print ()


        elif choice == '3':
            if ligand_dict == {}:
                print ("\ n No ligands added yet")
            else:
                print ("\n List of Ligand Environments")
                print (" ____________________________")
                for k, v in ligand_dict.items():
                    print ("\n Ligand Environment : " + str(k))
                    print (" \n List of added ligands: \n\n")
                    for kk, vv in v.items():
                        print (" ", kk, " - ", vv)
                        print ()


                print ("\n Which ligand would you like to display?\n")

                ligand = Input()

                temp = check_ligand(ligand, ligand_file)

                if temp[0] == True:
                    ligand_file_temp = str(temp[1].split(",")[0].split(":")[1])


                for k, v in ligand_dict.items():
                    if ligand not in v:
                        print ("\n Ligand not found")
                        pass

                else:
                    try:
                        with open(MolSim + "Ligands/" + ligand_file_temp) as f:
                            for j in f:
                                print (str(j)[:-1])

                    except:
                        print (" \n No file associated with that ligand.")
                        print (" Ligand still found in dictionary file, though.\n")



        elif choice == '4':
            with open(MolSim + "Ligands/ligands.dict") as f:
                for line in f:
                    print (str(line)[:-1])

        elif choice == '5':
            if ligand_dict != {}:

                print ("\n List of Ligand Environments")
                print (" ____________________________")
                for k, v in ligand_dict.items():
                    print ("\n Ligand Environment : " + str(k))
                    print (" \n List of added ligands: \n\n")
                    for kk, vv in v.items():
                        print (" ", kk, " - ", vv)
                        print ()

                print ("\n\n Which ligand environment would you like to remove?\n\n")

                lig_rem = Input()

                try:
                
                    lig_rem = int(lig_rem)

                except:

                    print ("\n\n Invalid entry")

                if lig_rem not in ligand_dict:
                    print ("\n\n Ligand environment not found in list of given ligands")

                else:
                    del ligand_dict[lig_rem]

            elif ligand_dict == {}:
                print ("\n No ligands added yet")

        elif choice == '6':

            return ligand_dict


if __name__ == "__main__":

    ligand_dict = {}
    #LIGAND(ligand_dict)
    print (LIGAND(ligand_dict))
