import sys, sqlite3, csv, logging


class DatabaseInitializer():
    def __init__(self, logger, sqlite):
        self._logger = logger
        self._sqlite = sqlite


    def start(self):
        """
        Starts the initialize and populate process
        """
        GAMES_TABLE_NAME = "games"
        PLAYERS_TABLE_NAME = "players"
        RECORDS_TABLE_NAME = "records"

        try:
            # create our tables
            self._sqlite.execute("CREATE TABLE {} (id INTEGER PRIMARY KEY AUTOINCREMENT, name char(100) UNIQUE NOT NULL)".format(GAMES_TABLE_NAME))
            self._sqlite.execute("CREATE TABLE {} (id INTEGER PRIMARY KEY AUTOINCREMENT, name char(100) UNIQUE NOT NULL)".format(PLAYERS_TABLE_NAME))
            self._sqlite.execute("CREATE TABLE {} (date char(100) NOT NULL, time char(100) NOT NULL, game INTEGER NOT NULL, winner INTEGER NOT NULL, loser INTEGER NOT NULL, ip char(100) NOT NULL)".format(RECORDS_TABLE_NAME))
            self._sqlite.commit()

            # populate our tables
            self.populate_table(GAMES_TABLE_NAME, "Data/games.csv")
            self.populate_table(PLAYERS_TABLE_NAME, "Data/players.csv")

            self._logger.info("Database does not already exist. Creating it")
        except sqlite3.OperationalError:
            self._logger.warning("Database already exists, not overwriting it")


    def populate_table(self, TABLE_NAME, CSV_FILE_NAME):
        """
        Populates a table with CSV data
        """

        with open(CSV_FILE_NAME) as f:
            csv_file = csv.reader(f)

            self._logger.debug("Populating contents of {}".format(csv_file))
            for row in csv_file:
                val = row[0] # Only using the 0th column
                self._logger.debug("\t {} of type {}".format(val, type(val,)))
                self._sqlite.execute("INSERT into {} (name) VALUES (?)".format(TABLE_NAME), (val,))
                self._sqlite.commit()


def main():
    """
    Creates and kicks off our DatabaseInitializer
    """

    database_initializer = DatabaseInitializer()
    database_initializer.start()


if __name__ == "__main__":
    main()
