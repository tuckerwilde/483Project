import nflgame
import csv

################ WHAT DO I WANT TO DO? ################
# 1. Explore top paid players vs. top performing players.
#   1.1 How to do that? First, start with the receivers, are there any of the top 50 players being played in the top receivers?



# Test File to see if we can print out the top fantasy scorers
# for the week 1, 2013.
def calculate_fantasy_points(player):

    """
    Possible stats:
        1. passing_att
        2. passing_twoptm - passing two points made
        3. passing_twopta - passing two points attempted
        4. passing_yds
        5. passing_cmp
        6. passing_ints
        7. passing_tds
        8. rushing_lngtd - longest run for a td
        9. rushing_tds
        10. rushing_twopta
        11. rushing_lng
        12. rushing_yds
        13. rushing_att
        14. rushing_twoptm

    Standard scoring for passing:
        TD Pass = 4pts
        Per 25 passing = 1pts
        2pt passing conversion = 2pts
        Int. thrown = -2pts

    Standard scoring for rushing:
        TD Rush = 6pts
        Every 10 rushing yards = 1pt
        2pt rushing conversion = 2pts
    """
    def_positions = ['OLB', 'MLB', 'ILB', 'DE', 'CB', 'S', 'DT', 'SS', 'LB', 'FS']
    score = 0
    if player.guess_position not in def_positions:
        score += player.passing_yds/25
        score += player.passing_twoptm * 2
        score += player.passing_tds * 4
        score += player.rushing_yds/10
        score += player.rushing_twoptm * 2
        #negatives
        score += player.passing_ints * (-2)

    return score


def create_dict_points(players):
    """
    :param players: A list of NFLGAME player class
    :return: A dictionary of players, and their respective fantasy points
    """

    output = {}
    for p in players:
        output[p.name] = [calculate_fantasy_points(p)]
    return output

def print_players(players):
    """
    :param players: Dictionary of players and their fantasy points.
    :return: None
    """
    for key, value in players.iteritems():
        if value != 0:
            if len(value) == 2:
                print key, value


# All the games week 1, of the 2013 season.
games = nflgame.games(2015)
players = nflgame.combine(games, plays=True)
out = create_dict_points(players.sort('receiving_tar').limit(50))
#print_players(out)

with open('salaries2016.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        if row[0] in out:
            out[row[0]].append(row[1])


print_players(out)


