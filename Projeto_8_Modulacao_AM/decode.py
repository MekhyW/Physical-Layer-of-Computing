from suaBibSignal import *
from scipy.io import wavfile
soundfile = 'audio_modulated.wav'
carrier_rate = 14000
sd.default.samplerate = 44100
sd.default.channels = 2

def main():
    signalmeu = signalMeu()
    samplerate, data = wavfile.read(soundfile)
    signalmeu.plotOriginal(data)
    signalmeu.plotFFT(data, samplerate)

if __name__ == "__main__":
    main()