from datetime import datetime

def logger(log, sendOrRecieve, messageType, packageSize, packageIndex, totalPackages):
    if messageType != 3:
        log.write(str(datetime.now()) + " / " + str(sendOrRecieve) + " / " + str(messageType) + " / " + str(packageSize) + "\n")	
    else:
        log.write(str(datetime.now()) + " / " + str(sendOrRecieve) + " / " + str(messageType) + " / " + str(packageSize) + " / " + str(packageIndex) + " / " + str(totalPackages) + "\n")