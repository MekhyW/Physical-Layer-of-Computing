from datagrama import Head, Datagrama

def stringToDatagram(string):
    head = Head()
    head.messageType = string[0:2]
    head.senderId = string[2:4]
    head.receiverId = string[4:6]
    head.totalPayloads = string[6:12]
    head.currentPayloadIndex = string[12:18]
    head.payloadSize = string[18:20]
    head.finalString = string[0:20]

    datagram = Datagrama()
    datagram.head = head.finalString
    datagram.payload = string[20:(20 + int(head.payloadSize))]
    datagram.endOfPackage = string[(20 + int(head.payloadSize)):]

    return datagram