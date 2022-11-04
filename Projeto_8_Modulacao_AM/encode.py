from suaBibSignal import *
from scipy.signal import butter,sosfilt
from scipy.io import wavfile
import sounddevice as sd
soundfile = 'audio.wav'
carrier_rate = 14000

def butter_lowpass_filter(data, cutoff, fs, order):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    sos = butter(order, normal_cutoff, 'lowpass', output='sos')
    filtered = sosfilt(sos, data)
    return filtered

def main():
    samplerate, data = wavfile.read(soundfile)
    print("Tocando som original")
    sd.play(data, samplerate)
    sd.wait()
    filtered = butter_lowpass_filter(data, 2200, samplerate, 2)
    print("Com filtro passa baixa")
    sd.play(filtered, samplerate)
    sd.wait()
    carrier_tone = []
    for t in range(len(filtered)):
        carrier_tone.append(np.sin(2 * np.pi * carrier_rate * t/samplerate))
    modulated = []
    for t in range(len(filtered)):
        modulated.append(filtered[t] * carrier_tone[t])
    print("Modulado")
    sd.play(modulated, samplerate)
    sd.wait()

if __name__ == "__main__":
    main()
