from pytube import YouTube
import requests
from PyQt5.QtGui import QPixmap
import os
import platform
import pytube

def get_thumbnail(url):
    try:
        thumbnail_url = YouTube(url).thumbnail_url
        if thumbnail_url:
            thumbnail_response = requests.get(thumbnail_url)
            
            if thumbnail_response.status_code == 200:
                # Put the image in QPixmap
                thumbnail_data = thumbnail_response.content
                pixmap = QPixmap()
                pixmap.loadFromData(thumbnail_data)
                pixmap = pixmap.scaled(426, 240)
                
                return pixmap
            else:
                print(f"Error: "+thumbnail_response.status_code)
                return None
        else:
            print("Error, try it again")
    except Exception as e:
        print(e)
        return None
    
def move(fileName, path):
    operating_system = platform.system()
    if operating_system == 'Windows':
        os.system(f'move \"{fileName}\" {path}')
        return (True, None)
    elif operating_system == 'Linux':
        os.system(f'mv \"{fileName}\" {path}')
        return (True, None)
    else:
        
        return (False, (f"Operating System not compatible: {operating_system}", "orange"))
    
def isPlaylist(url):
    if "playlist" in url:
        return True
    return False

def download_audio(url, path):
    try:
        video = pytube.YouTube(url)
        audio_stream = video.streams.filter(only_audio=True).first()
        fitxers = os.listdir(path)
        mp3_filename = audio_stream.default_filename.replace(".mp4", ".mp3")
        if mp3_filename not in fitxers:
            if audio_stream is not None:
                audio_stream.download(filename=mp3_filename)
                moved, error = move(mp3_filename, path)
                if moved:
                    return (True, None)
                else:
                    print("Error moving the file")
                    return (False, error)
            else:
                print("Error: audio_stream is None")
                return (False, ("Internal Error", "red"))
        else:
            return (False, ("Alredy downloaded", "orange"))
    except Exception as e:
        print(e)
        return (False, ("Internal Error", "red"))

def download_audio_(url, path):
    try:
        video = pytube.YouTube(url)
        audio_stream = video.streams.filter(only_audio=True).first()
        fitxers = os.listdir(path)
        mp3_filename = audio_stream.default_filename.replace(".mp4", ".mp3")
        if mp3_filename not in fitxers:
            if audio_stream is not None:
                audio_stream.download(filename=mp3_filename)
                moved, error = move(mp3_filename, path)
                if moved:
                    return (True, None)
                else:
                    print("Error moving the file")
                    return (False, error)
            else:
                print("Error: audio_stream is None")
                return (False, ("Internal Error", "red"))
        else:
            return (False, ("Alredy downloaded", "orange"))
    except Exception as e:
        print(e)
        return (False, ("Internal Error", "red"))
    
