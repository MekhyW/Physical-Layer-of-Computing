from suaBibSignal import *
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
sd.default.samplerate = 44100
sd.default.channels = 2

def todB(s):
    sdB = 10*np.log10(s)
    return(sdB)

def main():
    signalmeu = signalMeu()
    duration =  3
    print("Inicializando encoder")
    print("Aguardando usuário")
    keys = ['1','2','3','A','4','5','6','B','7','8','9','C','*','0','#','D']
    first_freq = [1209, 1336, 1477, 1633] * 4
    second_freq = ([697] * 4) + ([770] * 4) + ([852] * 4) + ([941] * 4)
    NUM = input("Digite uma tecla do teclado numérico DTMF: ")
    if NUM not in keys:
        print("Tecla inválida")
        return
    print("Gerando Tons base")
    tone = []
    for t in range(duration * sd.default.samplerate):
        senA = np.sin(2 * np.pi * first_freq[keys.index(NUM)] * t / sd.default.samplerate)
        senB = np.sin(2 * np.pi * second_freq[keys.index(NUM)] * t / sd.default.samplerate)
        tone.append(senA + senB)
    print("Executando as senoides (emitindo o som)")
    print("Gerando Tom referente ao símbolo : {}".format(NUM))
    sd.play(tone, sd.default.samplerate)
    sd.wait()
    signalmeu.plotOriginal(tone)
    signalmeu.plotFFT(tone, sd.default.samplerate)

if __name__ == "__main__":
    main()
