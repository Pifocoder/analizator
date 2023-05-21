import queue
from .make_assoc_graphs import get_hash_without_adding
from pymystem3 import Mystem


def make_text_good(text):
    mystem = Mystem()
    lemmas = mystem.lemmatize(text)

    result = []
    for item in lemmas:
        if get_hash_without_adding(item) != -1:
            result.append(get_hash_without_adding(item))
    return result


def get_stat_by_dist(dist, graph, first_text_words, second_text_words, first_len, second_len):
    stat = 0.0

    target_word = ""
    while (len(first_text_words) != 0) | (len(second_text_words) != 0):
        if len(first_text_words) >= len(second_text_words):
            target_word = list(first_text_words.keys())[0]
        else:
            target_word = list(second_text_words.keys())[0]

        query = queue.PriorityQueue(maxsize=0)
        query.put((0.0, target_word))
        vertex_dist = dict()
        vertex_dist[target_word] = 0.0
        while not query.empty():
            weight, vertex = query.get()
            if weight > dist:
                break
            for child, edge in graph[vertex]:
                if weight + edge > dist:
                    continue
                if child not in vertex_dist:
                    vertex_dist[child] = edge + weight
                    if vertex_dist[child] < dist:
                        query.put((vertex_dist[child], child))
                else:
                    if (child in vertex_dist) & (vertex_dist.get(child) > edge + weight):
                        vertex_dist.update({child: edge + weight})
                        if vertex_dist.get(child) < dist:
                            query.put((vertex_dist.get(child), child))

        first_text_words_number = 0
        second_text_words_number = 0
        for item in vertex_dist:
            weight = vertex_dist[item]
            if weight <= dist:
                if (item in first_text_words) & (item in second_text_words):
                    first_text_words_number += first_text_words[item]
                    second_text_words_number += second_text_words[item]
                    first_text_words.pop(item)
                    second_text_words.pop(item)
                if item in first_text_words:
                    first_text_words_number += first_text_words[item]
                    first_text_words.pop(item)
                if item in second_text_words:
                    second_text_words_number += second_text_words[item]
                    second_text_words.pop(item)

        stat += min(first_text_words_number / first_len, second_text_words_number / second_len)
    return stat


def get_two_texts_stat_nodist(first_text, second_text, graph):
    first_text_adapt = make_text_good(first_text)
    second_text_adapt = make_text_good(second_text)

    first_text_words = {}
    for word in first_text_adapt:
        if word not in first_text_words:
            first_text_words[word] = 1
        else:
            first_text_words[word] += 1
    second_text_words = dict()
    for word in second_text_adapt:
        if word not in second_text_words:
            second_text_words[word] = 1
        else:
            second_text_words[word] += 1

    statistics = []

    for dist in range(3):
        statistics.append(get_stat_by_dist(float(dist), graph, first_text_words.copy(), second_text_words.copy(),
                                           len(first_text_adapt), len(second_text_adapt)))

    return statistics


def get_two_texts_stat_dist(first_text, second_text, graph):
    first_text_adapt = make_text_good(first_text)
    second_text_adapt = make_text_good(second_text)

    first_text_words = {}
    for word in first_text_adapt:
        if word not in first_text_words:
            first_text_words[word] = 1
        else:
            first_text_words[word] += 1
    second_text_words = dict()
    for word in second_text_adapt:
        if word not in second_text_words:
            second_text_words[word] = 1
        else:
            second_text_words[word] += 1

    statistics = []
    dist = 1
    statistics.append(
        get_stat_by_dist(float(dist) / 1000.0, graph, first_text_words.copy(), second_text_words.copy(),
                         len(first_text_adapt), len(second_text_adapt)))
    return statistics

# import vk_parser
# vk_parser.parse_vk()

# [0.34577464788732387, 0.5380281690140843, 0.7197183098591547]
# [0.809507042253521, 0.903169014084507, 0.9390845070422535]
#
# [0.08928571428571427, 0.3035714285714285, 0.45357142857142857]
# [0.6964285714285715, 0.7500000000000001, 0.817857142857143]

# разные
# [0.12151162790697673, 0.24127906976744182, 0.5750000000000001]
# [0.3290697674418605, 0.6662790697674419, 0.6779069767441861, 0.7476744186046512, 0.7825581395348837, 0.8523255813953489, 0.8872093023255815, 0.8872093023255815, 0.9337209302325582, 0.9500000000000001]

# синонимайзер
# [0.7325581395348844, 0.7579672695951771, 0.8288831467126044]
# [0.7565317255239741, 0.8730979041056562, 0.8875968992248063, 0.9267872523686478, 0.9282227964398507, 0.9412862474877979, 0.954349698535745, 0.9565030146425495, 0.9565030146425495, 0.9593741027849555]
