import requests
import time

def parse_vk_group(owner_id, access_token, api_version, count):
    url_get_posts = 'https://api.vk.com/method/wall.get?owner_id={owner_id}&count={count}&offset={offset}&access_token={access_token}&v={api_version}'
    result = []
    for offset in range(0, count, 100):
        url_get_posts_formatted = url_get_posts.format(owner_id=owner_id, count=100, offset=offset,
                                                       access_token=access_token, api_version=api_version)
        print(url_get_posts_formatted)
        posts = (requests.get(url_get_posts_formatted)).json()['response']['items']
        url_get_comments = 'https://api.vk.com/method/wall.getComments?owner_id={owner_id}&post_id={post_id}&need_likes={need_likes}&offset={offset}&count={count}&preview_length={preview_length}&access_token={access_token}&v={api_version}'

        for post in posts:
            result.append({
                'post' : {
                    'from_id': post['from_id'],
                    'text': post['text'].replace('\n', '. '),
                    'id': post['id'],
                    'likes': post['likes']['count'],
                    'views': post['views']['count']
                },
                'comments' : []
            })

            if (post['comments']['count'] > 0):
                for comment_offset in range(0, post['comments']['count'], 100):
                    url_get_comments_formated = url_get_comments.format(owner_id=post['from_id'],
                                                                        post_id=post['id'],
                                                                        need_likes=1,
                                                                        offset=comment_offset,
                                                                        count=min(100, post['comments']['count'] - comment_offset),
                                                                        preview_length=0,
                                                                        access_token=access_token,
                                                                        api_version=api_version)
                    print(url_get_comments_formated)
                    comments = (requests.get(url_get_comments_formated)).json()['response']['items']
                    for comment in comments:
                        # TODO stickers
                        if (comment['text'] != ''):
                            result[-1]['comments'].append(
                                {
                                    'id': comment['id'],
                                    'text' : comment['text'].replace('\n', '. '),
                                    'likes' : comment['likes']['count']
                                }
                            )
                    time.sleep(0.1)
    return result

def parse_vk(access_token, api_version, count):
    result = []
    groups = [-170206299, -211210115, -26323016, 453382669, -30266386, -52620949, 561960677, 565282958, -148321046, -98331381, -216321473]
    for group in groups:
        print(parse_vk_group(group, access_token, api_version, count))
        result += parse_vk_group(group, access_token, api_version, count)

def main():
    access_token = input("Enter VK access_token")
    count = int(input("Enter number of posts"))
    api_version = "5.131"
    parse_vk(access_token, api_version, count)

if __name__ == "__main__":
    main()