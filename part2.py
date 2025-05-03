import os
import numpy as np
import pandas as pd
from scipy.io import wavfile
import matplotlib.pyplot as plt
from scipy.io.wavfile import write


folderPath = './notes'  
outputFolder = './notesOptimized'

noteHarryPotter = [
    'B 4 0.3', 'E 5 0.6', 'G 5 0.2', 'F# 5 0.3', 'E 5 0.6',
    'B 5 0.4', 'A 5 0.8', 'F# 5 0.8', 'E 5 0.6', 'G 5 0.2',
    'F# 5 0.3', 'D# 5 0.7', 'F 5 0.4', 'B 4 1.6', 'B 4 0.3',
    'E 5 0.6', 'G 5 0.2', 'F# 5 0.3', 'E 5 0.6', 'B 5 0.4',
    'D 6 0.6', 'C# 6 0.3', 'C 6 0.6', 'G# 5 0.3', 'C 5 0.5',
    'B 5 0.2', 'A# 5 0.3', 'A# 4 0.6', 'G 5 0.3', 'E 5 1.6',
    'G 5 0.3', 'B 5 0.6', 'G 5 0.3', 'B 5 0.6', 'G 5 0.3',
    'C 6 0.6', 'B 5 0.3', 'A# 5 0.6', 'F# 5 0.3', 'G 5 0.5',
    'B 5 0.2', 'A# 5 0.3', 'A# 4 0.6', 'B 4 0.4', 'B 5 1.6',
    'G 5 0.3', 'B 5 0.7', 'G 5 0.3', 'B 5 0.7', 'G 5 0.3',
    'D 6 0.7', 'C# 6 0.3', 'C 6 0.8', 'G# 5 0.3', 'C 6 0.6',
    'B 5 0.2', 'A# 5 0.3', 'A# 4 0.6', 'G 5 0.4', 'E 5 1.0', 'E 5 1.6'
]


def load_wav(filePath):
    sampleRate, data = wavfile.read(filePath)
    if len(data.shape) > 1:
        data = data[:, 0] 
    return sampleRate, data

def save_optimized_note_to_wav(noteName, optimizedSignal, sampleRate, outputFolder):
    os.makedirs(outputFolder, exist_ok = True)
    outputFile = os.path.join(outputFolder, f"{noteName}Optimized.wav")
    write(outputFile, sampleRate, optimizedSignal)

def plot_fft(data, sampleRate, noteName):
    N = len(data)
    fftResult = np.fft.fft(data)
    freqs = np.fft.fftfreq(N, d = 1/sampleRate)
    positiveFreqs = freqs[:N//2]
    positiveFft = np.abs(fftResult[:N//2])
    
    plt.figure(figsize=(12, 6))
    plt.plot(positiveFreqs, positiveFft)
    plt.title(f'FFT of {noteName}')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Amplitude')
    plt.xlim(0, 4000)  
    plt.grid(True)
    plt.show()

def get_harmonics(data, sampleRate, numHarmonics = 6):
    N = len(data)
    fftResult = np.fft.fft(data)
    freqs = np.fft.fftfreq(N, d = 1/sampleRate)
    positiveFreqs = freqs[:N//2]
    positiveFft = np.abs(fftResult[:N//2])
    fundamentalFreq = positiveFreqs[np.argmax(positiveFft)]

    harmonics = []
    for i in range(2, numHarmonics + 2):
        harmonicFreq = fundamentalFreq * i
        idx = np.argmin(np.abs(positiveFreqs - harmonicFreq))
        harmonics.append((positiveFreqs[idx], positiveFft[idx]))
    
    return fundamentalFreq, harmonics

def generate_optimized_note(fundamentalFreq, harmonics, sampleRate, duration = 2.0, amplitude = 0.5):
    t = np.linspace(0, duration, int(sampleRate * duration), endpoint = False)
    optimizedSignal = amplitude * np.sin(2 * np.pi * fundamentalFreq * t)
    
    for harmonic in harmonics:
        freq, amp = harmonic 
        harmonicSignal = (amplitude * amp) * np.sin(2 * np.pi * freq * t)   
        optimizedSignal += harmonicSignal
    
    decayEnvelope = np.exp(-2 * t)
    optimizedSignal *= decayEnvelope
    optimizedSignal = np.int16(optimizedSignal / np.max(np.abs(optimizedSignal)) * 32767)
    return optimizedSignal

def create_song(noteSequence, sampleRate, outputFolder):
    song = []
    for note in noteSequence:
        noteName, octave, duration = note.split()
        filePath = os.path.join(outputFolder, f"{noteName}Optimized.wav")
        if os.path.exists(filePath):
            _, noteData = load_wav(filePath)
            noteDuration = float(duration)
            noteLength = int(sampleRate * noteDuration)
            song.extend(noteData[:noteLength])
    return np.array(song, dtype=np.int16)

def process_notes(folderPath, outputFolder, numHarmonics = 6):
    harmonicsData = []
    noteFiles = [f for f in os.listdir(folderPath) if f.endswith('.wav')]
    
    for noteFile in noteFiles:
        noteName = noteFile.split('.')[0]
        filePath = os.path.join(folderPath, noteFile)
        sampleRate, data = load_wav(filePath)
        fundamentalFreq, harmonics = get_harmonics(data, sampleRate, numHarmonics)
        harmonicValues = [harmonic[1] for harmonic in harmonics] 
        harmonicsData.append([noteName, fundamentalFreq] + harmonicValues)
        optimizedSignal = generate_optimized_note(fundamentalFreq, harmonics, sampleRate)
        save_optimized_note_to_wav(noteName, optimizedSignal, sampleRate, outputFolder)

        if noteName in ['A', 'C', 'D']:  
            plot_fft(data, sampleRate, noteName)
    
    df = pd.DataFrame(harmonicsData, columns=['Note', 'Fundamental Frequency'] + [f'Harmonic {i}' for i in range(1, numHarmonics + 1)])
    df.to_excel('harmonicsData.xlsx', index=False)


process_notes(folderPath, outputFolder)
song = create_song(noteHarryPotter, 44100, outputFolder)
write('noteHarryOptimized.wav', 44100, song)
