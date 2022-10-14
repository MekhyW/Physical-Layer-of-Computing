from neoDatagram import *
from enlace import *
import time
import math
from logger import *
from neoStringToDatagram import neoStringToDatagram
from validatePackage import validatePackage

serialName = "COM11"
com1 = enlace(serialName)
arquivo = None
payload_size_limit = 99
cont = 0
fileId = ''
log = open("clientlog.txt", "w", encoding="utf-8")

totalPackages = 0
restartPackage = 1
lastValidatedPackage = 1

def sacrificeBytes():
    com1.enable()
    time.sleep(.2)
    com1.sendData(b'00')
    time.sleep(1)
    print("Bytes de sacrifício enviados")

def loadFile():
    global arquivo, fileId
    #filename = input("Digite o nome do arquivo a ser enviado: ")
    filename = "jureg.txt"
    while len(fileId) != 2:
        #fileId = input("Digite o ID do arquivo (2 dígitos): ")
        fileId = "00"
    try:
        with open(filename, "r") as file:
            arquivo = file.read()
            print(arquivo)
            print("\nArquivo carregado e lido")
            file.close()
    except FileNotFoundError:
        print("Arquivo não encontrado")
        quit()

def handshake():
    global fileId, totalPackages, restartPackage, lastValidatedPackage
    handshakeHead = Head('01', 'CC', '55', str(totalPackages).zfill(2), '00', str(fileId).zfill(2), str(restartPackage).zfill(2), str(lastValidatedPackage).zfill(2))
    handshake = Datagram(handshakeHead, '')
    logger(log, 'envio', handshake.head.h0, len(handshake.fullPackage), handshake.head.h4, handshake.head.h3, handshake.head.crc)
    com1.sendData(bytes(handshake.fullPackage, "utf-8"))
    print('Handshake enviado, aguardando resposta do servidor...')
    time.sleep(5)
    rxLen = com1.rx.getBufferLen()
    if not rxLen or not com1.getData(rxLen)[0].decode().startswith('02'):
        print("Servidor inativo")
        return False
    rxBuffer, nRx = com1.getData(rxLen)
    packageString = rxBuffer.decode()
    packageDatagram = neoStringToDatagram(packageString)
    logger(log, 'recebimento', packageDatagram.head.h0, len(packageString), packageDatagram.head.h4, packageDatagram.head.h3, packageDatagram.head.crc)
    com1.rx.clearBuffer()
    print('Handshake recebido, servidor ativo')
    return True


def buildPackages():
    global totalPayloads, restartPackage, lastValidatedPackage
    restartPackagelocal = restartPackage
    lastValidatedPackagelocal = lastValidatedPackage
    packages = []
    datagrams = []
    totalPayloads = math.ceil(len(arquivo)/payload_size_limit)
    for i in range(totalPayloads):
        payload = ''
        for j in range(payload_size_limit):
            try:
                payload += str(arquivo[i*payload_size_limit+j])
            except IndexError:
                break
        head = Head('03', 'CC', '55', str(totalPayloads).zfill(2), str(i+1).zfill(2), str(len(payload)).zfill(2), str(restartPackagelocal).zfill(2), str(lastValidatedPackagelocal).zfill(2))
        datagram = Datagram(head, payload)
        packages.append(bytes(datagram.fullPackage, "utf-8"))
        datagrams.append(datagram)
        restartPackagelocal += 1
        lastValidatedPackagelocal += 1
    return packages, datagrams
        

def transferPackage(package, datagram: Datagram):
    global cont, totalPayloads, restartPackage, lastValidatedPackage, log
    logger(log, 'envio', datagram.head.h0, len(datagram.fullPackage), datagram.head.h4, datagram.head.h3, datagram.head.crc)
    com1.sendData(package)
    print("Pacote enviado: " + str(package))
    timer1 = time.time()
    timer2 = time.time()
    rxLen = 0
    packageValidity = False
    while not packageValidity:
        while not rxLen:
            rxLen = com1.rx.getBufferLen()
            tempoatual = time.time()
            if tempoatual - timer2 > 20:
                timeoutHead = Head('05', 'CC', '55', str(totalPackages).zfill(2), '00', '00', str(restartPackage).zfill(2), str(lastValidatedPackage).zfill(2))
                timeout = Datagram(timeoutHead, '')
                logger(log, 'envio', timeout.head.h0, len(timeout.fullPackage), timeout.head.h4, timeout.head.h3, timeout.head.crc)
                com1.sendData(bytes(timeout.fullPackage, "utf-8"))
                print("Pacote enviado: " + str(package))
                print("Timeout :-(")
                encerrar()
            elif tempoatual - timer1 > 5:
                logger(log, 'envio', datagram.head.h0, len(datagram.fullPackage), datagram.head.h4, datagram.head.h3, datagram.head.crc)
                com1.sendData(package)
                print("Pacote enviado: " + str(package))
                timer1 = tempoatual
            elif rxLen:
                rxBuffer, nRx = com1.getData(rxLen)
                packageString = rxBuffer.decode()
                packageDatagram = neoStringToDatagram(packageString)
                logger(log, 'recebimento', packageDatagram.head.h0, len(packageString), packageDatagram.head.h4, packageDatagram.head.h3, packageDatagram.head.crc)
                packageValidity = validatePackage(packageDatagram, restartPackage, lastValidatedPackage)
                if packageValidity and packageString.startswith('04'):
                    lastValidatedPackage += 1
                    restartPackage += 1
                    cont += 1
                if packageString.startswith('06'):
                    cont -= 1
        com1.rx.clearBuffer()
    time.sleep(2)
        
def encerrar():
    print("-------------------------")
    print("Comunicação encerrada")
    print("-------------------------")
    com1.disable()
    log.close()
    quit()

if __name__ == "__main__":
    sacrificeBytes()
    loadFile()
    packages, datagrams = buildPackages()
    totalPackages = len(packages)
    while not cont:
        if handshake():
            cont = 1
    print("Iniciando transmissão de mensagem")
    while cont <= totalPackages:
        print("Pacote: {} / {}".format(cont, totalPackages))
        transferPackage(packages[cont-1], datagrams[cont-1])
    print("SUCESSO!")
    encerrar()
