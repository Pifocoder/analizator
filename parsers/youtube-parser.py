from api_youtube import *
def getVideoID_VideoURL(videoURL):
    from pytube import extract
    return extract.video_id(videoURL)

def getBasicInfo(response):
    dict = {}
    dict['id'] = response['items'][0]['id']
    dict['title'] = response['items'][0]['snippet']['title']
    dict['description'] = response['items'][0]['snippet']['description']
    dict['date'] = response['items'][0]['snippet']['publishedAt']
    dict['viewCnt'] = response['items'][0]['statistics']['viewCount']
    return dict

def makeCommDict(id, snippet, parentId = False):
    tmp = {
        'id': id,
        'text': snippet['textOriginal'],
        'parent_id': parentId,
        'author': snippet['authorDisplayName'],
        'authorId': snippet['authorChannelId']['value'],
        'likes': snippet['likeCount'],
        'date_published': snippet['publishedAt'],
        'date_updated': snippet['updatedAt'],
        'video_id': snippet['videoId'],
        'author_channel_id' : snippet['authorChannelId']['value']  if 'authorChannelId' in snippet else False,
        'replies' : 0
    }
    #tmp['author_comment'] = tmp['author_channel_id'] and tmp['author_channel_id'] == channel_ID
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
    limit = 20 # var changeable
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
    src = YouTubeTranscriptApi.get_transcript(videoId, languages=['ru'])
    return src

def getVideoInfo_byVideoURL(videoURL: str):
    videoID = getVideoID_VideoURL(videoURL);
    videoInfo = {}
    request = youtube.videos().list(
        part="snippet,contentDetails,statistics,id",
        id=videoID
    )
    response = request.execute()
    videoInfo = getBasicInfo(response)
    videoInfo['likeCnt'] = response['items'][0]['statistics']['likeCount']
    videoInfo['commCnt'] = response['items'][0]['statistics']['commentCount']
    comments = commentThreads_VideoID(videoID)
    videoInfo['captions'] = getVideoCaptions(videoID);
    return [videoInfo, comments]

def getINFO(video_URL):
    # example ntv video
    ntv_url = "https://www.youtube.com/watch?v=Diz-6gO6wrY&t=14s&ab_channel=%D0%9D%D0%A2%D0%92%D0%9D%D0%BE%D0%B2%D0%BE%D1%81%D1%82%D0%B8"

    data = getVideoInfo_byVideoURL(ntv_url)
    video_comments = data[1]
    captions = "".join(" ".join([a['text'] for a in data[0]['captions']]).split("[Музыка]"))
    captions_list = captions.split()
    return data
