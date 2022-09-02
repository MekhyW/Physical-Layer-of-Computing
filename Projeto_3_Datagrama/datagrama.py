class Head:
    messageType: str
    senderId: str
    receiverId: str
    totalPayloads: str = '0'
    currentPayloadIndex: str = '0'
    payloadSize: str = '0'
    finalString = ''

    def __init__(self, messageType, senderId, receiverId):
        self.messageType = messageType
        self.senderId = senderId
        self.receiverId = receiverId

    def payloadData(self, totalPayloads, currentPayloadIndex, payload):
        if self.messageType == 'DD':
            self.totalPayloads = str(totalPayloads)
            self.currentPayloadIndex = str(currentPayloadIndex)
            self.payloadSize = str(len(payload))
        else:
            raise Exception("Error: Message type does not support non-0 payload")

    def buildHead(self):
        if len(self.totalPayloads) == 1:
            self.totalPayloads = '00' + self.totalPayloads
        elif len(self.totalPayloads) == 2:
            self.totalPayloads = '0' + self.totalPayloads
        if len(self.currentPayloadIndex) == 1:
            self.currentPayloadIndex = '00' + self.currentPayloadIndex
        elif len(self.currentPayloadIndex) == 2:
            self.currentPayloadIndex = '0' + self.currentPayloadIndex
        if len(self.payloadSize) == 1:
            self.payloadSize = '00' + self.payloadSize
        elif len(self.payloadSize) == 2:
            self.payloadSize = '0' + self.payloadSize
        self.finalString = self.messageType + self.senderId + self.receiverId + self.totalPayloads + self.currentPayloadIndex + self.payloadSize


class Datagrama:
    head: Head
    payload: str = ''
    endOfPackage: str = 'FEEDBACC'

    def __init__(self, head, payload):
        self.head = head
        self.payload = payload