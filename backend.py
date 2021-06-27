import requests
import json


def print_roster():
	url = 'https://statsapi.web.nhl.com/api/v1/teams/10/roster'
	response = requests.get(url)
	json_data = response.json()
	roster = json_data['roster']
	for player in roster:
		name_data = player['person']
		position_data = player['position']
		print(player['jerseyNumber'], name_data['fullName'], position_data['abbreviation'])

def get_name():
	name = input("Enter full name of player: ")
	return name


def get_link(name):
	player_link = ''
	url = 'https://statsapi.web.nhl.com/api/v1/teams/10/roster'
	response = requests.get(url)
	json_data = response.json()
	roster = json_data['roster']
	for player in roster:
		data = player['person']
		if name in data['fullName']:
			player_link = data['link']
	return player_link
 

def is_goalie(name):
	url = 'https://statsapi.web.nhl.com/api/v1/teams/10/roster'
	response = requests.get(url)
	json_data = response.json()
	roster = json_data['roster']
	for player in roster:
		player_info = player['person']
		position_info = player['position']
		if (name in player_info['fullName']) and (position_info['code'] == 'G'):
			return True
	return False 

def get_goalie_stats(player_link):
	url = 'https://statsapi.web.nhl.com' + player_link + '/stats?stats=statsSingleSeason&season=20202021'
	response = requests.get(url)
	json_data = response.json()
	stats = json_data['stats']
	stats = stats[0]
	stats_list = stats['splits']
	stats_dict = stats_list[0]
	print("Wins = ", stats_dict['stat']['wins'])
	print("Losses = ", stats_dict['stat']['losses'])
	print("OT Losses = ", stats_dict['stat']['ot'])
	print("Save Percentage = ", stats_dict['stat']['savePercentage'])
	print("Goals Allowed = ", stats_dict['stat']['goalsAgainst'])
	print("Goals against average = ", stats_dict['stat']['goalAgainstAverage'])

def get_individual_stats(player_link):
	url = 'https://statsapi.web.nhl.com' + player_link + '/stats?stats=statsSingleSeason&season=20202021'
	response = requests.get(url)
	json_data = response.json()
	stats = json_data['stats']
	stats = stats[0]
	stats_list = stats['splits']
	stats_dict = stats_list[0]
	print("Goals = ", stats_dict['stat']['goals'])
	print("Assists = ", stats_dict['stat']['assists'])
	print("Points = ", stats_dict['stat']['points'])
	print("+/- = ", stats_dict['stat']['plusMinus'])
	print("Powerplay Goals = ", stats_dict['stat']['powerPlayGoals'])
	print("Shorthanded Goals = ", stats_dict['stat']['shortHandedGoals'])
	print("Hits = ", stats_dict['stat']['hits'])
	print("Blocked Shots = ", stats_dict['stat']['blocked'])


def print_stats():
	name = get_name()
	link = get_link(name)
	while(len(link) == 0):
		name = get_name()
		link = get_link(name)
	if(is_goalie(name)):
		get_goalie_stats(link)
	else:	
		get_individual_stats(link)

def print_standings_data():
	url = 'https://statsapi.web.nhl.com/api/v1/standings'
	response = requests.get(url)
	json_data = response.json()
	data = json_data['records']
	north_info = data[0]
	a = north_info['teamRecords']
	leafs_info = a[0]
	print("North Division Rank: ", leafs_info['divisionRank'])
	print("Games played = ", leafs_info['gamesPlayed'])
	print("Wins = ", leafs_info['leagueRecord']['wins'])
	print("Losses = ", leafs_info['leagueRecord']['losses'])
	print("OT losses = ", leafs_info['leagueRecord']['ot'])
	print("Points = ", leafs_info['points'])
	print("Goals scored = ", leafs_info['goalsScored'])
	print("Goals against = ", leafs_info['goalsAgainst'])

# print_standings_data()
print_roster()
# print_stats()

