import numpy as np
import pandas as pd
from pymystem3 import Mystem
from tqdm import tqdm
import re


def clear_text(text):
    clear_text = re.sub(r'[^А-яЁё]+', ' ', text).lower()
    return " ".join(clear_text.split())


def clean_stop_words(text, stopwords_list, mystem):
    lemmas = [word for word in mystem.lemmatize(text) if word not in [" ", "\n"]]
    text = text.split()
    result = []
    for i in range(len(lemmas)):
        if lemmas[i] not in stopwords_list:
            if (len(lemmas) == len(text)):
                result.append(text[i])
            else:
                result.append(lemmas[i])
    return " ".join(result)


def lemmatize(df,
              text_column,
              n_samples,
              break_str):
    result = []
    m = Mystem()
    for i in tqdm(range((df.shape[0] // n_samples) + 1)) :
        start = i * n_samples
        stop = start + n_samples
        sample = break_str.join(df[text_column][start : stop].values)
        lemmas = m.lemmatize(sample)
        lemm_sample = ''.join(lemmas).split(break_str)
        result += lemm_sample
    return pd.Series(result, index = df.index)