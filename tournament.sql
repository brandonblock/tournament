-- If a tournament db already exists, ditch it
DROP DATABASE IF EXISTS tournament;

-- Create the "Tournament" database
CREATE DATABASE tournament;

-- Connect to the tournament db
\connect tournament

-- If tables and views exist, drop them
DROP TABLE IF EXISTS players;
DROP TABLE IF EXISTS matches CASCADE;
DROP VIEW IF EXISTS standing;

-- Create the players table
CREATE TABLE players (
  player_id   SERIAL PRIMARY KEY,
  player_name TEXT
);

-- Create the matches table;
CREATE TABLE matches (
  match_id SERIAL PRIMARY KEY,
  win      INTEGER,
  lose     INTEGER,
  FOREIGN KEY (win) REFERENCES players (player_id),
  FOREIGN KEY (lose) REFERENCES players (player_id)
);

-- Create standings view sorted by number of wins
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