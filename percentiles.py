# Total Expected Wins
# Calculating points_scored percentiles
season = 2018
week = 6
franchise = 1

def franchise_identification(number, year):
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
    

for franchise in range(1,13):

    import pymysql
    # Connect to the database
    con = pymysql.connect('')
    # Create a cursor to do things in the database
    cur = con.cursor()
    
    # First check to see if an entry exists for this franchise during the specified week
    cur.execute("SELECT points_scored FROM matchuptable WHERE season=%s AND franchise=%s AND week=%s;", (season, franchise_identification(franchise, season), week))
    points_scored_tuple = cur.fetchall()
    con.commit()
    if points_scored_tuple == ():
        print("No entry for franchise {}".format(franchise))
    else: 
        points_convert = points_scored_tuple[0][0]
        cur.execute("SELECT COUNT(points_scored) AS total FROM matchuptable WHERE season > 2014;")
        total_tuple = cur.fetchall()
        con.commit()
        # Total number of scores posted
        total = total_tuple[0][0]
        # Get the number of scores less than this specific points_scored
        cur.execute("SELECT COUNT(points_scored) FROM matchuptable WHERE season > 2014 AND points_scored < %s;", (points_convert))
        amount_below_tuple = cur.fetchall()
        con.commit()
        amount_below = amount_below_tuple[0][0]
        # Find the percentile
        percentile = amount_below / total
        # Write the percentile to the appropriate row in the SQL db
        cur.execute("UPDATE matchuptable SET score_percentile=%s WHERE season=%s AND week=%s AND franchise=%s;", (percentile, season, week, franchise_identification(franchise, season)))
        con.commit()
        con.close()
    
