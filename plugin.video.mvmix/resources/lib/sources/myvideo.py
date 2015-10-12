# -*- coding: utf-8 -*-

from resources.lib import simple_requests as requests
import json

site = 'myvideo'
base_url = 'https://papi.myvideo.de%s'
headers = {'Accept-Language': 'en_US',
            'X-PAPI-AUTH': '39927b3f31d7c423ad6f862e63d8436d954aecd0',
            'Host': 'papi.myvideo.de',
            'Connection': 'Keep-Alive',
            'User-Agent': 'iPad'}

def get_videos(artist):
    videos = []
    url = base_url % ('/myvideo-app/v1/tablet/search')
    params = {'query': artist}
    try:
        json_data = requests.get(url, headers=headers, params=params).json()
        screen_objects = json_data['screen']['screen_objects']
        for c in screen_objects:
            try:
                if c['title'] == 'Musik':
                    s = c['screen_objects']
                    for r in s:
                        name = r['format_title']
                        if name.encode('utf-8').lower() == artist.lower():
                            title = r['video_title']
                            id = r['link'].split('/')[-1]
                            image = r['image_url']
                            duration = ''
                            try: duration = r['duration']
                            except: pass
                            if duration and int(duration) > 120:
                                videos.append({'site':site, 'artist':[name], 'title':title, 'duration':duration, 'id':id, 'image':image})
            except:
                pass
    except:
        pass
    return videos
    
def get_video_url(id):
    video_url = None
    try:
        url = base_url % '/myvideo-app/v1/vas/video.json'
        params = {'clipid':id, 'method':'4'}
        json_data = requests.get(url, headers=headers, params=params).json()
        file = json_data['VideoURL']
        import re
        file_name = re.findall('(movie.+?/.+?/\d+)', file)
        if file_name:
            video_urls = ['http://is.myvideo.de/%s.mp4_hd.mp4' % file_name[0], 'http://is.myvideo.de/%s.mp4' % file_name[0]]
            video_url = check_file_type(video_urls)
        if not video_url: video_url = file
    except:
        pass
    return video_url

def check_file_type(urls):
    try:
        for u in urls:
            r = requests.head(u)
            type = r.headers.get('content-type')
            if type == 'video/mp4' or type == 'video/x-flv' or type == 'application/octet-stream' or type == 'application/x-mpegurl':
                return u
    except:
        pass