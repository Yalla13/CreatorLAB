
import random
import secrets


def generate_edit(
    beat_times,
    video_duration: float,
    short_duration: float = 15.0,
    min_clip: float = 0.5,
    max_clip: float = 2.5,
    seed: int | None = None,
):
    if seed is None:
        seed = secrets.randbits(32)

    if video_duration < short_duration:
        raise ValueError(
            "For the first version, footage must be "
            "at least as long as the short."
        )

    if not 0 < min_clip <= max_clip:
        raise ValueError("Invalid clip length limits.")

    rng = random.Random(seed)

    # 1. Decide where to cut on the short timeline.
    cut_points = [0.0]

    for beat in beat_times:
        beat = float(beat)

        if beat <= 0 or beat >= short_duration:
            continue

        gap = beat - cut_points[-1]
        remaining = short_duration - beat

        if gap < min_clip or remaining < min_clip:
            continue

        if gap >= max_clip or rng.random() < 0.35:
            cut_points.append(beat)

    cut_points.append(short_duration)

    # 2. Generate source ranges for every clip.
    clips = []

    for start, end in zip(cut_points, cut_points[1:]):
        clip_duration = end - start

        source_start = rng.uniform(
            0, video_duration - clip_duration
        )

        clips.append({
            "source_start": round(source_start, 3),
            "timeline_start": round(start, 3),
            "duration": round(clip_duration, 3),
        })

    return {
        "seed": seed,
        "duration": short_duration,
        "clips": clips,
    }
