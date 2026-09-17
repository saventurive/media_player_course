PYTHON DESKTOP MEDIA PLAYER: 6-DAY MASTERCLASS

Welcome to the Python Desktop Media Player course! This hands-on, project-based curriculum takes you step-by-step through building a fully functional, professional-grade desktop media player from scratch using Python and Tkinter.

Whether you want to learn advanced GUI layout design, handle audio/video codecs, or master metadata extraction, this course bridges theory and practical application over six structured modules.

COURSE OVERVIEW & OBJECTIVES

By the end of this masterclass, you will have built a unified desktop application capable of playing both audio files (.mp3, .flac, .wav) with album art and video files (.mp4, .mkv, .avi) with hardware-accelerated playback.

DAILY CURRICULUM BREAKDOWN

Day 1: UI Layout & Architecture
Learn how to structure a multi-pane desktop app using Tkinter frames, geometry managers, and a clean dark-themed UI.

Day 2: Playlist Management & Search Filtering
Implement file dialog selection, dynamic listbox updating, and a real-time search filter to quickly find tracks.

Day 3: Metadata Extraction & Album Art
Use Mutagen to read ID3 and FLAC tags, handle embedded album art vs. folder JPEGs (cover.jpg), and resize images smoothly using Pillow (PIL).

Day 4: Audio Playback, Seeking & Speed Controls
Integrate audio backends, implement jump-forward/backward controls (+/- 5 seconds), and set up playback speed scaling.

Day 5: Progress Sliders, Time Displays & Troubleshooting
Master non-blocking UI polling loops (root.after), build real-time digital time displays (00:00 / 04:50), and troubleshoot common seeking and VBR audio bugs.

Day 6: Advanced Video Playback & VLC Integration
Transition from audio-only mixers to the robust VLC Media Player backend (python-vlc), embedding video streams directly inside your Tkinter application window.

TECH STACK & PREREQUISITES

This project relies on modern Python libraries for multimedia processing and UI rendering.

Python Packages (pip install):
Run the following command to install all required dependencies:
pip install mutagen Pillow pygame python-vlc

tkinter: Python's built-in standard GUI framework.

mutagen: Parses audio metadata, tags, and track durations.

Pillow: Image processing library used for resizing album artwork.

pygame: Lightweight audio engine used in early audio modules.

python-vlc: Python bindings for the libvlc multimedia framework, enabling robust audio and video decoding.

System Prerequisites:

Python 3.8+ installed on your system.

VLC Media Player installed on your operating system (Windows, macOS, or Linux) so that the python-vlc wrapper can access system codecs and shared libraries (libvlc).

QUICK START

Clone or download this repository to your local machine.

Ensure you have installed Python, VLC, and the required Python packages listed above.

Run the final unified media player script:
python media_player.py

Click "Add Media Files" to load your favorite audio and video files into the playlist, and enjoy!
