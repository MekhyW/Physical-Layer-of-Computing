def crc16(head: bytes):
    xor_in = 0x0000
    xor_out = 0x0000
    generator = 0xBABA

    register = xor_in
    for octet in head:
        for value in range(8):
            topBit = register & 0x8000
            if octet & (0x80 >> value):
                topBit ^= 0x8000
            register <<= 1
            if topBit:
                register ^= generator
        register &= 0xFFFF

    print(type(register ^ xor_out))
    return register ^ xor_out