import time

def printAndLog(log, string):
    print(string)
    log.write(time.now() + string + "\n")