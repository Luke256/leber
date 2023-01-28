from client import Client
import random
import traceback
from util import *
import sys

userData = __import__('USER_DATA_SECRET')

try:

    client = Client(userData.PHONE_NUMBER, userData.PASSWORD)

    client.getTemprtureQuestion()

    # client.submitTemperture([random.randint(21, 28), 118, 136])

except Exception as e:
    logfile = get_logfile_name()
    with open(logfile, 'a') as f:
        traceback.print_exc(file=f)
    print('[ERROR] Program was Stopped with an Error. Check the log file: ' + logfile)