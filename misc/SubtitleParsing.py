import re

import pysrt
import os, io
import json


quotes = {'lines' : {}}

number = {
    '01': 'one',
    '02': 'two',
    '04': 'four',
    '05': 'five',
    '03': 'three',
    '06': 'six',
    '07': 'seven',
    '08': 'eight',
    '09': 'nine',
    '10': 'ten',
    '11': 'eleven',
    '12': 'twelve',
    '13': 'thirteen',
    '14': 'fourteen',
    '15': 'fifteen',
    '16': 'sixteen',
    '17': 'seventeen',
    '18': 'eighteen',
    '19': 'nineteen',
    '20': 'twenty',
    '21': 'twenty-one',
    '22': 'twenty-two',
    '23': 'twenty-three',
    '24': 'twenty-four',
    '25': 'twenty-five'

}

def convertFilesToUTF8(folderPath):
    folderPath = os.path.join(os.path.expanduser("~"),
                              'PycharmProjects\\theofficequotesdb-backend\Subtitles\TheOfficeUS\\' + folderPath)
    for (dirname, dirs, files) in os.walk(folderPath):
        for filename in files:
            with io.open(folderPath + '/' + filename, 'r') as f:
                text = f.read()
                f.close()
            with io.open(folderPath + '/' +filename, 'w', encoding='utf8') as f:
                f.write(text)
                f.close()
            print("Converted:", filename)

def quoteJSON(line_id, time, line, season, episode):
    (min, sec) = time
    return {
        'id' : line_id,
        'line' : line,
        'time' : {
                'minutes' : min,
                'seconds' : sec
        },
        'season' : {
            'text': season,
            'number': line_id[:2]
        },
        'episode' : {
            'text': episode,
            'number': line_id[2:4]
        },
    }

def subtitlesToJson(subtitles, season, episode):
    for subtitle in subtitles:
        time = (subtitle.start.minutes, subtitle.start.seconds)
        line = re.sub('\n', ' ', subtitle.text)
        line_id = season + episode + '{0:06d}'.format(subtitle.index)
        quotes['lines'][line_id] = quoteJSON(line_id, time, line, number[season], number[episode])

def subtitlesFolderWalk(folderPath):
    episodes = []


    folderPath = os.path.join(os.path.expanduser("~"), 'PycharmProjects\\theofficequotesdb-backend\Subtitles\TheOfficeUS\{}'.format(folderPath))

    for (dirname, dirs, files) in os.walk(folderPath):
        episodes = files

    for episode in episodes:
        subs = pysrt.open(folderPath + '\\' + episode, encoding='utf-8')
        season, episode = re.match(r'(?P<season>[0-9]{2}){1}(?P<episode>[0-9]{2}){1}', episode).groups()

        subtitlesToJson(subs, season, episode)

    with open('quote_db_s2.json', 'w') as outfile:
        json.dump(quotes, outfile, sort_keys=True, indent=4)

def renameFiles(folderPath):
    se = '0'+ folderPath[-1]
    episodes = []
    folderPath = os.path.join(os.path.expanduser("~"),
                              'PycharmProjects\\theofficequotesdb-backend\Subtitles\TheOfficeUS\\' + folderPath)
    for (dirname, dirs, files) in os.walk(folderPath):
        episodes = files

    filenames = getEpisodeId(se)

    for i in range(len(episodes)):
        ep = re.match('S04E(?P<ep>[0-9]{2})',episodes[i]).group('ep')
        # ep = re.match('The Office \[%s.(?P<ep>[0-9]{2})\]' % se, episode).group('ep')
        os.rename(folderPath + '\\' + episodes[i], folderPath + '\\' + '{0:}{1:}'.format(se, ep))

def getEpisodeId(se):
    with open('C:\\Users\\tjdaw\PycharmProjects\\theofficequotesdb-backend\misc\episode_links', 'rb') as fb:
        ep_links = json.load(fb)
        ids = []
        for (id, link) in ep_links.items():
            if re.match('%s'%se, id):
                ids.append(id)
        ids.sort()
        return(ids)

# renameFiles('Season2')

# TODO: IMPORTANT DO NOT OVERWRITE ONLY APPEND. I have made changes to some quotes in the json file
renameFiles('Season4')
# print(getEpisodeId('06'))
# convertFilesToUTF8('Season3')
# subtitlesFolderWalk('Season2')