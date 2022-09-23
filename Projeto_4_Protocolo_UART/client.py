from neoDatagram import *
from enlace import *
import time
import math

serialName = "COM12"
com1 = enlace(serialName)
arquivo = None
payload_size_limit = 99
cont = 0
numPck = 0
fileId = ''

def sacrificeBytes():
    com1.enable()
    time.sleep(.2)
    com1.sendData(b'00')
    time.sleep(1)
    print("Bytes de sacrifício enviados")

def loadFile():
    global arquivo, fileId
    filename = input("Digite o nome do arquivo a ser enviado: ")
    while len(fileId) != 2:
        fileId = input("Digite o ID do arquivo (2 dígitos): ")
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
    global fileId
    handshakeHead = Head('01', 'CC', '55', '00', '00', '00', '00', '00', fileId=fileId)
    handshake = Datagram(handshakeHead, '')
    com1.sendData(bytes(handshake.fullPackage, "utf-8"))
    print('Handshake enviado, aguardando resposta do servidor...')
    time.sleep(5)
    rxLen = com1.rx.getBufferLen()
    if not rxLen or not com1.getData(rxLen)[0].decode().startswith('02'):
        print("Servidor inativo")
        return False
    com1.rx.clearBuffer()
    print('Handshake recebido, servidor ativo')
    return True


def buildPackages():
    packages = []
    totalPayloads = math.ceil(len(arquivo)/payload_size_limit)
    for i in range(totalPayloads):
        payload = ''
        for j in range(payload_size_limit):
            try:
                payload += str(arquivo[i*payload_size_limit+j])
            except IndexError:
                break
        head = Head('03', 'CC', '55', str(totalPayloads), str(i).zfill(2), str(len(payload)), '00', '00')
        datagram = Datagram(head, payload)
        packages.append(bytes(datagram.fullPackage, "utf-8"))
    return packages
        

def transferPackage(package):
    global cont
    com1.sendData(package)
    timer1 = time.time()
    timer2 = time.time()
    rxLen = 0
    while not rxLen:
        rxLen = com1.rx.getBufferLen()
        tempoatual = time.time()
        if tempoatual - timer1 > 5:
            com1.sendData(package)
            timer1 = tempoatual
        if tempoatual - timer2 > 10:
            timeoutHead = Head('05', 'CC', '55', '00', '00', '00', '00', '00')
            timeout = Datagram(timeoutHead, '')
            com1.sendData(bytes(timeout.fullPackage, "utf-8"))
            print("Timeout :-(")
            encerrar()
        elif rxLen:
            rxBuffer, nRx = com1.getData(rxLen)
            packageString = rxBuffer.decode()
            if packageString.startswith('06'):
                cont -= 1
    com1.rx.clearBuffer()
        
def encerrar():
    print("-------------------------")
    print("Comunicação encerrada")
    print("-------------------------")
    com1.disable()
    quit()

if __name__ == "__main__":
    sacrificeBytes()
    while not cont:
        if handshake():
            cont = 1
    loadFile()
    packages = buildPackages()
    numPck = len(packages)
    print("Iniciando transmissão de mensagem")
    while cont <= numPck:
        transferPackage(packages[cont-1])
        print("Pacote: {} / {}".format(cont, numPck))
        cont += 1
    print("SUCESSO!")
    encerrar()
