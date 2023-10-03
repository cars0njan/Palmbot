import os
import csv
import pandas as pd

def read_tail_index(file_path):
    with open(file_path, 'r') as f:
        for line in f:
            pass
        
        return line.split(',')[0].replace('"','')

def csv_append(file_path, data):
    with open(file_path, 'a') as csv_file:
        csv_file.write(data)
        csv_file.write('\n')

def add_file(file_path, name, data):
    with open(file_path,name, 'w') as add_file:
        add_file.write(data)

def stats():
    stats_csv = pd.read_csv('./stats.csv')
    stats_csv.Command_runs[0] = stats_csv.Command_runs[0] + 1
    stats_csv.to_csv("./stats.csv", index=False)
