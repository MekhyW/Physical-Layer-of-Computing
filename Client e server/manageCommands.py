import random

def generateCommands(numberOfCommands, bytesize = 8):
    commands = ["00FA0000", "0000FA00", "FA0000", "00FA00", "0000FA", "00FA", "FA00", "00", "FA"]
    commandList = random.choices(commands, k=numberOfCommands)
    random.shuffle(commandList)
    commandString = ""
    for value in range(numberOfCommands):
        command = commandList[value]
        while len(command) < bytesize:
            command = "0" + command
        commandString += command
    commandBytes = commandString.encode()
    return commandBytes