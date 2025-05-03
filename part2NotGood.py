import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.fft import fft
import pandas as pd
import os

num_harmonics = 6
notes_folder = './notes'
output_excel = 'harmonic_coefficients.xlsx'
output_wav = 'noteOptimized.wav'

# Analyze a single note and return harmonic frequencies, coefficients, and full spectrum
def analyze_note(filepath):
    # Read .wav file
    sample_rate, data = wavfile.read(filepath)
    if len(data.shape) > 1:
        data = data[:, 0]  # Convert to mono if stereo

    data = data / np.max(np.abs(data))  # Normalize the input signal
    n = len(data)

    # Perform Fourier Transform 
    fft_result = fft(data)
    freqs = np.fft.fftfreq(n, 1/sample_rate)

    # Get magnitude spectrum
    magnitude = np.abs(fft_result[:n//2])  # Use half spectrum
    freqs = freqs[:n//2]

    # Threshold to find significant harmonics
    threshold = 0.05 * np.max(magnitude)
    peak_indices = np.where(magnitude > threshold)[0][:num_harmonics]

    # Handle cases where fewer than num_harmonics are found
    if len(peak_indices) < num_harmonics:
        peak_indices = np.pad(peak_indices, (0, num_harmonics - len(peak_indices)), 'constant')

    harmonic_coeffs = magnitude[peak_indices]
    harmonic_freqs = freqs[peak_indices]

    # Sort by frequency
    sorted_indices = np.argsort(harmonic_freqs)
    harmonic_coeffs = harmonic_coeffs[sorted_indices]
    harmonic_freqs = harmonic_freqs[sorted_indices]

    return harmonic_freqs, harmonic_coeffs, freqs, magnitude

# Process all notes
sample_rate = 44100
harmonic_data = {}
plots = 3
plt.figure(figsize=(12, 10))

for i, filename in enumerate(sorted(os.listdir(notes_folder))):
    if filename.endswith('.wav'):
        filepath = os.path.join(notes_folder, filename)
        freqs, coeffs, full_freqs, full_mag = analyze_note(filepath)  
        
        # Store only the harmonic coefficients (flatten to ensure 1D array)
        harmonic_data[filename] = coeffs.flatten()
        
        # Plot first 3 notes in detail
        if i < plots:
            plt.subplot(3, 1, i + 1)
            plt.plot(full_freqs, full_mag)
            plt.title(f'Fourier Transform of {filename}')
            plt.xlabel('Frequency (Hz)')
            plt.ylabel('Magnitude')

plt.tight_layout()
plt.show()

# Save harmonic coefficients to Excel
df = pd.DataFrame.from_dict(harmonic_data, orient='index', columns=[f'Harmonic {i+1}' for i in range(num_harmonics)])
df.to_excel(output_excel)

# Generate optimized sound sample_rate = 44100
duration = 2.0  # seconds
t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)

optimized_signal = np.zeros_like(t)
for i, (filename, coeffs) in enumerate(harmonic_data.items()):
    fundamental_freq = analyze_note(os.path.join(notes_folder, filename))[0][0]  # Use the first harmonic as base
    
    # Generate the sound by summing harmonics
    for j, coeff in enumerate(coeffs):
        optimized_signal += coeff * np.sin(2 * np.pi * (fundamental_freq * (j + 1)) * t)

# Normalize and save to .wav
optimized_signal *= np.exp(-t)
optimized_signal = np.int16(optimized_signal / np.max(np.abs(optimized_signal)) * 32767)
wavfile.write(output_wav, sample_rate, optimized_signal)
