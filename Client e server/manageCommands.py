import random

def generateCommands(numberOfCommands, bytesize = 8):
    commands = ["00FF00FF", "00FFFF00", "FF", "00", "FF00", "00FF"]
    commandList = random.choices(commands, k=numberOfCommands-len(commands)) + commands
    random.shuffle(commandList)
    commandString = ""
    for value in range(numberOfCommands):
        command = commandList[value]
        while len(command) < bytesize:
            command = "0" + command
        commandString += command
    commandBytes = commandString.encode()
    return commandBytes