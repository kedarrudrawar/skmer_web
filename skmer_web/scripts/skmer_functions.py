import os
import subprocess
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import scipy.spatial as sp, scipy.cluster.hierarchy as hc

############################ QUERYING AND PARSING #############################

## 
# Returns parsed list of tuples [(hit, distance), ...]
#  Inputs: 
#  query_file - the path to the query file
#  library_dir = the path to the library directory
#  output_prefix - the path to + prefix of the desired output file
# 
def query(query_file, library_dir, output_prefix):
    
    command = "skmer query --debug"+ query_file + " " + library_dir + " -o " + output_prefix
    command = command.split(' ')
    print(command)
    subprocess.call(command)
    
    output_suffix = query_file.split("/")[-1]
    output_suffix = output_suffix.split(".")[0]
    
    dist_file = output_prefix + '-' + output_suffix.lower() + ".txt"
    stats_folder = output_suffix
    
    return dist_file, stats_folder

##
# Takes as input a filepath "dist_file"
# outputs parsed list of tuples [(hit, distance), ...] 
# AND DELETES THE FILE AT dist_file when clean=True
#
def parse_distout(dist_file, clean=False):
    
    distances = []
    with open(dist_file, 'r') as f:
        for line in f:
            line = line.strip()
            splits = line.split()
            distances.append((splits[0], splits[1]))
            
    if os.path.exists(dist_file):
        os.remove(dist_file)
    else:
        print("The file does not exist")
        
    return distances

##
# Takes as input a filepath "dist_file"
# outputs dictionary of stat:value
# AND DELETES THE FILE AT dist_file when clean=True
#
def parse_statsout(stats_folder, n_decimals=5, clean=False):
    
    dat_fp = stats_folder + "/" + stats_folder + ".dat"
    stats = dict()
    with open(dat_fp, 'r') as f:
        for line in f:
            line = line.strip()
            splits = line.split()
            if splits[0]=="repeat_profile":
                stats[splits[0]] = splits[1:] 
            else:
                stats[splits[0]] = round(float(splits[1]), n_decimals)
    
    profile = []
    for item in stats["repeat_profile"]:
        profile.append(round(float(item), n_decimals))
    stats["repeat_profile"] = profile

    if clean and os.path.exists(stats_folder):
        try:
            shutil.rmtree(stats_folder)
        except OSError as e:
            print ("Error: %s - %s." % (e.filename, e.strerror))
    else:
        print("The file does not exist")
        
    return stats

######################### GENERATING LIBRARY, DISTANCES ########################

## 
# Takes in the path to an already-constructed library directory
# Generates a matrix in the same folder where the library lives:
# "libraryname--distance_matrix.txt"
# Returns filepath of the distance matrix generated
#
def generate_distances(library_dir):
    
    output_dist_mat = library_dir + "--distance_matrix"
    
    print(output_dist_mat)
    
    if not os.path.isfile(output_dist_mat+".txt"):
        print("Generating distances for: " + library_dir)
        command = "skmer distance "+ library_dir + " -t -o " + output_dist_mat
        print(command)
        command = command.split(' ')
        subprocess.call(command)
    else:
        print("Distance Matrix already exists for this library")
    
    return output_dist_mat+".txt"

## 
# VERY EXPENSIVE, do not run on your own computer.
# Takes in the path to a directory of .fastq inputs
# Generates a reference library based on those inputs
# "libraryname--distance_matrix.txt"
# Returns filepath of the library_dir generated
#
def generate_library(fastq_dir):
    
    output_library = fastq_dir+"_library"
    if not os.path.isdir(output_library):
        print("Generating library " + output_library + " for: " + fastq_dir)
        print("This may take a while... ")
        command = "skmer reference "+ fastq_dir + " -l " + output_library
        print(command)
        command = command.split(' ')
        subprocess.call(command)
    else:
        print("library " + output_library + " already exists!")
    
    return output_library

############################ GENERATING FIGURES ##############################

def plot_repeat_profile_bar(stat_dict, output_fig, logscale=False):
    # Initialize figure and ax
    fig, ax = plt.subplots()

    # Set the scale of the x-and y-axes
    if logscale:
        ax.set(yscale="log")
        output_fig += "_logscaled"
    sns.barplot(x = ["Unique", "2", "3", "4", "5+"], 
                y = stat_dict["repeat_profile"], ax=ax)
    ax.set_title("K-mer Repeat Ratios")
    plt.savefig(output_fig)
    

def plot_repeat_profile_donut(stat_dict, output_fig):    
    names=["Unique", "2", "3", "4", "5+"]
    size= stat_dict["repeat_profile"]

    # Create a circle for the center of the plot
    my_circle=plt.Circle( (0,0), 0.7, color='white')
    plt.pie(size, labels=names)
    p=plt.gcf()
    p.gca().add_artist(my_circle)
    ax.set_title("K-mer Repeat Ratios")
    plt.savefig(output_fig)


##
# Returns a dataframe of the distance matrix, saves a figure to "output_fig"
# Takes in a path to the distance matrix (given by generate_distances(library_dir))
# names_to_include - optional list of 
def plot_distance_heatmap(dm_path, output_fig, names_to_include=None):
    
    dm_df = pd.DataFrame()
    with open(dm_path) as dm:
        get_index=True
        for line in dm:
            line = line.strip().split()
            if get_index:
                names = line[1:]
                dm_df = pd.DataFrame(columns=names, index=names)
                get_index = False
            else:
                #Append series' to dataframe
                dm_df[line[0]] = [float(val) for val in line[1:]]
    
    if names_to_include:
        dm_df = dm_df.loc[names_to_include, names_to_include]
    
    sns.set(font="monospace")

    linkage = hc.linkage(sp.distance.squareform(dm_df), method='average')
    sns.clustermap(dm_df, row_linkage=linkage, col_linkage=linkage)
    ax.set_title("Heatmap and Dendrogram of Pairwise Distances")
    plt.savefig(output_fig)
    return dm_df
