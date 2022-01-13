from SAT import *
import numpy as np
import sys
import os
import pathlib
import time
import shutil

current_dir=pathlib.Path().resolve()
aux_folder = f'{current_dir}/aux_folder'
solutions_folder = f'{current_dir}/solutions'
args = sys.argv
input_file = args[1]


def main():
    create_DIMACS_files_from_txt(input_file)
    prepare_results_folders()
    for i in range(4):
        for file in os.listdir(aux_folder):
            i_time = time.time()
            thruth, solution, n_splits, n_backtracks = SAT(file,i)
            f_time = time.time()

            Total_time = str(f_time-i_time)
            n_splits = str(n_splits)
            n_backtracks=str(n_backtracks)
            save_result_as_DIMACS(solution, file, n_splits, n_backtracks, Total_time, i)
            #show_solution(solution)

   
def create_DIMACS_files_from_txt(path:str): 
    prepare_folders()
    n=1
    with open(path, "r") as f:
        for line in f:
            generate_DIMACS_file_from_line(n, line.strip())
            n+=1

def generate_DIMACS_file_from_line(n: int, line: str):
    sudoku_size = int(np.sqrt(len(line)))
    #check if is valid size, i.e, If the line size is a perfect square
    if len(line) != sudoku_size ** 2:
        raise AttributeError(f"The following line is not valid [{line}]. Size of the line must be a perfect square.")
    sudoku_puzzle = []
    k=0
    for i in range(1,sudoku_size+1):
        for j in range(1,sudoku_size+1):
            if line[k] != ".": 
                sudoku_puzzle.append(f"{i}{j}{line[k]}")
            k+=1
   
    f = open(f'{aux_folder}/sudoku_{n}.txt','w+')
    rules = get_sudoku_rules(sudoku_size)
    for clause in rules:
        f.write(clause)
    for clause in sudoku_puzzle:
        f.write(clause + ' 0 \n')
    
    #show_puzzle(sudoku_size,sudoku_puzzle)


#returns the list of rules of a sudoku with 'sudoku_size' , Strings in DIMACS form
def get_sudoku_rules(sudoku_size : int ):
    file_name = 'sudoku-rules'
    if sudoku_size == 4:
        file_name = file_name + '-4x4'
    else:
        if sudoku_size == 16:
            file_name = file_name + '-16x16'
    rules_file = f'{current_dir}/rules/{file_name}.txt'
    rule_clauses = [] 
    
    with open(rules_file,'r') as f:
        rule_clauses = f.readlines()
    
    return rule_clauses
        
def save_result_as_DIMACS(solution, filename, n_splits, n_backtracks, Total_time, used_heuristic):
    heuristics=['MOMs', 'Jeroslaw_OS',  'MOMs', 'Jeroslaw_OS']
    heuristics_folder = f'{solutions_folder}/{heuristics[used_heuristic]}'

    with open(f'{heuristics_folder}/{filename}','w+') as f:
        print("SAVING SOLUTION")
        f.write("n_splits: " + n_splits+'\n')
        f.write("n_backtracks: " + n_backtracks+'\n')
        f.write("Total_time: " + Total_time+'\n')

        f.write("p cnf "+ str(len(solution))+" "+str(len(solution))+'\n')
        for var, thruth_value in solution.items():
            if thruth_value==True: 
                f.write(var + ' 0 \n')

def show_puzzle(sudoku_size, sudoku_puzzle):
    print(sudoku_puzzle)
    game_matrix = np.zeros(shape=(sudoku_size, sudoku_size), dtype=int)
    for i in sudoku_puzzle:
        x,y,value = [int(a) for a in i]
        game_matrix[x-1][y-1]=value
    print(game_matrix)

def show_solution(solution):
    game_list=[]
    for key, value in solution.items():
        if value==True:
            game_list.append(key)
    sudoku_size = int(np.sqrt(len(game_list))) 
    game_matrix = np.zeros(shape=(sudoku_size, sudoku_size), dtype=int)
    for i in game_list:
        x,y,value = [int(a) for a in i]
        game_matrix[x-1][y-1]=value
    print(game_matrix)

def prepare_folders():
    if os.path.exists(aux_folder):
        for file in os.scandir(aux_folder):
            os.remove(file.path)
    else: os.mkdir(aux_folder)

    if os.path.exists(solutions_folder):
        shutil.rmtree(solutions_folder)
        os.makedirs(solutions_folder)
    else: os.mkdir(solutions_folder)

def prepare_results_folders():
    folders_list=['MOMs', 'Jeroslaw_OS', 'MOMs', 'Jeroslaw_OS']
    for i in range(len(folders_list)):
        heuristic_folder = f'{solutions_folder}/{folders_list[i]}'
        if os.path.exists(heuristic_folder):
            for file in os.scandir(heuristic_folder):
                os.remove(file.path)
        else: os.mkdir(heuristic_folder)


if __name__ == "__main__":
    main()