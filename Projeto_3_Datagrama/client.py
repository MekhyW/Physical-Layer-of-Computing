from datagrama import *
from enlace import *
import time
import math
import numpy as np

serialName = "COM11"
com1 = enlace(serialName)
arquivo = None
payload_size_limit = 114

def start():
    com1.enable()
    time.sleep(.2)
    com1.sendData(b'00')
    time.sleep(1)
    print("Bytes de sacrifício enviados")

def loadFile():
    global arquivo
    filename = input("Digite o nome do arquivo a ser enviado: ")
    try:
        with open(filename, "rb") as file:
            arquivo = file.read()
            print("Arquivo carregado e lido")
            file.close()
    except FileNotFoundError:
        print("Arquivo não encontrado")
        quit()

def buildPackages():
    packages = []
    totalPayloads = math.ceil(len(arquivo)/payload_size_limit)
    for i in range(totalPayloads):
        head = Head('DD', '00', '00')
        payload = ''
        for j in range(payload_size_limit):
            try:
                payload += str(arquivo[i*payload_size_limit+j])
            except IndexError:
                break
        head.payloadData(totalPayloads, i, payload)
        head.buildHead()
        datagram = Datagrama(head, payload)
        packages.append(bytes(datagram.head.finalString + datagram.payload + datagram.endOfPackage, "utf-8"))
    return packages
        

def main():
    try:
        # Implementar handshake aqui

        print("Iniciando transmissão de mensagem")
        
        packages = buildPackages()
        for package_id in range(len(packages)):
            com1.sendData(packages[package_id])
            print("Pacote: {}".format(package_id))
            timer=0
            print(timer)
            rxLen = com1.rx.getBufferLen()
            while not rxLen:
                rxLen = com1.rx.getBufferLen()
                time.sleep(1)
                timer += 1
                print(timer)
                if timer >= 5:
                    raise TimeoutError
            rxBuffer, nRx = com1.getData(rxLen)
            serverCommands = int.from_bytes(rxBuffer, "little")
            # Implementar análise da resposta do servidor aqui

        print("-------------------------")
        print("Comunicação encerrada")
        print("-------------------------")
        com1.disable()
    
    except TimeoutError:
        if "s" in input("Servidor inativo. Tentar novamente? S/N ").lower():
            main()
        else:
            com1.disable()
            quit()

    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()
        

#so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    start()
    loadFile()
    main()
