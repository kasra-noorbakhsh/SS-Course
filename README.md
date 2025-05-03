# 🎵 Signals and Systems – Final Project

This project is developed for the **Signals and Systems** course and implements a full pipeline of musical signal processing using Python. It involves **synthesizing a melody from notes**, **smoothing and enhancing it using harmonics**, and finally **reconstructing notes and durations from the generated signal**.

---

## 📌 Project Overview

The goal is to simulate how a piano generates sounds using **sinusoidal signals**, perform **harmonic analysis and reconstruction**, and finally apply **signal processing techniques** to decode a musical sequence from a waveform.

---

## 🎼 Part 1: Synthesizing the Song

Generate a `.wav` song by combining individual note files (`notes/*.wav`) based on a predefined sequence.

### Key Tasks:
- Use the notes to synthesize `noteHarryPoter.wav`.
- Add **25ms of silence** between notes.
- Use `fs = 44100Hz` sampling rate.
- Time array for each note:
  ```python
  t = np.arange(0, α, 1/fs)
  ```
- Must match the reference audio in tone and timing.

---

## 🎹 Part 2: Smoothing & Enhancing Using Harmonics

Simulate a realistic piano-like sound by analyzing and combining harmonic components:

### Steps:
1. Record or analyze each note from **C5 to B5** (12 notes).
2. Compute the **FFT** of each note to extract frequency content.
3. Retain only the **top 6 harmonics** for each note.
4. Reconstruct each note using:
   ```
   Σ A_i * e^(-αt) * sin(2πf_i * t)
   ```
   - `A_i`: amplitude from FFT
   - `α`: damping factor
   - `f_i`: frequency of the i-th harmonic

5. Save the new smoothed song as `noteOptimized.wav`.

---

## 🧠 Part 3: Reconstructing Notes from the Song

From the audio file (`noteHarryPoter.wav` or `noteOptimized.wav`), reconstruct the **original note sequence and durations**.

---

## 🛠️ Tools Used

- [Python 3](https://www.python.org/)
- `numpy`, `scipy`, `matplotlib`, `wave`, and `soundfile` for processing
- `Audacity` or any tool to verify audio files

---

## 🚀 How to Run

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/kasra-noorbakhsh/SS-Course.git
   cd SS-Course
   ```

2. **Run Part 1 – Create the Initial Song**:
   ```bash
   python part1.py
   ```

3. **Run Part 2 – Smooth the Song with Harmonics**:
   ```bash
   python part2.py
   ```

4. **Run Part 3 – Extract Notes and Durations**:
   ```bash
   python part3.py
   ```

> Ensure that the `notes/` directory is present and contains all the octave 5 `.wav` note files.

---

## 🎤 Sample Output Files

- ✅ `noteHarryPoter.wav`: Synthesized basic version  
- 🎧 `noteOptimized.wav`: Smoother, realistic piano version

---

## 📬 Contact

Made by **Kasra Noorbakhsh**  
📧 Feel free to connect or provide feedback!
