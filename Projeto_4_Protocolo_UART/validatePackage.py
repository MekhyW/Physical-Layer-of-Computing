from neoDatagram import Datagram

def printAndLog(log, string):
    print(string)
    log.write(string + "\n")

def validatePackage(log, package : Datagram, restartPackage = 1, lastValidatedPackage = 0):
    printAndLog("Validando pacote...")
    print(package.head.fullHead)
    if package.head.h3 == "00" or package.head.h6 == "00":
        printAndLog("Erro: Pacote inválido - faltando dados cruciais")	
        return False
    elif int(package.head.h6) != restartPackage:
        printAndLog("Erro: Pacote inválido - valor de recomeço inválido")
        return False
    elif int(package.head.h7) != lastValidatedPackage:
        printAndLog("Erro: Pacote inválido - valor de último pacote válido inválido")
        return False
    else:
        if (len(package.payload) == int(package.head.h5)):
            if package.head.h0 == "03":
                if package.head.h4 == "00":
                    printAndLog("Erro: Pacote inválido")
                    return False
                else:
                    if package.head.h5 != "00":
                        printAndLog("Pacote válido")
                        return True
                    else:
                        printAndLog("Erro: Pacote inválido - pacote de dados com payload vazio")
                        return False
            elif package.head.h0 == "01":
                if package.head.h2 == "55":
                    printAndLog("Pacote válido")
                    return True
                else:
                    printAndLog("Erro: Pacote inválido - pacote de handshake com ID do destinatário incorreto")
                    return False
            elif package.head.h0 == "02":
                if package.head.h2 == "CC":
                    printAndLog("Pacote válido")
                    return True
                else:
                    printAndLog("Erro: Pacote inválido - pacote de handshake com ID do destinatário incorreto")
                    return False
            elif package.head.h0 == "04":
                printAndLog("Pacote válido")
                return True
            elif package.head.h0 == "05":
                printAndLog("Pacote válido")
                return True
            elif package.head.h0 == "06":
                if restartPackage != 0:
                    printAndLog("Pacote válido")
                    return True
                else:
                    printAndLog("Erro: Pacote inválido - índice do pacote solicitado para recomeço incorreto")
                    return False
            else:
                printAndLog("Erro: Pacote inválido")
                return False
        else:
            printAndLog("Erro: Pacote inválido - tamanho do payload incorreto")
            return False