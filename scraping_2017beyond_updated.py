from bs4 import BeautifulSoup
from selenium import webdriver
import re



## Welcome: Last updated for the 2018 season.
# FLEX Note: 2017 is the first year that the flex position is difinitively accounted for. The RB3, WR3, TE2 slot is FLEX

###  Instructions !!!
### IF USING FOR 2017 !!! GO CHANGE THE INDICES in points_scored points_against from [1] to [2]. Then change back and save when done

# Before you begin: if it's a new year, use the test_scrape.py program to make sure
# that none of the html tags that we're using to parse have changed. Also important to check to see
# if the cell indexing is still correct.

# The inputs: !!! Put in the correct week and season. Expecting to scrape once per week as the season goes along
week = 10      #2 starts us at week 1; Adding 1 to every week for this index has been taken care of in the specify_week var below
season = 2018


###  Instructions !!! 
# WEEK 14: Alter team # and range of this for loop for WEEK 14. Exclude the two 2 bye teams.  
    ## Why exclude them? Because they don't have a quickboxscore on bye weeks, so this program can't handle them 
# WEEK 15: Remember to go into the SQL to delete the two participants in the 3rd place game in week 15. Only the week 16 3rd place game counts. You could exclude them from here using the team numbers in the for loop just like for week 14, but the program actually takes their data since they have a quickboxscore, and I think it's easier to delete the two entries in SQL than to mess with the for loop here in python. Either way works though


# for loop over the team  for team in range(1,11)
team = 1
###  You shouldn't need to change anything below this point
# years 2011-2015 inclusive = range(1,11) for 10 teams ;; years 2016- = range(1,13) for 12 teams
for team in range(1,13):
    ### Input the url of the franchise's schedule page
    boxscore_url = "" % (team, week, season)
    schedule_url_template = "" % (team, season)
    
    ### Here's the first part of our program. We're scraping player position, name, and points from the quickboxscore.
    ### If the webdriver takes too long to load and runs into a w88.espn... loading thing, just refresh the page and it'll eventually work
    chrome_path = r""
    driver = webdriver.Chrome(chrome_path)
    driver.get(boxscore_url)
    html = driver.page_source
    soup = BeautifulSoup(html, "html5lib") # 'lxml' wasn't working: "FeatureNotFound: Couldn't find a tree builder with the features you requested: lxml. Do you need to install a parser library?"
    
    # need this for all home players
    # This finds the table of the franchise in question (according to the team variable above) and puts it into a variable
    home_team_table = soup.find('table', attrs={'class':'playerTableTable tableBody',
                                      'id': 'playertable_0'})
    # NOT USED in the current implementation. Leaving as a reminder that you can take opponent's score
    opponent_team_table = soup.find('table', attrs={'class':'playerTableTable tableBody',
                                      'id': 'playertable_1'})
    # loop through every row in the player table, and store each cell in a list. Storing as a list is important
    # because it makes indexing the data much easier in later steps
    player_cells = []
    for player_row in home_team_table.findAll("tr"):
        player_cells.append(player_row.findAll("td"))
    # close the webdriver browser
    driver.close()
    
    # Function used to pass a string of text into and spit out the position of the player
    def position_identifier(text):
        if 'QB' in text:
            return 'QB'
        if 'RB' in text:
            return 'RB'
        if 'WR' in text:
            return 'WR'
        if 'TE' in text:
            return 'TE'
        if 'D/ST' in text:
            return 'D/ST'
        # For when a position is left blank by not starting a player
        if text == '':
            return ''
        else:
            return 'K'
    
    # EXAMPLE CASE: Nick & Mickey 2017 week 9
    # To convert the points '' from a bye or missing player to a zero. Avoids throwing an error when trying to convert to float when putting into the PTS_K variable
    def convert_blank_points(points_raw):
        if points_raw == '':
            return '0'
        else:
            return points_raw
    
    
    ### Players start being found in player_cells[3]. Increment through a for loop range(3,12) (to the 11th index inclusive)
    performance_list = []
    # Starting at 3 because that's the first cell where players show up
    m = 3   # for m in range(3,12)
    for m in range(3,12):
        player_name = ''.join(re.findall(r'(?<=teamid="-2147483648">)[^<]*', str(player_cells[m]))) # ?<= is a lookbefore, and it takes [^<]* which is all characters that aren't a <   ; so this gives us the player name. Could make it much more specific with something like [a-zA-Z-\s]*, but keeping it generic for now
        string_position = ''.join(re.findall(r'(?<=%s</a>)[*,\sa-z/A-Z]*' % player_name, str(player_cells[m]))) #2018 note: this was the old re that didn't account for the injury asterisk [,\sa-z/A-Z]* . I in 2018 I added the [*] to this re.   ; INTERMEDIATE STEP: This is the string we're feeding into the position identifier below. Wanted to make this string as short and accurate as possible so there is no external noise for the identifier function
        position = position_identifier(string_position) # Feed the string from above into our position_identifier function to get the position
        points_raw = ''.join(re.findall(r'(?<=appliedPointsProGameFinal">)[^<]*', str(player_cells[m]))) # #[0-9.-]* might be a more precise implementation, but switching to the more general one for ease of use.
        points = convert_blank_points(points_raw) # Needed this for the special example case explained above the function.
        performance_list.append([position, player_name, points]) # Create a list of the 3 attributes for each player

        
    QB = 'empty'
    PTS_QB = 0
    RB1 = 'empty'
    PTS_RB1 = 0
    RB2 = 'empty'
    PTS_RB2 = 0
    WR1 = 'empty'
    PTS_WR1 = 0
    WR2 = 'empty'
    PTS_WR2 = 0
    TE1 = 'empty'
    PTS_TE1 = 0
    RB3 = 'empty'
    PTS_RB3 = 0
    WR3 = 'empty'
    PTS_WR3 = 0
    TE2 = 'empty'
    PTS_TE2 = 0
    DST = 'empty'
    PTS_DST = 0
    K = 'empty'
    PTS_K = 0
    
    # EXAMPLE CASE: Cameron & Gaudet 2017 week 3
    # This is tripped to 'full' in the case of an open slot that results from a player not being started
    # This method wasn't necessary in the pre-2017 iteration of this scraper since 
    # the list of players on the quickboxscore was just shortened by the number of players not started.
    # The 2017+ box scores leave an open cell for unstarted players, meaning that we need to tell the program what to do with that blank cell
    # Using the pre-'17 version of this scraper, the position identifier was classifying the empty cell
    # as 'K' since the else statement was so vague. Cleared that up to account for an empty cell in this version
    bugchecker_variable = 'empty'
    
    
    i = 0 #for i in range(0,9) because there are 9 players 
    for i in range(0,9):
        if performance_list[i][0] == 'QB':
            QB = performance_list[i][1]
            PTS_QB = float(performance_list[i][2])
        elif performance_list[i][0] == 'RB' and RB1 == 'empty':
            RB1 = performance_list[i][1]
            PTS_RB1 = float(performance_list[i][2])
        elif performance_list[i][0] == 'RB' and RB2 == 'empty':
            RB2 = performance_list[i][1]
            PTS_RB2 = float(performance_list[i][2])
        elif performance_list[i][0] == 'WR' and WR1 == 'empty':
            WR1 = performance_list[i][1]
            PTS_WR1 = float(performance_list[i][2])
        elif performance_list[i][0] == 'WR' and WR2 == 'empty':
            WR2 = performance_list[i][1]
            PTS_WR2 = float(performance_list[i][2])
        elif performance_list[i][0] == 'TE' and TE1 == 'empty':
            TE1 = performance_list[i][1]
            PTS_TE1 = float(performance_list[i][2])
        elif performance_list[i][0] == 'RB' and RB3 == 'empty':
            RB3 = performance_list[i][1]
            PTS_RB3 = float(performance_list[i][2])
        elif performance_list[i][0] == 'WR' and WR3 == 'empty':
            WR3 = performance_list[i][1]
            PTS_WR3 = float(performance_list[i][2])
        elif performance_list[i][0] == 'TE' and TE2 == 'empty':
            TE2 = performance_list[i][1]
            PTS_TE2 = float(performance_list[i][2])
        elif performance_list[i][0] == 'D/ST' and DST == 'empty':
            DST = performance_list[i][1]
            PTS_DST = float(performance_list[i][2])
        elif performance_list[i][0] == 'K' and K == 'empty':
            K = performance_list[i][1]
            PTS_K = float(performance_list[i][2])
        else: 
            bugchecker_variable = 'full'
            
    
    OFFENSE = (PTS_QB + PTS_RB1 + PTS_RB2 + PTS_WR1 + PTS_WR2 + PTS_TE1 + PTS_RB3 + PTS_WR3 + PTS_TE2)
    total_points = OFFENSE + PTS_DST + PTS_K
        
    
    
    
    ## ### to find everything from the schedule page ### ##
    
    
    ### This is the second chunk of the program. The webdriver will open a browser with the team's schedule page.
    ### We use this to get opponent info, but get scores from here too. So it provides a good bases to compare the 
    ### Calculated scores from the first chunk (total_points just above) to what we get from here
    chrome_path = r""
    driver = webdriver.Chrome(chrome_path)
    driver.get(schedule_url_template)
    html = driver.page_source
    soup = BeautifulSoup(html, "html5lib") # 'lxml' wasn't working: "FeatureNotFound: Couldn't find a tree builder with the features you requested: lxml. Do you need to install a parser library?"
    
    # If one of these snippets is in the cell we give the function, it'll output the full/formal franchise name
    # Make sure the snippets are unique to the one franchise
    def opponent_identification(text):
        if 'Ross' in text:
            return 'Matt & Ross'    
        if 'Scott' in text:
            return 'Scott & James'    
        if 'Doug' in text:
            return 'Doug'    
        if 'godlegend' in text:
            return 'Crockett'    
        if 'Fischer' in text:
            return 'Kfish'    
        if 'Kyle' in text:
            return 'Kyle'    
        if 'john gaudet' in text:
            return 'Gaudet & Cameron'    
        if 'Pohlig' in text:
            return 'Gilhop & MJ'    
        if 'Mitch' in text:
            return 'Mitch'
        if 'Blake' in text:
            return 'Blake'
        if 'Graphia' in text:
            return 'Nick & Mickey'
        if 'Joseph' in text:
            return 'Joseph & Mike'
    
    ## This finds the table containing the whole schedule. The exact name of the table and class are liable to change annually
    table = soup.find('table', attrs={'class':'tableBody'})
    
    opponent_cells = [] # initiate a list to store all of the data from the schedule table derived from the for loop below
    # Loop through the schedule table, and put every week's worth of data into a list within cells var
    for table_row in table.findAll("tr"):
        opponent_cells.append(table_row.findAll("td"))
    
    # We get our result based on the difference in points
    def result_generator(margin):
        if margin < 0:
            return 'L'     
        if margin == 0:
            return 'T'
        if margin > 0:
            return 'W'
            
    
    ## Make sure this stays updated with franchises according to their number. Used for identifying the home franchise
    def franchise_identification(number, year):
        if number == 1:
            return 'Matt & Ross'
        elif number == 2: 
            return 'Scott & James'
        elif number == 3:
            return 'Doug'
        elif number == 4:
            return 'Crockett'
        elif number == 5:
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
    
    ### These are the 3 new functions
    def update_wins():
        if week == 1:
            if result_generator(margin) == 'W':
                return(1)
            else:
                return(0)
        else:
            import pymysql
            # Connect to the database
            con = pymysql.connect()
            # Create a cursor to do things in the database
            cur = con.cursor()
            # Use the cursor to execute a function. Here we insert all of our scraped and cleaned data
            cur.execute("SELECT wins FROM matchuptable WHERE franchise=%s AND week=%s AND season=%s;", (franchise, week-1, season))
            wins_tuple = cur.fetchall()
            # Commit the executed function
            con.commit()
            # Close the connection to our SQL Server
            con.close()
            ##################### Change this accordingly. Just need the number of wins from previous week
            previous_wins = wins_tuple[0]
                
            if result_generator(margin) == 'W':
                return(previous_wins + 1)
            else:
                return(previous_wins)
                
    def update_losses():
        if week == 1:
            if result_generator(margin) == 'L':
                return(1)
            else:
                return(0)
        else:
            import pymysql
            # Connect to the database
            con = pymysql.connect('')
            # Create a cursor to do things in the database
            cur = con.cursor()
            # Use the cursor to execute a function. Here we insert all of our scraped and cleaned data
            cur.execute("SELECT losses FROM matchuptable WHERE franchise=%s AND week=%s AND season=%s;", (franchise, week-1, season))
            losses_tuple = cur.fetchall()
            # Commit the executed function
            con.commit()
            # Close the connection to our SQL Server
            con.close()
            ##################### Change this accordingly. Just need the number of wins from previous week
            previous_losses = losses_tuple[0]
                
            if result_generator(margin) == 'L':
                return(previous_losses + 1)
            else:
                return(previous_losses)
                
    def update_ties():
        if week == 1:
            if result_generator(margin) == 'T':
                return(1)
            else:
                return(0)
        else:
            import pymysql
            # Connect to the database
            con = pymysql.connect('')
            # Create a cursor to do things in the database
            cur = con.cursor()
            # Use the cursor to execute a function. Here we insert all of our scraped and cleaned data
            cur.execute("SELECT ties FROM matchuptable WHERE franchise=%s AND week=%s AND season=%s;", (franchise, week-1, season))
            ties_tuple = cur.fetchall()
            # Commit the executed function
            con.commit()
            # Close the connection to our SQL Server
            con.close()
            ##################### Change this accordingly. Just need the number of wins from previous week
            previous_ties = ties_tuple[0]
                
            if result_generator(margin) == 'T':
                return(previous_ties + 1)
            else:
                return(previous_ties)
    
                
    
    
    ### The indexing changed slightly from 2017 to 2018, so this is something to keep an eye on.
    franchise = franchise_identification(team, season)
    opponent = opponent_identification(str(opponent_cells[week+1][-1])) ##2018 note: I added the [-1] as an extra slicer to make it more specific. This puts us into the cell at the end of the list that only contains the people's names   ; this finds the specific cell for the week in question. Add 1 to index properly
    points_scored = ''.join(re.findall(r'(?<=W\s|L\s|T\s)[0-9]*[.]?[0-9]', str(opponent_cells[week+1][1]))) #2018 note: the [1] was a [2] in 2017!!   ;  the regex outputs a list that needs to be converted to a string with .join
    points_against = ''.join(re.findall(r'(?<=-)[0-9]*[.]?[0-9]', str(opponent_cells[week+1][1]))) #2018 note: the [1] was a [2] in 2017!!
    week_total = round((float(points_scored) + float(points_against)),1) #the points have been converted from lists to strings within their own variables, but need to be converted to floats in order to manipulate them mathematically. Rounding because the float was getting out of control for some reason???
    margin = round((float(points_scored) - float(points_against)),1)
    result = result_generator(margin)
    wins = update_wins()
    losses = update_losses()
    ties = update_ties()
    status = 0 #will probably have to manually input this data to differentiate playoffs (1) from consolation (2)
    
    
    driver.close()
    
    ### Here's the SQL part.
    import pymysql
    # Connect to the database
    con = pymysql.connect('')
    # Create a cursor to do things in the database
    cur = con.cursor()
    # Use the cursor to execute a function. Here we insert all of our scraped and cleaned data
    cur.execute("INSERT INTO matchuptable (season, week, franchise, points_scored, points_against, result, margin, wins, week_total, opponent, status, QB, PTS_QB, RB1, PTS_RB1, RB2, PTS_RB2, WR1, PTS_WR1, WR2, PTS_WR2, TE1, PTS_TE1, RB3, PTS_RB3, WR3, PTS_WR3, TE2, PTS_TE2, OFFENSE, DST, PTS_DST, K, PTS_K, total_points, losses, ties) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);", (season, week, franchise, points_scored, points_against, result, margin, wins, week_total, opponent, status, QB, PTS_QB, RB1, PTS_RB1, RB2, PTS_RB2, WR1, PTS_WR1, WR2, PTS_WR2, TE1, PTS_TE1, RB3, PTS_RB3, WR3, PTS_WR3, TE2, PTS_TE2, OFFENSE, DST, PTS_DST, K, PTS_K, total_points, losses, ties))
    # Commit the executed function
    con.commit()
    # Close the connection to our SQL Server
    con.close()
    
    # Makes it easier to know which teams have been done already while the program is running
    print('done with team {}'.format(team))
