from neoDatagram import *

def neoStringToDatagram(string):
    head = Head(string[0:2], string[2:4], string[4:6], string[6:8], string[8:10], string[10:12], string[12:14], string[14:16])

    datagram = Datagram(head, string[20:-8])

    return datagram