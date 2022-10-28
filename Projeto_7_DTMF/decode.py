from suaBibSignal import *
import peakutils
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
import time
sd.default.samplerate = 44100 
sd.default.channels = 2

def todB(s):
    sdB = 10*np.log10(s)
    return(sdB)

def associate_key(A, B):
    keys = ['1','2','3','A','4','5','6','B','7','8','9','C','*','0','#','D']
    column = [1209, 1336, 1477, 1633]
    row = [697, 770, 852, 941]
    differenceA = lambda row : abs(row - A)
    differenceB = lambda first_freq : abs(first_freq - B)
    resA = min(row, key=differenceA)
    resB = min(column, key=differenceB)
    return keys[row.index(resA)*4 + column.index(resB)]

def main():
    signalmeu = signalMeu() 
    duration =  3
    numAmostras = sd.default.samplerate * duration
    freqDeAmostragem = sd.default.samplerate
    print("A captura começará em 3 segundos")
    time.sleep(3)
    print("A gravação foi inicializada")
    audio = sd.rec(int(numAmostras), freqDeAmostragem, channels=1)
    sd.wait()
    print("...     FIM")
    try:
        dados = audio[:,0]
    except:
        dados = audio
    tempo = np.linspace(0, duration, numAmostras)
    plt.plot(tempo, dados)
    plt.show()
    xf, yf = signalmeu.plotFFT(dados, sd.default.samplerate)
    index = peakutils.indexes(yf, thres=0.1, min_dist=50)
    index = [freq for freq in index if freq >= 1800 and freq <= 5100]
    index = [index[0]/3, index[1]/3]
    print("Picos detectados: {} Hz".format(index))
    print("Tecla pressionada: {}".format(associate_key(index[0], index[1])))

if __name__ == "__main__":
    main()
