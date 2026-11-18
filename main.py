from short_generator.audio_analysis import analyze_audio

bpm, beat_times, duration = analyze_audio("assets/song.wav")

print(bpm)
print(beat_times[:20])
print(duration)