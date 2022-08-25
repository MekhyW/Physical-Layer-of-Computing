from enlace import *
import time
import numpy as np

serialName = "COM6"

def main():
    try:
        com1 = enlace(serialName)
        com1.enable()

        #Byte de sacrifício
        print("Esperando 1 byte de sacrifício")
        rxBuffer, nRx = com1.getData(1)
        com1.rx.clearBuffer()
        time.sleep(.1)

        print("Comunicação aberta com sucesso")

        print("Iniciando recepção de dados")
        rxLen = com1.rx.getBufferLen()
        while rxLen == 0:
            rxLen = com1.rx.getBufferLen()
            time.sleep(1)
        rxBuffer, nRx = com1.getData(rxLen)

        #Conta numero de comandos recebidos
        bytesize = 8
        txBuffer = len(rxBuffer.decode()) / bytesize
        print("Quantidade de Comandos: {}".format(txBuffer))

        #Enviando dados para o client
        print("Iniciando transmissão de dados")
        
        com1.sendData(np.asarray(txBuffer))
            
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
