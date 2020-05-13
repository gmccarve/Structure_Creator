import os
import sys
import re
import itertools

from Ligand import LIGAND
from Core import CORE
from Mod import MOD
from Comp import COMP


def MENU():

    def clear():
        os.system('clear')

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


    clear()

    print (" Welcome to the Structure Creator Code V 3.0")
    print (" This code is able to create modified structures")
    print (" that can be used for quantum chemical calculations")
    print ("\n What would you like to do:")

    END = False

    core_dict   = {}
    ligand_dict = {}
    mod_dict    = {}
    extra_dict  = {}

    while END != True:

        print ("\n\n 1 - Define core(s) \
                  \n 2 - Define ligand(s)\
                  \n 3 - Define modification(s)\
                  \n 4 - Define molsimplify extras\
                  \n 5 - Compile structures\
                  \n 6 - Print information\
                  \n 7 - Exit")

        choice = input("\n\n > ").lower()
        choice = No_Inp(choice)
        choice = Trim(choice)


        if choice == '1':
            core_dict = CORE(core_dict)

        elif choice == '2':
            ligand_dict = LIGAND(ligand_dict)

        elif choice == '3':
            mod_dict = MOD(mod_dict)

        elif choice == '4':
            extra_dict = EXTRA(extra_dict)

        elif choice == '5':
            if mod_dict == {}:
                print ("\n\nNo modifications added. Structures can still be compiled, however.")
                print ("Would you like to [add] modifications or [compile]?")
                choice_ = input("\n\n > ").lower()

                if choice_ == 'add':
                    mod_dict = MOD(mod_dict)

                elif choice_ == 'compile':
                    COMP(ligand_dict, core_dict, mod_dict)

            else:
                COMP(ligand_dict, core_dict, mod_dict)

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
                for kk, vv in v.items():
                    print (kk, vv)
                print ()

            print ("________________________")
            print ("Modifications:\n")
            for k, v in mod_dict.items():
                print (k, v)

        elif choice == '7':
            sys.exit()


if __name__ == "__main__":
    MENU()
