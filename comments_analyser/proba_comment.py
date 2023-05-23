from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from .clean import *

def comments_proba(df_comments, model, count_idf):
    df_comments = clean_dicts(df_comments)
    df_comments['lemm_clean_text'] = lemmatize(
        df=df_comments,
        text_column='text_clear',
        n_samples=100,
        break_str='br',
    )
    df_tf_idf = count_idf.transform(df_comments['lemm_clean_text'])
    df_proba = model.predict_proba(df_tf_idf)
    df_comments['proba'] = df_proba[:, 0]
    return df_comments