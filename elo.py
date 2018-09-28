
#need franchise number to name dictionary to reference in sql elo pulls 
week = 2
season = 2015

team = 1


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

sqlfranchise = franchise_converter(team, season)
sqlseason = season_checker(week, season)
last_week = week_checker(week, season)
### Here's the SQL part.
import pymysql
# Connect to the database
con = pymysql.connect('host', '', 'pass', 'dbname')
# Create a cursor to do things in the database
cur = con.cursor()
testing = cur.execute("SELECT PTS_QB FROM matchuptable WHERE franchise='Mitch' AND season=2015 AND week=1;").findone

# Use the cursor to execute a function. Here we insert all of our scraped and cleaned data
#my_elo = cur.execute("SELECT elo FROM matchuptable WHERE franchise=(%s) AND season=(%s) AND week=(%s);", (sqlfranchise, sqlseason, last_week))
#my_opponent = cur.execute("SELECT opponent FROM matchuptable WHERE franchise=(%s) AND season=(%s) AND week=(%s);", (sqlfranchise, season, week))
#their_elo = cur.execute("SELECT elo FROM matchuptable WHERE franchise=(%s) AND season=(%s) AND week=(%s);", (my_opponent, sqlseason, last_week))
# Commit the executed function
con.commit()
# Close the connection to our SQL Server
con.close()

#cur.execute("INSERT INTO matchuptable (season, week, franchise, points_scored, points_against, result, margin, week_total, opponent, status, QB, PTS_QB, RB1, PTS_RB1, RB2, PTS_RB2, WR1, PTS_WR1, WR2, PTS_WR2, TE1, PTS_TE1, RB3, PTS_RB3, WR3, PTS_WR3, TE2, PTS_TE2, OFFENSE, DST, PTS_DST, K, PTS_K, total_points) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);", (season, week, franchise, points_scored, points_against, result, margin, week_total, opponent, status, QB, PTS_QB, RB1, PTS_RB1, RB2, PTS_RB2, WR1, PTS_WR1, WR2, PTS_WR2, TE1, PTS_TE1, RB3, PTS_RB3, WR3, PTS_WR3, TE2, PTS_TE2, OFFENSE, DST, PTS_DST, K, PTS_K, total_points))

#diff = abs(my_elo - their_elo)


# Makes it easier to know which teams have been done already while the program is running
print('done with team {}'.format(team))

print(testing)


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
