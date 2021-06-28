
from time import time, sleep
from dotenv import load_dotenv
import os


def isPending ():

    load_dotenv()
    # load environment variables
    SECONDS_INTERVAL = os.getenv('SECONDS_INTERVAL')
    THRESHOLD = os.getenv('THRESHOLD')
    
    # cast strings to integers
    SECONDS_INTERVAL = int(SECONDS_INTERVAL)
    THRESHOLD = int(THRESHOLD)

    # run aws command to retrieve the initial number of pending tasks
    PENDING_COUNT = 1

    # declare i variable for while loop
    i = 0

    # check if there are any tasks in pending state
    if PENDING_COUNT > 0:

        # looping pending state status for X seconds, if pending state is greater than 0 after X seconds, the function will prompt an alert.
        while (i <= THRESHOLD) and (PENDING_COUNT > 0): 

            # timer for while loop
            sleep(SECONDS_INTERVAL - time() % SECONDS_INTERVAL) 

            # aws cli command to retrieve number of current 'PEDNING' tasks
            PENDING_COUNT = 1

            # print how many seconds have been passed
            print ("{} seconds passed...".format(i))

            # print the current number of pending tasks
            print ("{} tasks are in pending state...".format(PENDING_COUNT))

            # tell the while loop to exit after the THRESHOLD has been reached
            if i == THRESHOLD:

                # send email via SNS
                print ("alarm")
                break
            i += SECONDS_INTERVAL
    else:
        print ("all good")

# execute the function
isPending()
