
from pathlib import Path
import subprocess


def convert_folder(input_folder: str, output_folder: str):
    input_path = Path(input_folder)
    output_path = Path(output_folder)

    if not input_path.is_dir():
        raise FileNotFoundError(
            f"Input folder does not exist: {input_path}"
        )

    output_path.mkdir(parents=True, exist_ok=True)

    avi_files = sorted(
        file for file in input_path.iterdir()
        if file.is_file() and file.suffix.lower() == ".avi"
    )

    if not avi_files:
        print("No AVI files found.")
        return

    print(f"Found {len(avi_files)} AVI files.")

    for avi_file in avi_files:
        output_file = output_path / f"{avi_file.stem}.mp4"

        if output_file.exists():
            print(f"Skipping existing file: {output_file.name}")
            continue

        command = [
            "ffmpeg",
            "-hide_banner",
            "-nostdin",
            "-n",
            "-i", str(avi_file),
            "-map", "0:v:0",
            "-map", "0:a:0?",
            "-c:v", "libx264",
            "-preset", "medium",
            "-crf", "18",
            "-pix_fmt", "yuv420p",
            "-c:a", "aac",
            "-b:a", "192k",
            str(output_file),
        ]

        print(f"Converting {avi_file.name}...")

        try:
            subprocess.run(command, check=True)
            print(f"Finished: {output_file.name}")
        except subprocess.CalledProcessError:
            print(f"Conversion failed: {avi_file.name}")
            if output_file.exists():
                output_file.unlink()
        except FileNotFoundError:
            raise RuntimeError(
                "FFmpeg was not found. Check your PATH."
            )
