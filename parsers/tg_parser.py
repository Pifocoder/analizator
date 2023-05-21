import configparser
import json
import time
import traceback
import csv

from telethon.sync import TelegramClient
from telethon import connection
# для корректного переноса времени сообщений в json
from datetime import date, datetime

# классы для работы с каналами
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch

# класс для работы с сообщениями
from telethon.tl.functions.messages import GetHistoryRequest

from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
from telethon.tl.types import PeerChannel



async def dump_all_messages(channel, client):
    """Записывает json-файл с информацией о всех сообщениях канала/чата"""
    offset_msg = 0    # номер записи, с которой начинается считывание
    limit_msg = 100   # максимальное число записей, передаваемых за один раз

    all_messages = []   # список всех сообщений
    total_messages = 0
    total_count_limit = 10  # поменяйте это значение, если вам нужны не все сообщения

    class DateTimeEncoder(json.JSONEncoder):
        '''Класс для сериализации записи дат в JSON'''
        def default(self, o):
            if isinstance(o, datetime):
                return o.isoformat()
            if isinstance(o, bytes):
                return list(o)
            return json.JSONEncoder.default(self, o)

    while True:
        time.sleep(3)
        try:
            history = await client(GetHistoryRequest(
                peer=channel,
                offset_id=offset_msg,
                offset_date=None, add_offset=0,
                limit=limit_msg, max_id=0, min_id=0,
                hash=0))
            if not history.messages:
                break
            messages = history.messages
            i = 0
            for message in messages:
                #all_messages.append(message.to_dict())
                i += 1
                post = message.to_dict()
                post_id = post['id']
                print(post)
                if 'reactions' in post:
                    react = post['reactions']
                else:
                    react = None
                all_messages.append({
                    'post': {
                        'id': post['id'],
                        'text': post['message'],
                        'reactions': react,
                        'date': post['date'],
                        'viewCnt': post['views']
                    },
                    'comments': []
                })
                async for comment in client.iter_messages(channel, reply_to=message.id):
                    comm = comment.to_dict()
                    all_messages[i - 1]['comments'].append(
                        {
                            'id': comm['id'],
                            'author_id': comm['from_id'],
                            'text': comm['message'],
                            'reply_id': comm['reply_to'],
                            'date_published': comm['date'],
                            'post_id': post_id
                        }
                    )
            offset_msg = messages[len(messages) - 1].id
            total_messages = len(all_messages)
            if total_count_limit != 0 and total_messages >= total_count_limit:
                break
        except:
            time.sleep(3)
    with open('channel_messages.json', 'w', encoding='utf8') as outfile:
        json.dump(all_messages, outfile, ensure_ascii=False, cls=DateTimeEncoder) #indent=2


async def main(urls, client):
    #url = "https://t.me/moscowach"
    #url = input("Введите ссылку на канал или чат: ")
    for url in urls:
        channel = await client.get_entity(url)
        await dump_all_messages(channel, client)

def parse_tg(urls):
    api_id = 20701539
    api_hash = '963f311e9676607de0705e1c43bd02d6'
    username = 'Dasha'

    # proxy = (proxy_server, proxy_port, proxy_key)
    client = TelegramClient(username, api_id, api_hash)
    #    connection=connection.ConnectionTcpMTProxyRandomizedIntermediate,
    #    proxy=proxy)

    client.start()
    with client:
        client.loop.run_until_complete(main(urls, client))
        client.loop.close()
