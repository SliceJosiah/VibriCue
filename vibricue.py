# VibriCue
# Copyright 2026 BrintonTua

# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

# You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>.

import subprocess
from pathlib import Path

# Define the out and in folders.
outFolder = Path("out")
inFolder = Path("in")

# Check the status of the out folder and in folder.
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

# If there's nothing in the out folder but there are files in the in folder, normalise the files in the in folder, convert them to CD quality WAV, and put them in the out folder.
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

# Put the tracks in an alphabetical list.
tracks = sorted(Path("out").glob("*.wav"))

# This function retrieves the duration of the track.
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

# This function converts a duration to mm:ss:ff as required by a cue sheet.
def secToCueTime(seconds):
    totalFrames = int(round(seconds * 75))
    mm = totalFrames // (75 * 60)
    ss = (totalFrames // 75) % 60
    ff = totalFrames % 75
    return f"{mm:02}:{ss:02}:{ff:02}"

# Generate the two second silence.
subprocess.run([
    "ffmpeg",
    "-f", "lavfi",
    "-i", "anullsrc=r=44100:cl=stereo",
    "-t", "2",
    "-c:a", "pcm_s16le",
    "silence_2s.wav"
    ], check=True)

# Generate a concat.txt file containing the paths of the audio files, with two second pregaps.
with open("concat.txt", "w") as concat:
    for i, track in enumerate(tracks):
        # If this is the last track, only write the track. Otherwise, write the track along with two seconds of silence.
        if i == len(tracks) - 1:
            concat.write(f"file '{track}'")
        else:
            concat.write(f"file '{track}'\nfile 'silence_2s.wav'\n")

# Run FFmpeg concat with the concat.txt file and create a new file called compmix.wav.
subprocess.run([
    "ffmpeg",
    "-f", "concat",
    "-safe", "0",
    "-i", "concat.txt",
    "-c", "copy",
    "compmix.wav"
    ], check=True)

# This variable is a time counter for the number of seconds which have passed in the WAV file, for the cue sheet index.
currentTime = 0

# Generate the cue sheet.
with open("mix.cue", "w") as cue:
    # Specify a placeholder title and the location of the WAV file.
    cue.write(f'TITLE "PlaceHolderName"\n')
    cue.write(f'FILE "compmix.wav" WAVE\n')
    
    # For each track, starting from 1.
    for i, track in enumerate(tracks, start=1):
        # Specify the track with the track number.
        cue.write(f"    TRACK {i:02} AUDIO\n")
        # If we are not on the first track, print the 00 and 01 indexes with a two second pregap. Otherwise, just print the 01 index as 00:00:00.
        if i != 1:
            cue.write(f"        INDEX 00 {secToCueTime(currentTime)}\n")
            currentTime += 2
            cue.write(f"        INDEX 01 {secToCueTime(currentTime)}\n")
        else:
            cue.write(f"        INDEX 01 00:00:00\n")
        duration = getDuration(track)   # Retrieve the duration of the current track.
        currentTime += duration         # Add it to the current time so we can get the start time of the next track.
