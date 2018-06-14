
from PyQt5.QtCore import QDir, Qt
from PyQt5.QtGui import QImage, QPainter, QPalette, QPixmap
from PyQt5.QtWidgets import (QAction, QApplication, QFileDialog, QLabel,QGroupBox,QHBoxLayout,QPushButton,
        QMainWindow, QMenu, QMessageBox, QScrollArea, QSizePolicy,QVBoxLayout)
from PyQt5.QtPrintSupport import QPrintDialog, QPrinter


class ImageViewer(QMainWindow):
    def __init__(self, parent=None):
        #super(ImageViewer, self).__init__()
        QMainWindow.__init__(self, parent)
        #self.dataImageLabel = QLabel(self)
        #self.dataImageLabel.setText("Hello World")
        #self.dataImageLabel.setAlignment(Qt.AlignCenter)
        #self.dataImageLabel.move(50, 50)
        #self.dataImageLabel.setStyleSheet("QLabel#nom_plan_label {color: yellow}")
        '''self.l1 = QLabel()
        self.l2 = QLabel()
        self.l3 = QLabel()
        self.l4 = QLabel()

        self.l1.setText("Hello World")
        self.l4.setText("TutorialsPoint")
        self.l2.setText("welcome to Python GUI Programming")

        self.l1.setAlignment(Qt.AlignCenter)
        self.l3.setAlignment(Qt.AlignCenter)
        self.l4.setAlignment(Qt.AlignRight)
        self.l3.setPixmap(QPixmap("C:/Users/BDI/Documents/wow.jpg"))

        self.l1.setOpenExternalLinks(True)
        self.l4.linkActivated.connect(self.clicked)
        self.l2.linkHovered.connect(self.hovered)
        self.l1.setTextInteractionFlags(Qt.TextSelectableByMouse)

        # self.vbox.addStretch()
        # self.vbox.addWidget(l2)
        # self.vbox.addStretch()
        # self.vbox.addWidget(l3)
        # self.vbox.addStretch()
        #self.vbox.addWidget(l4)
        # self.vbox.addWidget(l2)
        self.vBox_ = QVBoxLayout(self)
        self.vBox_.addWidget(self.dataImageLabel)
        self.vBox_.addStretch()
        self.vBox_.addWidget(self.l1)
        self.vBox_.addStretch()
        self.vBox_.addWidget(self.l2)
        self.vBox_.addStretch()
        self.vBox_.addWidget(self.l3)
        self.vBox_.addStretch()
        self.vBox_.addWidget(self.l4)
        self.setLayout(self.vBox_)
        #self.setCentralWidget(self.vBox_)
        '''
        self.createActions()
        self.createMenus()

        self.setWindowTitle("Image Viewer")
        self.resize(500, 400)


        self.createHorizontalLayout()
        windowLayout = QVBoxLayout()
        windowLayout.addWidget(self.horizontalGroupBox)
        self.setLayout(windowLayout)

    def createHorizontalLayout(self):
        self.horizontalGroupBox = QGroupBox("What is your favorite color?")
        layout = QHBoxLayout()

        dataImageLabel = QLabel(self)
        dataImageLabel.setText("Hello World")
        # self.dataImageLabel.setAlignment(Qt.AlignCenter)
        # self.dataImageLabel.move(50, 50)
        dataImageLabel.setStyleSheet("QLabel#nom_plan_label {color: yellow}")
        layout.addWidget(dataImageLabel)

        buttonBlue = QPushButton('Blue', self)
        layout.addWidget(buttonBlue)

        buttonRed = QPushButton('Red', self)
        layout.addWidget(buttonRed)

        buttonGreen = QPushButton('Green', self)
        layout.addWidget(buttonGreen)

        self.horizontalGroupBox.setLayout(layout)

    def hovered(self):
        print("hovering")

    def clicked(self):
        print("clicked")

    def open(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Open File",
                QDir.currentPath())
        if fileName:
            image = QImage(fileName)
            if image.isNull():
                QMessageBox.information(self, "Image Viewer",
                        "Cannot load %s." % fileName)
                return

            self.imageLabel.setPixmap(QPixmap.fromImage(image))
            self.scaleFactor = 1.0

            self.printAct.setEnabled(True)
            self.fitToWindowAct.setEnabled(True)
            self.updateActions()

            if not self.fitToWindowAct.isChecked():
                self.imageLabel.adjustSize()


    def print_(self):
        dialog = QPrintDialog(self.printer, self)
        if dialog.exec_():
            painter = QPainter(self.printer)
            rect = painter.viewport()
            size = self.imageLabel.pixmap().size()
            size.scale(rect.size(), Qt.KeepAspectRatio)
            painter.setViewport(rect.x(), rect.y(), size.width(), size.height())
            painter.setWindow(self.imageLabel.pixmap().rect())
            painter.drawPixmap(0, 0, self.imageLabel.pixmap())

    def createActions(self):
        self.openAct = QAction("&Open...", self, shortcut="Ctrl+O",
                triggered=self.open)

        self.printAct = QAction("&Print...", self, shortcut="Ctrl+P",
                enabled=False, triggered=self.print_)

        self.exitAct = QAction("E&xit", self, shortcut="Ctrl+Q",
                triggered=self.close)

    def createMenus(self):
        self.fileMenu = QMenu("&File", self)
        self.fileMenu.addAction(self.openAct)
        self.fileMenu.addAction(self.printAct)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.exitAct)

        self.menuBar().addMenu(self.fileMenu)


