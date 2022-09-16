from enlace import *
import time
from neoDatagram import *
from neoStringToDatagram import *
import os

if os.path.exists("recebido.txt"):
    os.remove("recebido.txt")
    
serialName = "COM7"
com1 = enlace(serialName)
ocioso = True
cont = 0
numPck = 0
payload = ''
previousPackageIndex = -1
fileId = ''

def receiveSacrificeBytes():
    print('Esperando 1 byte de sacrifício')
    rxBuffer, nRx = com1.getData(1)
    com1.rx.clearBuffer()
    time.sleep(.1)

def checkHandshake():
    global ocioso, numPck, fileId
    rxLen = com1.rx.getBufferLen()
    rxBuffer, nRx = com1.getData(rxLen)
    t1 = rxBuffer.decode()
    if t1.startswith('01CC55') and t1.endswith('AABBCCDD'):
        print('Handshake recebido do client')
        fileId = t1[10:12]
        print('Id do arquivo: {}'.format(fileId))
        numPck = int(t1[7:9], 16)
        print('Número de pacotes a serem recebidos: {}'.format(numPck))
        ocioso = False
    else:
        print('Mensagem não é handshake, ignorada')
        ocioso = True
    com1.rx.clearBuffer()
    
def handshake():
    global cont, fileId
    t2Head = Head('02', '55', 'CC', '00', '00', '00', '00', '00', fileId=fileId)
    t2 = Datagram(t2Head, '')
    com1.sendData(bytes(t2.datagram, "utf-8"))
    print('Confirmação de handshake enviada')
    cont = 1

def analisaPacote(datagram, decoded):
    global payload, previousPackageIndex
    global cont
    if not decoded.startswith('03'):
        print("Tipo do pacote errado, pedindo reenvio")
        t6Head = Head('06', '55', 'CC', '00', '00', '00', '00', '00')
        t6 = Datagram(t6Head, '')
        com1.sendData(bytes(t6.datagram, "utf-8"))
        return
    if not decoded.endswith('FEEDBACC'):
        print("EoP no local errado, pedindo reenvio do pacote")
        t6Head = Head('06', '55', 'CC', '00', '00', '00', '00', '00')
        t6 = Datagram(t6Head, '')
        com1.sendData(bytes(t6.datagram, "utf-8"))
        return
    if not int(datagram.head.h5) == len(datagram.payload):
        print("Index do pacote errado, pedindo reenvio do pacote")
        t6Head = Head('06', '55', 'CC', '00', '00', '00', '00', '00')
        t6 = Datagram(t6Head, '')
        com1.sendData(bytes(t6.datagram, "utf-8"))
        return
    payload += datagram.payload
    previousPackageIndex += 1
    t4Head = Head('04', '55', 'CC', '00', '00', '00', '00', previousPackageIndex)
    t4 = Datagram(t4Head, '')
    com1.sendData(bytes(t4.datagram, "utf-8"))
    cont += 1

def receivePackage():
    global payload, previousPackageIndex
    global ocioso
    timer1 = time.time()
    timer2 = time.time()
    rxLen = com1.rx.getBufferLen()
    while not rxLen:
        rxLen = com1.rx.getBufferLen()
        tempoatual = time.time()
        time.sleep(1)
        if tempoatual - timer2 > 20:
            ocioso = True
            t5Head = Head('05', '55', 'CC', '00', '00', '00', '00', '00')
            t5 = Datagram(t5Head, '')
            com1.sendData(bytes(t5.datagram, "utf-8"))
            print("Timeout :-(")
            encerrar()
        elif tempoatual - timer1 > 2:
            t4Head = Head('04', '55', 'CC', '00', '00', '00', '00', previousPackageIndex)
            t4 = Datagram(t4Head, '')
            com1.sendData(bytes(t4.datagram, "utf-8"))
            timer1 = tempoatual
    rxBuffer, nRx = com1.getData(rxLen)
    decoded = rxBuffer.decode()
    datagram = neoStringToDatagram(decoded)
    com1.rx.clearBuffer()
    analisaPacote(datagram, decoded)

def salvarArquivo():
    print("Salvando arquivo")
    with open("recebido.txt", "w") as arquivo:
        arquivo.write(payload)

def encerrar():
    print("-------------------------")
    print("Comunicação encerrada")
    print("-------------------------")
    com1.disable()
    quit()

if __name__ == "__main__":
    while ocioso:
        checkHandshake()
        time.sleep(1)
    handshake()
    while cont <= numPck:
        receivePackage()
        print("Pacote: {} / {}".format(cont, numPck))
    salvarArquivo()
    print("SUCESSO!")
    encerrar()
