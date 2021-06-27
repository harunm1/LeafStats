import tkinter as tk
from tkinter import *
import requests
from PIL import Image, ImageTk

HEIGHT = 800
WIDTH = 800

def print_roster():
	url = 'https://statsapi.web.nhl.com/api/v1/teams/10/roster'
	response = requests.get(url)
	json_data = response.json()
	roster = json_data['roster']
	roster_line = ''
	for player in roster:
		name_data = player['person']
		position_data = player['position']
		p = str(player['jerseyNumber']) + ' ' + str(name_data['fullName']) + ' ' + str(position_data['abbreviation'])
		roster_line += (p + '\n')
	output['text'] = roster_line

def print_standings_data():
	url = 'https://statsapi.web.nhl.com/api/v1/standings'
	response = requests.get(url)
	json_data = response.json()
	data = json_data['records']
	north_info = data[0]
	a = north_info['teamRecords']
	leafs_info = a[0]
	rank = "North Division Rank: " + str(leafs_info['divisionRank']) + '\n'
	games = "Games played = " + str(leafs_info['gamesPlayed']) + '\n'
	wins = "Wins = " + str(leafs_info['leagueRecord']['wins']) + '\n'
	losses = "Losses = " + str(leafs_info['leagueRecord']['losses']) + '\n'
	ot = "OT losses = " + str(leafs_info['leagueRecord']['ot']) + '\n'
	points = "Points = " + str(leafs_info['points']) + '\n'
	gf = "Goals scored = " + str(leafs_info['goalsScored']) + '\n'
	ga = "Goals against = " + str(leafs_info['goalsAgainst']) + '\n'
	team_line = rank + games + wins + losses + ot + points + gf + ga
	output['text'] = team_line


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

def get_goalie_stats(player_link):
	url = 'https://statsapi.web.nhl.com' + player_link + '/stats?stats=statsSingleSeason&season=20202021'
	response = requests.get(url)
	json_data = response.json()
	stats = json_data['stats']
	stats = stats[0]
	stats_list = stats['splits']
	stats_dict = stats_list[0]
	wins = "Wins = " + str(stats_dict['stat']['wins']) + '\n'
	losses = "Losses = " +  str(stats_dict['stat']['losses']) + '\n'
	ot_losses = "OT Losses = " + str(stats_dict['stat']['ot']) + '\n'
	save_percentage = "Save Percentage = " + str(stats_dict['stat']['savePercentage']) + '\n'
	goals_allowed = "Goals Allowed = " + str(stats_dict['stat']['goalsAgainst']) + '\n'
	goals_against_avg = "Goals against average = " + str(stats_dict['stat']['goalAgainstAverage']) + '\n'
	stats_line = wins + losses + ot_losses + save_percentage + goals_allowed + goals_against_avg
	output['text'] = stats_line
				  

def get_individual_stats(player_link):
	url = 'https://statsapi.web.nhl.com' + player_link + '/stats?stats=statsSingleSeason&season=20202021'
	response = requests.get(url)
	json_data = response.json()
	stats = json_data['stats']
	stats = stats[0]
	stats_list = stats['splits']
	stats_dict = stats_list[0]
	goals = "Goals = " + str(stats_dict['stat']['goals']) + '\n'
	assists = "Assists = " + str(stats_dict['stat']['assists']) + '\n'
	points = "Points = " + str(stats_dict['stat']['points']) + '\n'
	plus_minus = "+/- = " + str(stats_dict['stat']['plusMinus']) + '\n'
	pp_goals = "Powerplay Goals = " + str(stats_dict['stat']['powerPlayGoals']) + '\n'
	sh_goals = "Shorthanded Goals = " + str(stats_dict['stat']['shortHandedGoals']) + '\n'
	hits = "Hits = " + str(stats_dict['stat']['hits']) + '\n'
	blocked_shots = "Blocked Shots = " + str(stats_dict['stat']['blocked']) + '\n'
	stats_line = goals + assists + points + plus_minus + pp_goals + sh_goals + hits + blocked_shots
	output['text'] = stats_line

def print_stats(name):
	link = get_link(name)
	if(len(link) == 0):
		output['text'] = "Player not found!"
	if(is_goalie(name)):
		get_goalie_stats(link)
	else:	
		get_individual_stats(link)


root = tk.Tk()
root.title('Leafs Stats')

canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH)
canvas.pack()

background_image = Image.open('leafs.png')
resized = background_image.resize((HEIGHT, WIDTH), Image.ANTIALIAS)
leafs_pic = ImageTk.PhotoImage(resized)
background_label = tk.Label(root, image=leafs_pic)
background_label.place(relwidth=1, relheight=1)

frame = tk.Frame(root, bg='blue')
frame.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.3)

title = tk.Label(frame, text="Toronto Maple Leafs", fg='white', font=("Arial", 25), bg = 'blue')
title.pack()

roster_button = tk.Button(frame, text='Roster',command=lambda: print_roster())
roster_button.place(rely=0.20, relx=0.45)

team_stats_button = tk.Button(frame, text='Team Stats',command=lambda: print_standings_data())
team_stats_button.place(rely=0.35, relx=0.43)

label = tk.Label(frame, text="Enter player for individual stats below: ", bg='white')
label.place(rely=0.50, relx=0.30)

entry = tk.Entry(frame, bg='white')
entry.place(rely=0.65, relx=0.38)

search_button = tk.Button(frame, text="Search", bg="grey", command=lambda: print_stats(entry.get()))
search_button.place(rely=0.80, relx=0.45)

lower_frame = tk.Frame(root, bg='yellow')
lower_frame.place(relx=0.1, rely=0.4, relwidth=0.8, relheight=0.5)

output = tk.Label(lower_frame, bg='white')
output.place(relwidth=1, relheight=1)

root.mainloop()