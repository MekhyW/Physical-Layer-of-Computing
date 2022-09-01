from enlace import *
import time
import numpy as np
import manageCommands

serialName = "COM11"
com1 = enlace(serialName)

def main():
    try:
        # Implementar handshake aqui

        print("Iniciando transmissão de mensagem")
        
        # Implementar envio da mensagem fragmentada aqui
       
        print("Aguardando retorno do servidor")
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
            exit()

    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()
        

#so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    com1.enable()
    time.sleep(.2)
    com1.sendData(b'00')
    time.sleep(1)
    print("Bytes de sacrifício enviados")
    main()
