class Head:
    messageType: str
    senderId: str
    receiverId: str
    totalPayloads: int
    currentPayloadIndex: int
    payloadSize: int

class Datagrama:
    head: Head
    payload: str = ''
    endOfPackage: str = 'FEEDBACC'