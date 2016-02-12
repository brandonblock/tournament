# Udacity-Tournament-Database

Udacity-tournament-database is the second project completed for Udacity's full-stack [nanodegree program](https://www.udacity.com/nanodegree) program. The project demonstrates the design and use of a PostgreSQL database to manage a Swiss-system tournament.

To use the project files to setup a swiss-system tournament, follow the below steps (steps 2-3 are done for you by running the tournament.sql file). 

### 1. Download Files

Download the project files or clone the repository with git.

### 2. Create Database

Log into your PostgreSQL console and create a new tournament database:


```
CREATE DATABASE tournament 

```

### 3. Create Tables 

Two database tables and one viewwill be required. The first table is to track the players in the tournament (this can be used for individual players or teams). The second table is to track matches within the tournament. The view created helps to aggregate the standings.

```
CREATE TABLE players (
  player_id   SERIAL PRIMARY KEY,
  player_name TEXT
);

CREATE TABLE matches (
  match_id SERIAL PRIMARY KEY,
  win      INTEGER,
  lose     INTEGER,
  FOREIGN KEY (win) REFERENCES players (player_id),
  FOREIGN KEY (lose) REFERENCES players (player_id)
);

CREATE VIEW standing AS
  SELECT
    x.player_id                       AS player_id,
    x.player_name,
    (SELECT count(*)
     FROM matches
     WHERE matches.win = x.player_id) AS won,
    (SELECT count(*)
     FROM matches
     WHERE x.player_id IN (win, lose))
                                      AS played
  FROM players x
  GROUP BY x.player_id
  ORDER BY won DESC;
```

### 4. Import Functions

To use the tournament functions, import tournament.py into your python script.

```
import tournament

```

### 5. Use Functions 

The following functions are included in tournament.py

#### connect()
Connects to the PostgreSQL databas, returning a database connection.

#### deleteMatches()
Remove all match records from the tournament database.

#### deletePlayers()
Remove all player records from the tournament database.

#### countPlayers()
Returns the number of players currently registered in the tournament.

#### registerPlayer(name)
Adds a player to the tournament database and assigns a unique serial ID.

#### playerStandings()
Returns a list of the players and their win records, sorted by wins.

#### reportMatch(winner, loser)
Creates a new match record, recording the winner and the loser of the match.

#### swissPairings()
Returns a list containing pairs of players for the next round of the tournament.

## Testing Information

tournament_test.py is also included, which is used for testing that python functions met Udacity's project requirements.
