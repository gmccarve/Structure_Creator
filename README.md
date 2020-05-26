# Structure_Creator

This program is used to generate modified structures and is developed by the [Vogiatzis group](https://vogiatzis.utk.edu/)  in the [Department of Chemistry](https://chem.utk.edu/) at the [University of Tennessee](https://www.utk.edu/). It utilizes the molSimplify toolkit developed by the [Kulik Group](http://hjkgrp.mit.edu). 

Two methods of input are accepted: a commandline interface and an input file. The commandline interface walks you through the program to choose which cores, ligands, modifications, and parameters are to be used. The input file is able to do all that the commandline interface can do but in a more compact form. A list of possible input parameters and an example are included as Structure_Creator_Manual.pdf and example.inp. 

Currently, the code is stable towards core modifications (such as modifying the porphyrin ring in an iron-porphyrin system) and ligand modifications (such as modifying β-diketones bound to a lanthanide ion). In addition, simple symmetry has been added which can handle cases such as the hydrogen atoms on a methyl group. More complex symmetry (such as two identical methyl groups) are possible by carefully choosing the number of substitutions needed and the sites of said substitutions. 

To run the code, simply execute the Main.py program by itself or with a '-f' flag followed by your input file. The code will ask you wish to compile the structures or print the information given to check for any issues. Next, you will be prompted if you want to dispaly the number of structures that will be created or contintue with the structure generation. Finally, a prompt will ask if you would like to generate all possible structures or to try and eliminate redundancies. If symmetric hydrogens are being modified, then the 'eliminate redundancies' option should be used. 

While the code has shown stability in a wide range of cases, thourough testing is currently being underdone. 

This work was completed to aid in ours and other groups work as it relates to the development of chemical databases to be used for machine learning purposes. The first iteration of this work was completed by John Hymel of Georgia Tech and has been improved upon since. 
