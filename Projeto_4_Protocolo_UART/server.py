from enlace import *
import time
from neoDatagram import *
from neoStringToDatagram import *
import os
from logger import *
from validatePackage import validatePackage

if os.path.exists("recebido.txt"):
    os.remove("recebido.txt")
    
serialName = "COM7"
com1 = enlace(serialName)
ocioso = True
cont = 0
log = open("serverlog.txt", "w", encoding="utf-8")

payload = ''
fileId = ''

totalPackages = 0
restartPackage = 1
lastValidatedPackage = 0

def receiveSacrificeBytes():
    print('Esperando 1 byte de sacrifício')
    com1.enable()
    time.sleep(.2)
    rxBuffer, nRx = com1.getData(1)
    com1.rx.clearBuffer()
    time.sleep(.1)

def checkHandshake():
    global ocioso, totalPackages, fileId, log, restartPackage, lastValidatedPackage
    rxLen = com1.rx.getBufferLen()
    rxBuffer, nRx = com1.getData(rxLen)
    packageString = rxBuffer.decode()
    packageDatagram = neoStringToDatagram(packageString)
    print("{0} -> {1}".format(packageString, packageDatagram.head.fullHead))
    if packageString.startswith('01CC55') and packageString.endswith('AABBCCDD'):
        if validatePackage(packageDatagram,  restartPackage, lastValidatedPackage):
            print('Handshake recebido do client')
            logger(log, 'recebimento', packageDatagram.head.h0, len(packageString), packageDatagram.head.h4, packageDatagram.head.h3)
            fileId = packageDatagram.head.h5
            print('Id do arquivo: {}'.format(fileId))
            totalPackages = int(packageDatagram.head.h3, 16)
            print('Número de pacotes a serem recebidos: {}'.format(totalPackages))
            ocioso = False
        else:
            print('Pacote inválido')
            ocioso = True
    else:
        print('Mensagem não é handshake, ignorada')
        ocioso = True
    com1.rx.clearBuffer()
    
def handshake():
    global fileId, totalPackages, restartPackage, lastValidatedPackage
    handshakeHead = Head('02', '55', 'CC', str(totalPackages).zfill(2), '00', str(fileId).zfill(2), str(restartPackage).zfill(2), str(lastValidatedPackage).zfill(2))
    handshake = Datagram(handshakeHead, '')
    logger(log, 'envio', handshake.head.h0, len(handshake.fullPackage), handshake.head.h4, handshake.head.h3)
    com1.sendData(bytes(handshake.fullPackage, "utf-8"))
    print('Confirmação de handshake enviada')

def analisaPacote(datagram : Datagram, decoded : str):
    global payload, cont, totalPackages, restartPackage, lastValidatedPackage
    if not decoded.startswith('03'):
        print("Tipo do pacote errado, pedindo reenvio " + decoded)
        t6Head = Head('06', '55', 'CC', str(totalPackages).zfill(2), '00', '00', str(restartPackage).zfill(2), str(lastValidatedPackage).zfill(2))
        t6 = Datagram(t6Head, '')
        logger(log, 'envio', t6.head.h0, len(t6.fullPackage), t6.head.h4, t6.head.h3)
        com1.sendData(bytes(t6.fullPackage, "utf-8"))
        return
    if not decoded.endswith('AABBCCDD'):
        print("EoP no local errado, pedindo reenvio do pacote " + decoded)
        t6Head = Head('06', '55', 'CC', str(totalPackages).zfill(2), '00', '00', str(restartPackage).zfill(2), str(lastValidatedPackage).zfill(2))
        t6 = Datagram(t6Head, '')
        logger(log, 'envio', t6.head.h0, len(t6.fullPackage), t6.head.h4, t6.head.h3)
        com1.sendData(bytes(t6.fullPackage, "utf-8"))
        return
    if not int(datagram.head.h5) == len(datagram.payload):
        print("Index do pacote errado, pedindo reenvio do pacote " + decoded)
        t6Head = Head('06', '55', 'CC', str(totalPackages).zfill(2), '00', '00', str(restartPackage).zfill(2), str(lastValidatedPackage).zfill(2))
        t6 = Datagram(t6Head, '')
        logger(log, 'envio', t6.head.h0, len(t6.fullPackage), t6.head.h4, t6.head.h3)
        com1.sendData(bytes(t6.fullPackage, "utf-8"))
        return
    payload += datagram.payload
    lastValidatedPackage += 1
    restartPackage += 1
    cont += 1
    t4Head = Head('04', '55', 'CC', str(totalPackages).zfill(2), '00', '00', str(restartPackage).zfill(2), str(lastValidatedPackage).zfill(2))
    t4 = Datagram(t4Head, '')
    logger(log, 'envio', t4.head.h0, len(t4.fullPackage), t4.head.h4, t4.head.h3)
    com1.sendData(bytes(t4.fullPackage, "utf-8"))

def receivePackage():
    global payload, ocioso, totalPackages, restartPackage, lastValidatedPackage, log
    timer1 = time.time()
    timer2 = time.time()
    rxLen = com1.rx.getBufferLen()
    packageValidity = False
    while not packageValidity:
        while not rxLen:
            rxLen = com1.rx.getBufferLen()
            tempoatual = time.time()
            if tempoatual - timer1 > 2:
                t4Head = Head('04', '55', 'CC', str(totalPackages).zfill(2), '00', '00', str(restartPackage).zfill(2), str(lastValidatedPackage).zfill(2))
                t4 = Datagram(t4Head, '')
                logger(log, 'envio', t4.head.h0, len(t4.fullPackage), t4.head.h4, t4.head.h3)
                com1.sendData(bytes(t4.fullPackage, "utf-8"))
                time.sleep(1)
                timer1 = tempoatual
            if tempoatual - timer2 > 20:
                ocioso = True
                t5Head = Head('05', '55', 'CC', str(totalPackages).zfill(2), '00', '00', str(restartPackage).zfill(2), str(lastValidatedPackage).zfill(2))
                t5 = Datagram(t5Head, '')
                com1.sendData(bytes(t5.fullPackage, "utf-8"))
                logger(log, 'envio', t5.head.h0, len(t5.fullPackage), t5.head.h4, t5.head.h3)
                print("Timeout :-(")
                encerrar()
        rxBuffer, nRx = com1.getData(rxLen)
        packageString = rxBuffer.decode()
        packageDatagram = neoStringToDatagram(packageString)
        packageValidity = validatePackage(packageDatagram, restartPackage,  lastValidatedPackage)
        logger(log, 'recebimento', packageDatagram.head.h0, len(packageString), packageDatagram.head.h4, packageDatagram.head.h3)
        print(packageDatagram.head.fullHead)
        com1.rx.clearBuffer()
    analisaPacote(packageDatagram, packageString)

def salvarArquivo():
    print("Salvando arquivo")
    with open("recebido.txt", "w") as arquivo:
        arquivo.write(payload)

def encerrar():
    print("-------------------------")
    print("Comunicação encerrada")
    print("-------------------------")
    com1.disable()
    log.close()
    quit()

if __name__ == "__main__":
    try:
        receiveSacrificeBytes()
        while ocioso:
            checkHandshake()
            time.sleep(1)
        handshake()
        cont = 1
        while cont <= totalPackages:
            print("Pacote: {} / {}".format(cont, totalPackages))
            receivePackage()
            time.sleep(1)
        salvarArquivo()
        print("SUCESSO!")
        encerrar()
    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        encerrar()
