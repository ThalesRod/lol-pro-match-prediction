import os
import requests
import json
import time
from bs4 import BeautifulSoup

url = "https://lol.fandom.com/wiki/CBLOL/2021_Season/Split_2/Match_History"

api_prefix = 'https://acs.leagueoflegends.com/v1/stats/game/'

team_acronyms = {
    'LOUD': 'LLL',
    'PaiN Gaming': 'PNG',
    'INTZ': 'ITZ',
    'Netshoes Miners': 'NMG',
    'KaBuM! e-Sports': 'KBM',
    'RED Canids': 'RED',
    'Rensga Esports': 'RSG',
    'FURIA Esports': 'FUR',
    'Flamengo Esports': 'FLA',
    'Vorax Liberty': 'VRX'
}

# In order to this script work well, fill this dictionary with valid browser request headers, including the cookies
real_browser_headers = {
}


source_code = requests.get(url)
parsed_url = BeautifulSoup(source_code.text, 'html.parser')
games = parsed_url.find_all('tbody')[4].findChildren("tr", recursive=False)[3:]

filesInDir = os.listdir('data/')

for game in games:
    team1 = team_acronyms[game.findChildren('td')[2].findChild('a')['title']]
    team2 = team_acronyms[game.findChildren('td')[3].findChild('a')['title']]

    # verifying if its already downloaded
    if (team1 + '-' + team2 + '.json') in filesInDir:
        continue

    location = api_prefix + game.findChildren('td')[-2].findChild('a')['href'].split('match-details/')[1]

    location_timeline = location.split('?')[0] + '/timeline?' + location.split('?')[1]

    print("[+] Downloading game: \'%s\'..." % (team1 + ' X ' + team2))

    filename = team1 + '-' + team2 + '.json'
    filename_timeline = team1 + '-' + team2 + '-timeline.json'

    print('[+] File: ' + filename)
    result = requests.get(location, headers=real_browser_headers)

    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)
        exit()
    else:
        with open("data/" + filename, "w") as json_output:
            json_output.write(json.dumps(result.json()))
            json_output.close()

    time.sleep(5)

    print('[+] File: ' + filename_timeline)
    result = requests.get(location_timeline, headers=real_browser_headers)

    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)
        exit()
    else:
        with open("data/" + filename_timeline, "w") as json_output:
            json_output.write(json.dumps(result.json()))
            json_output.close()

    time.sleep(5)

    print('[+] Success downloaded \'%s\'!\n' % (team1 + ' X ' + team2))