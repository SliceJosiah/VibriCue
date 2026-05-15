# VibriCue
# Copyright 2026 BrintonTua

# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

# You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>.

import subprocess
from pathlib import Path

outFolder = Path("out")
inFolder = Path("in")

if not outFolder.exists():
    if inFolder.exists():
        if any(inFolder.iterdir()):
            print("\nMaking out folder...\n\n")
            subprocess.run([
                "mkdir",
                "out"
                ])
        else:
            raise Exception("\nNo out folder, and in folder is empty.\n")
    else:
        raise Exception("\nNo in or out folder.\n")
else:
    print("\nOut folder exists.", end=" ")

if not any(outFolder.glob("*.wav")):
    if not any(inFolder.iterdir()):
        raise Exception("\nBoth the out and in folders are empty.\n")
    print("Out folder has no contents. Normalising the contents of the in folder.")
    inTracks = [str(p) for p in Path("in").glob("*")]
    subprocess.run([
        "ffmpeg-normalize",
        *inTracks,
        "-t", "-18",
        "-lrt", "12",
        "-tp", "-1",
        "--keep-lra-above-loudness-range-target",
        "--auto-lower-loudness-target",
        "-ext", "wav",
        "-ar", "44100",
    "-c:a", "pcm_s16le",
    "-vn",
    "-pr",
    "-of", "out"
    ], check=True)

tracks = sorted(Path("out").glob("*.wav"))

def getDuration(fileName):
    result = subprocess.run(
            [
                "ffprobe",
                "-v", "error",
                "-show_entries", "format=duration",
                "-of", "default=noprint_wrappers=1:nokey=1",
                fileName
                ],
            capture_output=True,
            text=True,
        )
    return float(result.stdout.strip())

def secToCueTime(seconds):
    totalFrames = int(round(seconds * 75))
    mm = totalFrames // (75 * 60)
    ss = (totalFrames // 75) % 60
    ff = totalFrames % 75
    return f"{mm:02}:{ss:02}:{ff:02}"

with open("concat.txt", "w") as concat:
    for i, track in enumerate(tracks):
        if i == len(tracks) - 1:
            concat.write(f"file '{track}'")
        else:
            concat.write(f"file '{track}'\nfile 'silence_2s.wav'\n")

subprocess.run([
    "ffmpeg",
    "-f", "concat",
    "-safe", "0",
    "-i", "concat.txt",
    "-c", "copy",
    "compmix.wav"
    ], check=True)

currentTime = 0

with open("mix.cue", "w") as cue:
    cue.write(f'TITLE "PlaceHolderName"\n')
    cue.write(f'FILE "compmix.wav" WAVE\n')

    for i, track in enumerate(tracks, start=1):
        cue.write(f"    TRACK {i:02} AUDIO\n")
        if i != 1:
            cue.write(f"        INDEX 00 {secToCueTime(currentTime)}\n")
            currentTime += 2
            cue.write(f"        INDEX 01 {secToCueTime(currentTime)}\n")
        else:
            cue.write(f"        INDEX 01 00:00:00\n")
        duration = getDuration(track)
        currentTime += duration
