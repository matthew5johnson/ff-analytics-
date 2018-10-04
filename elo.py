####  Instructions: change the week and season to calculate and input a new elo column into the sql matchuptable
week = 4
season = 2018

team = 1

for team in range(1,13):
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
    
    def week_checker(week, season):
        if week == 1:
            return 16
        else:
            return week - 1
    
    home_franchise = franchise_converter(team, season)
    sqlseason = season_checker(week, season)
    last_week = week_checker(week, season)
    two_weeks_ago = last_week - 1
    three_weeks_ago = two_weeks_ago - 1 # only needed for the weird consolation bracket that we did in 2015. With two teams that had a double bye?
    ### Here's the SQL part.
    import pymysql
    # Connect to the database
    con = pymysql.connect('')
    # Create a cursor to do things in the database
    cur = con.cursor()
    
    
    ### Get this week's opponent
    cur = con.cursor()
    cur.execute("SELECT opponent FROM matchuptable WHERE franchise=%s AND season=%s AND week=%s;", (home_franchise, season, week))
    opponent_tuple = cur.fetchall()
    if opponent_tuple != ():
        # this week's opponent
        opponent = str(opponent_tuple[0][0])
        # Commit the executed function to get home_elo from last week  
        con.commit()
        
        ### Get the home team's elo from last week
        cur.execute("SELECT elo FROM matchuptable WHERE franchise=%s AND season=%s AND week=%s;", (home_franchise, sqlseason, last_week))
        # elo of the home team from the prior week
        home_elo_tuple = cur.fetchall()
        con.commit() 
        ## If the home team was on bye last week (seeds 1 + 2 in week 14 or the 3rd place game teams in week 15), this if statement goes back one more week to find their most recent elo
        if home_elo_tuple == ():   # ((None,),)
            cur.execute("SELECT elo FROM matchuptable WHERE franchise=%s AND season=%s AND week=%s;", (home_franchise, sqlseason, two_weeks_ago))
            home_elo_tuple = cur.fetchall()
            con.commit()
        home_elo = float(home_elo_tuple[0][0])
        
        ### Get the opponent's elo from last week
        cur.execute("SELECT elo FROM matchuptable WHERE franchise=%s AND season=%s AND week=%s;", (opponent, sqlseason, last_week))
        opponent_elo_tuple = cur.fetchall()
        # this week's opponent's elo from the prior week
        con.commit()   
        ## If the opponent team was on bye last week (seeds 1 + 2 in week 14 or the 3rd place game teams in week 15), this if statement goes back one more week to find their most recent elo
        if opponent_elo_tuple == ():
            cur.execute("SELECT elo FROM matchuptable WHERE franchise=%s AND season=%s AND week=%s;", (opponent, sqlseason, two_weeks_ago))
            opponent_elo_tuple = cur.fetchall()
            con.commit()
        opponent_elo = float(opponent_elo_tuple[0][0])
        
        ### Get the result from the perspective of the home team
        cur.execute("SELECT result FROM matchuptable WHERE franchise=%s AND season=%s AND week=%s;", (home_franchise, season, week))
        result_tuple = cur.fetchall()
        # result of the matchup (W, L, or T) << elo won't change for a tie
        result = str(result_tuple[0][0])  
        con.commit()
        
        #hardcoded for week 15 of 2015
        #opponent_elo = 1038.71
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
        
        
        
        cur.execute("UPDATE matchuptable SET elo=%s WHERE franchise=%s AND season=%s AND week=%s;", (new_elo, home_franchise, season, week))
        con.commit()
        # Close the connection to our SQL Server
        con.close()
        
        # Makes it easier to know which teams have been done already while the program is running
        print('done with team {}'.format(team))
        
        print(new_elo)
            

        
        
    else: print('Team {} on bye or in 3rd place game in week {}'.format(team, week)) 
