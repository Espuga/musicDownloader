from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QFileDialog, QLineEdit, QSizePolicy, QFrame
from PyQt5.QtCore import Qt
import sys
from pytube import Playlist

from functions import get_thumbnail, isPlaylist
from NewThread import NewThread



class MusicDownloader(QMainWindow):
    def __init__(self):
        super().__init__()

        # Window creation and configuration
        self.setWindowTitle("YouTube music Downloader")
        self.setMinimumSize(800, 450)

        # Layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

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
        self.folder_label.setText("C:/Users/marce/OneDrive/Escriptori")
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

        
        self.open_button.clicked.connect(self.startDownload)

        #self.thread = threading.Thread(target=self.download)
        #self.open_button.clicked.connect(lambda: self.thread.start())
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
        
    def startDownload(self):
        # problema, la classe NewThreads no accedeix a les variables de la classe 
        self.newThread = NewThread(self.url_input.text(), self.folder_label.text(), self)
        self.newThread.start()
    
    def mododify(self, msg, color):
        self.info_label.setText(msg)
        self.info_label.setStyleSheet(f"color: {color}")
    def modifyThumbnail(self, pixmap):
        self.thumbnail_label.setPixmap(pixmap)

    def open_directory_dialog(self):
        self.directory = QFileDialog.getExistingDirectory(
            None,
            "Select Folder",
            "",
            QFileDialog.ShowDirsOnly | QFileDialog.ReadOnly
        )
        if self.directory:
            self.folder_label.setText(self.directory)

    def display_thumbnail(self, url):
        if url:
            if isPlaylist(url) == False:
                pixmap = get_thumbnail(url)
                if pixmap is not None:
                    self.thumbnail_label.setPixmap(pixmap)
            else:
                pixmap = get_thumbnail(Playlist(url).video_urls[0])
                if pixmap is not None:
                    self.thumbnail_label.setPixmap(pixmap)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MusicDownloader()
    window.show()
    sys.exit(app.exec_())