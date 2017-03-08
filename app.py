import os, sqlite3, logging
from scoreboard import Scoreboard
from Data.initialize_database import DatabaseInitializer


# setting up our logger to write to a log file
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG) # Process all levels of logging messages

# create file handler
file_handler = logging.FileHandler(__name__  + ".log", mode='w')
file_handler.setLevel(logging.DEBUG)

# create stream handler
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)

# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
stream_handler.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(stream_handler)


def main():
    DATABASE_NAME = "Data/scoreboard.db"
    sqlite = sqlite3.connect(DATABASE_NAME)

    # initialize and populate our database
    database_initializer = DatabaseInitializer(logger, sqlite)
    database_initializer.start()

    # start our web app
    scoreboard = Scoreboard(logger, sqlite)
    scoreboard.run(host='localhost', port=8080)


if __name__ == "__main__":
    main()
