"""
Programmer: Cody Sigvartson
Description: Generates a .csv file containing the top players by both year and week
            for fantasy football positions (QB, RB, WR, TE, K, Defense). Top players
            are calculated using a custom scoring system based on the standard scoring
            system used in the American Fantasy Football leagues. All player stat data
            is taken from the NFL Game Center JSON data from the nflgame API.
"""
import nflgame
import csv
import os

# All regular season weeks
game_weeks = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17]
# Seasons 2010-2016
years = [2010,2011,2012,2013,2014,2015,2016,2017]

my_csv = open("top_players.csv","a")
# define table features
#my_csv.write("player,position,team,week,year,passing_td,passing_yd,perc_throws,rushing_td,rushing_yd,rec_td,rec_yd,receptions,fgmd,fgyd,perc_fg,tackles,sacks,ints\n")

# calculates a score for offensive players based on NFL Fantasy Point Scoring System
def calculate_offensive_score(player):
    """
    Relevant offensive stats:
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
        15. fumbles_lost
        16. fumbles_trcv

    Standard scoring for passing:
        TD Pass = 4pts
        Per 25 passing = 1pts
        2pt passing conversion = 2pts
        Int. thrown = -2pts

    Standard scoring for rushing:
        TD Rush = 6pts
        Every 10 rushing yards = 1pt
        2pt rushing conversion = 2pts

    Standard scoring for receiving:
        Reception = 1pt
        Every 10 receiving yards = 1pt
        Each receiving TD = 6pts
        Each 2-point conversion = 2pts

    Standard scoring for fumbles:
        Fumble recovered for TD: 6pts
        Each lost fumble = -2pts
    """

    score = 0

    score += player.passing_yds/25
    score += player.passing_twoptm * 2
    score += player.passing_tds * 4
    score += player.rushing_yds/10
    score += player.rushing_twoptm * 2
    score += player.fumbles_trcv * 6
    score += player.receiving_rec
    score += player.receiving_yds/10
    score += player.receiving_tds * 6
    score += player.receiving_twoptm * 2
    #negatives
    score += player.passing_ints * (-2)
    score += player.fumbles_lost * (-2)

    return score


def calculate_k_score(player):
    """
     Relevant kicker stats:
        1. kicking_fgm
        2. kicking_fgyds

    Standard scoring for kicking:
        PAT made = 1pt
        Every 30 yds kicked for FG = 1pt
    """
    score = 0

    score += player.kicking_fgm
    score += player.kicking_fgyds/30

    return score


def calculate_def_score(player):
    """
         Relevant defensive stats:
            1. defensive_tkl
            2. defense_ast
            3. defensive_sk
            4. defensive_int
            5. defensive_ffum
            6. fumbles_rcv
            7. fumbles_trcv

        Standard scoring for defense:
            Solo tackle: 1pt
            Assisted tackle: 0.5pt
            Each sack: 2pts
            Each interception: 3pts
            Forced fumble: 3pts
            Recovered fumble: 3pts
            Defensive TD: 6pts
        """
    score = 0

    score += player.defense_tkl
    score += player.defense_ast * .5
    score += player.defense_sk * 2
    score += player.defense_int * 3
    score += player.defense_ffum * 3
    score += player.fumbles_rcv * 3
    score += player.fumbles_trcv * 6

    return score


# top QB is defined as the QB with highest total score from calculate_offensive_score()
def get_top_qb(week,year):
    best_score = -1000
    games = nflgame.games(year,week=week)
    players = nflgame.combine_game_stats(games)
    for p in players:
        if p.guess_position == 'QB':
            score = calculate_offensive_score(p)
            if score > best_score:
                best_score = score
                player = p.name
                team = p.team
                passing_td = p.passing_tds
                passing_yd = p.passing_yds
                pass_cmp = p.passing_cmp
                pass_att = p.passing_att
                if pass_att == 0: pass_att = 1
                percent_made = (pass_cmp/float(pass_att))*100
    if type(week) is list:
        my_csv.write(str(player.encode("ascii"))+",QB,"+str(p.team)+",ALL,"+str(year)+','+str(passing_td)+','+
            str(passing_yd)+','+str(percent_made)+",0,0,0,0,0,0,0,0,0,0,0\n")
    else:
        my_csv.write(str(player.encode("ascii")) + ",QB," + str(p.team) + ',' + str(week) +',' + str(year) + ',' + str(passing_td) + ',' +
            str(passing_yd) + ',' + str(percent_made) + ",0,0,0,0,0,0,0,0,0,0,0\n")
    return {player.encode("ascii"):[passing_td, passing_yd,percent_made]}


# top RB is defined as the player with highest total score from calculate_offensive_score()
def get_top_rb(week,year):
    best_score = -1000
    games = nflgame.games(year, week=week)
    players = nflgame.combine_game_stats(games)
    for p in players:
        if p.guess_position == 'RB':
            score = calculate_offensive_score(p)
            if score > best_score:
                best_score = score
                player = p.name
                team = p.team
                rushing_td = p.rushing_tds
                rushing_yd = p.rushing_yds
    if type(week) is list:
        my_csv.write(str(player.encode("ascii"))+",RB,"+str(team)+",ALL,"+str(year)+",0,0,0,"+str(rushing_td)+','+
                    str(rushing_yd)+",0,0,0,0,0,0,0,0,0\n")
    else:
        my_csv.write(str(player.encode("ascii")) + ",RB," + str(team) + ',' + str(week) + ',' + str(year) + ",0,0,0," + str(rushing_td) + ',' +
                    str(rushing_yd) + ",0,0,0,0,0,0,0,0,0\n")
    return {player.encode("ascii"): [rushing_td, rushing_yd]}


# top WR is defined as the player with highest total score from calculate_offensive_score()
def get_top_wr(week,year):
    best_score = -1000
    games = nflgame.games(year, week=week)
    players = nflgame.combine_game_stats(games)
    for p in players:
        if p.guess_position == 'WR':
            score = calculate_offensive_score(p)
            if score > best_score:
                best_score = score
                player = p.name
                team = p.team
                receiving_td = p.receiving_tds
                receiving_yd = p.receiving_yds
                receptions = p.receiving_rec
    if type(week) is list:
        my_csv.write(str(player.encode("ascii"))+",WR,"+str(team)+",ALL,"+str(year)+",0,0,0,0,0,"+str(receiving_td)+','+
                     str(receiving_yd)+','+str(receptions)+",0,0,0,0,0,0\n")
    else:
        my_csv.write(str(player.encode("ascii")) + ",WR," + str(team) + ',' + str(week) + ',' + str(year) + ",0,0,0,0,0," + str(receiving_td) + ',' +
                     str(receiving_yd) + ',' + str(receptions) + ",0,0,0,0,0,0\n")
    return {player.encode("ascii"): [receiving_td, receiving_yd, receptions]}


# top TE is defined as the player with highest total score from calculate_offensive_score()
def get_top_te(week,year):
    best_score = -1000
    games = nflgame.games(year, week=week)
    players = nflgame.combine_game_stats(games)
    for p in players:
        if p.guess_position == 'TE':
            score = calculate_offensive_score(p)
            if score > best_score:
                best_score = score
                player = p.name
                team = p.team
                receiving_td = p.receiving_tds
                receiving_yd = p.receiving_yds
                receptions = p.receiving_rec
    if type(week) is list:
        my_csv.write(str(player.encode("ascii"))+",TE,"+str(team)+",ALL,"+str(year)+",0,0,0,0,0,"+str(receiving_td)+','+
                     str(receiving_yd)+','+str(receptions)+",0,0,0,0,0,0\n")
    else:
        my_csv.write(str(player.encode("ascii")) + ",TE," + str(team) + ',' + str(week) + ',' + str(year) + ",0,0,0,0,0," + str(receiving_td) + ',' +
                     str(receiving_yd) + ',' + str(receptions) + ",0,0,0,0,0,0\n")
    return {player.encode("ascii"): [receiving_td, receiving_yd, receptions]}


# top K is defined as the player with highest total score from calculate_offensive_score()
def get_top_k(week,year):
    best_score = -1000
    games = nflgame.games(year, week=week)
    players = nflgame.combine_game_stats(games)
    for p in players:
        if p.guess_position == 'K':
            score = calculate_k_score(p)
            if score > best_score:
                best_score = score
                player = p.name
                team = p.team
                kicking_totfgm = p.kicking_fgm
                kicking_fga = p.kicking_fga
                kicking_fgyd = p.kicking_fgyds
                if kicking_fga == 0: kicking_fga = 1
                percent_made = (kicking_totfgm/float(kicking_fga))*100

    if type(week) is list:
        my_csv.write(str(player.encode("ascii"))+",K,"+str(team)+",ALL,"+str(year)+",0,0,0,0,0,0,0,0,"+
                     str(kicking_totfgm) + ',' + str(kicking_fgyd) + ',' + str(percent_made) + ",0,0,0\n")
    else:
        my_csv.write(str(player.encode("ascii")) + ",K," + str(team) + ',' + str(week) + ',' + str(year) + ",0,0,0,0,0,0,0,0," +
                     str(kicking_totfgm) + ',' + str(kicking_fgyd) + ',' + str(percent_made) + ",0,0,0\n")
    return {player.encode("ascii"): [kicking_totfgm, kicking_fgyd, percent_made]}


def get_top_def_players(week,year):
    best_score = -1000
    all_players = []
    def_positions = ['OLB', 'MLB', 'ILB', 'DE', 'CB', 'S', 'DT', 'SS', 'LB', 'FS']
    games = nflgame.games(year, week=week)
    players = nflgame.combine_game_stats(games)
    for p in players:
        if p.guess_position in def_positions:
            score = calculate_def_score(p)
            if score > best_score:
                best_score = score
                player = p.name
                position = p.guess_position
                team = p.team
                tackles = p.defense_tkl
                sacks = p.defense_sk
                ints = p.defense_int
    if type(week) is list:
        my_csv.write(str(player.encode("ascii")) + ',' + str(position) + ',' + str(team) + ",ALL," + str(year) + ",0,0,0,0,0,0,0,0,0,0,0," +
                     str(tackles) + ',' + str(sacks) + ',' + str(ints) + '\n')
    else:
        my_csv.write(
            str(player.encode("ascii")) + ',' + str(position) + ',' + str(team) + ',' + str(week) + ',' + str(year) + ",0,0,0,0,0,0,0,0,0,0,0," +
            str(tackles) + ',' + str(sacks) + ',' + str(ints) + '\n')
    return {player.encode("ascii"):[tackles,sacks,ints]}


# retrieves the top player for a given position, week, and year
def get_top_player(week, year, position):
    if position == 'QB':
        return get_top_qb(week,year)
    elif position == 'RB':
        return get_top_rb(week,year)
    elif position == 'WR':
        return get_top_wr(week,year)
    elif position == 'TE':
        return get_top_te(week,year)
    elif position == 'K':
        return get_top_k(week,year)
    else:
        return get_top_def_players(week,year)


### MAIN ###

def main():
    top_players = []
    #for year in years:
        #for week in game_weeks:
            # top_players.append(get_top_player(game_weeks,year,'QB'))
            # top_players.append(get_top_player(game_weeks, year, 'RB'))
            # top_players.append(get_top_player(game_weeks, year, 'WR'))
            # top_players.append(get_top_player(game_weeks, year, 'TE'))
            # top_players.append(get_top_player(game_weeks, year, 'K'))
            # top_players.append(get_top_player(game_weeks,year,'DEF'))
    top_players.append(get_top_player(game_weeks, 2017, 'QB'))
    top_players.append(get_top_player(game_weeks, 2017, 'RB'))
    top_players.append(get_top_player(game_weeks, 2017, 'WR'))
    top_players.append(get_top_player(game_weeks, 2017, 'TE'))
    top_players.append(get_top_player(game_weeks, 2017, 'K'))
    top_players.append(get_top_player(game_weeks, 2017, 'DEF'))
    for dict in top_players:
        for k,v in dict.iteritems():
            print k,v



if __name__ == "__main__":
    main()