import os
import sys
import re
from collections import defaultdict

def PARAM(param_dict):

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

    avail_param = {'ccatoms'  : 'custom core connection atom(s) indices', 
                   'replig'   : 'flag for modify/replace feature (True/False)', 
                   'geometry' : 'coordination geometry', 
                   'coord'    : 'coordination number', 
                   'keepHs'   : 'do not remove Hydrogens from ligand (True/False)', 
                   'smicat'   : 'custom ligand connecion atom(s) indices', 
                   'ligloc'   : 'force location of ligands on the template (True/False)', 
                   'ligalign' : 'smart allignment of ligands (True/False)',
                   'MLbonds'  : 'custom M-L bond length for ligand (A)'}

                # Copied from the Molsimplify User's Manual version 1.0

    molsim = MolSimplify()
    
    choice = ''

    while choice != 'end':

        print ("\n What would you like to do?")
        print (" \n 1 - Add parameter\
                \n 2 - Show list of added parameters\
                \n 3 - Show list of available parameters\
                \n 4 - Remove a modification\
                \n 5 - Go Back \n\n")

        choice = Input()

        if choice == '1':

            print ("\n Which parameter would you like to add? \n")

            param = Input()

            if param not in avail_param:
                print (" Parameter not available")
            
            else:

                print ("\n Which value would you like to add to this parameter? \n")

                value = Input()

                if param not in param_dict:
                    param_dict[param] = value


        elif choice == '2':
            if param_dict == {}:
                print ("\n No parameters added yet")
            else:
                print (" \nList of added parameters:\n")
                for k, v in param_dict.items():
                    print (" - ", k, v)
                print ()

        elif choice == '3':
            print ()
            for k, v in avail_param.items():
                print (" - ", k, "\t :\t ",  v)
            print ()


        elif choice == '4':

            if param_dict == {}:
                print ("\n No parameters added yet")

            else:
                print (" \nList of added parameterss: ")
                for k, v in param_dict.items():
                    print (k, v)

                param_rem = print ("\n\n Which parameter would you like to remove?\n\n")
                param_rem = Input()

                if mod_rem not in param_dict:
                    print ("\n\n Parameter not found in list of given parameters")

                else:
                    param_dict.remove(param_rem)

        elif choice == '5':

            return param_dict


    return


if __name__ == "__main__":

    param_dict = {'geometry': 'oct'}
    print (PARAM(param_dict))



