
import json
import subprocess


def get_video_duration(path: str) -> float:
    command = [
        "ffprobe",
        "-v", "error",
        "-show_entries", "format=duration",
        "-of", "json",
        str(path),
    ]

    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
        check=True
    )

    data = json.loads(result.stdout)

    return float(data["format"]["duration"])
