# VibriCue
This is a simple Python script to convert a group of audio files into a single CD quality WAV file along with a cue file, in order to model a proper Red Book CD in video game emulators for games such as Vib-Ribbon. It will also normalise all of the tracks (in the future I will aim to make this an optional and configurable feature) This script exists because Vib-Ribbon assumes two second pregaps in tracks which is annoying for multi-file cue sheets and making a single file cue sheet with properly calculated pregaps was super tedious.
## DISCLAIMERS
At the moment, this project is ONLY designed for my personal use. Its method of use and defaults are heavily tied to me and my own system. I will be designing the early versioning system around this fact and tying it heavily with my roadmap. I do not suggest you use this unless you already have all of the dependencies and are fine with the current process of using it.

This script is currently only designed for use on Linux. It currently uses a mkdir command instead of Python's normal filesystem tools. There is not much else I am concerned with especially when I change that but more stuff could end up popping up in the future. I will try to make it as OS agnostic as possible.

At least a large part of this script was... technically written by AI? Initially, I asked ChatGPT how I would create a .cue file for all of these songs in a single WAV file expecting it to name a piece of software but instead it wrote me a Python script. At the time, I wasn't familiar with Python at all but I had been taught C# and I thought it would be a good idea to learn to automate it myself. Instead of just copy-pasting that code, I went through each line and made sure I knew what they were doing before adding them to my own project, making alterations and developing the WAV generation functions of the script based on what I learnt from that. I feel I'm comfortable enough with Python now so further updates should not contain AI-generated code.
## Dependencies
* Python
* FFmpeg
* [ffmpeg-nomalize](https://github.com/slhck/ffmpeg-normalize)
## Usage guide
1. Create a new directory to hold all of the files for the disc project.
2. Create a directory inside that directory named 'in'. Transfer all of your audio files to that directory.
3. In the main project directory, add the 'vibricue.py' file.
4. Run the 'vibricue.py' script.
5. Bob's your uncle, Jack's your auntie, use the .cue file in an emulator and have fun.
## Specifications
Currently, what this script will do is it will check if the out folder already exists and has .wav files in it. If it doesn't it will check if the in folder exists and has files in it. If it does, it will normalise those files with EBU R 128 normalisation at a loudness target of -18 LUFS and a loudness range of 12, and turn them into CD quality WAV files. It will then use FFmpeg concatenate to turn them into a single WAV file with two second pregaps, in alphabetical filename order. Lastly, it will use the lengths of those converted WAV files to generate a cue file for the final WAV file.
## License
Copyright 2026 BrintonTua

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>.
