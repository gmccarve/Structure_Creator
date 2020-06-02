import os
import sys
import re
from collections import defaultdict

""" 

    To fix:

    -Add xyz file for modification (ligand)

"""

def MOD(mod_dict):

    def clear():
        os.system('clear')

    def Input():

        x = input(" > ").lower()

        while x == '':
            x = str(input("\033[A > ")).lower()
        while x.endswith(" ") == True:
            x = x[:-1]
        while x.startswith(" ") == True:
            x = x[1:]
        return re.sub(" +", " ", x)

    def MolSimplify():
        for root, dir, files in os.walk(os.path.expanduser('~')):
            if 'cores.dict' in files:
                return str(root)[:-5]

    molsim = MolSimplify()
    
    if mod_dict == {}:
        mod_dict['Modifications'] = []
        mod_dict['Number of Substitutions'] = [1]
        mod_dict['Permanent'] = []

    mod_list = mod_dict['Modifications']
    sub_list = mod_dict['Number of Substitutions']

    choice = ''

    while choice != 'end':

        print("\n What would you like to do?\
               \n\n 1 - Add modification\
                 \n 2 - Show list of added modifications\
                 \n 3 - Choose how many modifications to perform\
                 \n 4 - Remove a modification\
                 \n 5 - Go Back \n\n")

        choice = Input()

        if choice == '1':

            print ("\n Which modification would you like to add? \n")

            mod = Input()

            print ("\n Does this modification need to be added to the system (y/n)? \n")

            add_mod = Input()

            if add_mod == 'y':

                print ("\n Enter location of file\n")
                
                mod_loc = Input()

                mod_xyz = mod_loc.split("/")[-1].lower()

                print ("\n Enter connection atom index/[indeces] \n\n")
                
                con_atom = Input()

                try:

                    os.system("molsimplify -ligadd " + mod_loc + " -ligname " + mod + " -ligcon " + con_atom )
                    os.system("cp " + mod_loc + " " + molsim + "Ligands/" + mod_xyz)

                    print ("\n\n Modification added but use at your own risk")

                    if mod not in mod_list:
                        mod_list.append(mod)

                except:
                    print ("\n\n Modification unable to be added")

            print ("\n Would you like this modification to be permanent in all structures (y/n)? \n")

            perm_ = Input()

            if perm_ == 'y':
                
                print ("\n Which position would like to modify? \n")

                perm_ind = Input()

                try:
                    mod_dict['Permanent'].append([mod, perm_ind])

                except:
                    mod_dict['Permanent'] = []
                    mod_dict['Permanent'].append([mod, perm_ind])


            else:
                if mod not in mod_list:
                    mod_list.append(mod)


        elif choice == '2':
            if mod_list == [] and mod_dict['Permanent'] == []:
                print ("\n No modifications added yet")
            else:
                print (" \n List of added modifications: ")
                for j in mod_list:
                    print (" - " + str(j))
                print ()

                print ("\n List of permanent modfications: ")
                for j in mod_dict['Permanent']:
                    print (" - " + str(j[0]) + ' : ' + str(j[1]))
                print ()


        elif choice == '3':

            print ("\n 1 - To view number of modifications already given\n 2 - To change the number of modifications\n")

            choice_ = Input()

            if choice_ == '1':
                print ("\n\n Number of modifications - ", end='' )
                for j in sub_list:
                    print (str(j), end=' ')

                print ("\n")

            elif choice_ == '2':

                sub_list = []
                    
                print ("\n How many modifications would you like to make?")
                print (" For multiple modifications, separate values by spaces")
                    
                sub = Input()

                try:
                    for j in sub.split(" "):
                        if int(j) not in sub_list:
                            sub_list.append(int(j))
    
                except:
                    print ("Incorrect input type. Only integers are accepted.")
                    print ("Setting number of modifications to 1")

                    sub_list = [1]


        elif choice == '4':

            if mod_list == []:
                print ("\n No modifications added yet")

            else:
                print (" \nList of added modifications: ")
                for j in mod_list:
                    print (" - " + str(j))

                print ("\n\n Which modification would you like to remove?\n\n")
                
                mod_rem = Input()

                if mod_rem not in mod_list:
                    print ("\n\n Modification not found in list of given modifications")

                else:
                    mod_list.remove(mod_rem)

        elif choice == '5':

            mod_dict['Modifications'] = []
            mod_dict['Modifications'] = mod_dict.get('Modifications', []) + mod_list

            mod_dict['Number of Substitutions'] = []
            mod_dict['Number of Substitutions'] = mod_dict.get('Number of Substitutions', []) + sub_list

            return mod_dict


    return


if __name__ == "__main__":

    mod_dict = {'Modifications': ['f', 'cl'], 'Number of Substitutions': ['1']}
    print (MOD(mod_dict))



