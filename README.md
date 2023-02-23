# CS493-Latex-Automata-Generator
Project to allow you to make a latex graph using the tikz automata library

## How to use
- The first step to using this program is to make sure that you have python 3 Installed
- Python can be downloaded from https://www.python.org/downloads/ 
- Next in the command line you run the latexgen.py program
- latexgen.py has 2 flags
    - -h which displays how to use the command
    - -i < inputfile > that takes the desired file in
- once the program has completed its run you can copy and paste the output from the terminal into your latex sheet

## Fixing bad layout
-For some automats the program strugles with the layout
- https://tikz.dev/library-automata is the library page and has examples of what the library can do.
-To fix said problems:
    - Step one is to make sure that all nodes are in the correct order so that a node at the top of the list isnt bound to a node at the bottom of the list
    -Step Two change the location of your nodes to make the redability better
