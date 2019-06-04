file_name = 'insects_species_list.txt'

from Bio import Entrez


def get_common_names(file_name):
    data = []
    with open(file_name, 'r+') as fp:
        for line in fp.readlines():
            line = line.rstrip()
            data.append(line)

    sci_to_common_dict = {}

    for sci_name in data:
        sci_name = sci_name.replace("_", " ")
        if sci_name in sci_to_common_dict:
            continue
        else:
            Entrez.email = 'greatsahil@gmail.com'
            handle = Entrez.esearch(db='taxonomy', term=sci_name, rettype='xml')
            record = Entrez.read(handle)

            taxID = record['IdList'][0]
            handle.close()
            handle = Entrez.efetch(db='taxonomy', id=taxID, rettype="gb")
            record = Entrez.read(handle)
            if record[0]:
                if record[0].get('OtherNames'):
                    if record[0].get('OtherNames').get('GenbankCommonName'):
                        common_name = record[0].get('OtherNames').get('GenbankCommonName')
                        sci_to_common_dict[sci_name] = common_name
                        if isinstance(common_name, list):
                            common_name = (common_name[0])
                        print(common_name)
                    elif record[0].get('OtherNames').get('CommonName'):
                        common_name = record[0].get('OtherNames').get('CommonName')
                        sci_to_common_dict[sci_name] = common_name
                        if isinstance(common_name, list):
                            common_name = (common_name[0])
                        print(common_name)
                    else:
                        continue
                else:
                    continue
            else:
                continue

    species_dict = {
        "Anopheles": "Mosquito",
        "Atta": "Ant",
        "Vollenhovia": "Ant",
        "Belgica": "Antarctic Midge",
        "Catajapyx": "Japygid",
        "Chironomus": "Midge (Fly)",
        "Copidosoma": "Wasp",
        "Microplitis": "Wasp",
        "Trichogramma": "Wasp",
        "Drosophila": "Fruit Fly",
        "Ephemera": "Mayfly",
        "Fopius": "Parasatoid",
        "Gerris": "Water Strider",
        "Glossina": "Tsetse Fly",
        "Limnephilus": "Caddisfly",
        "Lutzomyia": "Sand Fly",
        "Phlebotomus": "Sand Fly",
        "Mengenilla": "Twisted Wing Parasite",
        "Onthophagus": "Dung Beatle",
        "Orussus": "Wood Wasp",
        "Rhodnius": "Assassin Bug",
        "Timema": "Walking Stick",
        "Zootermopsis": "Termite",
    }

    for sci_name in data:
        sci_name = sci_name.replace("_", " ")
        if sci_name not in sci_to_common_dict:
            species = (sci_name.split(" "))[0]
            sci_to_common_dict[sci_name] = species_dict[species]

    return sci_to_common_dict
