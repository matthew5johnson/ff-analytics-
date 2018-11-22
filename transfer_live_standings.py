import pymysql
######## !!! Update the week to the prior week each time
week = 11
season = 2018

def franchise_identification(number):
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


######################################
####  Now we access ClearDB on Heroku
######################################


con = pymysql.connect()
cur = con.cursor()
# Delete the previous week's table
cur.execute("DROP TABLE temporary_scrape_standings;")
con.commit()
# Create a new blank table
cur.execute("CREATE TABLE temporary_scrape_standings (franchise INT, wins INT, losses INT, ties INT, sum_points DECIMAL(5,1), primary key(franchise))")
con.commit()
con.close()


for i in range(1,13):
    # Connect to the database
    con = pymysql.connect()
    # Create a cursor to do things in the database
    cur = con.cursor()

    cur.execute("SELECT wins, losses, ties FROM matchuptable WHERE franchise=%s AND season=%s AND week=%s;", (franchise_identification(i), season, week))
    record = cur.fetchall()[0]
    #con.commit()
    
    cur.execute("SELECT SUM(points_scored) FROM matchuptable WHERE franchise=%s AND season=%s;", (franchise_identification(i), season))
    sum_points = cur.fetchall()[0][0]
    con.commit()
    con.close()
    
    # record[0] = wins  record[1] = losses  record[2] == ties
    # sum_points is total points
    
    ######################################
    ####  Now we access ClearDB on Heroku
    ######################################
    
    #################### Inserting weekly Records
    con = pymysql.connect()
    cur = con.cursor()
    
    cur.execute("INSERT INTO temporary_scrape_standings (franchise, wins, losses, ties, sum_points) VALUES (%s, %s, %s, %s, %s);", (i, record[0], record[1], record[2], sum_points))
    con.commit()
    con.close()
    
print('done')
