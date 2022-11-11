from suaBibSignal import *
from scipy.signal import butter,sosfilt
from scipy.io import wavfile
import soundfile as sf
soundfile = 'audio_modulated.wav'
carrier_rate = 14000
sd.default.samplerate = 44100
sd.default.channels = 2

def butter_lowpass_filter(data, cutoff, fs, order):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    sos = butter(order, normal_cutoff, 'lowpass', output='sos')
    filtered = sosfilt(sos, data)
    return filtered

def main():
    signalmeu = signalMeu()
    samplerate, data = wavfile.read(soundfile)
    print("Som modulado")
    signalmeu.plotOriginal(data)
    signalmeu.plotFFT(data, samplerate)
    carrier_tone = []
    for t in range(len(data)):
        carrier_tone.append(np.sin(2 * np.pi * carrier_rate * t / samplerate))
    demodulated_audio = data*carrier_tone
    print("Som demodulado")
    signalmeu.plotOriginal(demodulated_audio)
    signalmeu.plotFFT(demodulated_audio, samplerate)
    filtered = butter_lowpass_filter(demodulated_audio, 2200, samplerate, 2)
    print("Som demodulado e filtrado")
    signalmeu.plotOriginal(filtered)
    signalmeu.plotFFT(filtered, samplerate)
    sd.play(filtered, samplerate)
    sd.wait()
    sf.write('audio_demodulated.wav', filtered, samplerate)

if __name__ == "__main__":
    main()