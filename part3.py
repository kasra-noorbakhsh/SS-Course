import numpy as np
from scipy.io import wavfile


noteOctave0Freqs = {
    'C': 16.352, 'C#': 17.324, 'D': 18.354, 'D#': 19.445, 'E': 20.602, 
    'F': 21.827, 'F#': 23.125, 'G': 24.500, 'G#': 25.957, 'A': 27.500, 
    'A#': 29.135, 'B': 30.868
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


def load_wav(filePath):
    sampleRate, data = wavfile.read(filePath)
    return sampleRate, data

def detect_song_segments(data, sampleRate):
    windowSize = int(0.001 * sampleRate)
    amplitude = np.abs(data)
    smoothedAmplitude = np.convolve(amplitude, np.ones(windowSize) / windowSize, mode = 'same')
    silenceMask = (smoothedAmplitude == 0)

    segments = []
    start = None
    for i, isSilent in enumerate(silenceMask):
        if isSilent and start is not None:
            segments.append((start, i))
            start = None
        elif not isSilent and start is None:
            start = i
    if start is not None:
        segments.append((start, len(silenceMask)))
    return [(start / sampleRate, end / sampleRate) for start, end in segments], segments

def extract_notes(segments, data, sampleRate):
    notesFrequencies = []
    for seg in segments:
        dataSegment = data[seg[0]:seg[1]]
        n = len(dataSegment)
        fftResult = np.fft.fft(dataSegment)
        freqs = np.fft.fftfreq(n, d = 1 / sampleRate)
        magnitude = np.abs(fftResult)
        notesFrequencies.append(np.abs(freqs[np.argmax(magnitude)]))
    return notesFrequencies

def find_note_freq(noteFrequencies, notesFreq):
    notes = []
    for freq in noteFrequencies:
        minDiff = float('inf')
        closestNote = None
        for note, baseFreq in notesFreq.items():
            for octave in range(0, 9):
                noteFreq = baseFreq * (2 ** octave)
                diff = abs(noteFreq - freq)
                if diff < minDiff:
                    minDiff = diff
                    closestNote = f'{note} {octave}'
        notes.append(closestNote)
    return notes


sampleRate, data = load_wav("noteHarryShutter.wav")
songSegments, segments = detect_song_segments(data, sampleRate)
notesFrequencies = extract_notes(segments, data, sampleRate)
notes = find_note_freq(notesFrequencies, noteOctave0Freqs)
durations = [round(end - start, 1) for start, end in songSegments]

output = [f'{note} {duration}' for note, duration in zip(notes, durations)]
print(output)

if output == noteHarryPotter:
    print("The arrays match exactly!")
else:
    print("The arrays do not match.")
