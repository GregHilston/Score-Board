import json, sqlite3, datetime
from bottle import Bottle, route, error, run, request, template, debug


class Scoreboard(Bottle):
    def __init__(self, logger, sqlite):       
        super(Scoreboard, self).__init__()
        self._logger = logger
        self._sqlite = sqlite
        self._cur = self._sqlite.cursor()
        self.route("/", callback=self.index)
        self.route("/games", callback=self.games)
        self.route("/players", callback=self.players)
        self.route("/records", callback=self.records)
        self.route("/player_records", callback=self.player_records)
        self.route("/game", method="POST", callback=self.game)
        self.route("/add_player", method="POST", callback=self.player)
        self.route("/add_record", method="POST", callback=self.record)


    def index(self):
        """
        Displays DB data and allows users to enter a new win
        """

        games = json.loads(self.games())
        players = json.loads(self.players())
        records = json.loads(self.records())

        record_game = template("record_game", games=games, players=players)

        games_table = template("games_or_players", title="Games", values=games)
        players_table = template("games_or_players", title="Players", values=players)

        data = self.create_score_data_structure(players, games)
        data = self.populate_score_data_structure(data, records)

        return record_game + games_table + players_table


    def create_score_data_structure(self, players, games):
        """
        Creates a data structure to represent all data in our database
        """
        
        data = {}

        for winner in players:
            self._logger.debug("winner {} of type {}".format(winner, type(winner)))
            data[str(winner)] = {}

            for loser in players:
                if winner != loser:
                    data[str(winner)][str(loser)] = {}

                    for game in games:
                        self._logger.debug("game {} of type {}".format(game, type(game)))
                        data[str(winner)][str(loser)][str(game)] = 0

        self._logger.debug("data without records {} of type {}".format(data, type(data)))
        return data


    def populate_score_data_structure(self, data, records):
        """
        Populates the data with the wins from records
        """

        for record in records:
            # self._logger.debug(f"record {record} of type {str(type(record))}")
            for key in record:
                val = record[key]
                # self._logger.debug(f"key {key} of type {str(type(key))}")
                # self._logger.debug(f"val {val} of type {str(type(val))}")


        self._logger.debug("data with records {}".format(data))
        return data


    def games(self):
        """
        Returns a JSON list of all games
        """

        self._cur.execute("SELECT \"name\" FROM games")
        games = self._cur.fetchall()

        return json.dumps(games, sort_keys=True)


    def players(self):
        """
        Returns a JSON list of all players
        """

        self._cur.execute("SELECT \"name\" FROM players")
        players = self._cur.fetchall()

        return json.dumps(players, sort_keys=True)


    def records(self):
        """
        Returns a JSON list of all records
        """

        self._cur.execute("SELECT * FROM records")
        records = self._cur.fetchall()


        # get the names of our columns
        cursor = self._sqlite.execute("SELECT * from records")
        names = list(map(lambda x: x[0], cursor.description))

        record_dicts = []

        for record in records:
            record_dict = dict(zip(names, record))
            record_dicts.append(record_dict)

        return json.dumps(record_dicts)

    def player_records(self):
        """
        Returns a JSON list of a player's records
        """

        player_name = request.params["player_name"]
        player_records = ""
        print("player_name {}".format(player_name))

        if player_name is None:
            self._logger.warning("cannot get records of player_name {}".format(player_name))
        else:
            # get our player's id
            self._cur.execute("SELECT ID FROM players WHERE \"name\" = \"{}\"".format(player_name))
            player_id = self._cur.fetchall()[0][0] # Unpack list of tuples of size 1

            # get our player's records in an array of arrays
            self._cur.execute("SELECT * FROM records WHERE \"winner\" = \"{}\"".format(player_id))
            player_records = self._cur.fetchall()

            # create a dictionary of all this player's records

            # get the names of our columns
            cursor = self._sqlite.execute("SELECT * from records")
            names = list(map(lambda x: x[0], cursor.description))

            # format our records as a dictionary
            record_dicts = []

            for record in player_records:
                record_dict = dict(zip(names, record))
                record_dicts.append(record_dict)

        return json.dumps(record_dicts)


    def game(self):
        """
        Adds a game to the games table
        """

        game_name = request.forms.get("game_name")

        if game_name is None or game_name in self.games():
            self._logger.warning("{} is either None or already in our list of games".format(game_name))
        else:
            self._cur.execute("INSERT into games (name) VALUES(\"{}\")".format(game_name))
            self._sqlite.commit()
            self._logger.info("added new game {}".format(game_name))

        return self.index()


    def player(self):
        """
        Adds a player to the Players table
        """

        player_name = request.forms.get("player_name")

        if player_name is None or player_name in self.players():
            self._logger.warning("{} is either None or already in our list of players".format(player_name))
        else:
            self._cur.execute("INSERT into players (name) VALUES(\"{}\")".format(player_name))
            self._sqlite.commit()
            self._logger.info("added new player {}".format(player_name))

        return self.index()

    def record(self):
        """
        Adds a record to the records table
        """

        game = request.forms.get("game")
        winner = request.forms.get("winner")
        loser = request.forms.get("loser")

        if winner == loser:
            self._logger.error("Can not play with yourself")
        else:
            print("valid")
            date = datetime.datetime.today().strftime("%m-%d-%Y")
            time = datetime.datetime.today().strftime("%H:%M")
            ip = request.environ.get('HTTP_X_FORWARDED_FOR') or request.environ.get('REMOTE_ADDR')
            self._cur.execute("INSERT into records (date, time, game, winner, loser, ip) VALUES(\"{}\", \"{}\", \"{}\", \"{}\", \"{}\", \"{}\")".format(date, time, game, winner, loser, ip))
            self._sqlite.commit()
            self._logger.info("{} recorded win against {} in {} at {} {} from {}".format(winner, loser, game, time, date, ip))

        return self.index()
