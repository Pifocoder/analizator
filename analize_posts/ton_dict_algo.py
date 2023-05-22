import re
import csv
import usual
import relations
from natasha import (
    Segmenter,
    MorphVocab,
    NewsEmbedding,
    NewsMorphTagger,
    NewsSyntaxParser,
    NewsNERTagger,
    PER,
    NamesExtractor,
    Doc
)
import json
import pandas as pd


def take_messages(file):
    mess = []
    with open(file, 'r', encoding="utf-8") as file:
        data = json.load(file)
        for message in data:
            mess.append(message["message"])

    # data = pd.read_csv(file)
    # mess = data['text_clear']
    # return data
    return mess


def make_dict():
    dicts = {}
    with open('kartaslovsent.csv', 'r', encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            info = row['term;tag;value;pstv;ngtv;neut;dunno;pstvNgtvDisagreementRatio'].split(';')
            dicts[info[0]] = info[1:]
    return dicts


def analize(file):
    messages = take_messages(file)
    #messages = take_messages(file)
    dictt = make_dict()

    emb = NewsEmbedding()
    morph_vocab = MorphVocab()
    segmenter = Segmenter()
    morph_tagger = NewsMorphTagger(emb)
    syntax_parser = NewsSyntaxParser(emb)
    # messages1 = [messages[492]]
    # messages2 = ["Встретились плохие люди, инопланетяне, эльфы и орки"]
    similar_result = 0
    relation_result = 0
    cnt = -1
    neutral = 0
    for text in messages:
        if str(type(text)) == "<class 'float'>":
            continue
        cnt += 1
        text = text.replace('\n', ' ')
        #print(cnt, text)
        doc = Doc(text)
        doc.segment(segmenter)
        doc.tag_morph(morph_tagger)

        words = []

        for token in doc.tokens:
            token.lemmatize(morph_vocab)
        for token in doc.tokens:
            words.append(token.lemma)

        doc.parse_syntax(syntax_parser)
        # doc.sents[0].syntax.print()

        # dictionaries
        marker = {}

        # print("usual algo: ")
        usual_mark = usual.mark(words, dictt)
        relations_mark = relations.mark(dictt, doc.tokens)
        return usual_mark, relations_mark

        #if res[cnt] == usual_mark:
        #    similar_result += 1
        # print("algo with relations: ")
        #if res[cnt] == relations_mark:
        #    relation_result += 1
    #print("usual algo: " + str(similar_result / len(res)))
    #print("algo with relations: " + str(relation_result / len(res)))


analize('data/labeled_tweets_clean.csv')
