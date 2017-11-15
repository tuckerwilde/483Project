import nflgame

f = open("WinsLossesByTeam.csv", "w")

f.write("team,wins,losses\n")

teams = [
    ['ARI', 'Arizona', 'Cardinals', 'Arizona Cardinals'],
    ['ATL', 'Atlanta', 'Falcons', 'Atlanta Falcons'],
    ['BAL', 'Baltimore', 'Ravens', 'Baltimore Ravens'],
    ['BUF', 'Buffalo', 'Bills', 'Buffalo Bills'],
    ['CAR', 'Carolina', 'Panthers', 'Carolina Panthers'],
    ['CHI', 'Chicago', 'Bears', 'Chicago Bears'],
    ['CIN', 'Cincinnati', 'Bengals', 'Cincinnati Bengals'],
    ['CLE', 'Cleveland', 'Browns', 'Cleveland Browns'],
    ['DAL', 'Dallas', 'Cowboys', 'Dallas Cowboys'],
    ['DEN', 'Denver', 'Broncos', 'Denver Broncos'],
    ['DET', 'Detroit', 'Lions', 'Detroit Lions'],
    ['GB', 'Green Bay', 'Packers', 'Green Bay Packers', 'G.B.', 'GNB'],
    ['HOU', 'Houston', 'Texans', 'Houston Texans'],
    ['IND', 'Indianapolis', 'Colts', 'Indianapolis Colts'],
    ['JAC', 'Jacksonville', 'Jaguars', 'Jacksonville Jaguars', 'JAX'],
    ['KC', 'Kansas City', 'Chiefs', 'Kansas City Chiefs', 'K.C.', 'KAN'],
    ['LA', 'Los Angeles', 'Rams', 'Los Angeles Rams', 'L.A.'],
    ['MIA', 'Miami', 'Dolphins', 'Miami Dolphins'],
    ['MIN', 'Minnesota', 'Vikings', 'Minnesota Vikings'],
    ['NE', 'New England', 'Patriots', 'New England Patriots', 'N.E.', 'NWE'],
    ['NO', 'New Orleans', 'Saints', 'New Orleans Saints', 'N.O.', 'NOR'],
    ['NYG', 'Giants', 'New York Giants', 'N.Y.G.'],
    ['NYJ', 'Jets', 'New York Jets', 'N.Y.J.'],
    ['OAK', 'Oakland', 'Raiders', 'Oakland Raiders'],
    ['PHI', 'Philadelphia', 'Eagles', 'Philadelphia Eagles'],
    ['PIT', 'Pittsburgh', 'Steelers', 'Pittsburgh Steelers'],
    ['SD', 'San Diego', 'Chargers', 'San Diego Chargers', 'S.D.', 'SDG'],
    ['SEA', 'Seattle', 'Seahawks', 'Seattle Seahawks'],
    ['SF', 'San Francisco', '49ers', 'San Francisco 49ers', 'S.F.', 'SFO'],
    ['STL', 'St. Louis', 'Rams', 'St. Louis Rams', 'S.T.L.'],
    ['TB', 'Tampa Bay', 'Buccaneers', 'Tampa Bay Buccaneers', 'T.B.', 'TAM'],
    ['TEN', 'Tennessee', 'Titans', 'Tennessee Titans'],
    ['WAS', 'Washington', 'Redskins', 'Washington Redskins', 'WSH'],
]

all_teams = []
	
for t in teams:
	all_teams.append(t[0])

def scores_for_team(team_to_check):
	# Create a list to store each score
	game_scores_for = []
	game_scores_against = []
	win = 0
	loss = 0
	tie = 0

	# Get the games team played in the 2013 Regular Season
	games = nflgame.games_gen(2016, home=team_to_check, away=team_to_check, kind='REG')

	if games == None:
		return
	
	# Iterate through the games
	for g in games:
		# If team was home, add the score_home to the points for list and the score_away to the points against list
		if g.home == team_to_check:
			game_scores_for.append(g.score_home)
			game_scores_against.append(g.score_away)
		# If team was away, add the score_away to the points for list and the score_home to the points against list
		else:
			game_scores_for.append(g.score_away)
			game_scores_against.append(g.score_home)
	
		#loss
		if game_scores_against[-1] > game_scores_for[-1]:
			loss += 1
		#win
		elif game_scores_against[-1] < game_scores_for[-1]:
			win += 1
		#tie
		else:
			tie += 1
			
#	f.write(team_to_check + "," + str(sum(game_scores_for) - sum(game_scores_against)) + "\n")
#	print team_to_check, (sum(game_scores_for) - sum(game_scores_against))

	print team_to_check, "WINS: ", win, "LOSSES: ", loss
	f.write(team_to_check + "," + str(win) + "," + str(loss) + "\n")
	
for i in all_teams:
	scores_for_team(i)
