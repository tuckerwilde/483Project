# Receiving Yards vs. Salaries
import nflgame
import csv

# Let's calculate the fantasy points
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
        15. receiving_tds
        16. receiving_yds
        17. receiving_twoptm

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
    score = 0
    score += player.passing_yds/25
    score += player.passing_twoptm * 2
    score += player.passing_tds * 4
    score += player.rushing_yds/10
    score += player.rushing_twoptm * 2
    score += player.receiving_yds/10
    score += player.receiving_tds*6
    score += player.receiving_twoptm*2
    #negatives
    score += player.passing_ints * (-2)

    return score

# Get the top 50 salaries, attach to the players.
salaries = {}
with open('salaries2017.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        # row[1] == name
        # row[4] == salary
        full = row[1].split("\\")
        full = full[0].split(" ")
        full = full[0][:1] + '.' + full[1]
        salary = row[4][1:]
        salaries[full] = salary

with open('top_passers_fantasy.csv', 'wb') as csvfile:
    writer = csv.writer(csvfile)
    games = nflgame.games(2016)
    players = nflgame.combine_game_stats(games)
    players = players.sort('passing_yds').limit(50)
    writer.writerow(["name","salary","passing_att", "passing_cmp","passing_yds", "passing_ints", "passing_tds", "fantasy_points"])
    for p in players:
        if p.name in salaries:
            writer.writerow([p.name, salaries[p.name], 
                p.passing_att, p.passing_cmp, p.passing_yds,
                p.passing_ints, p.passing_tds, calculate_fantasy_points(p)])

