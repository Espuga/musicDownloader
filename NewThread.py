from PyQt5.QtCore import QThread
from pytube import Playlist

from functions import get_thumbnail, isPlaylist, download_audio

class NewThread(QThread):
    def __init__(self, url, path, main_window_instance):
        super().__init__()
        self.url = url
        self.path = path
        self.main_window_instance = main_window_instance
    
    def run(self):
        self.main_window_instance.mododify("Downloading...", "blue")
        if isPlaylist(self.url):
            self.downloadPlaylist(self.url, self.path)
        else:
            self.downloaded, self.msg = download_audio(self.url, self.path)
            if self.downloaded:
                self.main_window_instance.mododify("Downloaded correctly", "green")
            else:
                self.main_window_instance.mododify(self.msg[0], self.msg[1])

    def downloadPlaylist(self, url, path):
        self.playlist = Playlist(url)
        self.main_window_instance.mododify("Downloading...", "blue")
        for video_url in self.playlist.video_urls:
            # Get thumbnail
            pixmap = get_thumbnail(video_url)
            if pixmap is not None:
                self.main_window_instance.modifyThumbnail(pixmap)

            self.downloaded, self.msg = download_audio(video_url, path)
            if self.downloaded == False:
                self.main_window_instance.mododify(self.msg[0], self.msg[1])
        self.main_window_instance.mododify("Downloaded correctly", "green")