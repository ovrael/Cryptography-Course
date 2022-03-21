import base64
import os
import unittest
from databaseManager import DatabaseManager
from logics import Logics

class TestDatabaseManager(unittest.TestCase):
    __currentDir = os.getcwd()
    __dbFile = 'test_users.sqlite'
    __dbFileFullPath = os.path.join(__currentDir, "DatabaseFiles\\", __dbFile)
    __dbContext = DatabaseManager(__dbFileFullPath)
        
    def test_addRecord(self):
        self.assertTrue(TestDatabaseManager.__dbContext.addRecord('Users', 'Jacek', 'P4$$w0Rd!*!', 'SALT'))
        self.assertFalse(TestDatabaseManager.__dbContext.addRecord('Users', 'Jacek'))

    def test_getUserData(self):
        TestDatabaseManager.__dbContext.addRecord('Users', 'JacekGetUserData', 'PasswordGetUserData', 'SaltGetUserData')
        TestDatabaseManager.__dbContext.update()
        self.assertEqual(TestDatabaseManager.__dbContext.getUserData('JacekGetUserData'), ('PasswordGetUserData', 'SaltGetUserData'))

class TestLogics(unittest.TestCase):
    __data = base64.b32encode(os.urandom(16))
    
    def test_encodeFromBytes(self):
        self.assertEqual(Logics.__encodeFromBytes(TestLogics.__data), f'{TestLogics.__data}')
        

if __name__ == '__main__':
    unittest.main()