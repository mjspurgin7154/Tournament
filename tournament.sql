-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.

DROP DATABASE IF EXISTS tournament;

CREATE DATABASE tournament;

\c tournament;

-- Create list of players in the current tournament.

CREATE TABLE playerList ( id SERIAL PRIMARY KEY,
                               fullname TEXT NOT NULL);
                                -- wins integer DEFAULT 0.0,
                                -- matches integer DEFAULT 0.0);

-- Create list of to track tournament match results.

CREATE TABLE matchList ( id integer PRIMARY KEY REFERENCES playerList(id),
                            wins integer DEFAULT 0.0,
                            matches integer DEFAULT 0.0);

-- Creates a list of tournament matches players for the next round of the tournament.

CREATE TABLE swissPairings(id1 integer REFERENCES playerlist(id),
                            name1 TEXT, id2 integer REFERENCES playerlist(id),
                            name2 TEXT);

CREATE VIEW finalStandings as (SELECT id,fullname,wins,matches from playerlist
                                left join matchlist using (id) order by wins desc);

