from datagrama import Head, Datagrama

def stringToDatagram(string):
    head = Head(string[0:2], string[2:4], string[4:6])
    head.totalPayloads = string[6:12]
    head.currentPayloadIndex = string[12:18]
    head.payloadSize = string[18:20]
    head.finalString = string[0:20]

    datagram = Datagrama(head, string[20:-8])
    datagram.endOfPackage = string[(20 + int(head.payloadSize)):]

    return datagram