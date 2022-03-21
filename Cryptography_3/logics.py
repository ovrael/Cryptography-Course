from hashlib import pbkdf2_hmac
import hmac
import base64
import os
from databaseManager import DatabaseManager

class Logics():
    """
    Manages user's operations: login, registration.

    ...

    Attributes
    ----------
    __iterations : int
        Number of repeats for hash function
    __dbContext : DatabaseManager
        Database context for multiple operations

    Methods
    -------
    static connectDatabase(dbFileName):
        Connects to database in specified path and creates DatabaseManager object

    static mainMenu(login):
        Displays and manages main menu

    static __register():
        Displays ana manages registration menu

    static __encodeFromBytes():
        Encodes encoded bytes into string

    static __login():
        Displays ana manages login menu

    static __quit():
        Updates database and closes connection to it.
        
    static __quit():
        Gets any input then cleans screen.
    """

    __iterations = 321347
    __dbContext = None

    @staticmethod
    def connectDatabase(dbFileName):
        """Connects to database file in DatabaseFile\\dbFileName

        Parameters:
        dbFileName (str): File name with extension sqlite

        Returns:
                None
        """
        currentDir = os.getcwd()
        dbFileFullPath = os.path.join(
            currentDir, "DatabaseFiles\\", dbFileName)
        Logics.__dbContext = DatabaseManager(dbFileFullPath)

    @staticmethod
    def mainMenu():
        """Displays menu with options and gets user's choice

        Returns:
        bool:Whether program is still running
        """
        print("1. Create new user")
        print("2. Log in")
        print("\n0. QUIT")
        choice = input()
        os.system('cls')
        
        match choice:
            case '1':
                Logics.__register()
                return True
            case '2':
                Logics.__login()
                return True
            case '0':
                Logics.__quit()
                return False
            case _:
                return True
    
    @staticmethod
    def __pressKey():
        """Gets any input then cleans screen

        Returns:
            None
        """
        input("\n\nPress any key to continue...")       
        os.system('cls')

    @staticmethod
    def __register():
        """Displays registration procedure.
        Gets user login and password with confirmation (checks if same)
        Then tries to add user to database.

        Returns:
            None
        """

        login = input("Your user login:")
        password1 = input("Your password:")
        password2 = input("Confirm password:")
        if(password1 != password2):
            print("Passwords are not equal, please try again.")
            return

        salt = base64.b32encode(os.urandom(16))
        hashedPassword = pbkdf2_hmac(
            'sha256', password1.encode(), salt, Logics.__iterations)

        if(Logics.__dbContext.addRecord("Users", login, hashedPassword, salt)):
            print(f"User {login} successfully added!")
            Logics.__dbContext.update()
        else:
            print("We are sorry, we could not create account. Please try again.")
        
        Logics.__pressKey()

    @ staticmethod
    def __encodeFromBytes(data):
        """Encodes encoded bytes data into string

        Parameters:
        data (bytes): Encoded bytes data

        Returns:
        str:Encoded data
        """
        data = f"{data}"
        data = data[data.find("'")+1:data.rfind("'")]
        return data.encode()

    @ staticmethod
    def __login():
        """Displays login procedure.
        Gets user login and password
        Then compares hash of provided password with hash from database.

        Returns:
            None
        """
        login = input("Login:")
        # not sure if password should be stored in variable like this?
        password = input("Passowrd:")
        userData = Logics.__dbContext.getUserData(login)

        if userData is None:
            print("User doesn't exist in database!")
            Logics.__pressKey()
            return

        salt = Logics.__encodeFromBytes(userData[1])

        hashedPassword = pbkdf2_hmac(
            'sha256', password.encode(), salt, Logics.__iterations)

        if hmac.compare_digest(Logics.__encodeFromBytes(hashedPassword), Logics.__encodeFromBytes(userData[0])):
            print("Login successfully!")
        else:
            print("Wrong password :(")
            
        Logics.__pressKey()

    @ staticmethod
    def __quit():
        """Updates database and closes connection to it.

        Returns:
            None
        """
        Logics.__dbContext.update()
        Logics.__dbContext.closeConnection()
