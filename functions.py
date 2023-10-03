import os
import csv

def read_tail_index(file_path):
    with open(file_path, 'r') as f:
        for line in f:
            pass
        
        return line.split(',')[0].replace('"','')
    # with open(file_path, 'r') as file:
    #     file.seek(0, os.SEEK_END)
    #     file.seek(file.tell() - 2, os.SEEK_SET)
    #     print(file.readline())

    #     last_line = file.readline().strip().split(',')

    #     first_column = last_line[0]

    #     return first_column


# def csv_append(file_path, data):
#     with open(file_path, 'a', newline='') as csv_file:
#         writer = csv.writer(csv_file)
#         writer.writerow(data)
#         # append data as a list, eg: ["0","test","test"]

def csv_append(file_path, data):
    with open(file_path, 'a') as csv_file:
        csv_file.write(data)
        csv_file.write('\n')

def add_file(file_path, name, data):
    with open(file_path,name, 'w') as add_file:
        add_file.write(data)