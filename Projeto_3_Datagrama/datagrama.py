import re


class Head:
    messageType: str
    senderId: str
    receiverId: str
    totalPayloads: int = 0
    currentPayloadIndex: int = 0
    payloadSize: int = 0

    def __init__(self, messageType, senderId, receiverId):
        self.messageType = messageType
        self.senderId = senderId
        self.receiverId = receiverId

    def payloadData(self, totalPayloads, currentPayloadIndex, payload):
        if self.messageType == 'DD':
            self.totalPayloads = totalPayloads
            self.currentPayloadIndex = currentPayloadIndex
            self.payloadSize = len(payload)
        else:
            raise Exception("Error: Message type does not support non-0 payload")


class Datagrama:
    head: Head
    payload: str = ''
    endOfPackage: str = 'FEEDBACC'

    def __init__(self, head, payload):
        self.head = head
        self.payload = payload