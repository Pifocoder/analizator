import time
import requests
import json


# graphs = make_dataset_assoc.get_graphs()
def get_syn_text(text):
    param = {'method': 'getSynText', 'text': text}
    resp = requests.post("https://rustxt.ru/api/index.php", data=param)
    result = {}
    try:
        result = json.loads(resp.text)
    except:
        result = {'modified_text': text}
        time.sleep(10)
    if 'modified_text' not in result:
        return text
    return result["modified_text"]


import vk_parser_for_dataset

posts = vk_parser_for_dataset.parse_vk()
texts = []
number = 0
for post in posts:
    number += 1
    if (len(post['post']['text']) > 40):
        texts.append([post['post']['text'], get_syn_text(post['post']['text']), 'sport'])  # sport - now group
        time.sleep(1)

from csv import writer

with open('datasets/syn_api.csv', 'a', newline='') as file:
    writer_object = writer(file)
    writer_object.writerows(texts)
    file.close()
