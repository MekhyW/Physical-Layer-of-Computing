from datetime import datetime

def printAndLog(log, string):
    print(string)
    log.write(str(datetime.now()) + ' ' + string + "\n")