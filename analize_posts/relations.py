import re
import csv

def mark(dict_, tokens):
    result = 0
    pos = 1
    neg = 0
    operation = 0
    marker = {}
    neutral_proc = 0.2
    pred_proc = 0.3

    for token in tokens:
        word = token.lemma
        pred = token.head_id
        pred = int(pred.split('_')[1]) - 1
        pred_word = ""
        pred_val = 0
        pred_pos = ""
        if pred >= 0:
            pred_word = tokens[pred].lemma
            pred_pos = tokens[pred].pos
        val = "None"
        if word in dict_:
            val = float(dict_[word][1]) * 10
        if val == "None":
            val = 0
        if pred_word in dict_:
            pred_val = float(dict_[pred_word][1]) * 10
            if pred_pos == "VERB":
                val += pred_val
            val += pred_val * pred_proc

        if val > 0:
            pos += val
        if val < 0:
            neg += val

        result += val
        #print(word, pred_word, val, pred_val)
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