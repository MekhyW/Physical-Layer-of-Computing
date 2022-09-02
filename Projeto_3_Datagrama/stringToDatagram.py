from datagrama import Head, Datagrama

def stringToDatagram(string):
    head = Head()
    head.messageType = string[0:2]
    head.senderId = string[2:4]
    pass