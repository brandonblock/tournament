#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    conn = connect()
    c = conn.cursor()
    c.execute('DELETE FROM matches')
    conn.commit()
    conn.close()


def deletePlayers():
    """Remove all the player records from the database."""
    conn = connect()
    c = conn.cursor()
    c.execute('DELETE FROM players')
    conn.commit()
    conn.close()


def countPlayers():
    """Returns the number of players currently registered."""
    conn = connect()
    c = conn.cursor()
    c.execute('SELECT COUNT(*) FROM players')
    conn.commit()
    num = c.fetchone()[0]
    conn.close()

    return num


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    Args:
      name: the player's full name.
    """
    conn = connect()
    c = conn.cursor()
    c.execute('INSERT INTO players(player_name) VALUES (%s)', (name,))
    conn.commit()
    conn.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    conn = connect()
    c = conn.cursor()
    c.execute("SELECT * FROM standing")
    conn.commit()
    num = c.fetchall()
    conn.close()

    return num


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    conn = connect()
    c = conn.cursor()
    c.execute("INSERT INTO matches (win, lose) VALUES (%s, %s)",
              (winner, loser,))
    conn.commit()
    conn.close()


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    results = playerStandings()
    count = len(results)

    pairings = []
    for x in range(0, count - 1, 2):
        paired = (results[x][0], results[x][1],
                  results[x + 1][0], results[x + 1][1])
        pairings.append(paired)

    return pairings

