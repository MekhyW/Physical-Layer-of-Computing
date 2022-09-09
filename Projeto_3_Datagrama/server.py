from enlace import *
import time
import numpy as np
from datagrama import *
from stringToDatagram import *
import os

serialName = "COM7"

previousPackageIndex = -1

if os.path.exists("recebido.txt"):
    os.remove("recebido.txt")

com1 = enlace(serialName)
com1.enable()
payload = ''

def handshake():
    handshake_head = Head('AA', '55', 'CC')
    handshake_head.buildHead()
    handshake = Datagrama(handshake_head, '')
    com1.sendData(bytes(handshake.head.finalString + handshake.endOfPackage, "utf-8"))
    print('Handshake recebido, enviando confirmação')

def acknowledge():
    confirmationHead = Head('77', '55', 'CC')
    confirmationHead.buildHead()
    confirmation = Datagrama(confirmationHead, '')
    confirmationString = confirmation.head.finalString + confirmation.endOfPackage
    while len(confirmationString) < 27:
        confirmationHead = Head('77', '55', 'CC')
        confirmationHead.buildHead()
        confirmation = Datagrama(confirmationHead, '')
        confirmationString = confirmation.head.finalString + confirmation.endOfPackage
    print(confirmationString)
    com1.sendData(bytes(confirmationString, "utf-8"))

def not_acknowledge():
    confirmationHead = Head('99', '55', 'CC')
    confirmationHead.buildHead()
    confirmation = Datagrama(confirmationHead, '')
    confirmationString = confirmation.head.finalString + confirmation.endOfPackage
    while len(confirmationString) < 27:
        confirmationHead = Head('99', '55', 'CC')
        confirmationHead.buildHead()
        confirmation = Datagrama(confirmationHead, '')
        confirmationString = confirmation.head.finalString + confirmation.endOfPackage
    #print(confirmationString)
    com1.sendData(bytes(confirmationString, "utf-8"))

def main():
    global payload
    global previousPackageIndex
    try:
        #Byte de sacrifício
        print("Esperando 1 byte de sacrifício")
        rxBuffer, nRx = com1.getData(1)
        com1.rx.clearBuffer()
        time.sleep(.1)

        print("Comunicação aberta com sucesso")

        # Handshake
        print("Esperando handshake...")
        rxLen = com1.rx.getBufferLen()
        while rxLen == 0:
            rxLen = com1.rx.getBufferLen()
            time.sleep(.5)
        rxBuffer, nRx = com1.getData(rxLen)

        decoded = rxBuffer.decode()
        datagram = stringToDatagram(decoded)

        if decoded.startswith('AA'):
            handshake()
        else:
            raise Exception("Erro: pacote recebido não é handshake")
        
        com1.rx.clearBuffer()

        # Recebendo pacotes

        print("Iniciando recebimento de pacotes")
        print("-----------------------------------------")

        while True:
            rxLen = com1.rx.getBufferLen()
            while rxLen == 0:
                rxLen = com1.rx.getBufferLen()
                time.sleep(1)
            rxBuffer, nRx = com1.getData(rxLen)

            decoded = rxBuffer.decode()
            datagram = stringToDatagram(decoded)

            print(int(datagram.head.payloadSize))
            print(len(datagram.payload))

            if decoded.startswith('DD'):
                if decoded.endswith('FEEDBACC'):
                    if int(datagram.head.payloadSize) == len(datagram.payload):
                        if int(datagram.head.currentPayloadIndex) == previousPackageIndex + 1:
                            print("Pacote {0} recebido com sucesso".format(previousPackageIndex+1))
                            payload += datagram.payload
                            acknowledge()
                            previousPackageIndex += 1
                            print(previousPackageIndex)
                        else:
                            print("Index do pacote errado, pedindo reenvio do pacote")
                            not_acknowledge()
                        
                        print("Current Payload Index:{0}".format(int(datagram.head.currentPayloadIndex) + 1))
                        print("Total Payload Index: {0}".format(int(datagram.head.totalPayloads)))
                        if int(datagram.head.currentPayloadIndex) + 1 == int(datagram.head.totalPayloads):
                            print("Todos pacotes recebidos com sucesso")
                            break
                    else:
                        print("Tamanho do payload errado, pedindo reenvio do pacote")
                        not_acknowledge()
                else:
                        print("EoP no local errado, pedindo reenvio do pacote")
                        not_acknowledge()
                        
                print("--------------------------------------------------")    
                com1.rx.clearBuffer()	
            else:
                print("Tipo do pacote errado, pedindo reenvio do pacote")
                not_acknowledge()


        # Salvando arquivo
        decodedPayload = payload
        print("Salvando arquivo")
        with open("recebido.txt", "w") as arquivo:
            arquivo.write(decodedPayload)

        acknowledge()

        # Encerra comunicação
        print("-------------------------")
        print("Comunicação encerrada")
        print("-------------------------")
        com1.disable()
        
    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()
        

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()
