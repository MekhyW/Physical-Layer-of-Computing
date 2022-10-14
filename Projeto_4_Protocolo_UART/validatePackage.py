from neoDatagram import Datagram
from logger import *

def validatePackage(package : Datagram, restartPackage, lastValidatedPackage):
    print("Validando pacote recebido...")
    print("Pacote recebido: " + package.fullPackage)
    if package.head.h3 == "00" or package.head.h6 == "00":
        print("Erro: Pacote inválido - faltando dados cruciais")	
        return False
    elif int(package.head.h6) != restartPackage:
        print(package.head.h6, type(package.head.h6))
        print("Erro: Pacote inválido - valor de recomeço inválido")
        return False
    elif int(package.head.h7) != lastValidatedPackage:
        print("Erro: Pacote inválido - valor de último pacote válido inválido")
        return False
    else:
        if (len(package.payload) >= int(package.head.h5)):
            if package.head.h0 == "03":
                if package.head.h4 == "00":
                    print("Erro: Pacote inválido")
                    return False
                else:
                    if package.head.h5 != "00":
                        print("Pacote válido")
                        return True
                    else:
                        print("Erro: Pacote inválido - pacote de dados com payload vazio")
                        return False
            elif package.head.h0 == "01":
                if package.head.h2 == "55":
                    print("Pacote válido")
                    return True
                else:
                    print("Erro: Pacote inválido - pacote de handshake com ID do destinatário incorreto")
                    return False
            elif package.head.h0 == "02":
                if package.head.h2 == "CC":
                    print("Pacote válido")
                    return True
                else:
                    print("Erro: Pacote inválido - pacote de handshake com ID do destinatário incorreto")
                    return False
            elif package.head.h0 == "04":
                print("Pacote válido")
                return True
            elif package.head.h0 == "05":
                print("Pacote válido")
                return True
            elif package.head.h0 == "06":
                if restartPackage != 0:
                    print("Pacote válido")
                    return True
                else:
                    print("Erro: Pacote inválido - índice do pacote solicitado para recomeço incorreto")
                    return False
            else:
                print("Erro: Pacote inválido")
                return False
        else:
            print("Erro: Pacote inválido - tamanho do payload incorreto")
            print("Tamanho do payload esperado: {0}".format(len(package.head.h5)))
            print("Tamanho do payload recebido: {0}".format(len(package.payload)))
            print("Mensagem recebida: {0}".format(package.fullPackage))
            return False