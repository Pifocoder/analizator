import csv
import random

hashing_modul = 1000000
hashing_cof = 239
hash_table = [[]]


def get_hash_without_adding(word, max_sub_array_size=10):
    result = 0

    for letter in word:
        result = (result * hashing_cof + (ord(letter) - ord('а'))) % hashing_modul
    if word in hash_table[result]:
        return result * max_sub_array_size + hash_table[result].index(word)

    return -1


def get_hash(word, max_sub_array_size=10):
    result = 0
    for letter in word:
        result = (result * hashing_cof + (ord(letter) - ord('а'))) % hashing_modul
    if word in hash_table[result]:
        return result * max_sub_array_size + hash_table[result].index(word)
    hash_table[result].append(word)

    return result * max_sub_array_size + len(hash_table[result]) - 1


def make_nodist_graph():
    for i in range(hashing_modul):
        hash_table.append([])
    max_sub_array_size = 10

    graph = []
    for i in range(len(hash_table) * max_sub_array_size):
        graph.append([])

    with open('../datasets/assoc.csv') as assoc_dataset:
        reader = csv.reader(assoc_dataset)
        for row in reader:
            if row[0].split(';')[3] == "REV":
                graph[get_hash(row[0].split(';')[1], max_sub_array_size)].append(
                    (get_hash(row[0].split(';')[0], max_sub_array_size), 1.0)
                    # в этой версии деалем граф невзвешенный <=> вес == 1
                )
            if row[0].split(';')[3] == "DIR":
                graph[get_hash(row[0].split(';')[0], max_sub_array_size)].append(
                    (get_hash(row[0].split(';')[1], max_sub_array_size), 1.0)
                    # в этой версии деалем граф невзвешенный <=> вес == 1
                )
            if row[0].split(';')[3] == "BIDIR":
                graph[get_hash(row[0].split(';')[0], max_sub_array_size)].append(
                    (get_hash(row[0].split(';')[1], max_sub_array_size), 1.0)
                    # в этой версии деалем граф невзвешенный <=> вес == 1
                )
                graph[get_hash(row[0].split(';')[1], max_sub_array_size)].append(
                    (get_hash(row[0].split(';')[0], max_sub_array_size), 1.0)
                    # в этой версии деалем граф невзвешенный <=> вес == 1
                )

    return graph


def make_dist_graph():
    for i in range(hashing_modul):
        hash_table.append([])
    max_sub_array_size = 10

    graph = []
    for i in range(len(hash_table) * max_sub_array_size):
        graph.append([])
    with open('../datasets/assoc.csv') as assoc_dataset:
        reader = csv.reader(assoc_dataset)

        for row in reader:
            if row[0].split(';')[3] == "REV":
                graph[get_hash(row[0].split(';')[1], max_sub_array_size)].append(
                    (get_hash(row[0].split(';')[0], max_sub_array_size), random.random())
                )
            if row[0].split(';')[3] == "DIR":
                graph[get_hash(row[0].split(';')[0], max_sub_array_size)].append(
                    (get_hash(row[0].split(';')[1], max_sub_array_size), 1 - float(row[0].split(';')[4]))
                )
            if row[0].split(';')[3] == "BIDIR":
                graph[get_hash(row[0].split(';')[0], max_sub_array_size)].append(
                    (get_hash(row[0].split(';')[1], max_sub_array_size), 1 - float(row[0].split(';')[4]))
                )
                graph[get_hash(row[0].split(';')[1], max_sub_array_size)].append(
                    (get_hash(row[0].split(';')[0], max_sub_array_size), 1 - float(row[0].split(';')[4]))
                )
    return graph


def get_graphs():
    return [make_nodist_graph(), make_dist_graph()]
