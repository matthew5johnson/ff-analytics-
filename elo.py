week = 15
season = 2015

team = 9

for team in range(9,10):
    def franchise_converter(number, season):
        if number == 1:
            return 'Matt & Ross'
        elif number == 2: 
            return 'Scott & James'
        elif number == 3:
            return 'Doug'
        elif number == 4:
            return 'Crockett'
        elif number == 5 and season == 2015:
            return 'Garner & Doyle'
        elif number == 5 and season > 2015:
            return 'Blake'
        elif number == 6: 
            return 'Kfish'
        elif number == 7: 
            return 'Kyle'
        elif number == 8: 
            return 'Gaudet & Cameron'
        elif number == 9:
            return 'Gilhop & MJ'
        elif number == 10:
            return 'Mitch'
        elif number == 11:
            return 'Nick & Mickey'
        elif number == 12:
            return 'Joseph & Mike'
    
    def season_checker(week, season):
        if week == 1:
            return season - 1
        else:
            return season  
    
    ## This is not going to find an elo for the two week 14 byes and the two week 15 third place participants.
    ## Easy. Just make a catch procedure for if the pull of my_elo or their_elo returns null to subtract another week
    def week_checker(week, season):
        if week == 1:
            return 16
        else:
            return week - 1
    
    home_franchise = franchise_converter(team, season)
    sqlseason = season_checker(week, season)
    last_week = week_checker(week, season)
    ### Here's the SQL part.
    import pymysql
    # Connect to the database
    con = pymysql.connect('')
    # Create a cursor to do things in the database
    cur = con.cursor()
    
    ### Get the home team's elo from last week
    cur.execute("SELECT elo FROM matchuptable WHERE franchise=%s AND season=%s AND week=%s;", (home_franchise, sqlseason, last_week))
    # elo of the home team from the prior week
    home_elo_tuple = cur.fetchall()
    #home_elo = float(home_elo_tuple[0][0])  
    con.commit()    
    
    print(home_elo_tuple)
    '''
    ### Get this week's opponent
    cur = con.cursor()
    cur.execute("SELECT opponent FROM matchuptable WHERE franchise=%s AND season=%s AND week=%s;", (home_franchise, season, week))
    opponent_tuple = cur.fetchall()
    # this week's opponent
    opponent = str(opponent_tuple[0][0])
    # Commit the executed function to get home_elo from last week  
    con.commit()    
    
    ### Get the opponent's elo from last week
    cur.execute("SELECT elo FROM matchuptable WHERE franchise=%s AND season=%s AND week=%s;", (opponent, sqlseason, last_week))
    opponent_elo_tuple = cur.fetchall()
    # this week's opponent's elo from the prior week
    opponent_elo = float(opponent_elo_tuple[0][0])  
    con.commit()    
    
    ### Get the result from the perspective of the home team
    cur.execute("SELECT result FROM matchuptable WHERE franchise=%s AND season=%s AND week=%s;", (home_franchise, season, week))
    result_tuple = cur.fetchall()
    # result of the matchup (W, L, or T) << elo won't change for a tie
    result = str(result_tuple[0][0])  
    con.commit()
    
    ### initialize elo constants
    k_factor = 15
    diff = abs(home_elo - opponent_elo)
    beta = 200
    r_1 = 10 ** (home_elo/beta)
    r_2 = 10 ** (opponent_elo/beta)
    e_1 = r_1 / (r_1 + r_2)
    #e_2 = r_2 / (r_1 + r_2) not needed here since this is for the opponent, and will be taken care of further down in the overall for loop
    
    if result == 'W':
        new_elo = home_elo + k_factor * (1 - e_1)
    elif result == 'L':
        new_elo = home_elo + k_factor * (0 - e_1)
    elif result == 'T':
        new_elo = home_elo + k_factor * (0.5 - e_1)
    
    
    
    # Use the cursor to execute a function. Here we insert all of our scraped and cleaned data
    #my_elo = cur.execute("SELECT elo FROM matchuptable WHERE franchise=(%s) AND season=(%s) AND week=(%s);", (sqlfranchise, sqlseason, last_week))
    #my_opponent = cur.execute("SELECT opponent FROM matchuptable WHERE franchise=(%s) AND season=(%s) AND week=(%s);", (sqlfranchise, season, week))
    #their_elo = cur.execute("SELECT elo FROM matchuptable WHERE franchise=(%s) AND season=(%s) AND week=(%s);", (my_opponent, sqlseason, last_week))
    
    # Close the connection to our SQL Server
    con.close()
    
    #cur.execute("INSERT INTO matchuptable (season, week, franchise, points_scored, points_against, result, margin, week_total, opponent, status, QB, PTS_QB, RB1, PTS_RB1, RB2, PTS_RB2, WR1, PTS_WR1, WR2, PTS_WR2, TE1, PTS_TE1, RB3, PTS_RB3, WR3, PTS_WR3, TE2, PTS_TE2, OFFENSE, DST, PTS_DST, K, PTS_K, total_points) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);", (season, week, franchise, points_scored, points_against, result, margin, week_total, opponent, status, QB, PTS_QB, RB1, PTS_RB1, RB2, PTS_RB2, WR1, PTS_WR1, WR2, PTS_WR2, TE1, PTS_TE1, RB3, PTS_RB3, WR3, PTS_WR3, TE2, PTS_TE2, OFFENSE, DST, PTS_DST, K, PTS_K, total_points))
    
    #diff = abs(my_elo - their_elo)
    
    
    # Makes it easier to know which teams have been done already while the program is running
    print('done with team {}'.format(team))
    
    print(new_elo)'''

'''
k_factor = 32

diff = my_rating

R_1 = 

win_expected =
loss_expected =



diff = float(other_rating) - float(rating)
f_factor = 2 * self.beta  # rating disparity
return 1. / (1 + 10 ** (diff / f_factor))
'''
