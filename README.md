# Structure_Creator

This program is used to generate modified structures using the molSimplify toolkit developed by the Kulik Group](http://hjkgrp.mit.edu) in the [Department of Chemical Engineering](http://web.mit.edu/cheme/) at [MIT](http://web.mit.edu).

Two methods of input are accepted: a commandline interface and an input file. The commandline interface walks you through the program to choose which cores, ligands, modifications, and parameters are to be used. The input file is able to do all that the commandline interface can do but in a more compact form. A list of possible input parameters and an example are included as "Structure_Creator Manual" and example.inp. 

Currently, the code is stable towards core modifications (such as modifying the porphyrin ring in an iron-porphyrin system) and ligand modificatinos (such as modifying beta-diketones bound to a lanthanide ion). In addition, simple symmetry has been added which can handle cases such as the hydrogen atoms on a methyl group. More complex symmetry (such as two identical methyl groups) are possible by carefully choosing the number of substitutions needed and the sites of said substitutions. 
