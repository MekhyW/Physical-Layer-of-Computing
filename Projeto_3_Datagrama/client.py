from enlace import *
import time
import numpy as np
import manageCommands

serialName = "COM7"

def main():
    try:
        com1 = enlace(serialName)
        com1.enable()

        #Byte de sacrifício
        time.sleep(.2)
        com1.sendData(b'00')
        time.sleep(1)

        print("Comunicação aberta com sucesso")

        print("Criando comandos...")
        generator = np.random.default_rng()
        numberOfCommands = generator.integers(10,30)
        txBuffer = manageCommands.generateCommands(numberOfCommands)
        print("Quantidade de Comandos: {}".format(numberOfCommands))

        print("Iniciando transmissão de dados")
        
        com1.sendData(np.asarray(txBuffer))
       
        print("Iniciando retorno do servidor")
        timer=0
        print(timer)

        rxLen = com1.rx.getBufferLen()
        while not rxLen:
            rxLen = com1.rx.getBufferLen()
            time.sleep(1)
            timer += 1
            print(timer)
            if timer >= 5:
                raise Exception("Timeout")
        rxBuffer, nRx = com1.getData(rxLen)

        serverCommands = int.from_bytes(rxBuffer, "little")

        if serverCommands == numberOfCommands:
            print("Comandos enviados (client): {}".format(numberOfCommands))
            print("Comandos enviados (server): {}".format(serverCommands))
            print("Todos comandos foram recebidos!")
        else:
            print("Comandos enviados (client): {}".format(numberOfCommands))
            print("Comandos enviados (server): {}".format(serverCommands))
            print("Erro: Comandos perdidos durante comunicação")

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
