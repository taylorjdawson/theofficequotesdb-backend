from bs4 import BeautifulSoup
from urllib import request
from urllib.error import URLError, HTTPError
import re
from collections import  namedtuple
import json
import pickle
from urllib.parse import urlparse, parse_qs, unquote

def get_all_video_urls():
    with open('C:\\Users\\tjdaw\PycharmProjects\\theofficequotesdb-backend\misc\officeVidSiteUrls.pickle', 'rb') as f:
        urls = pickle.load(f)

    vid_url_dic = {

    }

    for url in urls:
        r = request.urlopen(url)
        soup = BeautifulSoup(r, "lxml")

        path = urlparse(url).path
        se, ep = re.match('\/s(?P<s>[0-9]{2})e(?P<e>[0-9]{2})', path).groups()


        link = soup.find_all('a', 'video1')[2]['data-youtube']
        vid_url_dic[se + ep] = link
        print("Completed: ", se, ep, "Link: ", link)
        # episode = 0
        # for episode in :
        #     episode += 1
        #     video = namedtuple('Video',['episode','season'])
        #     video.season = "{0:02d}".format(season)
        #     video.episode = "{0:02d}".format(episode)
        #
        #     try:
        #         r = request.urlopen("http://watchtheofficeonline.net/S{}E{}/".format(video.season, video.episode))
        #         soup = BeautifulSoup(r, "lxml")
        #         vid_url_dic[video.season + video.episode] = soup.find_all('a','video1')[2]['data-youtube']
        #
        #     except HTTPError as e:
        #         print("Error: ", e)
        #         print('Season: ' + video.season + " completed")
        #         break

    with open("episode_links", "w") as outfile:
        json.dump(vid_url_dic, outfile, sort_keys=True, indent=4)


get_all_video_urls()