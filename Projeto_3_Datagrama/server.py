from enlace import *
import time
import numpy as np
from datagrama import *
from stringToDatagram import *

serialName = "COM7"

previousPackageIndex = -1

com1 = enlace(serialName)
com1.enable()
payload = ''

def handshake():
    handshake_head = Head('AA', '55', 'CC')
    handshake_head.buildHead()
    handshake = Datagrama(handshake_head, '')
    com1.sendData(bytes(handshake.head.finalString + handshake.endOfPackage, "utf-8"))
    print('Handshake recebido, enviando confirmação')

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

        while True:
            rxLen = com1.rx.getBufferLen()
            while rxLen == 0:
                rxLen = com1.rx.getBufferLen()
                time.sleep(1)
            rxBuffer, nRx = com1.getData(rxLen)

            decoded = rxBuffer.decode()
            datagram = stringToDatagram(decoded)

            if datagram.head.messageType == 'DD':
                print(datagram.head.currentPayloadIndex)
                print(type(datagram.head.currentPayloadIndex))
                if int(datagram.head.currentPayloadIndex) == previousPackageIndex + 1:
                    print("Pacote recebido com sucesso")
                    payload += datagram.payload
                    confirmation = Datagrama(Head('77', '55', 'CC'), '')
                    com1.sendData(bytes(confirmation.head.finalString + confirmation.endOfPackage, "utf-8"))
                    previousPackageIndex += 1
                else:
                    print("Index do pacote errado, pedindo reenvio do pacote")
                    confirmation = Datagrama(Head('99', '55', 'CC'), '')
                    com1.sendData(bytes(confirmation.head.finalString + confirmation.endOfPackage, "utf-8"))
                
                if datagram.head.currentPayloadIndex == datagram.head.totalPayloads:
                    print("Todos pacotes recebidos com sucesso")
                    confirmation = Datagrama(Head('77', '55', 'CC'), '')
                    com1.sendData(bytes(confirmation.head.finalString + confirmation.endOfPackage, "utf-8"))
                    break
                
                com1.rx.clearBuffer()	
            else:
                raise Exception("Erro: tipo do pacote recebido não é de dados")


        # Salvando arquivo

        print("Salvando arquivo")
        with open("recebido.png", "wb") as arquivo:
            arquivo.write(payload)

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
