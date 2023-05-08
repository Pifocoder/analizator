import get_tow_texts_stat
from sklearn.linear_model import LinearRegression

def are_texts_same(first, second, first_category, second_category, graphs, model):
    nodist_stat = get_tow_texts_stat.get_two_texts_stat_nodist(first, second, graphs[0])
    dist_stat = get_tow_texts_stat.get_two_texts_stat_dist(first, second, graphs[1])
    if first_category != second_category:
        return 0

    if model.predict([nodist_stat + dist_stat + [1]]) >= 1:
        return 1
    return 0

