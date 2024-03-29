import os
import shutil
import subprocess
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import scipy.spatial as sp, scipy.cluster.hierarchy as hc

import io



############################ QUERYING AND PARSING #############################

## 
# Returns parsed list of tuples [(hit, distance), ...]
#  Inputs: 
#  query_file - the path to the query file
#  library_dir = the path to the library directory
#  output_prefix - the path to + prefix of the desired output file
# 
def query(query_file, library_dir, output_prefix):
    
    command = "skmer query "+ query_file + " " + library_dir + " -o " + output_prefix
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
def parse_distout(dist_file, n_results=5, clean=False):
    print('DIST FILE:', dist_file)
    sci_to_common_dict = get_sci_common_dict()
    distances = []
    with open(dist_file, 'r') as f:
        for line in f:
            print(line)
            line = line.strip()
            splits = line.split()
            distances.append((sci_to_common_dict[splits[0].replace("_", " ")], splits[0].replace("_", " "), splits[1]))
            
    if clean and os.path.exists(dist_file):
        os.remove(dist_file)
        
    return distances[:n_results]

##
# Takes as input a filepath "dist_file"
# outputs dictionary of stat:value
# AND DELETES THE FILE AT dist_file when clean=True
#
def parse_statsout(stats_folder, n_decimals=5, clean=False):
    
    dat_fp = stats_folder + "/" + stats_folder + ".dat"
    
    print("dat_fp: ", dat_fp)
    stats = dict()
    with open(dat_fp, 'r') as f:
        for line in f:
            line = line.strip()
            splits = line.split()
            if splits[0]=="repeat_profile":
                stats[splits[0]] = splits[1:] 
            else:
                stats[splits[0]] = round(float(splits[1]), n_decimals)
    print("stats dict: ", stats)
    
    profile = []
    for item in stats["repeat_profile"]:
        profile.append(round(float(item), n_decimals))
    stats["repeat_profile"] = profile
    
    print("the repeat profile is: ", profile)
    '''
    if clean and os.path.exists(stats_folder):
        try:
            shutil.rmtree(stats_folder)
        except OSError as e:
            print ("Error: %s - %s." % (e.filename, e.strerror))
    '''
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
    
    print("Attempting to use plt for barplot:")
    # Initialize figure and ax
    fig, ax = plt.subplots()
    print("Initialized fig, ax")
    # Set the scale of the x-and y-axes
    if logscale:
        ax.set(yscale="log")
        output_fig += "_logscaled"
        
    sns.barplot(x = ["Unique", "2", "3", "4", "5+"], 
                y = stat_dict["repeat_profile"], ax=ax)
    print("Created sns plot")
    ax.set_title("K-mer Repeat Ratios")
    
    print("About to save")
    
    plt.savefig(output_fig)
    print("Saved:", output_fig)
    return(output_fig)
    

def plot_repeat_profile_donut(stat_dict, output_fig): 
    print("Attempting to use plt for donutplot:")
    names=["Unique", "2", "3", "4", "5+"]
    size= stat_dict["repeat_profile"]

    # Create a circle for the center of the plot
    my_circle=plt.Circle( (0,0), 0.7, color='white')
    plt.pie(size, labels=names)
    p=plt.gcf()
    p.gca().add_artist(my_circle)
    #ax.set_title("K-mer Repeat Ratios")
    plt.savefig(output_fig)
    
    return(output_fig)

##
# Returns a dataframe of the distance matrix, saves a figure to "output_fig"
# Takes in a path to the distance matrix (given by generate_distances(library_dir))
# names_to_include - optional list of 
def plot_distance_heatmap(dm_path, output_fig, names_to_include=None):
    sci_to_common_dict = get_sci_common_dict()
    dm_df = pd.DataFrame()
    with open(dm_path) as dm:
        get_index=True
        for line in dm:
            line = line.strip().split()
            if get_index:
                names = line[1:] #[sci_to_common_dict[n.replace("_", " ")] for n in line[1:]]
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
    plt.savefig(output_fig)

    
    return [(sci_to_common_dict[name.replace("_"," ")], name) for name in dm_df.index]

def get_sci_common_dict():
    sci_to_common_dict = {'Acromyrmex echinatior': 'Panamanian leafcutter ant', 'Acyrthosiphon pisum': 'pea aphid', 'Aedes aegypti': 'yellow fever mosquito', 'Agrilus planipennis': 'emerald ash borer', 'Anopheles darlingi': 'American malaria mosquito', 'Anopheles funestus': 'African malaria mosquito', 'Anopheles gambiae': 'African malaria mosquito', 'Anopheles stephensi': 'Asian malaria mosquito', 'Anoplophora glabripennis': 'Asian longhorned beetle', 'Apis florea': 'little honeybee', 'Apis mellifera': 'honey bee', 'Athalia rosae': 'coleseed sawfly', 'Bactrocera cucurbitae': 'melon fly', 'Bactrocera dorsalis': 'oriental fruit fly', 'Blattella germanica': 'German cockroach', 'Bombus terrestris': 'buff-tailed bumblebee', 'Bombyx mori': 'domestic silkworm', 'Camponotus floridanus': 'Florida carpenter ant', 'Cephus cinctus': 'wheat stem sawfly', 'Cerapachys biroi': 'clonal raider ant', 'Ceratitis capitata': 'Mediterranean fruit fly', 'Chilo suppressalis': 'striped riceborer', 'Cimex lectularius': 'bed bug', 'Cotesia vestalis': 'diamondback moth parasitoid', 'Culex quinquefasciatus': 'southern house mosquito', 'Danaus plexippus': 'monarch butterfly', 'Diaphorina citri': 'Asian citrus psyllid', 'Drosophila melanogaster': 'fruit fly', 'Frankliniella occidentalis': 'western flower thrips', 'Glossina austeni': 'tsetse fly', 'Glossina brevipalpis': 'tsetse fly', 'Glossina fuscipes': 'tsetse fly', 'Glossina morsitans': 'tsetse fly', 'Glossina pallidipes': 'tsetse fly', 'Glossina palpalis': 'tsetse fly', 'Halyomorpha halys': 'brown marmorated stink bug', 'Harpegnathos saltator': "Jerdon's jumping ant", 'Heliconius melpomene': 'postman butterfly', 'Homalodisca vitripennis': 'glassy-winged sharpshooter', 'Ladona fulva': 'scarce chaser', 'Leptinotarsa decemlineata': 'Colorado potato beetle', 'Linepithema humile': 'Argentine ant', 'Locusta migratoria': 'migratory locust', 'Lucilia cuprina': 'Australian sheep blowfly', 'Manduca sexta': 'tobacco hornworm', 'Mayetiola destructor': 'Hessian fly', 'Megachile rotundata': 'alfalfa leafcutting bee', 'Melitaea cinxia': 'Glanville fritillary', 'Monomorium pharaonis': 'pharaoh ant', 'Musca domestica': 'house fly', 'Nasonia vitripennis': 'jewel wasp', 'Oncopeltus fasciatus': 'milkweed bug', 'Pachypsylla venusta': 'hackberry petiole gall psyllid', 'Papilio glaucus': 'eastern tiger swallowtail', 'Papilio polytes': 'common Mormon', 'Pediculus humanus': 'human louse', 'Plutella xylostella': 'diamondback moth', 'Pogonomyrmex barbatus': 'red harvester ant', 'Solenopsis invicta': 'red fire ant', 'Spodoptera frugiperda': 'fall armyworm', 'Stomoxys calcitrans': 'stable fly', 'Tribolium castaneum': 'red flour beetle', 'Wasmannia auropunctata': 'little fire ant', 'Anopheles albimanus': 'Mosquito', 'Anopheles arabiensis': 'Mosquito', 'Anopheles atroparvus': 'Mosquito', 'Anopheles christyi': 'Mosquito', 'Anopheles culicifacies': 'Mosquito', 'Anopheles dirus': 'Mosquito', 'Anopheles epiroticus': 'Mosquito', 'Anopheles farauti': 'Mosquito', 'Anopheles koliensis': 'Mosquito', 'Anopheles maculatus': 'Mosquito', 'Anopheles melas': 'Mosquito', 'Anopheles merus': 'Mosquito', 'Anopheles minimus': 'Mosquito', 'Anopheles nili': 'Mosquito', 'Anopheles punctulatus': 'Mosquito', 'Anopheles quadriannulatus': 'Mosquito', 'Anopheles sinensis': 'Mosquito', 'Atta cephalotes': 'Ant', 'Belgica antarctica': 'Antarctic Midge', 'Catajapyx aquilonaris': 'Japygid', 'Chironomus tentans': 'Midge (Fly)', 'Copidosoma floridanum': 'Wasp', 'Drosophila ananassae': 'Fruit Fly', 'Drosophila biarmipes': 'Fruit Fly', 'Drosophila bipectinata': 'Fruit Fly', 'Drosophila elegans': 'Fruit Fly', 'Drosophila erecta': 'Fruit Fly', 'Drosophila eugracilis': 'Fruit Fly', 'Drosophila ficusphila': 'Fruit Fly', 'Drosophila grimshawi': 'Fruit Fly', 'Drosophila kikkawai': 'Fruit Fly', 'Drosophila miranda': 'Fruit Fly', 'Drosophila mojavensis': 'Fruit Fly', 'Drosophila rhopaloa': 'Fruit Fly', 'Drosophila sechellia': 'Fruit Fly', 'Drosophila simulans': 'Fruit Fly', 'Drosophila suzukii': 'Fruit Fly', 'Drosophila takahashii': 'Fruit Fly', 'Drosophila virilis': 'Fruit Fly', 'Drosophila willistoni': 'Fruit Fly', 'Drosophila yakuba': 'Fruit Fly', 'Ephemera danica': 'Mayfly', 'Fopius arisanus': 'Parasatoid', 'Gerris buenoi': 'Water Strider', 'Limnephilus lunatus': 'Caddisfly', 'Lutzomyia longipalpis': 'Sand Fly', 'Mengenilla moldrzyki': 'Twisted Wing Parasite', 'Microplitis demolitor': 'Wasp', 'Onthophagus taurus': 'Dung Beatle', 'Orussus abietinus': 'Wood Wasp', 'Phlebotomus papatasi': 'Sand Fly', 'Rhodnius prolixus': 'Assassin Bug', 'Timema cristinae': 'Walking Stick', 'Trichogramma pretiosum': 'Wasp', 'Vollenhovia emeryi': 'Ant', 'Zootermopsis nevadensis': 'Termite'}
    return sci_to_common_dict