from neoDatagram import *
from enlace import *
import time
import math

serialName = "COM11"
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

def askStart():
    global cont
    if input('Iniciar? S/N ').lower() == 's':
        cont = 1
    elif handshake():
        cont = 1

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
    #FALTA MANDAR TIPO T1 E CHECAR SE RESPOSTA É T2
    global fileId
    handshakeHead = Head('01', 'CC', '55', '00', '00', '00', '00', '00', fileId=fileId)
    handshake = Datagram(handshakeHead, '')
    com1.sendData(bytes(handshake.datagram, "utf-8"))
    print('Handshake enviado, aguardando resposta do servidor...')
    time.sleep(5)
    rxLen = com1.rx.getBufferLen()
    if not rxLen:
        print("Servidor inativo")
        return False
    com1.rx.clearBuffer()
    print('Handshake recebido, servidor ativo')
    return True


def buildPackages():
    #FALTA FAZER CADA PACOTE MONTADO SER TIPO T3
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
        packages.append(bytes(datagram.datagram, "utf-8"))
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
            #mandar mensagem de timeout aqui
            print("Timeout :-(")
            encerrar()
        elif rxLen:
            #se for t6, cont-=1 e com1.sendData(package)
            pass
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
        askStart()
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
