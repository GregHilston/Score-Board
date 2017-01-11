from Data.initialize_database import DatabaseInitializer


def main():
    database_initializer = DatabaseInitializer("Data/scoreboard.db")
    database_initializer.start()


if __name__ == "__main__":
    main()
