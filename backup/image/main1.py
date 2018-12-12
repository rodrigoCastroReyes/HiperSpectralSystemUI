from PyQt5.QtCore import *
from PyQt5.QtGui  import *
from PyQt5.QtWidgets import *
from QtImageViewer import QtImageViewer
import sys
from libtiff import TIFF
import re

def handleLeftClick(x, y):
    row = int(y)
    column = int(x)
    print("Pixel (row=" + str(row) + ", column=" + str(column) + ")")

class MyMainWindow(QMainWindow):

    def __init__(self, parent=None):

        super(MyMainWindow, self).__init__(parent)
        self.form_widget = FormWidget2(self)
        self.setCentralWidget(self.form_widget)
        self.createActions()
        self.createMenus()

    def open(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Open File",
                QDir.currentPath())
        if fileName:
            print(fileName)
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

    def createActions(self):
        self.openAct = QAction("&Open...", self, shortcut="Ctrl+O",
                triggered=self.open)

        self.exitAct = QAction("E&xit", self, shortcut="Ctrl+Q",
                triggered=self.close)

    def createMenus(self):
        self.fileMenu = QMenu("&File", self)
        self.fileMenu.addAction(self.openAct)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.exitAct)

        self.menuBar().addMenu(self.fileMenu)


class FormWidget(QWidget):

    def __init__(self, parent):
        super(FormWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)

        self.button1 = QPushButton("Button 1")
        self.layout.addWidget(self.button1)

        self.button2 = QPushButton("Button 2")
        self.layout.addWidget(self.button2)

        self.setLayout(self.layout)

class FormWidget2(QWidget):

    def __init__(self, parent):
        super(FormWidget2, self).__init__(parent)
        self.layout = QVBoxLayout(self)

        self.button1 = QLabel("Button 1")
        self.button1.setText("x=0 , y=0")
        self.layout.addWidget(self.button1)

        # Create an image viewer widget.
        self.viewer = QtImageViewer()

        self.viewer.label_=self.button1

        # Set viewer's aspect ratio mode.
        # !!! ONLY applies to full image view.
        # !!! Aspect ratio always ignored when zoomed.
        #   Qt.IgnoreAspectRatio: Fit to viewport.
        #   Qt.KeepAspectRatio: Fit in viewport using aspect ratio.
        #   Qt.KeepAspectRatioByExpanding: Fill viewport using aspect ratio.
        self.viewer.aspectRatioMode = Qt.KeepAspectRatio

        # Set the viewer's scroll bar behaviour.
        #   Qt.ScrollBarAlwaysOff: Never show scroll bar.
        #   Qt.ScrollBarAlwaysOn: Always show scroll bar.
        #   Qt.ScrollBarAsNeeded: Show scroll bar only when zoomed.
        self.viewer.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.viewer.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        # Allow zooming with right mouse button.
        # Drag for zoom box, doubleclick to view full image.
        self.viewer.canZoom = True

        # Allow panning with left mouse button.
        self.viewer.canPan = True
        
        # Load an image to be displayed.
        if QT_VERSION_STR[0] == '4':
            fileName = QFileDialog.getOpenFileName(None, "Open image file...")
        elif QT_VERSION_STR[0] == '5':
            fileName, dummy = QFileDialog.getOpenFileName(None, "Open image file...")
        
        #fileName = "/home/rodfcast/Documents/CVR/Proyecto Investigacion/dataset/Experimento-2016-04-29 18-24-24/fotoThor/planta40-11-30-58.tif"
        print(fileName)
        if re.search(".tif",fileName) != None:
            image = self.getImage(fileName)#soporte para leer imagenes tif RGB
        else:
            image = QImage(fileName)
        # Display the image in the viewer.
        self.viewer.setImage(image)

        # Handle left mouse clicks with your own custom slot
        # handleLeftClick(x, y). (x, y) are image coordinates.
        # For (row, col) matrix indexing, row=y and col=x.
        # ImageViewerQt also provides similar signals for
        # left/right mouse button press, release and doubleclick.
        #self.viewer.leftMouseButtonPressed.connect(handleLeftClick)

        # Show the viewer and run the application.
        self.viewer.show()
        self.layout.addWidget(self.viewer)

        self.setLayout(self.layout)

    def getImage(self,fileName):
        #image = tiff.imread(fileName)
        tif = TIFF.open(fileName, mode='r')
        # to read an image in the currect TIFF directory and return it as numpy array:
        image = tif.read_image()
        if len(image.shape) >2 :
            rows,cols,channels = image.shape
            qimage = QImage(cols, rows, QImage.Format_RGB32)
            for i in range(0, rows):
                for j in range(0, cols):
                    valueBGR =  image[i,j]
                    value = qRgb(valueBGR[0], valueBGR[1], valueBGR[2])
                    qimage.setPixel(j, i, value)
        else:
            rows,cols = image.shape
            qimage = QPixmap(cols, rows,QImage.Format_Grayscale8)
            
            for i in range(0, rows):
                for j in range(0, cols):
                    value = qGray(image[i,j])
                    qimage.setPixel(j, i, value)
            

        return qimage


    def handleLeftClick(self,x, y):
        row = int(y)
        column = int(x)
        print("Pixel (row=" + str(row) + ", column=" + str(column) + ")")

    # Custom slot for handling mouse clicks in our viewer.
    # Just prints the (row, column) matrix index of the
    # image pixel that was clicked on.

app = QApplication([])
foo = MyMainWindow()
foo.show()
sys.exit(app.exec_())