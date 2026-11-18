import librosa
import numpy as np
import matplotlib.pyplot as plt

def analyze_audio(path):

    y, sr = librosa.load(path, sr=None, mono=True)

    tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
    beat_times = librosa.frames_to_time(beat_frames, sr=sr)

    bpm = float(np.asarray(tempo).reshape(-1)[0])
    duration = len(y) / sr

    return bpm, beat_times, duration

def visualize_audio(y, sr, beat_times):

    plt.plot(np.arange(len(y)) / sr, y, linewidth=0.5)

    for t in beat_times:
        plt.axvline(t, color="red", alpha=0.4)

    plt.xlim(0, 30)
    plt.show()

