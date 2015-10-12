# -*- coding: utf-8 -*-

import xbmc,xbmcvfs
import json,os,re

from resources.lib import common

site = 'local'

def get_videos(name):
    videos = []
    if common.video_source() == 'Music Video Library':
        videos = get_videos_from_library(name)
    else:
        if common.video_path():
            videos = get_videos_from_folder(name)
    return videos
    
def get_video_url(id):
    return id

def get_videos_from_library(name):
    videos = []
    json_query = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "VideoLibrary.GetMusicVideos", "params": { "properties": [ "title", "artist", "runtime", "file", "streamdetails", "thumbnail" ] }, "id": "libMusicVideos"}')
    json_query = unicode(json_query, 'utf-8', errors='ignore')
    json_response = json.loads(json_query)
    if json_response.has_key('result') and json_response['result'] != None and json_response['result'].has_key('musicvideos'):
        for mv in json_response['result']['musicvideos']:
            try:
                artists = mv['artist']
                title = mv['title']
                id = mv['file'].encode('utf-8')
                duration = mv['runtime']
                image = mv['thumbnail']
                if artists[0].encode('utf-8').lower() == name.encode('utf-8').lower():
                    videos.append({'site':site, 'artist':artists, 'title':title, 'duration':duration, 'id':id, 'image':image})
            except:
                pass
    return videos

def get_videos_from_folder(name):
    videos = []
    dirs, files = xbmcvfs.listdir(common.video_path())
    for f in files:
        if f.endswith(('.strm','.webm','.mkv','.flv','.vob','.ogg','.avi','.mov','.qt','.wmv','.rm','.asf','.mp4','.m4v','.mpg','.mpeg','.3gp')):
            try:
                id = os.path.join(common.video_path(),f).encode('utf-8')
                filename = os.path.splitext(os.path.basename(id))[0]
                filename = re.sub('\_|\.', ' ', filename)
                match = filename.split(' - ')
                artist = match[0].strip()
                title = match[1].strip()
                if artist.encode('utf-8').lower() == name.lower():
                    videos.append({'site':site, 'artist':[artist], 'title':title, 'duration':'', 'id':id, 'image':''})
            except:
                pass
    return videos