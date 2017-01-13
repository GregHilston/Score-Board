import sqlite3
from json import dumps
from bottle import Bottle, route, error, run, request, template, debug


class Scoreboard(Bottle):
    def __init__(self, logger, sqlite):
        super(Scoreboard, self).__init__()
        self._logger = logger
        self._sqlite = sqlite
        self._cur = self._sqlite.cursor()
        self.route("/", callback=self.index)
        self.route("/get_games", callback=self.get_games)
        self.route("/get_players", callback=self.get_players)
        self.route("/get_records", callback=self.get_records)
        self.route("/add_game", callback=self.add_game)
        self.route("/add_player", callback=self.add_player)
        self.route("/add_record", callback=self.add_record)


    def index(self):
        """
        Displays DB data and allows users to enter a new win
        """

        json_games = self.get_games()
        # players = self.get_players()
        # records = self.get_records()

        return template("index", json_games=json_games)


    def get_games(self):
        """
        Returns a JSON list of all games
        """

        self._cur.execute("SELECT * FROM games")
        data = self._cur.fetchall()

        return dumps(data, sort_keys=True)


    def get_players(self):
        """
        Returns a JSON list of all players
        """

        self._cur.execute("SELECT * FROM players")
        data = self._cur.fetchall()

        return dumps(data, sort_keys=True)


    def get_records(self):
        """
        Returns a JSON list of all records
        """

        self._cur.execute("SELECT * FROM records")
        data = self._cur.fetchall()

        return dumps(data)


    def add_game(self):
        """
        Adds a game to the games table
        """

        return "Add game!"


    def add_player(self):
        """
        Adds a player to the Players table
        """

        return "Add Player!"


    def add_record(self):
        """
        Adds a record to the records table
        """

        return "Add record!"
