import os
import sys
import platform
import re
import time

from File_Input import FILE_INPUT
from Menu import MENU


def clear():
    # Clears the terminal screen

    os.system('clear')

def Input():
    # Sanitizes the user input by removing leading and trailing spaces
    # and removes multiple spaces

    x = input(" > ")

    while x == '':
        x = str(input("\033[A > "))
    while x.endswith(" ") == True:
        x = x[:-1]
    while x.startswith(" ") == True:
        x = x[1:]
    return re.sub(" +", " ", x)

def check_molsimplify():
    # Checks to see if .molsimplify is available. 
    # If not, then it is assumed that molsimplify
    # has not been installed and the program quits. 

    for f in os.listdir(os.path.expanduser('~')):
        if f == '.molSimplify':
            return True

    return False

if __name__ == "__main__":

    if check_molsimplify() == False:
        print (" molSimplify must be installed to use this program.\
              \n Please see https://github.com/hjkgrp/molSimplify \
              \n on how to install molSimplify.")
        time.sleep(15)
        sys.exit()

    OS = platform.system()

    clear()

    print (" Welcome to the Structure Creator Code V 3.0\
        \n\n This code is able to create modified structures\
          \n that can be used for quantum chemical calculations.\n")

    # Check to see if input file is given and if so, reads in the 
    # input data


    if len(sys.argv[1:]) > 0:
        if sys.argv[1] == '-f':
            FILE_INPUT(sys.argv[2])
            sys.exit()

    print (" To be taken to the commandline menu, simply type\
          \n [menu]. Otherwise, to read in an input file,\
          \n either excecute this code with a '-f' flag followed by the\
          \n input file or type in the name of the input file\n")

    choice = Input()
    
    if choice.lower() == 'menu':
        MENU()
    
    elif os.path.exists(choice):
        FILE_INPUT(choice)


