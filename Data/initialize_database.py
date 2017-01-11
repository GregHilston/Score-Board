import sqlite3, csv, logging


# setting up our logger to write to a log file
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG) # Process all levels of logging messages

# create file handler
file_handler = logging.FileHandler(__name__  + ".log", mode='w')
file_handler.setLevel(logging.DEBUG)

# create stream handler
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)

# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
stream_handler.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(stream_handler)


class DatabaseInitializer():
    def __init__(self, database_name):
        self._sqlite = sqlite3.connect(database_name)


    def start(self):
        """
        Starts the initialize and populate process
        """
        GAMES_TABLE_NAME = "games"
        PLAYERS_TABLE_NAME = "players"
        RECORDS_TABLE_NAME = "records"

        # create our tables
        self._sqlite.execute("CREATE TABLE {} (name char(100) NOT NULL)".format(GAMES_TABLE_NAME))
        self._sqlite.execute("CREATE TABLE {} (name char(100) NOT NULL)".format(PLAYERS_TABLE_NAME))
        self._sqlite.execute("CREATE TABLE {} (date char(100) NOT NULL, game INTEGER NOT NULL, winner INTEGER NOT NULL, loser INTEGER NOT NULL)".format(RECORDS_TABLE_NAME))
        self._sqlite.commit()

        # populate our tables
        self.populate_table(GAMES_TABLE_NAME, "Data/games.csv")
        self.populate_table(PLAYERS_TABLE_NAME, "Data/players.csv")


    def populate_table(self, TABLE_NAME, CSV_FILE_NAME):
        """
        Populates a table with CSV data
        """

        f = open(CSV_FILE_NAME)
        csv_file = csv.reader(f)

        logger.debug("Printing {}".format(csv_file))
        for row in csv_file:
            val = row[0] # Only using the 0th column
            logger.debug("\t {} of type {}".format(val, type(val,)))
            self._sqlite.execute("insert into {} values (?)".format(TABLE_NAME), (val,))
            self._sqlite.commit()

def main():
    """
    Creates and kicks off our DatabaseInitializer
    """

    database_initializer = DatabaseInitializer()
    database_initializer.start()


if __name__ == "__main__":
    main()
