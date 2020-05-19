import os
import sys
import re

from File_Input import FILE_INPUT
from Menu import MENU

"""

    To Do:
        
    1 - check for OS
    2 - check if molsimplify added/active
    3 - Add Classes ******


"""



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



if __name__ == "__main__":

    if len(sys.argv[1:]) > 0:
        if sys.argv[1] == '-f':
            FILE_INPUT(sys.argv[2])

    clear()

    print (" Welcome to the Structure Creator Code V 3.0\n")
    print (" This code is able to create modified structures")
    print (" that can be used for quantum chemical calculations.\n")
    print (" To be taken to the commandline menu, simply type")
    print (" [menu]. Otherwise, to read in an input file, ")
    print (" either excecute this code with a '-f' flag followed by the")
    print (" input file or type in the name of the input file")

    _ = False

    while _ != True:
        choice = Input()
    
        if choice == 'menu':
            MENU()
    
        elif os.path.exists(choice):
            FILE_INPUT(choice)
