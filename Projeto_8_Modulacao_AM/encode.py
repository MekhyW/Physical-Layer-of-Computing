from suaBibSignal import *
from scipy.signal import butter,sosfilt
from scipy.io import wavfile
import sounddevice as sd
import soundfile as sf
soundfile = 'audio.wav'
carrier_rate = 14000

def butter_lowpass_filter(data, cutoff, fs, order):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    sos = butter(order, normal_cutoff, 'lowpass', output='sos')
    filtered = sosfilt(sos, data)
    normalized = filtered / np.max(np.abs(filtered))
    return normalized

def main():
    signalmeu = signalMeu()
    samplerate, data = wavfile.read(soundfile)
    print("Tocando som original")
    sd.play(data, samplerate)
    sd.wait()
    data = data.sum(axis=1) / 2
    signalmeu.plotOriginal(data)
    signalmeu.plotFFT(data, samplerate)
    ########################################################################
    filtered = butter_lowpass_filter(data, 2200, samplerate, 2)
    print("Com filtro passa baixa")
    sd.play(filtered, samplerate)
    sd.wait()
    signalmeu.plotOriginal(filtered)
    signalmeu.plotFFT(filtered, samplerate)
    ########################################################################
    carrier_tone = []
    for t in range(len(filtered)):
        carrier_tone.append(np.sin(2 * np.pi * carrier_rate * t / samplerate))
    modulated = []
    for t in range(len(filtered)):
        modulated.append(filtered[t] * carrier_tone[t])
    modulated = np.array(modulated)
    maxamp = np.max(np.abs(modulated))
    modulated = modulated / maxamp
    print("Modulado")
    sd.play(modulated, samplerate)
    sd.wait()
    sf.write('audio_modulated.wav', modulated, samplerate)
    signalmeu.plotOriginal(modulated)
    signalmeu.plotFFT(modulated, samplerate)

if __name__ == "__main__":
    main()
