
from pathlib import Path
import subprocess


def render_short(
    edit_plan: dict,
    video_path: str,
    audio_path: str,
    output_path: str,
    width: int = 540,
    height: int = 960,
    fps: int = 30,
):
    clips = edit_plan["clips"]
    duration = float(edit_plan["duration"])

    if not clips:
        raise ValueError("Edit plan is empty.")

    if width <= 0 or height <= 0 or fps <= 0:
        raise ValueError("Invalid output dimensions or FPS.")

    if width % 2 or height % 2:
        raise ValueError("Output dimensions must be even.")

    # Verify that clips form one continuous timeline.
    timeline_position = 0.0

    for clip in clips:
        start = float(clip["timeline_start"])
        length = float(clip["duration"])

        if abs(start - timeline_position) > 0.01:
            raise ValueError("Timeline has a gap or overlap.")

        if length <= 0 or float(clip["source_start"]) < 0:
            raise ValueError("Invalid clip range.")

        timeline_position += length

    if abs(timeline_position - duration) > 0.02:
        raise ValueError("Clip durations do not match short duration.")

    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)

    if output.exists():
        raise FileExistsError(f"Output already exists: {output}")

    filters = []
    labels = []

    for index, clip in enumerate(clips):
        source_start = float(clip["source_start"])
        length = float(clip["duration"])

        filters.append(
            f"[0:v:0]"
            f"trim=start={source_start:.6f}:duration={length:.6f},"
            f"setpts=PTS-STARTPTS,"
            f"scale={width}:{height}:"
            f"force_original_aspect_ratio=increase,"
            f"crop={width}:{height},"
            f"setsar=1,"
            f"fps={fps},"
            f"format=yuv420p"
            f"[v{index}]"
        )

        labels.append(f"[v{index}]")

    filters.append(
        f"{''.join(labels)}"
        f"concat=n={len(clips)}:v=1:a=0[video]"
    )

    # Use the beginning of the song for this MVP.
    filters.append(
        f"[1:a:0]"
        f"atrim=start=0:duration={duration:.6f},"
        f"asetpts=PTS-STARTPTS,"
        f"apad=whole_dur={duration:.6f}"
        f"[audio]"
    )

    command = [
        "ffmpeg",
        "-hide_banner",
        "-nostdin",
        "-n",
        "-i", str(video_path),
        "-i", str(audio_path),
        "-filter_complex", ";".join(filters),
        "-map", "[video]",
        "-map", "[audio]",
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-crf", "20",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "192k",
        "-t", str(duration),
        "-movflags", "+faststart",
        str(output),
    ]

    print("Rendering short...")

    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError:
        output.unlink(missing_ok=True)
        raise

    print(f"Saved: {output}")
