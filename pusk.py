from parsers.youtube_parser import getINFO
from comments_analyser.model import get_model_count_idf
from comments_analyser.proba_comment import comments_proba
import pandas as pd
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 500)


from sql_db.sql_queries import create_connection, execute_query, execute_read_query
from sql_db.add_post_comments import *


from parsers.vk_parser import parse_vk
from parsers.tg_parser import parse_tg

#
model, count_idf = get_model_count_idf()
groups = [-211210115, -26323016, 453382669, -30266386, -52620949, 561960677, 565282958, -148321046, -98331381, -216321473]
data = parse_vk(groups)
db_name_, db_user_, db_password_, db_host_, db_port_ = map(str, input())
connection = create_connection(db_name_, db_user_, db_password_, db_host_, db_port_)
for post in data[10:]:
    if len(post['comments']) > 0:
        add_post(connection, post['post'])
        comments = post['comments']
        df_comments = pd.DataFrame(comments)
        df_comments = comments_proba(df_comments, model, count_idf)
        add_comments(connection, df_comments)
#

# groups = [-170206299, -211210115, -26323016, 453382669, -30266386, -52620949, 561960677, 565282958, -148321046, -98331381, -216321473]
# parse_vk(groups)
# urls = ['https://t.me/moscowach']
# parse_tg(urls)

# from analize.make_assoc_graphs import get_graphs
# from analize.compare_texts import are_texts_same
# from analize.train_model_compare_texts import get_model
#
# graphs = get_graphs()
# model = get_model()
# first_text ="Трое подозреваемых в попытке совершения диверсии на Южно-Уральской железной дороге 7 мая задержаны, сообщили РИА Новости в понедельник в пресс-службе УФСБ России по региону. Источник РИА Новости в правоохранительных органах пояснил, что 7 мая произошла попытка вывода из строя релейных шкафов на одном из участков Южно-Уральской железной дороги. 'В результате проведенного комплекса мероприятий в Магнитогорске задержано трое граждан, причастных к осуществлению деяния на участке Южно-Уральской железной дороги', - сказала собеседница агентства. По данным источника, подозреваемые действовали в интересах украинских спецслужб за материальное вознаграждение. В отношении данных лиц возбуждено уголовное дело по статье 281 УК России (диверсия), добавил он."
# second_text = "В Магнитогорске задержали подозреваемых в попытке устроить диверсию на железной дороге, сообщили РИА Новости в пресс-службе регионального управления ФСБ. Как рассказал источник агентства в правоохранительных органах, накануне злоумышленники попытались вывести из строя релейные шкафы на одном из участков Южно-Уральской железной дороги. 'В результ те проведенного комплекса мероприятий в Магнитогорске задержано трое граждан', — сказал собеседник агентства. По информации источника, подозреваемые действовали по заданию украинских спецслужб, обещавших за это материальное вознаграждение. Против них возбудили уголовное дело о диверсии."
#
# a = are_texts_same(first_text, second_text, 1, 1, graphs, model)
# print(a)

