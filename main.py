from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QFileDialog, QLineEdit, QSizePolicy, QFrame
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QIcon
import os
import pytube
from pytube import Playlist
import requests
import platform
import threading

class MusicDownloader():
    def __init__(self):
        # Create PyQt instance
        self.app = QApplication([])

        # Window creation and configuration
        self.window = QMainWindow()
        self.window.setWindowTitle("YouTube music Downloader")
        self.window.setMinimumSize(800, 450)

        # Layout
        self.central_widget = QWidget()
        self.window.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        # Global style
        self.format_content = """
                        border: 1px solid gray; 
                        border-radius: 4px; 
                        background-color: white;"""
        
        #Header
        self.header_label = QLabel("Youtube Music Downloader")
        self.header_label.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        self.header_label.setStyleSheet("""
                                font-size: 24px; 
                                color: red; 
                                font-weight: bold; 
                                margin-bottom: 25px""")
        self.layout.addWidget(self.header_label)

        # 2nd layout, same row
        self.layout2 = QHBoxLayout()

        # Text input readonly
        self.folder_label = QLineEdit("No Folder Selected")
        self.folder_label.setReadOnly(True)
        self.folder_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.layout2.addWidget(self.folder_label, 7)
        self.folder_label.setStyleSheet(self.format_content)

        # Button select directory
        self.open_button = QPushButton("Seleccionar archivo")
        self.open_button.clicked.connect(self.open_directory_dialog)
        self.open_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.layout2.addWidget(self.open_button, 3)
        self.open_button.setStyleSheet(self.format_content)

        self.frame = QFrame()
        self.frame.setStyleSheet("""
                            border: 1px solid rgba(0, 0, 0, 0.5); 
                            border-radius: 8px;
                            padding: 0 10px;
                            background-color: rgba(255, 0, 0, 0.1)""")
        self.border_layout = QVBoxLayout(self.frame)
        self.border_layout.addLayout(self.layout2)
        self.layout.addWidget(self.frame)

        # 3nd layout, same row
        self.layout3 = QHBoxLayout()

        # Text input readonly
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Enter URL")
        self.url_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.layout3.addWidget(self.url_input, 7)
        self.url_input.setStyleSheet(self.format_content)

        # Button select directory
        self.open_button = QPushButton("Download")
        self.thread = threading.Thread(target=self.download)
        self.open_button.clicked.connect(lambda: self.thread.start())
        self.open_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.layout3.addWidget(self.open_button, 3)
        self.open_button.setStyleSheet(self.format_content)

        self.frame = QFrame()
        self.frame.setStyleSheet("""
                            border: 1px solid rgba(0, 0, 0, 0.5); 
                            border-radius: 8px;
                            padding: 0 10px;
                            background-color: rgba(255, 0, 0, 0.1)""")
        self.border_layout = QVBoxLayout(self.frame)
        self.border_layout.addLayout(self.layout3)
        self.layout.addWidget(self.frame)

        # 4nd layout, same row
        self.layout4 = QHBoxLayout()

        # Img 
        self.thumbnail_label = QLabel()
        self.layout4.addWidget(self.thumbnail_label, 6)
        self.thumbnail_label.setFixedSize(426, 240)
        self.thumbnail_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.thumbnail_label.setStyleSheet(self.format_content)

        # Info label
        self.info_label = QLabel()
        self.info_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.layout4.addWidget(self.info_label, 4)
        self.info_label.setStyleSheet(self.format_content)
        self.info_label.setStyleSheet("color: green")

        self.frame = QFrame()
        self.frame.setStyleSheet("""
                            border: 1px solid rgba(0, 0, 0, 0.5); 
                            border-radius: 8px;
                            padding: 0 10px;
                            background-color: rgba(255, 0, 0, 0.1)""")
        self.border_layout = QVBoxLayout(self.frame)
        self.border_layout.addLayout(self.layout4)
        self.layout.addWidget(self.frame)

        # Alinear De d'alt a baix
        self.layout.addStretch(1)
        self.url_input.textChanged.connect(lambda: self.display_thumbnail(self.url_input.text()))
        # Other
        self.window.show()
        self.app.exec_()
    
    def open_directory_dialog(self):
        self.directory = QFileDialog.getExistingDirectory(
            None,
            "Select Folder",
            "",
            QFileDialog.ShowDirsOnly | QFileDialog.ReadOnly
        )
        if self.directory:
            self.folder_label.setText(self.directory)

    def get_thumbnail(self, url):
        try:
            self.thumbnail_url = pytube.YouTube(url).thumbnail_url
            self.thumbnail_response = requests.get(self.thumbnail_url)
            
            if self.thumbnail_response.status_code == 200:
                # Cargar la imagen en un QPixmap
                self.thumbnail_data = self.thumbnail_response.content
                self.pixmap = QPixmap()
                self.pixmap.loadFromData(self.thumbnail_data)
                self.pixmap = self.pixmap.scaled(426, 240)
                
                # Mostrar la imagen en un QLabel
                self.thumbnail_label.setPixmap(self.pixmap)
            else:
                print("Error getting the photo")
        except Exception as e:
            print(e)

    def display_thumbnail(self, url):
        if self.isPlaylist(url) == False:
            self.get_thumbnail(url)

    def move(self, fileName, path):
        self.operating_system = platform.system()
        if self.operating_system == 'Windows':
            os.system(f'move \"{fileName}\" {path}')
            return True
        elif self.operating_system == 'Linux':
            os.system(f'mv \"{fileName}\" {path}')
            return True
        else:
            self.info_label.setText(f"Operating System not compatible: {self.operating_system}")
            self.info_label.setStyleSheet("color: orange")
            return False

    def download(self):
        self.url = self.url_input.text()
        self.info_label.setText("Downloading...")
        self.info_label.setStyleSheet("color: blue")
        if self.isPlaylist(self.url):
            self.downloadPlaylist(self.url)
        else:
            self.download_audio()
    
    def download_audio(self):
        self.url = self.url_input.text()
        self.path = self.folder_label.text()
        try:
            self.video = pytube.YouTube(self.url)
            self.audio_stream = self.video.streams.filter(only_audio=True).first()
            self.fitxers = os.listdir(self.path)
            self.mp3_filename = self.audio_stream.default_filename.replace(".mp4", ".mp3")
            if self.mp3_filename not in self.fitxers:
                if self.audio_stream is not None:
                    self.audio_stream.download(filename=self.mp3_filename)
                    mp3_filepath = os.path.join(self.path, self.mp3_filename)
                    self.a = self.move(self.mp3_filename, self.path)
                    if self.a:
                        self.info_label.setText("Download finished")
                        self.info_label.setStyleSheet("color: green")
                else:
                    self.info_label.setText("Error")
                    self.info_label.setStyleSheet("color: red")
            else:
                self.info_label.setText("Is alredy downloaded")
                self.info_label.setStyleSheet("color: orange")
        except Exception as e:
            print(e)

    def downloadPlaylist(self, url):
        self.playlist = Playlist(url)
        self.path = self.folder_label.text()
        self.info_label.setText("Downloading...")
        self.info_label.setStyleSheet("color: blue")
        for video_url in self.playlist.video_urls:
            self.get_thumbnail(video_url)
            if self.download_audio_(video_url, self.path) == False:
                self.info_label.setText("Error downloading playlist")
                self.info_label.setStyleSheet("color: red")
        self.info_label.setText("Downloaded correctly")
        self.info_label.setStyleSheet("color: green")

    def download_audio_(self, video_url, path):
        try:
            self.video = pytube.YouTube(video_url)
            self.audio_stream = self.video.streams.filter(only_audio=True).first()
            self.fitxers = os.listdir(path)
            self.mp3_filename = self.audio_stream.default_filename.replace(".mp4", ".mp3")
            if self.mp3_filename not in self.fitxers:
                if self.audio_stream is not None:
                    self.audio_stream.download(filename=self.mp3_filename)
                    mp3_filepath = os.path.join(path, self.mp3_filename)
                    self.a = self.move(self.mp3_filename, path)
                    if self.a:
                        return True
                else:
                    return False
            else:
                return False
        except Exception as e:
            print(e)

    def isPlaylist(self, url):
        if "playlist" in url:
            return True
        return False


if __name__ == '__main__':
    MusicDownloader()