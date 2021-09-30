import json
import os
import csv
from functools import reduce

dataset_file = 'cblol_data_updated_at_10.csv'
game_time = 10

table_header = [
  'game_id',
  'team1_total_gold',
  'team2_total_gold',
  'team1_total_kills',
  'team2_total_kills',
  'team1_total_buildings',
  'team2_total_buildings',
  'team1_total_dragons',
  'team2_total_dragons',
  'winner_team'
]

with open(dataset_file, 'w', encoding='UTF8') as file:
    writer = csv.writer(file)
    writer.writerow(table_header)
    file.close()

game_files = [ game_file for game_file in os.listdir('data') if len(game_file) == 12 ]
game_files.sort()

game_files_timeline = [ game_file_timeline for game_file_timeline in os.listdir('data') if len(game_file_timeline) == 21 ]
game_files_timeline.sort()

for game_file, game_file_timeline in zip(game_files, game_files_timeline):
  print("[+] Writing game: %s..." % game_file[:7])
  with open("data/" + game_file_timeline, "r") as read_file:
    data = json.load(read_file)

  with open("data/" + game_file, "r") as read_file:
    game_data = json.load(read_file)

  participants_gold = list([ participant['totalGold'] for participant in data['frames'][game_time]['participantFrames'].values() ])

  team1_total_gold = reduce(lambda val1, val2: val1 + val2, participants_gold[:5])
  team2_total_gold = reduce(lambda val1, val2: val1 + val2, participants_gold[5:])

  team1_total_kills = 0
  team2_total_kills = 0

  for frame in data['frames'][:game_time]:
    for event in frame['events']:
      if event['type'] == 'CHAMPION_KILL':
        if event['killerId'] in range(1, 6):
          team1_total_kills += 1
        elif event['killerId'] in range(6, 11):
          team2_total_kills += 1

  team1_total_buildings = 0
  team2_total_buildings = 0

  for frame in data['frames'][:game_time]:
    for event in frame['events']:
      if event['type'] == 'BUILDING_KILL' and event['buildingType'] == 'TOWER_BUILDING':
        if event['teamId'] == 200:
          team1_total_buildings += 1
        elif event['teamId'] == 100:
          team2_total_buildings += 1

  team1_total_dragons = 0
  team2_total_dragons = 0

  for frame in data['frames'][:game_time]:
    for event in frame['events']:
      if event['type'] == 'ELITE_MONSTER_KILL' and event['monsterType'] == 'DRAGON':
        if event['killerId'] in range(1, 6):
          team1_total_dragons += 1
        elif event['killerId'] in range(6, 11):
          team2_total_dragons += 1

  winner_team = 1 if game_data['teams'][0]['win'] == 'Win' else 2

  data_row = list([ game_data['gameId'], team1_total_gold, team2_total_gold, team1_total_kills, team2_total_kills, team1_total_buildings, team2_total_buildings, team1_total_dragons, team2_total_dragons, winner_team ])
  with open(dataset_file, 'a', encoding='UTF8') as file:
      writer = csv.writer(file)
      writer.writerow(data_row)
      file.close()