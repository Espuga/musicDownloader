# YouTube Music Downloader

This is a Python program that allows you to download music from YouTube. The application uses the PyQt5 library to create a graphical user interface (GUI) to facilitate music downloads from YouTube URLs.
You can pass, a YouTube video URL or a YouTube Playlist URL

## Requirements

Before using this application, make sure you have the following requirements installed:

- Python 3.x
- PyQt5
- pytube
- requests

You can install the Python dependencies using pip:

```bash
pip install PyQt5 pytube requests
```
## Usage

1. Run the Python script music_downloader.py from the command line or a Python IDE.

2. A window of the application will open with the following features:

    - You can select the destination folder where downloaded songs will be saved by clicking on "Select folder"
    - Enter the YouTube URL of the song or playlist you want to download in the "Enter URL" field.
    - Click "Download" to initiate the download.
    - The application will display a preview of the song's thumbnail (if available) and show status messages.
3. The song will be downloaded in MP3 format to the selected folder.

## Additional Features
- The application can download individual songs or entire playlists from YouTube.
- It displays a preview of the song's thumbnail (if available).
- It provides status messages to indicate whether the download completed successfully or if any errors occurred.

## Notes
- Ensure that YouTube URLs are valid and that you have permission to download the content before using this application.


Enjoy your downloaded music!

Made by Espuga