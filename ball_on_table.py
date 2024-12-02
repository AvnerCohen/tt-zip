import sys
import math

import librosa
import numpy as np
import scipy.signal as signal

EXTRA_SECONDS = 1.5


def detect_ball_hits(audio_file):
    y, sr = librosa.load(audio_file)
    nyquist = 0.5 * sr
    low = 1000 / nyquist
    high = 5000 / nyquist
    b, a = signal.butter(4, [low, high], btype='band')
    filtered_y = signal.lfilter(b, a, y)
    energy = librosa.feature.rms(y=filtered_y)[0]
    threshold = np.mean(energy) + 1.7 * np.std(energy)
    ball_hit_times = librosa.frames_to_time(np.where(energy > threshold)[0], sr=sr)
    return ball_hit_times


def merge_overlapping_ranges(ranges):
    if not ranges:
        return []

    ranges.sort()
    merged_ranges = [ranges[0]]
    for current_start, current_end in ranges[1:]:
        last_start, last_end = merged_ranges[-1]
        if current_start <= last_end:
            merged_ranges[-1] = (last_start, max(last_end, current_end))
        else:
            merged_ranges.append((current_start, current_end))
    return merged_ranges


def process_timestamps(timestamps):
    adjusted_timestamps = []
    for t in timestamps:
        if t > EXTRA_SECONDS:
            adjusted_timestamps.append(math.floor(t - EXTRA_SECONDS))
    ranges = [(t, t + (EXTRA_SECONDS * 2)) for t in adjusted_timestamps]
    merged_ranges = merge_overlapping_ranges(ranges)

    return [f"{int(start)}-{int(end)}" for start, end in merged_ranges]


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python your_python_script.py <filename.mp4>")
        sys.exit(1)
    video_file = sys.argv[1]
    ball_hit_times = detect_ball_hits(f"{video_file}.wav")
    for time_range in process_timestamps(ball_hit_times):
        print(time_range)
