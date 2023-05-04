import pymysql as db
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from collections import Counter
from konlpy.tag import Okt

local = 'team0402.c43ypw0liaa2.ap-northeast-2.rds.amazonaws.com'  # aws rds 접근
con = db.connect(
    host=local,
    user='team0402',
    db='Team0402_Youtube',
    password='team0402',
    charset='utf8mb4'
)
cur = con.cursor()

def get_result_byQuery(query):
    cur.execute(query)
    return cur.fetchall()

def get_wordCloud(tuples):
    """
    Make WordCloud
    여러개의 문자열로 이루어진 튜플을 인자로 받는다.
    만들어진 img를 리턴한다.
    """
    # 하나의 문자열로 만들어주는 작업 / 튜플안에서 튜플꺼내기
    longStr = ''.join([text for tuple in tuples for text in tuple])

    # 형태소 분석 및 카운터 - 한글만
    okt = Okt()
    nouns = okt.nouns(longStr)
    counter = Counter(nouns)

    wordcloud = WordCloud(
        font_path ="./BMJUA.ttf",
        width=800,
        height=600,
        max_words=80,
        prefer_horizontal=1,
        max_font_size=250,
        background_color='white',
    )

    img = wordcloud.generate_from_frequencies(counter)
    return img

query_result = get_result_byQuery(
    """
    SELECT cmt.content
    FROM TB_VIDEO_INFO as v
    INNER JOIN TB_COMMENT_INFO as cmt ON v.video_id = cmt.video_id
    WHERE v.channel_id = 'UCbzI92w5vWa6mEj1dACfy6g'
    ORDER BY v.view_count desc LIMIT 500;
    """
)
plt.figure(figsize=(8,6))
plt.axis('off')
plt.imshow(get_wordCloud(query_result))
plt.savefig('UCbzI92w5vWa6mEj1dACfy6g_CHANNEL_COMMENT_WORDCLOUD.png')