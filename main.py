
import json
from pathlib import Path

from short_generator.audio_analysis import analyze_audio
from short_generator.media import get_video_duration
from short_generator.edit_generator import generate_edit
from short_generator.renderer import render_short


def main():
    audio_path = "assets/songs/CZ_MERC.wav"
    video_path = "assets/videos/DSCF3888.MOV"

    bpm, beat_times, audio_duration = analyze_audio(audio_path)
    video_duration = get_video_duration(video_path)

    short_duration = 15.0

    if audio_duration < short_duration:
        raise ValueError("Audio is shorter than requested short.")

    if video_duration < short_duration:
        raise ValueError("Video is shorter than requested short.")

    edit_plan = generate_edit(
        beat_times=beat_times,
        video_duration=video_duration,
        short_duration=short_duration,
    )

    output_dir = Path("outputs/shorts")
    output_dir.mkdir(parents=True, exist_ok=True)

    seed = edit_plan["seed"]

    json_path = output_dir / f"edit_{seed}.json"
    mp4_path = output_dir / f"short_{seed}.mp4"

    with open(json_path, "w", encoding="utf-8") as file:
        json.dump(edit_plan, file, indent=4)

    print(f"BPM: {bpm:.2f}")
    print(f"Seed: {seed}")
    print(f"Clips: {len(edit_plan['clips'])}")

    render_short(
        edit_plan=edit_plan,
        video_path=video_path,
        audio_path=audio_path,
        output_path=str(mp4_path),
    )


if __name__ == "__main__":
    main()
