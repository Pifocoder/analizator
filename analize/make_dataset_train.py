import csv

data = []
new_data = []
with open('datasets/syn_api.csv', 'r', newline='') as file:
    reader = csv.reader(file)

    for row in reader:
        data.append(row)
change_type = []
min_change_type_dist = len(data)
for row in range(1, len(data)):
    new_data.append([data[row][0], data[row][2], data[row][1], data[row][2], 1])  # 1 - same
    if data[row][2] != data[row - 1][2]:
        change_type.append(row)
        if len(change_type) > 1:
            min_change_type_dist = min(min_change_type_dist,
                                       change_type[len(change_type) - 1] - change_type[len(change_type) - 2])
    for dist in range(1, 2):

        if (row - dist >= 1) and (data[row - dist][2] == data[row][2]):
            new_data.append(
                [data[row - dist][0], data[row - dist][2], data[row][0], data[row][2], 0])  # 0 - different
# print(change_type)
for change_row_id in range(len(change_type)):
    for next_change in range(change_row_id + 1, len(change_type)):
        for item in range(min_change_type_dist):
            new_data.append([data[change_type[change_row_id] + item][0], data[change_type[change_row_id] + item][2],
                             data[change_type[next_change] + item][0], data[change_type[next_change] + item][2], 0])
# print(new_data)

train = []
import make_assoc_graphs

nodist_graph = make_assoc_graphs.make_nodist_graph()
dist_graph = make_assoc_graphs.make_dist_graph()

import get_tow_texts_stat

index = 0
for item in new_data:
    print("next")
    nodist_stat = get_tow_texts_stat.get_two_texts_stat_nodist(item[0], item[2], nodist_graph)
    dist_stat = get_tow_texts_stat.get_two_texts_stat_dist(item[0], item[2], dist_graph)
    if item[1] == item[3]:
        train.append(nodist_stat + dist_stat + [1, item[4]])
    else:
        train.append(nodist_stat + dist_stat + [0, item[4]])
    index += 1
    if index == 10:
        break

from csv import writer

with open('datasets/log_reg_train.csv', 'a', newline='') as file:
    writer_object = writer(file)
    writer_object.writerows(train)
    file.close()
