import os

def CORE(core_dict):

    def No_Inp(x):
        while x == '':
            x = str(input("\033[A > ")).lower()
        return x

    def Trim(x):
        while x.endswith(" ") == True:
            x = x[:-1]
        while x.startswith(" ") == True:
            x = x[1:]
        return x

    def load_cores():
        for root, dir, files in os.walk(os.path.expanduser('~')):
            if 'cores.dict' in files:
                core_file = os.path.join(root, 'cores.dict')
                return str(root)[:-5], core_file


    def check_core(core, core_file):
        with open(core_file) as f:
            CORE = False
            for line in f:
                if line[:len(core)+1].lower() == (str(core)  + ":").lower():
                    print ()
                    print (" " + line)
                    temp = [True, line]
                    return temp
            if CORE != True:
                temp = [False, 0]
                return temp
        return

    def ADD(core_dict, core):
        print ("\n\n Which hydrogens (if any) would you like to modify for this core?")
        core_mod = input(" Type 'all' to modify all hydrogens, \
                        \n      'none' to modify no hydrogens, or\
                        \n      'manual' to add hydrogens by index\n\n > ").lower()

        core_mod = No_Inp(core_mod)
        core_mod = Trim(core_mod)

        if core_mod == 'all':

            core_dict[core]['All Hs'] = []
            with open(MolSim + "Cores/" + core_location) as f:
                lines = f.readlines()
                count = 0

                if END == '.mol':
                    Num_atoms = int(lines[3].split(" ")[1])
                    del lines[:4]
                elif END == '.xyz':
                    Num_atoms = int(lines[1])
                    del lines[:2]
                for line in lines:
                    if count < Num_atoms:
                        for j in line.split(" "):
                            if j.lower() == 'h':
                                core_dict[core]['All Hs'].append(count)
                        count += 1

            return

        elif core_mod == 'none':
            return

        elif core_mod == 'manual':
            symmetric_hs = input("\n Type the indices of any symmetric hydrogens or 'skip' to skip\n\n > ").lower()
            
            symmetric_hs = No_Inp(symmetric_hs)
            symmetric_hs = Trim(symmetric_hs)

            if symmetric_hs != 'skip':

                symmetric_hs = symmetric_hs.split(" ")
            
                for j in range(len(symmetric_hs)):
                    symmetric_hs[j] = int(symmetric_hs[j])

                core_dict[core]['Symmetric Hs'] = symmetric_hs


            nonsymmetric_hs = input("\n Type the indices of any non-symmetric hydrogens or 'skip' to skip\n\n > ").lower()

            nonsymmetric_hs = No_Inp(nonsymmetric_hs)
            nonsymmetric_hs = Trim(nonsymmetric_hs)

            if nonsymmetric_hs != 'skip':

                nonsymmetric_hs = nonsymmetric_hs.split(" ")

                for j in range(len(nonsymmetric_hs)):
                    nonsymmetric_hs[j] = int(nonsymmetric_hs[j])

                core_dict[core]['Non-Symmetric Hs'] = nonsymmetric_hs

        return


    MolSim, core_file = load_cores()

    choice = ''

    while choice != 'end':

        print("\n What would you like to do?")
        choice = str(input(" \
                \n 1 - Add core\
                \n 2 - Show list of added cores\
                \n 3 - Show data from core file\
                \n 4 - Show available cores\
                \n 5 - Remove a core\
                \n 6 - Go Back \n\n > ")).lower()

        choice = No_Inp(choice)
        choice = Trim(choice)

        if choice == '1':

            print ("\n Which core would you like to add? \n")
            core = str(input(" > ")).lower()

            core = No_Inp(core)
            core = Trim(core)
            
            temp = check_core(core, core_file)

            if temp[0] == True:
                print (" Core found\n")
                core_dict[core] = {}
                core_location = str(temp[1].split(",")[0].split(":")[1])
                END = core_location[-4:]

            else:
                y_n = input("\n Core not found. \
                        \n Would you like to supply a .mol or .xyz file for this core (y/n)? \n\n > ").lower()

                if y_n == 'y':
                    core_location = input("\n Enter location of file \n\n > ")

                    core_location = No_Inp(core_location)
                    core_location = Trim(core_location)

                    add_core_file = core_location.split("/")[-1]

                    con_atom = str("[" + input("\n Enter connection atom(s) index separated by commas\n\n > ").lower() + "]")

                    con_atom = No_Inp(con_atom)
                    con_atom = Trim(con_atom)

                    max_den = input(" Enter maximum denticity \n\n").lower()

                    max_den = no_Inp(max_den)
                    max_den = Trim(max_den)
                
                    os.system("cp " + core_location + " " + MolSim + "Cores/" + add_core_file)

                    with open(MolSim + "Cores/cores.dict", "a") as f:
                        f.write(core + ":" + add_core_file + "," + con_atom + "," + max_den + "\n")

                    print ("\n\n Core added successfully")

                    core_dict[core] = {}
                    END = core_location[-4:]

            try:
                with open(MolSim + "Cores/" + core_location) as f:
                    for i, l in enumerate(f):
                        pass
                    core_len = i
            except:
                core_len = 0


            if core_len > 2:

                print("\n What would you like to do?")
                print (" 1 - Display the core file\
                      \n 2 - Choose which atoms to modify\
                      \n 3 - Skip")
                show_mod = input(" \n > ")

                show_mod = No_Inp(show_mod)
                show_mod = Trim(show_mod)


                if show_mod == '1':
                    with open(MolSim + "Cores/" + core_location) as f:
                        for line in f:
                            print (str(line)[:-1])

                    ADD(core_dict, core)


                elif show_mod == '2':

                    ADD(core_dict, core)

                elif show_mod == '3':

                    temp = 0

        
        elif choice == '2':
            if core_dict == {}:
                print ("\n No cores added yet")
            else:
                print (" \n List of added cores: \n\n")
                for k, v in core_dict.items():

                    print (" ", k)

                    for kk, vv in v.items():
                        print (" ", kk," - ", vv)

                    print ()


        elif choice == '3':
            if core_dict != {}:

                print ("\n Which core would you like to display?")
                for k, v, in core_dict.items():
                    print ("  - " + str(k))

                core = input("\n\n > ").lower()

                core = No_Inp(core)
                core = Trim(core)

                temp = check_core(core, core_file)

                if temp[0] == True:
                    temp_core_file = str(temp[1].split(",")[0].split(":")[1])

                if core not in core_dict:
                    print ("\n Core not found")
                    pass

                else:
                    try:
                        with open(MolSim + "Cores/" + temp_core_file) as f:
                            for j in f:
                                print (str(j)[:-1])

                    except:
                        print (" \n No file associated with that core.")
                        print (" Core still found in dictionary file, though.\n")



            elif core_dict == {}:
                print ("\n No cores added yet")

        elif choice == '4':
            with open(MolSim + "Cores/cores.dict") as f:
                for line in f:
                    print (str(line)[:-1])

        elif choice == '5':
            if core_dict != {}:

                print (" Current list of cores")
                for k, v, in core_dict.items():
                    print ("  - " + str(k))

                core_rem = input ("\n\n Which core would you like to remove?\n\n >")

                core_rem = No_Inp(core_rem)
                core_rem = Trim(core_rem)

                if core_rem not in core_dict:
                    print ("\n\n Core not found in list of given Cores")

                else:
                    del core_dict[core_rem]

            elif core_dict == {}:
                print ("\n No cores added yet")

        elif choice == '6':

            return core_dict


if __name__ == "__main__":

    core_dict = {}
    #CORE(core_dict)
    print (CORE(core_dict))
