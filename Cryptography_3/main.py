# 1. Zaprojektuj i zaimplementuj prosty własny sposób przechowywania haseł w bazie sqlite:
# użytkownik podaje hasło dwa razy, losujesz sól, hashujesz wszystko i zapisujesz hash oraz sól do bazy.
# Dodaj funkcję weryfikującą hasło.

# 2. Przerób pkt 1. aby używał pbkdf2_hmac.
# Zrób z tego porządny projekt (testy, docstringi, itp.)
import os
from logics import Logics
dbFileName = "users.sqlite"

if __name__ == '__main__':
    Logics.connectDatabase(dbFileName)
    while Logics.mainMenu():
        pass
    
    os.system('cls')
    print("Program closed.")
