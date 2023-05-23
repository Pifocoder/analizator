from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import cross_validate
from sklearn.model_selection import train_test_split

from sklearn.linear_model import LogisticRegression

from sklearn.metrics import *
from .clean import *
def get_model_count_idf():
    selected, labeled_tweets = get_df_train()
    sample_1 = labeled_tweets[['text_clear', 'lemm_text_clear', 'label']]
    sample_2 = selected[['text_clear', 'lemm_clean_tex', 'label_binary']]
    sample_2.columns = ['text_clear', 'lemm_text_clear', 'label']
    sample_2 = sample_2.dropna()
    joined_text = pd.concat([sample_1, sample_2])
    joined_text.columns = ['text', 'lemm_text', 'label']
    joined_text.index = range(joined_text.shape[0])
    joined_text = joined_text.dropna()
    sample_2.columns = ['text', 'text_lemm', 'label']
    sample_1.columns = ['text', 'text_lemm', 'label']
    # предварительно разделим выборку на тестовую и обучающую
    train, test = train_test_split(sample_1,
                                   test_size=0.2,
                                   random_state=12348,
                                   )

    count_idf_1 = TfidfVectorizer(ngram_range=(1, 1))
    tf_idf_base_1 = count_idf_1.fit(sample_1['text'])
    tf_idf_train_base_1 = count_idf_1.transform(train['text'])
    tf_idf_test_base_1 = count_idf_1.transform(test['text'])
    model_lr_base_1 = LogisticRegression(solver='lbfgs',
                                         random_state=12345,
                                         max_iter=10000,
                                         n_jobs=-1)
    model_lr_base_1.fit(tf_idf_train_base_1, train['label'])
    predict_lr_base_proba = model_lr_base_1.predict_proba(tf_idf_test_base_1)

    count_idf_lemm = TfidfVectorizer(ngram_range=(1, 1))
    tf_idf_lemm = count_idf_lemm.fit(sample_1['text_lemm'])
    tf_idf_train_lemm = count_idf_lemm.transform(train['text_lemm'])
    tf_idf_test_lemm = count_idf_lemm.transform(test['text_lemm'])
    model_lr_lemm = LogisticRegression(solver='lbfgs',
                                       random_state=12345,
                                       max_iter=10000,
                                       n_jobs=-1)
    model_lr_lemm.fit(tf_idf_train_lemm, train['label'])
    predict_lr_lemm_proba = model_lr_lemm.predict_proba(tf_idf_test_lemm)

    weights = pd.DataFrame({'words': count_idf_1.get_feature_names_out(), 'weights': model_lr_base_1.coef_.flatten()})
    weights_min = weights.sort_values(by='weights')
    weights_max = weights.sort_values(by='weights', ascending=False)
    weights_min = weights_min[:100]
    weights_min['weights'] = weights_min['weights'] * -1
    weights_max = weights_max[:100]
    vocab = weights.query('weights > 0.25 or weights < -0.25')['words']

    count_idf = TfidfVectorizer(vocabulary=vocab,
                                ngram_range=(1, 1))
    tf_idf = count_idf.fit_transform(joined_text['text'])
    tf_idf_train = count_idf.transform(train['text'])
    tf_idf_test = count_idf.transform(test['text'])
    model_lr_base = LogisticRegression(solver='lbfgs',
                                       random_state=12345,
                                       max_iter=10000,
                                       n_jobs=-1)
    model_lr_base.fit(tf_idf_train, train['label'])
    predict_lr_base_proba_1 = model_lr_base.predict_proba(tf_idf_test)
    return model_lr_base, count_idf
