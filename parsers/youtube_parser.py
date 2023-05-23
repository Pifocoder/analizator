from parsers.api_youtube import *
import re

def getVideoID_VideoURL(videoURL):
    from pytube import extract
    return extract.video_id(videoURL)

def getBasicInfo(response):
    dict = {}
    dict['url'] = 'https://www.youtube.com/watch?v=' + response['items'][0]['id']
    dict['id'] = response['items'][0]['id']
    dict['title'] = response['items'][0]['snippet']['title']
    dict['description'] = response['items'][0]['snippet']['description']
    dict['date'] = response['items'][0]['snippet']['publishedAt']
    dict['viewCnt'] = response['items'][0]['statistics']['viewCount']
    return dict

def makeCommDict(id, snippet, parentId = False):
    tmp = {
        'id': id,
        'text': snippet['textOriginal'].replace('"', '').replace("'", ""),
        'parent_id': parentId,
        'author': snippet['authorDisplayName'],
        'author_id': snippet['authorChannelId']['value'],
        'likes': snippet['likeCount'],
        'date_published': snippet['publishedAt'],
        'date_updated': snippet['updatedAt'],
        'video_id': snippet['videoId'],
        'replies': 0
    }
    return tmp

def process_comments(response):
    comments = []
    for res in response['items']:
        # loop through the replies
        infoTopComment = res['snippet']['topLevelComment']
        comment = makeCommDict(infoTopComment['id'], infoTopComment['snippet'])
        if 'replies' in res.keys():
           for reply in res['replies']['comments']:
                commReply = makeCommDict(reply['id'], reply['snippet'], infoTopComment['id'])
                if commReply['text'] != "":
                    comments.append(commReply)
                    comment['replies'] += 1
        if comment['text'] != "":
            comments.append(comment)
    return comments

def commentThreads_VideoID(videoID: str):
    response = youtube.commentThreads().list(
        part='id,snippet,replies',
        videoId=videoID,
        order='relevance'
    ).execute()
    comments_list = []
    comments_list.extend(process_comments(response))
    limit = 10 # var changeable
    while response.get('nextPageToken', None) and limit:
        request = youtube.commentThreads().list(
            part='id,replies,snippet',
            videoId=videoID,
            order='relevance',
            pageToken=response['nextPageToken'],
        )
        response = request.execute()
        comments_list.extend(process_comments(response))
        limit -= 1
        # print(json.dumps(response, indent=2)
    return comments_list

def getVideoCaptions(videoId: str) :
    try:
        return YouTubeTranscriptApi.get_transcript(videoId, languages=['ru'])
    except:
        return ""


def getVideoInfo(videoID: str, channelID):
    # videoID = getVideoID_VideoURL(videoURL);
    videoInfo = {}
    request = youtube.videos().list(
        part="snippet,contentDetails,statistics,id",
        id=videoID
    )
    response = request.execute()
    videoInfo = getBasicInfo(response)
    videoInfo['channel_id'] = channelID
    videoInfo['likeCnt'] = response['items'][0]['statistics']['likeCount']
    videoInfo['commCnt'] = response['items'][0]['statistics']['commentCount']
    comments = commentThreads_VideoID(videoID)
    capt = list(getVideoCaptions(videoID))
    videoInfo['captions'] = "".join(" ".join([a['text'] for a in capt]).split("Музыка")).replace('"', '').replace("'", "")
    return { "videoINFO" : videoInfo,
             "comments" : comments }


def getINFO_posts(channelID):
    # request = youtube.channels().list(
    #     part="snippet,contentDetails,statistics",
    #     id=channelID
    # )
    # response = request.execute()
    # channelInfo = getBasicInfo(response)
    # channelInfo['subscrib'] = response['items'][0]['statistics']['subscriberCount']
    # channelInfo['videoCnt'] = response['items'][0]['statistics']['videoCount']
    # channelInfo['listVideoIDs'] = []
    videoIDs = []
    request = youtube.search().list(
        part="snippet",
        channelId=channelID,
        type="video",
        #order="viewCount",
        maxResults=50
    )
    response = request.execute()
    responseItems = response['items']
    videoIDs.extend([item['id']['videoId'] for item in responseItems if item['id'].get('videoId', None) != None])
    limit = 2
    # есть лимит на количество запросов, самая дорогая операция - получение списка всех видео на канале
    # поэтому делаю запрос на максимум 50-100 видео с канала
    while response.get('nextPageToken', None) and limit:
        request = youtube.search().list(
            part="snippet",
            channelId=channelID,
            pageToken=response['nextPageToken'],
            type="video",
            order="viewCount",
            maxResults=50
        )
        response = request.execute()
        responseItems = response['items']
        videoIDs.extend([item['id']['videoId'] for item in responseItems if item['id'].get('videoId', None) != None])
        limit -= 1
    videos = []
    for id_i in videoIDs:
        data = getVideoInfo(id_i, channelID)
        if data['videoINFO']['captions'] != "" and len(data['comments']) != 0:
            data['videoINFO']['captions'] = data['videoINFO']['captions'].replace("'", "")
            print(data['videoINFO']['captions'])
            videos.append(data)
    return videos

def getINFO(channel_IDS):
    posts = []
    for id_ in channel_IDS:
        posts += getINFO_posts(id_)
    return posts