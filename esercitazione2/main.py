
from esercitazione2.functs import *


if __name__ == '__main__':
    print("Content to form")

    data = read_load_csv()
    #print(data[0])

    candidate_genus = []
    concepts = []
    div = [0, 11, 23, 35, 47, 59, 71, 83, 95]

    for i in range(0, len(data)):
        for j in range(0, len(data[i])):
            concepts.append(preprocessing(data[i][j].split()))

    for i in range(0, len(div) - 1):
        if i != len(div):
            concat = [j for i in concepts[div[i]:div[i+1]] for j in i]
            #print(div[i], div[i+1])
            candidate_genus.append(concat)

    #print(candidate_genus)

    genus = [get_genus(g) for g in candidate_genus]

    #print("Genus")
    #print(genus)
    genus_synset = [[get_synset(g) for g in y] for y in genus]

    #print("Genus Synset")
    #print(genus_synset)

    final_synset = []

    for i in range(0, len(genus)):
        final_synset.append(get_best_synset(candidate_genus[i], genus_synset[i]))
        #print(final_synset[i].definition())

    print(final_synset)









