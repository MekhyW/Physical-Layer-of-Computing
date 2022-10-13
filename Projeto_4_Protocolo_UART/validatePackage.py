from neoDatagram import Datagram

def printAndLog(log, string):
    print(string)
    log.write(string + "\n")

def validatePackage(log, package : Datagram, restartPackage = 1, lastValidatedPackage = 0):
    printAndLog(log, "Validando pacote...")
    print("Pacote recebido: " + package.fullPackage)
    if package.head.h3 == "00" or package.head.h6 == "00":
        printAndLog(log, "Erro: Pacote inválido - faltando dados cruciais")	
        return False
    elif int(package.head.h6) != restartPackage:
        print(package.head.h6, type(package.head.h6))
        printAndLog(log, "Erro: Pacote inválido - valor de recomeço inválido")
        return False
    elif int(package.head.h7) != lastValidatedPackage:
        printAndLog(log, "Erro: Pacote inválido - valor de último pacote válido inválido")
        return False
    else:
        if (len(package.payload) >= int(package.head.h5)):
            if package.head.h0 == "03":
                if package.head.h4 == "00":
                    printAndLog(log, "Erro: Pacote inválido")
                    return False
                else:
                    if package.head.h5 != "00":
                        printAndLog(log, "Pacote válido")
                        return True
                    else:
                        printAndLog(log, "Erro: Pacote inválido - pacote de dados com payload vazio")
                        return False
            elif package.head.h0 == "01":
                if package.head.h2 == "55":
                    printAndLog(log, "Pacote válido")
                    return True
                else:
                    printAndLog(log, "Erro: Pacote inválido - pacote de handshake com ID do destinatário incorreto")
                    return False
            elif package.head.h0 == "02":
                if package.head.h2 == "CC":
                    printAndLog(log, "Pacote válido")
                    return True
                else:
                    printAndLog(log, "Erro: Pacote inválido - pacote de handshake com ID do destinatário incorreto")
                    return False
            elif package.head.h0 == "04":
                printAndLog(log, "Pacote válido")
                return True
            elif package.head.h0 == "05":
                printAndLog(log, "Pacote válido")
                return True
            elif package.head.h0 == "06":
                if restartPackage != 0:
                    printAndLog(log, "Pacote válido")
                    return True
                else:
                    printAndLog(log, "Erro: Pacote inválido - índice do pacote solicitado para recomeço incorreto")
                    return False
            else:
                printAndLog(log, "Erro: Pacote inválido")
                return False
        else:
            printAndLog(log, "Erro: Pacote inválido - tamanho do payload incorreto")
            print("Tamanho do payload esperado: {0}".format(len(package.head.h5)))
            print("Tamanho do payload recebido: {0}".format(len(package.payload)))
            print("Mensagem recebida: {0}".format(package.fullPackage))
            return False