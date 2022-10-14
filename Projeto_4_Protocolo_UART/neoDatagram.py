class Head:
    h0: str = '00'    # Tipo de mensagem : '01' - handhake client, '02' - handshake server, '03' - data, '04' - verification, '05' - timeout, '06' - error
    h1: str = '00'    # Livre, será tilizado como Id do remetente: 'CC' - client, '55' - server
    h2: str = '00'    # Livre, será tilizado como Id do destinatário: 'CC' - client, '55' - server
    h3: str = '00'    # Número total de pacotes do arquivo
    h4: str = '01'    # Número do pacote sendo enviado - começa em 01
    h5: str = '00'    # Se h0 == '01' : Id do arquivo; se h0 == '03' : Tamanho do payload
    h6: str = '01'    # Pacote solicitado para recomeço - começa em 01
    h7: str = '00'    # Último pacote recebido e verificado com sucesso - começa em 00
    h8: str = '00'    # Em branco, será parte do Projeto 5 (CRC)
    h9: str = '00'    # Em branco, será parte do Projeto 5 (CRC)
    fullHead: str

    def __init__(self, messageType, senderId, receiverId, totalPackages, currentPackageIndex, payloadSizeOrFileId, restartPackage, lastVerifiedPackage):
        self.h0 = messageType
        self.h1 = senderId
        self.h2 = receiverId
        self.h3 = totalPackages
        self.h4 = currentPackageIndex
        self.h5 = payloadSizeOrFileId
        self.h6 = restartPackage
        self.h7 = lastVerifiedPackage
        
        self.fullHead = self.h0 + self.h1 + self.h2 + self.h3 + self.h4 + self.h5 + self.h6 + self.h7 + self.h8 + self.h9

class Datagram:
    head: Head
    payload: str = ''
    endOfPackage: str = 'AABBCCDD'
    fullPackage = str

    def __init__(self, head, payload):
        self.head = head
        self.payload = payload
        self.fullPackage = self.head.fullHead + self.payload + self.endOfPackage