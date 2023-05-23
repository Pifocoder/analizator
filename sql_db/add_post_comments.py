from sql_db.sql_queries import *
def add_comments(connection, df_comments, table='comments'):
    # df_comments = df_comments.rename(columns={'video_id': 'post_id'})
    df_comments.drop(columns="date_published")
    cols = ','.join(list(df_comments.columns))
    for x in df_comments.to_numpy():
        try:
            tuples = str(tuple(x))
            query = "INSERT INTO %s (%s) \nVALUES \n%s;" % (table, cols, tuples)
            print(query)
            execute_query(connection, query)
        except:
            print('error_occurred')

def add_post(connection, post):
    values = """('%s', 2, '%s', '%s', %s)""" % (str(post['id']), post['text'], str(post['from_id']), str((post['likes'])))
    query_post = """INSERT INTO posts (id, type, text, author_id, likes) VALUES %s;""" % values
    print(query_post)
    execute_query(connection, query_post)