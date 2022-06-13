# Python
Python programs to help develop my skills

The first program is a sudoku solver that I began to code as a way to practice Python and devlop a familiarity with the language. 
Sudokus are a puzzle in which all cells within a 9x9 grid must be filled in with the numbers 1-9. The numbers 1-9 must appear only once in every
box (Nine 3x3 grids within the puzzle), every row, and every column. A true sudoku will have only one possible solution.

The purpose of the program is to take a user inputed sudoku puzzle and either solve it or declare it impossible. 
Currently it utilizes two logical methods to determine solutions; naked singles and hidden singles. 
Naked singles are found within cells that only contain one possible solution. 
Hidden singles are found within cells that have multiple possible solutions but are the only cell within a given box, row, or column that contains that possible value. 
If the puzzle cannot be solved using these two logical methods it will begin a guess-solve-backtrack loop until the puzzle is solved or all possible solutions have
been tried and the puzzle declared impossible. 

The program starts with version 3.1 as that is where the program was when it was added to this repository. 
I would like to add additional logic methods using pairs and subsets (where two or more cells with shared possibilities eliminate solutions for other cells), 
X-Wings, and Swordfish (advanced logical techniques that look for cell patterns). 
Additionally I would like to modify the guess functions within the program to look for more than one possible solution to verify if it is a true sudoku or not. 

I would like the end product to have GUI that the user can use to solve the puzzle manually with the option of having the program alert them if they've made a mistake. 
Optionally I would like to add additional functionality for optional rules that allow for sudoku-variants such as knights move, non-subsequent cells, etc. 
