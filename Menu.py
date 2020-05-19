import os
import sys

from Ligand import LIGAND
from Core import CORE
from Mod import MOD
from Parameters import PARAM
from Comp import COMP

#TODO Add core symmetric [[], []]]


def MENU():

    def Input():

        x = input(" > ").lower()

        while x == '':
            x = str(input("\033[A > ")).lower()
        while x.endswith(" ") == True:
            x = x[:-1]
        while x.startswith(" ") == True:
            x = x[1:]
        return x


    END = False

    core_dict   = {}
    ligand_dict = {}
    mod_dict    = {}
    param_dict  = {}

    while END != True:

        print ("\n What would you like to do?")

        print ("\n\n 1 - Define core(s) \
                  \n 2 - Define ligand(s)\
                  \n 3 - Define modification(s)\
                  \n 4 - Define molsimplify parameters\
                  \n 5 - Compile structures\
                  \n 6 - Print information\
                  \n 7 - Exit\n")

        choice = Input()


        if choice == '1':
            core_dict = CORE(core_dict)

        elif choice == '2':
            ligand_dict = LIGAND(ligand_dict)

        elif choice == '3':
            mod_dict = MOD(mod_dict)

        elif choice == '4':
            param_dict = PARAM(param_dict)

        elif choice == '5':
            if mod_dict == {}:
                print ("\n\nNo modifications added. Structures can still be compiled, however.")
                print ("Would you like to [add] modifications or [compile]?")

                choice_ = Input()

                if choice_ == 'add':
                    mod_dict = MOD(mod_dict)

                elif choice_ == 'compile':
                    COMP(ligand_dict, core_dict, mod_dict, param_dict)

            else:
                COMP(ligand_dict, core_dict, mod_dict, param_dict)

        elif choice == '6':
            print ("________________________")
            print ("Cores:\n")
            for k, v in core_dict.items():
                print (k, v)

            print ("________________________")
            print ("Ligand Environments:\n")
            for k, v in ligand_dict.items():
                print (k)
                print ()
                for kk in v:
                    for kkk, vvv in kk.items():
                        print (kkk, vvv)
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


        elif choice == '7':
            sys.exit()


if __name__ == "__main__":
    MENU()
