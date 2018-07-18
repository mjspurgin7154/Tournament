#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#
'''IMPORTANT - For this tournament to work the total number of players must
                be equal to 2 to the nth power where n = 1,2,3,4,5,6.  The
                number of total players should not exceed 64.'''

import psycopg2
import random
import math


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    db = connect()
    c = db.cursor()
    c.execute("update matchlist set wins = 0, matches = 0;")
    db.commit()
    db.close


def deletePlayers():
    """Remove all the player records from the database."""
    db = connect()
    c = db.cursor()
    c.execute("truncate playerList, matchList, swisspairings;")
    db.commit()
    db.close()


def countPlayers():
    """Returns the number of players currently registered."""
    db = connect()
    c = db.cursor()
    c.execute("SELECT count(*) as num FROM playerList")
    result = c.fetchone()
    return result[0]


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    db = connect()
    c = db.cursor()
    c.execute("with insert_name as (insert into playerlist(fullname) values (%s) returning id) insert into matchlist select id from insert_name;",(name,))
    db.commit()
    db.close()

def setupmatchlist_table():
    db = connect()
    c = db.cursor()
    c.execute("insert into matchlist select id from playerlist;")
    db.commit()
    db.close()

def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    db = connect()
    c = db.cursor()
    #c.execute("insert into matchlist(id) select playerlist.id from playerlist")
    c.execute("select id,fullname,wins,matches from playerlist left join matchlist using (id) order by wins;")
    standings = c.fetchall()
    db.close()
    return standings


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    idw, idl = winner, loser
    db = connect()
    c = db.cursor()
    c.execute("UPDATE matchlist set wins = (wins + 1), matches = (matches + 1) WHERE id = (%s);", (idw,))
    c.execute("UPDATE matchlist set matches = (matches + 1) WHERE id = (%s);", (idl,))
    db.commit()
    db.close

def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    db = connect()
    c = db.cursor()
    c.execute("truncate swisspairings;")
    results = playerStandings()
    index = 0
    while index < len(results):
        pid1,pname1 = results[index][0],results[index][1]
        pid2,pname2 = results[index + 1][0],results[index + 1][1]
        c.execute("insert into swissPairings values (%s,%s,%s,%s);",(pid1,pname1,pid2,pname2))
        index = index + 2
    db.commit()
    c.execute("select * from swissPairings;")
    matchlist = c.fetchall()
    db.close()
    return matchlist

def playMatch():
    """Randomly returns winners of the current round of matches and passes
        the results to the reportMatch function where tournament standings
        are recorded."""

    results = swissPairings()
    for row in results:
        if random.choice(['winner','loser']) == 'winner':
            reportMatch(row[0], row[2])
        else:
            reportMatch(row[2], row[0])

def playerInput():
    """Inputs the player names which are sent to the registerPlayer function
        to be added to the tournament database."""

    registerPlayer("Twilight Sparkle")
    registerPlayer("Fluttershy")
    registerPlayer("Applejack")
    registerPlayer("Pinkie Pie")
    registerPlayer("Rarity")
    registerPlayer("Rainbow Dash")
    registerPlayer("Princess Celestia")
    registerPlayer("Princess Luna")
    registerPlayer("Sparkle Twilight")
    registerPlayer("Shyflutter")
    registerPlayer("JackApple")
    registerPlayer("Pie Pinkie")
    registerPlayer("Oddity")
    registerPlayer("Dash Rainbow")
    registerPlayer("Celestia Princess")
    registerPlayer("Lune Princess")

def totalRounds():
    """Returns the total rounds to be played befor a winner is determined."""

    x = [1,2,3,4,5,6] # 2 to the power of x.
    n = countPlayers() # players registered.
    if n >= 2:
        for elem in x:
            if elem == math.log10(n)/math.log10(2):
                return elem
        print
        print
        print "INPUT ERROR"
        print
        return 0
    else:
        print
        print "INPUT ERROR"
        print
        return 0

def playRound(r):
    """Play each round of the tournament."""

    if r == 0:
        return
    db = connect()
    c = db.cursor()
    index = 0
    while index < r:
        playMatch()
        index = index + 1
    c.execute("SELECT id,fullname,wins,matches FROM playerlist LEFT JOIN matchlist USING (id) ORDER BY wins desc;")
    final_Standings = c.fetchall()
    for elem in final_Standings:
            print elem
    print
    print
    print "The tournament winner is " + str(final_Standings[0][1])
    print
    print
    db.commit()
    db.close()

if __name__ == '__main__':
    deleteMatches()
    deletePlayers()
    playerInput()
    playRound(totalRounds())
