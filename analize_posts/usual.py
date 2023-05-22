import re
import csv

def mark(words, dict_):
    result = 0
    pos = 1
    neg = 0
    operation = 0
    marker = {"не": 3, "очень": 1}
    neutral_proc = 0.2

    for word in words:
        val = "None"
        if word in dict_:
            val = float(dict_[word][1]) * 10
        if val == "None":
            val = 0

        if operation == 1: # marker words
            val *= 2
        elif operation == 2:
            val /= 2
        elif operation == 3:
            val *= -1
        result += val
        if val > 0:
            pos += val
        if val < 0:
            neg += val
        operation = marker.get(word)
        if operation == 1:
            val *= 2
        elif operation == 2:
            val /= 2
        elif operation == 3:
            val *= -1
        result += val
        if val > 0:
            pos += val
        if val < 0:
            neg += val
        #operation = marker.get(word)
    #print(int(result), int(pos), int(neg))
    if abs(result / pos) < neutral_proc:
        answer = "neutral"
        ans = 0
    elif pos > abs(neg):
        answer = "positive"
        ans = 1
    else:
        answer = "negative"
        ans = 2
    #print(answer)
    return ans