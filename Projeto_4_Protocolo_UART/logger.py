from datetime import datetime

def printAndLog(log, string):
    print(string)
    log.write(datetime.now() + string + "\n")