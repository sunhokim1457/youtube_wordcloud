from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from pandas import DataFrame

DEVELOPER_KEY = 'AIzaSyAoMzPjwS1LxBs1XtrWxq-eRiC-ot4Gcr8'
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION ='v3'

youtube=build(YOUTUBE_API_SERVICE_NAME,YOUTUBE_API_VERSION,developerKey=DEVELOPER_KEY)

# 특정 채널의 재생목록 뽑아내기
channel_playlist = youtube.playlists().list(
    part = "snippet",
    channelId = "UCtm_QoN2SIxwCE-59shX7Qg", # SPOTV
    maxResults = "5",
).execute()

# 재생목록안의 비디오들 뽑아내기
playlists = []
playlists_title = []
for item in channel_playlist['items']:
    videoList = youtube.playlistItems().list(
        part = 'snippet',
        playlistId = item['id'],
        maxResults = 10,
    ).execute()
    playlists.append(videoList)
    playlists_title.append(item['snippet']['title'])

# 각 재생목록의 통계 계산
playlists_viewCount = [] # 총 조회수
playlists_commentCount = [] # 총 덧글수
playlists_likeCount = [] # 총 좋아요 개수
playlists_videoCount = [] # 총 비디오 개수

# 각 재생목록마다 반복

for i in range(len(playlists)):
    playlists_viewCount.append(0)
    playlists_commentCount.append(0)
    playlists_likeCount.append(0)
    playlists_videoCount.append(0) 

    # 재생목록에 들어있는 비디오 정보를 사용하여 계산
    for video in playlists[i]['items']:
        videoStat = youtube.videos().list(
            part = 'snippet ,statistics',
            id = video['snippet']['resourceId']['videoId']
        ).execute()
        if videoStat['items']: # 비공개 동영상은 제외
            playlists_viewCount[-1] += int(videoStat['items'][0]['statistics']['viewCount'])
            playlists_commentCount[-1] += int(videoStat['items'][0]['statistics']['viewCount'])
            playlists_likeCount[-1] += int(videoStat['items'][0]['statistics']['likeCount'])
            playlists_videoCount[-1] += 1

raw_data ={
    'viewCount' : [round(x/y) for x,y in zip(playlists_viewCount, playlists_videoCount)],
    'commentCount' : [round(x/y) for x,y in zip(playlists_commentCount, playlists_videoCount)],
    'likeCount' : [round(x/y) for x,y in zip(playlists_likeCount, playlists_videoCount)],
}

data = DataFrame(raw_data, index=playlists_title)