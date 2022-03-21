import sqlite3


class DatabaseManager:
    """
    A class to manage the database.

    ...

    Attributes
    ----------
    __connection : connection
        Connection to sqlite database
    __cursor : cursor
        Executes databse commands

    Methods
    -------
    addRecord(table, *valuesCollection):
        Add record to table in database with values in collection.

    getUserData(login)::
        Gets user data row from database based on login.

    update():
        Updates database.

    closeConnection():
        Closes connection to database.
    """

    def __init__(self, pathToDatabase):
        """Creates instance of database manager.
        Creates connection (and sets cursor) to database in given path

        Returns:
            DatabaseManager
        """
        self.__connection = None
        self.__cursor = None

        try:
            self.__connection = sqlite3.connect(pathToDatabase)
        except Exception as e:
            raise e
        self.__cursor = self.__connection.cursor()

    def addRecord(self, table, *valuesCollection):
        """Adds provided values to chosen table in database

        Parameters:
        table (str): Name of table to add record
        values (collection): Values that will be added to the table

        Returns:
        bool:Whether adding record was successful

        """
        if(self.__cursor is None):
            return False

        try:
            data = self.__cursor.execute(f'SELECT * FROM {table} LIMIT 1')

            columnNames = ""
            for i in range(1, len(data.description)):
                columnNames += data.description[i][0]
                columnNames += ', ' if i < len(data.description) - 1 else ''

                # '"{login}", "{hashedPassword}", "{salt}"'
            values = ''

            i = 0
            for i, value in enumerate(valuesCollection):
                values += f'"{value}"'
                if i < len(valuesCollection) - 1:
                    values += ','

            self.__cursor.execute(f'INSERT INTO {table} ({columnNames}) VALUES ({values})')

            return True

        except Exception as e:
            if("UNIQUE constraint failed: Users.login" in str(e)):
                print("Login already exists in database!")

            print("Add record error: " + str(e))

            return False

    def getUserData(self, login):
        """Gets row of user data based on login

        Parameters:
        login (str): User login

        Returns:
        array: UserId, Login, PasswordHash, PasswordSalt
        """

        self.__cursor.execute(f"SELECT passwordHash, passwordSalt from Users WHERE login='{login}';")
        row = self.__cursor.fetchone()

        return row

    def update(self):
        """Updates database if connection exists

        Returns:
                None
        """

        if(self.__connection is None):
            return False

        self.__connection.commit()

    def closeConnection(self):
        """Closes connection to database if exists

        Returns:
                None
        """

        if(self.__connection is None):
            return False

        self.__connection.close()
