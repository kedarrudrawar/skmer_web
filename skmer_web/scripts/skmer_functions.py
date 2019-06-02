import os
import subprocess

## 
# Takes in the path to the library directory
# Generates a matrix in the same folder where the library lives:
# "libraryname--distance_matrix.txt"
# Returns filepath of the distance matrix generated
#
def generate_distances(library_dir):
    
    output_dist_mat = library_dir + "--distance_matrix"
    
    if not os.path.isfile(output_dist_mat+".txt"):
        os.popen("skmer distance "+ library_dir + " -o " + output_dist_mat)
    else:
        print("DM already exists for this library")
    
    return output_dist_mat+".txt"

## 
# Returns parsed list of tuples [(hit, distance), ...]
#  Inputs: 
#  query_file - the path to the query file
#  library_dir = the path to the library directory
#  output_prefix - the path to + prefix of the desired output file
# 
def query(query_file, library_dir, output_prefix, add_query_to_ref=False):
    output_suffix = query_file.split("/")[-1]
    output_suffix = output_suffix.split(".")[0]
    
    output_file = output_prefix + '-' + output_suffix.lower() + ".txt"
    
    if add_query_to_ref:
        command = "skmer query "+ query_file + " " + library_dir + " -a -o " + output_prefix
        command = command.split(' ')
    else:
        command = "skmer query "+ query_file + " " + library_dir + " -o " + output_prefix
        command = command.split(' ')
    print(command)
    subprocess.call(command)
    return output_file

# outputs parsed list of tuples [(hit, distance), ...]
def parse_queryout(output_file):
    
    distances = []
    with open(output_file, 'r') as f:
        for line in f:
            line = line.strip()
            splits = line.split()
            distances.append((splits[0], splits[1])) 
    return distances