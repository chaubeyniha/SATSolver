from SAT import *
import numpy as np
import sys
import os
import pathlib
import time
import shutil
import statistics


current_dir=pathlib.Path().resolve()
solutions_folder = f'{current_dir}/solutions_niha'

#for sub_folder in solutions_folder:
#for file in sub_folder:

splits_list=[]
backtracks_list=[]
time_list=[]

#change name to file name
sub_folder=f'{solutions_folder}/Jeroslaw_OS'
filesii = [1,2,3,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39]
for i in filesii:
    file= f'{sub_folder}/sudoku_{i}.txt'
    with open(file,'r') as f:
        line1=f.readline().rstrip("\n")
        splits_info= line1.split(":")
        splits_list.append(int(splits_info[1]))

        line2=f.readline().rstrip("\n")
        backtracks_info=line2.split(":")
        backtracks_list.append(int(backtracks_info[1]))

        line3=f.readline().rstrip("\n")
        time_info=line3.split(":")
        time_list.append(int(float(time_info[1])))

print('splits_list',splits_list)

split_mean=statistics.mean(splits_list)
split_std=statistics.stdev(splits_list)
split_max= max(splits_list)
split_min= min(splits_list)

backtrack_mean=statistics.mean(backtracks_list)
backtracks_std=statistics.stdev(backtracks_list)
backtracks_max= max(backtracks_list)
backtracks_min= min(backtracks_list)

time_mean=statistics.mean(time_list)
time_std=statistics.stdev(time_list)
time_max= max(time_list)
time_min= min(time_list)

with open(f'{sub_folder}/results.txt','w+') as f:
    print("SAT RESULTS")
    print("{sub_folder}/results.txt")
    f.write("split_mean: " + str(split_mean)+'\n')
    f.write("split_std: " + str(split_std)+'\n')
    f.write("split_max: " + str(split_max)+'\n')
    f.write("split_min: " + str(split_min)+'\n')
    f.write('\n')
    f.write("backtrack_mean: " + str(backtrack_mean)+'\n')
    f.write("backtracks_std: " + str(backtracks_std)+'\n') 
    f.write("BT_max: " + str(backtracks_max)+'\n')
    f.write("BT_min: " + str(backtracks_min)+'\n')       
    f.write('\n')
    f.write("time_mean: " + str(time_mean)+'\n')
    f.write("time_std: " + str(time_std)+'\n')   
    f.write("time_max: " + str(time_max)+'\n')
    f.write("time_min: " + str(time_min)+'\n')     


                

