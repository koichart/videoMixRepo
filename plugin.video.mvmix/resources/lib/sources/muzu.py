# -*- coding: utf-8 -*-

from resources.lib import simple_requests as requests
from resources.lib import common

site = 'muzu'
headers = {'User-Agent':'iPhone'}

def get_videos(artist):
    videos = []
    country = common.get_muzu_country()
    if not country:
        country = get_country()
    url = 'http://www.muzu.tv/search/typeAhead/'
    headers.update({'X-Requested-With':'XMLHttpRequest'})
    params = {'country': country, 'term': artist}
    try:
        json_data = requests.get(url, headers=headers, params=params).json()
        for v in json_data:
            try:
                if v['isVideo']:
                    video_info = v['video']
                    name = video_info['ArtistName']
                    if artist.lower() == name.encode('utf-8').lower():
                        id = v['id']
                        title = video_info['Title']
                        image = video_info['Thumbnail_6']
                        duration = ''
                        try: duration = r['duration']
                        except: pass
                        if video_info['AssetCategoryIdentity'] == 1:
                            videos.insert(0, {'site':site, 'artist':[name], 'title':title, 'duration':duration, 'id':id, 'image':image})
            except:
                pass
    except:
        pass
    return videos
    
def get_video_url(id):
    video_url = None
    qv = get_qv(id)
    try:
        url = 'http://player.muzu.tv/player/requestVideo'
        params = {'ai':id, 'viewhash':'VBNff6djeV4HV5TRPW5kOHub2k', 'qv':qv}
        json_data = requests.get(url, headers=headers, params=params).json()
        video_url = json_data['url']
    except:
        pass
    return video_url
    
def get_qv(id):
    qv = '480'
    try:
        url = 'http://player.muzu.tv/player/playerVideos'
        params = {'ai': id}
        json_data = requests.get(url, headers=headers, params=params).json()
        for q in ['v720','v480','v360','v240']:
            if json_data[0][q]:
                qv = q.replace('v','')
                break
    except:
        pass
    return qv
        
def get_country():
    country = 'gb'
    url = 'http://muzu.tv/'
    try:
        r = requests.head(url, stream=True, headers=headers, allow_redirects=True)
        new_url = r.url
        spl = new_url.split('/')
        if len(spl) == 5:
            if len(spl[-2]) == 2:
                country = spl[-2]
    except:
        pass
    common.set_muzu_country(country)
    return country