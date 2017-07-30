from bs4 import BeautifulSoup
from urllib import request
from urllib.error import URLError, HTTPError
import re
from collections import  namedtuple
import json
def get_all_video_urls():
    vid_url_dic = {

    }

    for season in range(1,10):
        episode = 0
        while True:
            episode += 1
            video = namedtuple('Video',['episode','season'])
            video.season = "{0:02d}".format(season)
            video.episode = "{0:02d}".format(episode)

            try:
                r = request.urlopen("http://watchtheofficeonline.net/S{}E{}/".format(video.season, video.episode))
                soup = BeautifulSoup(r, "lxml")
                vid_url = re.match('<a class="video1" data-youtube="(?P<video_url>.*)" href="#">G Drive</a>',
                                   str(soup.find_all('a','video1')[2]))
                try:
                    vid_url_dic[video.season + video.episode] = vid_url.group('video_url')
                except AttributeError:
                    print('Issue processing url: ' + "http://watchtheofficeonline.net/S{}E{}/".format(video.season, video.episode))
            except HTTPError as e:
                print('Season: ' + video.season + " completed")
                break
    with open("episode_links", "w") as outfile:
        json.dump(vid_url_dic, outfile, sort_keys=True, indent=4)


get_all_video_urls()