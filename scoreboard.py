import sqlite3
from json import dumps
from bottle import route, run, request, template, debug


# TODO remove and instead pass in
DATABASE_NAME = "Data/scoreboard.db"
sqlite3 = sqlite3.connect(DATABASE_NAME)
cur = sqlite3.cursor()


@route("/", method="GET")
def index():
    """
    Displays DB data and allows users to enter a new win
    """

    return "Hello World!"


# begin API endpoints
@route("/get_games", method="GET")
def get_games():
    """
    Returns a JSON list of all games
    """

    cur.execute("SELECT * FROM games")
    data = cur.fetchall()

    return dumps(data)


@route("/get_players", method="GET")
def get_players():
    """
    Returns a JSON list of all players
    """

    cur.execute("SELECT * FROM players")
    data = cur.fetchall()

    return dumps(data)


@route("/get_records", method="GET")
def get_records(self):
    """
    Returns a JSON list of all records
    """

    cur.execute("SELECT * FROM records")
    data = cur.fetchall()

    return dumps(data)


@route("/add_game", method="POST")
def add_game():
    """
    Adds a game to the games table
    """

    return "Add game!"


@route("/add_player", method="POST")
def add_player():
    """
    Adds a player to the Players table
    """

    return "Add Player!"


@route("/add_record", method="POST")
def add_record():
    """
    Adds a record to the records table
    """

    return "Add record!"

debug(True)
run(reloader=True)
