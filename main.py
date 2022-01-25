import os
import shutil
import sys
import random
import glob
from PySide6 import QtCore, QtWidgets, QtGui


class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # window configuration
        self.title = "Image Viewer"
        self.left = 30
        self.top = 30
        self.width = 530
        self.height = 530

        # index of the image currently displayed
        self.current_image_index = 0

        # get selected directory
        self.dir_path = QtWidgets.QFileDialog.getExistingDirectory(self)

        # valid image file extensions
        valid_ext = ['png', 'jpg', 'jpeg', 'tiff', 'bmp', 'gif']

        # find files with valid extension inside the selected directory
        self.files = []
        for ext in valid_ext:
            self.files.extend(glob.glob(f'{self.dir_path}/*.{ext}'))

        # map each image file with the assigned label
        self.map = {}

        # initialize UI
        self.initUI()

    def initUI(self):
        # set layout and window configurations

        self.setWindowTitle(self.title)
        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)
        self.label = QtWidgets.QLabel(self)
        layout.addWidget(self.label)
        self.information = QtWidgets.QLabel(self)
        layout.addWidget(self.information)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # show image in current_image_index
        if len(self.files) > 0:
            self.show_image(self.files[self.current_image_index])
        else:
            self.no_image()

        # show UI
        self.show()

    def keyPressEvent(self, event):
        # pressing q quits app
        if event.key() == QtCore.Qt.Key_Q:
            self.move_mapped_files()
            self.deleteLater()
        # right arrow moves to next image
        elif event.key() == QtCore.Qt.Key_Right:
            self.next()
        # left arrow moves to previous image
        elif event.key() == QtCore.Qt.Key_Left:
            self.previous()
        # numeric input maps current image with the input as a label
        elif event.text().isdigit():
            self.map_image(event.text())
        event.accept()

    def closeEvent(self, event):
        # when user trys to close the app, move mapped files and quit
        self.move_mapped_files()
        event.accept()

    def next(self):
        if len(self.files) > 0:
            # cycles through next images
            self.current_image_index = (
                self.current_image_index + 1) % len(self.files)
            self.show_image(self.files[self.current_image_index])
        else:
            self.no_image()

    def previous(self):
        if len(self.files) > 0:
            # cycles through previous images
            self.current_image_index = (len(self.files) +
                                        self.current_image_index - 1) % len(self.files)
            self.show_image(self.files[self.current_image_index])
        else:
            self.no_image()

    def map_image(self, key):
        # map each file path to numerical input as label
        self.map[self.files[self.current_image_index]] = key
        self.information.setText(f"Mapped to {key}")

    def move_mapped_files(self):
        try:
            # create subdirectories for labels if do not exist
            for num in self.map.values():
                os.makedirs(os.path.join(self.dir_path, num), exist_ok=True)

            # move the files to their labelled subdirectories
            for key, value in self.map.items():
                shutil.move(key, os.path.join(self.dir_path, value))

            # show success message
            msg = QtWidgets.QMessageBox(self)
            msg.setIcon(QtWidgets.QMessageBox.Information)
            msg.setWindowTitle("Success")
            msg.setInformativeText("Operation completed")
            msg.exec()

        except Exception as e:
            # show warning for exceptions
            msg = QtWidgets.QMessageBox(self)
            msg.setIcon(QtWidgets.QMessageBox.Critical)
            msg.setWindowTitle("Operation failed")
            msg.setInformativeText(str(e))
            msg.exec()

    def show_image(self, file):
        # shows an image from filepath and mapped label
        pixmap = QtGui.QPixmap(file)
        pixmap = pixmap.scaled(self.width, self.height,
                               QtCore.Qt.KeepAspectRatio)
        self.label.setPixmap(pixmap)
        self.label.setScaledContents(True)

        mapped = self.map.get(file, -1)
        if mapped != -1:
            self.information.setText(f"Mapped to {mapped}")
        else:
            self.information.setText("unmapped")

    def no_image(self):
        self.label.setText("No images")


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    widget = MyWidget()
    sys.exit(app.exec())
