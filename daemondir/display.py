import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QFrame
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QTimer, QSize  # Remove the import for QSizePolicy


class FileViewer(QMainWindow):
    def __init__(self, directory_path):
        super().__init__()
        self.directory_path = directory_path
        self.initUI()

    def initUI(self):
        self.setWindowTitle('File Viewer')
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.scroll_area = QFrame()  # Use QFrame for the black background
        self.scroll_area.setStyleSheet("background-color: black;")
        self.scroll_area.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)
        self.scroll_area.setLineWidth(1)

        self.scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout()
        self.scroll_widget.setLayout(self.scroll_layout)
        self.scroll_area.setLayout(self.scroll_layout)
        self.layout.addWidget(self.scroll_area)
        self.central_widget.setLayout(self.layout)

        self.timer_load = QTimer(self)
        self.timer_load.timeout.connect(self.load_files)
        self.timer_load.start(1000)  # Initial load every second

        self.timer_update = QTimer(self)
        self.timer_update.timeout.connect(self.update_files)
        self.timer_update.start(1000)  # Update every second

    def load_files(self):
        self.files = []
        print("Checking for files in directory:", self.directory_path)
        for filename in os.listdir(self.directory_path):
            if filename.endswith(('.png', '.jpg', '.jpeg')):
                self.files.append(filename)

        print("Found files:", self.files)

        # Clear existing widgets
        for i in reversed(range(self.scroll_layout.count())):
            widget = self.scroll_layout.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)

        # Define the desired size for each image
        image_width = 300
        image_height = 200

        for filename in self.files:
            label = QLabel()
            pixmap = QPixmap(os.path.join(self.directory_path, filename))
            pixmap = pixmap.scaled(image_width, image_height, Qt.KeepAspectRatio)
            
            label.setPixmap(pixmap)
            label.setAlignment(Qt.AlignCenter)
            
            # Add a thin orange border around the image
            label.setStyleSheet("border: 1px solid orange; padding: 4px;")

            self.scroll_layout.addWidget(label)

    def update_files(self):
        current_files = set(self.files)
        new_files = set()

        for filename in os.listdir(self.directory_path):
            if filename.endswith(('.png', '.jpg', '.jpeg')):
                new_files.add(filename)

        added_files = new_files - current_files
        removed_files = current_files - new_files

        if added_files:
            print("New files found:", added_files)
            for filename in added_files:
                label = QLabel()
                pixmap = QPixmap(os.path.join(self.directory_path, filename))
                pixmap = pixmap.scaled(image_width, image_height, Qt.KeepAspectRatio)
                
                label.setPixmap(pixmap)
                label.setAlignment(Qt.AlignCenter)
                
                # Add a thin orange border around the image
                label.setStyleSheet("border: 1px solid orange; padding: 4px;")

                self.scroll_layout.addWidget(label)

            self.files.extend(added_files)

        if removed_files:
            print("Removed files found:", removed_files)
            for filename in removed_files:
                # Find the widget associated with the removed file and remove it from the layout
                for i in range(self.scroll_layout.count()):
                    widget = self.scroll_layout.itemAt(i).widget()
                    if widget is not None and widget.toolTip() == filename:
                        widget.setParent(None)
                        self.files.remove(filename)

def main(directory_path):
    app = QApplication(sys.argv)
    window = FileViewer(directory_path)
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    directory_path = os.path.join(os.path.expanduser("~"), "Desktop", "SiloV2", "SH")  # Adjusted for desktop path
    image_width = 200  # Move image_width and image_height outside the class definition
    image_height = 150
    main(directory_path)


