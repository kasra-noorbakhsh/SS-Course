import numpy as np
from scipy.io.wavfile import write


noteOctave4Freqs = {        
    'C': 261.63, 'C#': 277.18, 'D': 293.66, 'D#': 311.13, 'E': 329.63,
    'F': 349.23, 'F#': 369.99, 'G': 392.00, 'G#': 415.30, 'A': 440.00,
    'A#': 466.16, 'B': 493.88
}

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


def get_frequency(note, octave):
    baseFreq = noteOctave4Freqs[note]
    return baseFreq * (2 ** (octave - 4))

def synthesize_note(freq, duration, sampleRate = 44100):
    t = np.linspace(0, duration, int(sampleRate * duration), endpoint = False)
    return 0.5 * np.sin(2 * np.pi * freq * t)

def parse_note(noteStr):
    parts = noteStr.split()
    note = parts[0]
    octave = int(parts[1])
    duration = float(parts[2])
    return note, octave, duration

def generate_signal(noteArray, silenceDuration = 0.025, sampleRate = 44100):
    song = np.array([])
    silence = np.zeros(int(sampleRate * silenceDuration))
    
    for noteStr in noteArray:
        note, octave, duration = parse_note(noteStr)
        freq = get_frequency(note, octave)
        tone = synthesize_note(freq, duration, sampleRate)
        song = np.concatenate((song, tone, silence))
    
    song = np.int16(song / np.max(np.abs(song)) * 32767)
    return song

    
song = generate_signal(noteHarryPotter)
write('noteHarryShutter.wav', 44100, song)
print("The audio file created!")
