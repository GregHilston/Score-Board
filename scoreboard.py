import json, sqlite3, datetime
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
        self.route("/add_game", method="POST", callback=self.add_game)
        self.route("/add_player", method="POST", callback=self.add_player)
        self.route("/add_record", method="POST", callback=self.add_record)


    def index(self):
        """
        Displays DB data and allows users to enter a new win
        """

        games = json.loads(self.get_games())
        players = json.loads(self.get_players())
        records = json.loads(self.get_records())
        games_table = template("games_or_players", title="Games", values=games)
        players_table = template("games_or_players", title="Players", values=players)
        record_game = template("record_game", games=games, players=players)

        return games_table + players_table + record_game


    def get_games(self):
        """
        Returns a JSON list of all games
        """

        self._cur.execute("SELECT * FROM games")
        data = self._cur.fetchall()

        return json.dumps(data, sort_keys=True)


    def get_players(self):
        """
        Returns a JSON list of all players
        """

        self._cur.execute("SELECT * FROM players")
        data = self._cur.fetchall()

        return json.dumps(data, sort_keys=True)


    def get_records(self):
        """
        Returns a JSON list of all records
        """

        self._cur.execute("SELECT * FROM records")
        data = self._cur.fetchall()

        return json.dumps(data)


    def add_game(self):
        """
        Adds a game to the games table
        """

        name = request.forms.get("name")

        if name is None or name in self.get_games():
            self._logger.warning("{} is either None or already in our list of games".format(name))
        else:
            self._cur.execute("INSERT into games (name) VALUES(\"{}\")".format(name))
            self._sqlite.commit()
            self._logger.info("added new game {}".format(name))

        return self.index()


    def add_player(self):
        """
        Adds a player to the Players table
        """

        name = request.forms.get("name")

        if name is None or name in self.get_players():
            self._logger.warning("{} is either None or already in our list of players".format(name))
        else:
            self._cur.execute("INSERT into players (name) VALUES(\"{}\")".format(name))
            self._sqlite.commit()
            self._logger.info("added new player {}".format(name))

        return self.index()

    def add_record(self):
        """
        Adds a record to the records table
        """

        game = request.forms.get("game")
        winner = request.forms.get("winner")
        loser = request.forms.get("loser")

        if winner == loser:
            logger.error("Can not play with yourself")
        else:
            print("valid")
            date = datetime.datetime.today().strftime("%m-%d-%Y")
            time = datetime.datetime.today().strftime("%H:%M")
            ip = request.environ.get('HTTP_X_FORWARDED_FOR') or request.environ.get('REMOTE_ADDR')
            self._cur.execute("INSERT into records (date, time, game, winner, loser, ip) VALUES(\"{}\", \"{}\", \"{}\", \"{}\", \"{}\", \"{}\")".format(date, time, game, winner, loser, ip))
            self._sqlite.commit()
            self._logger.info("{} recorded win against {} in {} at {} {} from {}".format(winner, loser, game, time, date, ip))

        return self.index()
