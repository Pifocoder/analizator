import time
from .tools import *
import nltk

def clean_dicts(df):
    start_clean = time.time()
    nltk.download("stopwords")
    stopwords_list = set(nltk.corpus.stopwords.words("russian"))
    stopwords_list.update(['всё', 'это', "то", "что", "какой", "каков", "чей", "который", "лишь", "вообще"])
    m = Mystem()
    # df - df с комментариями
    df['text_clear'] = df['text'].apply(lambda x: clean_stop_words(clear_text(str(x)), stopwords_list, m))
    print('Обработка текстов заняла: ' + str(round(time.time() - start_clean, 2)) + ' секунд')
    return df


def get_df_train():
    labeled_texts_1 = pd.read_excel(
        'comments_analyser/datasets/doc_comment_summary.xlsx',
        sheet_name=0,
        header=None
    )
    labeled_texts_1['label'] = pd.to_numeric(labeled_texts_1.iloc[:, 1], errors='coerce')
    labeled_texts_1 = labeled_texts_1[[0, 'label']]
    labeled_texts_1.columns = ['text', 'label']
    ind_drop = labeled_texts_1.query('label > 2 or label < - 2').index
    labeled_texts_1 = labeled_texts_1.query('index not in @ind_drop')
    selected = labeled_texts_1.query('label != 0')
    selected.loc[:, 'label_binary'] = np.nan
    selected.loc[((selected['label'] == -1) |
                  (selected['label'] == -2)), 'label_binary'] = 0
    selected.loc[((selected['label'] == 1) |
                  (selected['label'] == 2)), 'label_binary'] = 1

    selected = clean_dicts(selected)
    selected['lemm_clean_tex'] = lemmatize(
        df=selected,
        text_column='text_clear',
        n_samples=100,
        break_str='br',
    )
    labeled_tweets = pd.read_csv('comments_analyser/datasets/labeled_tweets_clean.csv', sep=',')[['text_clear', 'label']]
    labeled_tweets = labeled_tweets.dropna()
    labeled_tweets['lemm_text_clear'] = lemmatize(
        df=labeled_tweets,
        text_column='text_clear',
        n_samples=1000,
        break_str='br',
    )
    return selected, labeled_tweets

