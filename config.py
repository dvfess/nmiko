import os
import getpass


# Максимальное количество потоков.
# Минимальное высчитывается из количества ip-адресов
THREADS = 40
USER = input("Login: ")
PASSWORD = getpass.getpass()
FILENAME = input("Name of file with results: ") + '.txt'

IPFILE = (os.path.join(os.getcwd(), 'IP-ADD.txt'))
