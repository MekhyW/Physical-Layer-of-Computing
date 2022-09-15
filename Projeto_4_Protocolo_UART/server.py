from enlace import *
import time
from datagrama import *
from stringToDatagram import *
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

def receiveSacrificeBytes():
    print("Esperando 1 byte de sacrifício")
    rxBuffer, nRx = com1.getData(1)
    com1.rx.clearBuffer()
    time.sleep(.1)

def checkHandshake():
    #FALTA CHECAR SE MENSAGEM É T1 E SE É PARA MIM, E ATUALIZAR O NUMERO DE PACOTES
    global ocioso, numPck
    rxLen = com1.rx.getBufferLen()
    if not rxLen:
        return False
    com1.rx.clearBuffer()
    print('Handshake recebido do client')
    ocioso = False
    return True

def handshake():
    #FALTA MANDAR TIPO T2
    global cont
    handshake_head = Head('AA', '55', 'CC')
    handshake_head.buildHead()
    handshake = Datagrama(handshake_head, '')
    com1.sendData(bytes(handshake.head.finalString + handshake.endOfPackage, "utf-8"))
    print('Confirmação de handshake enviada')
    cont = 1

def analisaPacote(datagram, decoded):
    global payload, previousPackageIndex
    global cont
    if not decoded.startswith('DD'):
        print("Tipo do pacote errado, pedindo reenvio do pacote")
        #manda mensagem t6
        return
    if not decoded.endswith('FEEDBACC'):
        print("EoP no local errado, pedindo reenvio do pacote")
        #manda mensagem t6
        return
    if not int(datagram.head.payloadSize) == len(datagram.payload):
        print("Index do pacote errado, pedindo reenvio do pacote")
        #manda mensagem t6
        return
    payload += datagram.payload
    previousPackageIndex += 1
    #manda mensagem t4
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
            #manda mensagem t5
            print("Timeout :-(")
            encerrar()
        elif tempoatual - timer1 > 2:
            #manda mensagem t4
            timer1 = tempoatual
    rxBuffer, nRx = com1.getData(rxLen)
    decoded = rxBuffer.decode()
    datagram = stringToDatagram(decoded)
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
