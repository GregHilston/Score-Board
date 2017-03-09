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
        self.route("/player_wins", callback=self.player_wins)
        self.route("/game", method="POST", callback=self.game)
        self.route("/player", method="POST", callback=self.player)
        self.route("/record", method="POST", callback=self.record)


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


    def game_id_to_game_name(self, game_id):
        """
        Converts a game id to a game name
        """

        self._cur.execute(f"SELECT \"name\" FROM games WHERE \"id\" = {game_id}")
        game_id = self._cur.fetchall()

        return game_id[0][0]


    def player_id_to_player_name(self, player_id):
        """
        Converts a player id to a player name
        """

        self._cur.execute(f"SELECT \"name\" FROM players WHERE \"id\" = {player_id}")
        player_name = self._cur.fetchall()

        return player_name[0][0]


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


    def player_wins(self):
        """
        Returns a JSON array of players and the number of wins they have against opponents for each game
        """

        win_dicts = {}

        self._cur.execute("SELECT * FROM records")
        records = self._cur.fetchall()

        # get the names of our columns
        cursor = self._sqlite.execute("SELECT * from records")
        names = list(map(lambda x: x[0], cursor.description))

        record_dicts = []

        for record in records:
            record_dict = dict(zip(names, record))
            record_dicts.append(record_dict)

        for this_dict in record_dicts:
            game = self.game_id_to_game_name(this_dict["game"])
            winner = self.player_id_to_player_name(this_dict["winner"])
            loser = self.player_id_to_player_name(this_dict["loser"])

            if game not in win_dicts:
                win_dicts[game] = {}
            if winner not in win_dicts[game]:
                win_dicts[game][winner] = {}
            if loser not in win_dicts[game][winner]:
                win_dicts[game][winner][loser] = 1
            else:
                win_dicts[game][winner][loser] += 1

        return json.dumps(win_dicts)


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
