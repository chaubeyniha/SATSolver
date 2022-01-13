import pathlib
import random
import math

current_dir=pathlib.Path().resolve()
aux_folder = f'{current_dir}/aux_folder'

splits=0
backtracks=0

# takes a DIMACS_file with clauses and variables as input
# if it's satisfiable: it will return TRUE and a dict 
# with every var and its thruth value
# else: returs false

# function to pick heuristic
def SAT(DIMACS_file, heuristic_type):
    Knowledge_Base = load_file(DIMACS_file)
    assignments = get_elements_dict(Knowledge_Base)
    if heuristic_type == 0:
        sat, solution = DP_MOMs(Knowledge_Base, assignments)
        return sat, solution, splits, backtracks
    if heuristic_type ==1:
        sat, solution = DP_Jeroslow_Wang_OS(Knowledge_Base, assignments)
        return sat, solution, splits, backtracks 
    if heuristic_type ==2:   
        sat, solution = DP_MOMs(Knowledge_Base, assignments)
        return sat, solution, splits, backtracks
    if heuristic_type ==3:   
        sat, solution = DP_Jeroslow_Wang_OS(Knowledge_Base, assignments)
        return sat, solution, splits, backtracks
    
def DP_standard(Knowledge_Base, assignments): 
    assignments_local = assignments.copy()
    Knowledge_Base = fill_in_assignments(Knowledge_Base, assignments_local)
    global splits
    global backtracks

    ''' Checking if it is SAT or NOT '''
    if Knowledge_Base==[]: return True, assignments  #if there are no more clauses, return True
    for clause in Knowledge_Base:    #if any of the clauses are empty, return False
        if clause==[]:
            return False, assignments


    ''' SIMPLIFICATION '''
    #Tautology Rule
    # for clause in lines:
       # for element in clause:
           # if negated(element) in clause:
               # lines.remove(clause)
               #r eturn DP_standard(lines, assignments)

    # Unit Clause Rule:
    for clause in Knowledge_Base:
        if len(clause) == 1:
            if clause[0][0] == '-': assignments_local[clause[0][1:]] = False
            else: assignments_local[clause[0]] = True
            return DP_standard(Knowledge_Base, assignments_local)

    
    ''' SPLIT '''
    # gets the variables that still need a truth assigment
    empty_positions=[]
    for element in list(assignments.keys()):
        if assignments_local[element] is None:
            empty_positions.append(element)

    # it will select the first 'empty' variable 
    for element in list(assignments.keys()):
        if assignments_local[element] is None:
            # first, assign True to the choosen variable
            assignments_local[element] = True
            splits+=1
            sat, values = DP_standard(Knowledge_Base, assignments_local)
            if sat is True:
                return True, values
            else:
                # If it makes the Knowledege base inconsistent, we try assigning FALSE, and continue 
                # BACKTRACKING:
                assignments_local[element] = False
                backtracks+=1
                return DP_standard(Knowledge_Base, assignments_local)
        

def DP_standard_random_Split(Knowledge_Base, assignments): 
    assignments_local = assignments.copy()
    Knowledge_Base = fill_in_assignments(Knowledge_Base, assignments_local)
    global splits
    global backtracks

    ''' Checking if it is SAT or NOT '''
    if Knowledge_Base==[]: return True, assignments  #if there are no more clauses, return True
    for clause in Knowledge_Base:    #if any of the clauses are empty, return False
        if clause==[]:
            return False, assignments

    ''' SIMPLIFICATION '''
    # Unit Clause Rule:
    for clause in Knowledge_Base:
        if len(clause) == 1:
            if clause[0][0] == '-': assignments_local[clause[0][1:]] = False
            else: assignments_local[clause[0]] = True
            return DP_standard_random_Split(Knowledge_Base, assignments_local)

    ''' SPLIT '''
    # gets the variables that still need a truth assigment
    non_assigned = [element for element in list(assignments.keys()) if assignments[element] is None]

    # selecting random variable to Split
    selected_position=None
    if len(non_assigned)<2: selected_position = non_assigned[0]
    else: 
        x = random.randint(0, len(non_assigned)-1)
        selected_position = non_assigned[x]
        
    # first, assign True to the choosen variable
    assignments_local[selected_position] = True
    splits+=1
    sat, values = DP_standard_random_Split(Knowledge_Base, assignments_local)
    if sat is True: return True, values

    
    # if it makes the Knowledege base inconsistent, we try assigning FALSE, and continue 
    # BACKTRACKING:
    else:
        assignments_local[selected_position] = False
        backtracks+=1
        return DP_standard_random_Split(Knowledge_Base, assignments_local)


def get_assignment_with_Hightest_J_score(Knowledge_Base, not_assigned): 
    J_score_dict = dict(zip(not_assigned, [None for i in range(len(not_assigned))]))

    for element in not_assigned:
        lengths_of_clauses = [] #lengths of every clause that the element occurs in
        for clause in Knowledge_Base:
            if element in clause:
                lengths_of_clauses.append(len(clause))
        J_score=0
        for clause_size in lengths_of_clauses:
            J_score += math.pow((-1 * clause_size), 2)
        J_score_dict[element] = J_score

    return max(J_score_dict, key= lambda x: J_score_dict[x])


def DP_Jeroslow_Wang_OS(Knowledge_Base, assignments): 
    assignments_local = assignments.copy()
    Knowledge_Base = fill_in_assignments(Knowledge_Base, assignments_local)
    global splits
    global backtracks

    ''' Checking if it is SAT or NOT '''
    if Knowledge_Base==[]: return True, assignments  #if there are no more clauses, return True
    for clause in Knowledge_Base:    #if any of the clauses are empty, return False
        if clause==[]:
            return False, assignments

    ''' SIMPLIFICATION '''
    # Unit Clause Rule:
    for clause in Knowledge_Base:
        if len(clause) == 1:
            if clause[0][0] == '-': assignments_local[clause[0][1:]] = False
            else: assignments_local[clause[0]] = True
            return DP_Jeroslow_Wang_OS(Knowledge_Base, assignments_local)

    ''' SPLIT '''
    not_assigned = [element for element in list(assignments.keys()) if assignments[element] is None]
    next_assignment = get_assignment_with_Hightest_J_score(Knowledge_Base, not_assigned)
    print('next_assignment',next_assignment)
    assignments_local[next_assignment] = True
    splits+=1
    sat, values = DP_Jeroslow_Wang_OS(Knowledge_Base, assignments_local)
    if sat is True:
        return True, values
    else:
        assignments_local[next_assignment] = False
        backtracks+=1
        return DP_Jeroslow_Wang_OS(Knowledge_Base, assignments_local)



def DP_MOMs(Knowledge_Base, assignments): 
    """ Maximum Occurrence's in Clauses of Minimum Size """
    assignments_local = assignments.copy()
    Knowledge_Base = fill_in_assignments(Knowledge_Base, assignments_local)
    global splits
    global backtracks

    ''' Checking if it is SAT or NOT '''
    if Knowledge_Base==[]: return True, assignments  #if there are no more clauses, return True
    for clause in Knowledge_Base:    #if any of the clauses are empty, return False
        if clause==[]:
            return False, assignments

    ''' SIMPLIFICATION '''
    #Tautology Rule
    #for clause in Knowledge_Base:
    #   for element in clause:
    #       if negate(element) in clause:
    #           Knowledge_Base.remove(clause)
    #           return DP_standard(Knowledge_Base, assignments)

    # Unit Clause Rule:
    for clause in Knowledge_Base:
        if len(clause) == 1:
            if clause[0][0] == '-': assignments_local[clause[0][1:]] = False
            else: assignments_local[clause[0]] = True
            return DP_MOMs(Knowledge_Base, assignments_local)
    
    ''' SPLIT '''
    not_assigned = [element for element in list(assignments.keys()) if assignments[element] is None]
    min_clauses = get_min_clauses(Knowledge_Base)
    next_assignment = get_MOMs_literal(min_clauses, not_assigned)
    assignments_local[next_assignment] = True
    splits+=1
    sat, values = DP_MOMs(Knowledge_Base, assignments_local)

    if sat is True:
        return True, values
    else:
        backtracks+=1
        assignments_local[next_assignment] = False
        return DP_MOMs(Knowledge_Base, assignments_local)




def get_MOMs_literal(min_clauses, not_assigned):
    k=1 # tunning parameter

    score_list=[]
    for lit in not_assigned:
        
    # for lit in clause:
        f_x = count_numb_of_occurences(lit, min_clauses)
        f_not_x = count_numb_of_occurences(negate(lit), min_clauses)
        score = (f_x + f_not_x) * math.pow(2, k) + (f_x * f_not_x) 
        score_list.append([lit, score])

    value=max([sublist[-1] for sublist in score_list])
    for pair in score_list:
        if remove_negation(pair[0]) in not_assigned:
            if pair[1]==value:
                print("pair",pair)
                return pair[0]
  
    
def get_min_clauses(Knowledge_Base):
    """ Returns a list of clauses with minimum size """

    # GET A LIST [CLAUSE, LEN(CLAUSE)]
    clause_size_pair = []
    for clause in Knowledge_Base:
        clause_size_pair.append([clause, len(clause)])

    # GET THE MINIMAL SIZE
    minimum_existing_size=min([sublist[1] for sublist in clause_size_pair])
    min_clauses=[]
    
    # GET THE CLAUSES WITH MINIMAL SIZE
    for clause in Knowledge_Base:
        if len(clause)==minimum_existing_size:
            min_clauses.append(clause)
    return min_clauses

def count_numb_of_occurences(literal, clauses_list):
    numb_of_occurences = 0
    for clause in clauses_list:
        if literal in clause:
            numb_of_occurences+=1
    return numb_of_occurences
    
def remove_negation(element): #remove the negation if element has one. so '-1' becomes '1'.
    if element[0] == '-': return element[1:]
    else: return element

def get_elements_dict(lines): # returns a dictionary with every element that is used as keys, and None as value
    all_elements = []
    for clause in lines:
        for element in clause:
            element = remove_negation(element)
            if element not in all_elements:
                all_elements.append(element)
    all_elements.sort()

    nones = [None for i in range(len(all_elements))]


    dictionary = dict(zip(all_elements, nones))
    return dictionary

def fill_in_assignments(Knowledge_Base, tf_assignments):
    all_clauses = Knowledge_Base[:]
    new_clauses = []

    def truth_check(clause, boolean):
        if clause[0] == '-': return not boolean
        else: return boolean

    for clause in all_clauses:
        new_clause = clause[:]
        append = True
        for literal in clause:
            #IF STILL HASN'T BEEN ASSIGNED:
            if tf_assignments[remove_negation(literal)] != None:
                if truth_check(literal, tf_assignments[remove_negation(literal)]) is True:
                    append = False
                    break
                else: new_clause.remove(literal)
        if append is True: new_clauses.append(new_clause)

    return new_clauses

def negate(element): #returns the negated element, so eg switches a '1' to '-1' and vice versa. Will be usefull later
    if element[0] == '-': return element[1:]
    else: return '-' + element

def load_file(file): #loads file that is in dimacs format (with 0 seperator)
    file = open(f'{aux_folder}/{file}')
    lines = file.readlines()
    if lines[0][0] == 'p': lines = lines[1:] #remove the first line if it starts with 'p', this is the summary line
    lines = [i[:-1] for i in lines] #remove the /n line seperator
    Knowledge_Base = [clause.split()[:-1] for clause in lines] #seperate each clause into list of elements, and remove the 0 seperator
    
    return Knowledge_Base
