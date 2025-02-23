# -*- coding: utf-8 -*-
"""
Created on Tue May  3 18:18:39 2022

@author: caleb
"""
# The purpose of this puzzle is to determine if the sudoku (based on the provided solved cells) is valid and if so, solve the puzzle.
# The user submits the puzzle as a 81 character long number, the first digit being the top left cell, the last digit being the bottom right cell. 
# Unknown cells are entered as zeroes. The input is validated to make sure it is the correct length, that all characters are digits, and that 
# the provided digits follow the rules of sudoku (that no two cells in the same box, row, or column contain the same digit). Once this has been 
# validated a number of global varibles are created that will be used by the other functions of the program. Most notably, a dictionary that
# contains each cells value/possible values and it location in the puzzle, as well as lists of the presolved and unsolved cells. 
# The update function is then called which takes the values of each presolved cell and removes that digits as an option from each of their 
# related cells (in the same box, row, or column). Once this is complete the solve function is called which looks through each unsolved cell
# and tries to find any naked singles (a cell that has only one possible solution) or hidden singles (a cell that is the only one in it's 
# box, row, or column that can contain a particular digit) and then calls the update function. The update function then removes the solved cell's
# value from any related cells list of possibilities and the solve function is called again. This will repeat until the puzzle is solved or there
# are no solvable cells remaining in which case the guess function is called. The guess function finds the cell with the fewest number of possible 
# solutions and guesses one of these options. The puzzle will then continue to update, solve and guess until it reaches a point where the puzzle is
# solved within the parameters of sudoku, or there is no logical solution, in which case the undo function is called. Once a guess has been made
# the update, solve, and guess functions will log every change that has been made to the puzzle using Stack dataclasses. Whenever undo is called, 
# it will restore all the cells that have been changed since the last guess was made to their values at the time of the guess. It will then either
# choose another value for the most recently guessed cell (if there is another value to choose) or restore the puzzle to the next previous guess.
# Once one of these reversals have been processed the update, solve, guess, cycle will begin again, undoing itself whenever a guess/solve has failed
# to provide a solution. This will continue until a valid solution has been found, or all possible guesses have been made with no solution. The user
# will then receive either a print of the solved sudoku, or an error message that the puzzle was invalid. 



# The sudoku square is traditionally broken into three catagories; 9 3x3 boxes, 9 rows, and 9 columns. This program however breaks it down into 
# four catagories. Large rows, small rows, large columns, and small columns. The large rows each contain three small rows, and the large columns
# each contain three small columns. As arrays begin with 0, each catagory consist of value 0,1 and 2 i.e. Big row 0, big row 1, big row 2 etc. In the
# format of big row, little row, big column, little column this results in four digit codes, with the top left cell being 0000 and the bottom right
# cell being 2222. These codes are the ternary (base3) versions of the cell number they coincide with. If the top left cell is cell 0, the ternary
# is 0000, if the bottom right cell is 80, the ternary is 2222. Additionally the ternary codes can be used to determine the box, row and column numbers. By
# concatenating the various digits of the ternary code and converting them back into base10 it will return a number from 0 to 8. The first two digits
# correspond to the row number, the first and third digits to the box number, and the third and fourth digits to the column number. Once converted a 1 is added
# to make the numbers 1-9, the traditional numbering system for these categories in a sudoku puzzle. 

# The base10, base3, and translate functions are used to create a dictionary that contains the Box, Row, and Column numbers for each cell in the sudoku. 
# This data is then used to let the user know if a submitted puzzle contains inaccurrate information and to provide other functions within the program a set
# containing the numbers of cells that are related (same box, row, column, or all) as a provided cell. This is helpful in reducing the number of iterations the
# program has to run through as it limits the number of cells that must be looked at to update when a cell is solved/guessed. 


def base10(num): #converts a base3 digit to a base10 digit        
    new_num = 0
    for i in range(len(num)):
        new_num += (int(num[-1-i])*(3**i))
    return new_num

def base3(num): #converts a base10 digit to a base3 digit with preceding zeros        
    ternary = ''
    while num!= 0:
        q = num%3
        num //= 3
        ternary += str(q)
    ternary += '0000'
    return ternary[3::-1]

def translate(tern,cat): # takes a four digit base3 number, slices it and returns the slice in base10 + 1. 
    vals = {'b':base10(tern[0] + tern[2])+1,'r':base10(tern[0] + tern[1])+1,'c':base10(tern[2] + tern[3])+1}
    return vals[cat]

def selection(cell,group = None): # takes a cell and returns a set of all cells in the same provided group (row, column, or box) if a group is indicated, otherwise it returns all related cells
    groupcells = set()
    vals = {'r':'Row','c':'Column','b':'Box'}
    for i in range(81):
        if group:
            if dict1[i][vals[group]] == dict1[cell][vals[group]]:
                groupcells.add(i)
        else:
            for k in vals.keys():
                if dict1[i][vals[k]] == dict1[cell][vals[k]]:
                    groupcells.add(i)
    groupcells.remove(cell)                
    return groupcells

def sc(num): # returns an individual cell's possible digits as a set
    return set(dict1[num]['Digits'])
def dsc(num): # returns an individual cell's possible digits as a list if unsolved or a string if solved
    return dict1[num]['Digits']
def box(num): # returns what box a cell is in
    return dict1[num]['Box']
def row(num): # returns what row a cell is in
    return dict1[num]['Row']
def column(num): # returns what column a cell is in
    return dict1[num]['Column']

def shared(x,y): # takes two cells and returns a list that indicates if they share the same box, row, or column.
    l = {0:False,1:False,2:False}
    d = {0:'box',1:'row',2:'column'}
    x_brc = (box(x), row(x), column(x))
    y_brc = (box(y), row(y), column(y))
    s = []
    for i in l.keys():
        if x_brc[i] == y_brc[i]:
            l[i] = True
    for k,v in l.items():
        if v == True:
            s.append(d[k])
    return s        
    
class Stack: # creates a new data structure that adds new items to the top of the list and removes the last added item when requested
    def __init__(self):
        self.items = []
    def is_empty(self):
        return self.items == []
    def push(self, item):
        self.items.insert(0,item)
    def pop(self):
        return self.items.pop(0)
    def print_stack(self):
        print(self.items)

def update(cell = None): # Takes the values of solved cells and removes those values as possibilities from all related cells. Once all related cells have been updated, it calls the solve function. 
    def initial(): # Updates the initial unsolved cells to remove the provided solutions as possibilties. 
        global initial_var
        initial_var = False
        for i in pre_solved_cells:
            for x in selection(i):
                if type(dsc(x)) != str:
                    try:
                        dsc(x).remove(int(dsc(i)))
                    except ValueError:
                        continue
        solve()
    def not_guessing(): #Updates related cells whenever a cell is solved wihtout guessing. 
        for x in selection(cell):
                if type(dsc(x)) != str:
                    try:
                        dsc(x).remove(int(dsc(cell)))
                    except ValueError:
                        continue
        solve()
    def guessing(): #Updates realted cells whenever a cell is solved after a guess has been made. Then logs what cells where updated and how many cells were updated as a result of the most recent solve. 
                    #Once all cells have been updated, the solve function is called.
        count = 0
        for x in selection(cell):
            if type(dsc(x)) != str:
                try:
                    dsc(x).remove(int(dsc(cell)))
                    updated_cells.push([cell,x,int(dsc(cell))])
                    count += 1
                except ValueError:
                    continue
        updated_cells_count.push(count)
        solve()
        
    if initial_var:
        initial()
    elif not guessing_var:
        not_guessing()
    elif guessing_var:
        guessing()

def solve(): #Iterates through the puzzle to look for any cells that can be solved using naked singles (only one possible solution for a cell) or hidden singles 
            #(only one cell in a given box, row, or column that could be a specific digit). Once a cell is solved the update function is called. 
            #If no cells are solved after parsing through all remaining unsolved cells the guess fucntion is called. 
            #If all cells are solved it calls the pattern function. 
    global guessing_var
    s = 0
    for i in unsolved_cells:
        if len(dsc(i)) == 1:
            if guessing_var:
                g_solved_count.items[0] += 1
                g_solved.push(i)
                g_solved_defaults.push(list(dsc(i)))
            dict1[i]['Digits'] = str(dsc(i)[0])
            unsolved_cells.remove(i)
            solved_cells.append(i)
            s += 1
            update(i)
            return
        else:
            for x in ['b','r','c']:
                possible_values = sc(i)
                for y in selection(i,x):
                    possible_values -= sc(y)
                if len(possible_values) == 1:
                    if guessing_var:
                        g_solved_count.items[0] += 1
                        g_solved.push(i)
                        g_solved_defaults.push(list(dsc(i)))
                        
                    dict1[i]['Digits'] = str(list(possible_values)[0])
                    unsolved_cells.remove(i)
                    solved_cells.append(i)
                    s += 1
                    update(i)
                    return
                
    if s == 0 and unsolved_cells != []:
        guessing_var = True
        guess()
        return
    elif unsolved_cells == []:
        pattern()    

def pattern(): #Prints out the solved sudoku
    pattern = (('\n' + '-'*21 + '\n').join(['\n'.join([' | '.join([' '.join('c'*3)]*3)]*3)]*3))          
    list1 = [dict1[i]['Digits'] for i in range(81)]

    for i in list1:
        if type(i) == str:
            pattern = pattern.replace('c',i,1)
        else:
            pattern = pattern.replace('c','_',1)
    print(pattern)  
    
def guess(): # Finds the cell with the least possible number of solutions and guesses one of them. Logs the guessed cell, the current values of the cell, and the remaining possible values of the cell after the guess
            # If no further cells can be guessed, it calls the undo function. Otherwise it calls the update function. 
    global guessing_var
    guess_logic = [i[0] for i in sorted({i:dsc(i) for i in unsolved_cells}.items(), key = lambda item:len(item[1]))]   
    g = guess_logic[0]
    if dsc(g) == []:
        undo()
        return

    guesses.push(g)
    default.push(list(dsc(g)))
    options.push(list(dsc(g)))
    dict1[g]['Digits'] = str(options.items[0].pop(0))
    g_solved_count.push(0)
    solved_cells.append(g)
    unsolved_cells.remove(g)
    update(g)
    return


        
def undo(): # Undoes all changes (solutions and updates) to the puzzle since the last cell was guessed. If all guesses have been tried and reversed, the puzzle is declared invalid. 
    def undo_updates(): # reverses all updates that have been processed since the last solve or last guess.           
        for i in range(updated_cells_count.items[0]):
            a = updated_cells.items[0][1]
            b = updated_cells.items[0][2]
            dict1[a]['Digits'].append(b)
            dsc(a).sort()
            updated_cells.pop()
        updated_cells_count.pop() 
    def unsolve(): # reverses all cells that were solved as a result of the last guess
        for i in range(g_solved_count.items[0]):
            undo_updates()            
            c = g_solved.pop()
            solved_cells.remove(c)
            unsolved_cells.append(c)
            dict1[c]['Digits'] = g_solved_defaults.pop()
        g_solved_count.pop()        
                        
    def reguess(): # takes the last cell that was guessed and chooses a differnt value
        unsolve()
        undo_updates()
        dict1[guesses.items[0]]['Digits'] = str(options.items[0].pop(0))
        g_solved_count.push(0)
        update(guesses.items[0])
    def backstep(): # reverts the most recent guess back to its values at the time of the guess. Used when the current combination of guesses and solves has resulted in an incorrect solution. 
        unsolve()
        undo_updates()
        dict1[guesses.items[0]]['Digits'] = default.pop()
        solved_cells.remove(guesses.items[0])
        unsolved_cells.append(guesses.items[0])
        guesses.pop()
        options.pop()
        undo()     
    
    if guesses.is_empty(): 
        raise Exception('Puzzle is invalid, has no solution')
    if options.items[0] != []:
        reguess()
    elif options.items[0] == []:
        backstep()
        

def validate(): # validates the user input as the correct format, and a valid sudoku. If valid, the update function is called, otherwise it prompts the user to re-enter the puzzle. 

    global puzzle    
    global dict1
    global initial_var
    global guessing_var
    global pre_solved_cells
    global unsolved_cells 
    global solved_cells
    global updated_cells    
    global updated_cells_count
    global g_solved
    global g_solved_count    
    global g_solved_defaults
    global guesses    
    global options    
    global default
            
    print('Enter the digits of the puzzle using zeros for the unsolved cells, beginning with the top left cell and ending with the bottom right cell. ')
    puzzle = str(input())
    if len(puzzle) < 81:
        print('Please re-enter the digits, not enough digits were provided.')
        validate()
        return
    elif len(puzzle) > 81:
        print('Please re-enter the digits, too many digits were provided.')
        validate()
        return
    try:
        x = [int(i) for i in puzzle]
    except ValueError:
        print('Please use numeric digits')
        validate()
        return
    
    dict1 = {i:{'Digits':puzzle[i] if puzzle[i] != '0' else [x+1 for x in range(9)],  # The dictionary that contains each cells values and it's location. 
                         'Box':translate(base3(i),'b'),
                         'Row':translate(base3(i),'r'),
                         'Column':translate(base3(i),'c')} for i in range(81)}    

    initial_var = True
    guessing_var = False

    
    pre_solved_cells = [i for i in range(81) if puzzle[i] != '0']
    unsolved_cells = [i for i in range(81) if puzzle[i] == '0']
    solved_cells = []
    
    updated_cells = Stack()
    updated_cells_count = Stack()        
    g_solved = Stack()
    g_solved_count = Stack()
    g_solved_defaults = Stack()
    guesses = Stack()
    options = Stack()
    default = Stack()
    
    for i in pre_solved_cells:
        for y in selection(i):
            if dsc(i) == dsc(y):
                s = shared(i,y)
                print(f"The puzzle as provided is invalid, cells {str(i+1)} and {str(y+1)} which share the same {s[0] if len(s) == 1 else s[0] + ' and ' + s[1]} contain the same digit: {dsc(i)}")
                validate()
                return
    update()
        
validate()



