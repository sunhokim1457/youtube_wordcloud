from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.tools import argparser

# 사전 조건
DEVELOPER_KEY = 'AIzaSyAoMzPjwS1LxBs1XtrWxq-eRiC-ot4Gcr8'
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION ='v3'

youtube=build(YOUTUBE_API_SERVICE_NAME,YOUTUBE_API_VERSION,developerKey=DEVELOPER_KEY)

# 검색 옵션
search_response = youtube.search().list(
    # part = 'snippet',
    part = 'id',
    order = 'viewCount',
    topicId = '/m/06ntj', # topic : sport
    publishedAfter = '2023-04-01T00:00:00Z',
    maxResults = 5,
    regionCode = 'KR',
).execute()

print(search_response)
# views = []

# for item in search_response['items']:
#     print(item['snippet']['channelTitle'])