# Tournament
This Python module uses a PostgreSQL database (tournament) to keep track of
players and matches in a game tournament.

The tournament.py file is a the main client program that provides access to the database via a library of functions.

The tournament.SQL file is used to set up the database schema.

The tournament_test.py file is a client program which tests the implementation of functions in the tournament.py file.

How does the the tournament.py client program work.

1.  Provides a connection to the tournament database.
2.  Any existing match or player records are deleted each time the program
    is run.
3.  New player names are inputed into the database (with a unique id
    number assigned).  For this tournament to work the total number of players must be equal to 2 to the nth power where n = 1,2,3,4,5 or 6.  The
    number of total players should not exceed 64.  An error message will be
    output if the input requirements are not satisfied.
4.  The total number of rounds for the tournament is calculated.
5.  Prior to match play in each round, match pairings are made based upon
    the player standings.
6.  Match play results are randomly determined and player standings are
    updated.
7.  Pairings are determined for the next round and match play takes place.
8.  Once the final round is played, a winner is declared.

How to execute the program.
1.  Import the tournament.sql file via the psql vagrant CLI to create the
    database and tables.
2.  Manually input the player names into the playerInput function in the
    tournament.py file.  Save the file.
3.  Run the tournament.py file from the psql vagrant CLI.
4.  Read the winner on the CLI.

list of functions:
    connect
    deleteMatches
    deletePlayers
    countPlayers
    registerPlayers
    playerStandings
    reportMatch
    swissPairings
    playMatch
    playerInput
    totalRounds
    playRound
