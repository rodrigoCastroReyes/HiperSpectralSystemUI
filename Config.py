from PyQt5 import QtWidgets, QtCore
import json, codecs
from PyQt5.QtWidgets import QApplication, QWidget,QFileDialog, QListWidget, QVBoxLayout, QLabel, QPushButton, QListWidgetItem, QHBoxLayout
from PyQt5.QtGui import QStandardItem
from PyQt5.QtGui import QStandardItemModel
from pathlib import Path

from PyQt5.uic import loadUi

class CustomQWidget(QWidget):
    def __init__(self, parent=None):
        super(CustomQWidget, self).__init__(parent)
        label = QLabel("I am a custom widget")
        button = QPushButton("A useless button")
        layout = QHBoxLayout()
        layout.addWidget(label)
        layout.addWidget(button)
        self.fileName=None
        self.setLayout(layout)

class Config(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.initUi()

    def agregar_click(self):
        # shost is a QString object
        parametro = self.lineEdit.text()
        if parametro.strip():
            self.listWidget.addItem(parametro)
            self.lineEdit.setText("")

    def item_click(self):
        print(self.listWidget.currentItem().text())

    def deleteIten(self):
        item=self.listWidget.takeItem(self.listWidget.currentRow())
        item = None

    def guardarData(self):
        itemsTextList = [str(self.listWidget.item(i).text()) for i in range(self.listWidget.count())]
        print(itemsTextList)
        #json_str = json.dumps(itemsTextList)
        print(self.pathFileEdit.text())
        data = {}
        data["parametros"] = itemsTextList
        file_config = open(self.pathFileEdit.text(), 'w', encoding='utf-8')
        file_config.write(json.dumps(data))
        file_config.close()

    def initUi(self):
        #self.setWindowTitle('Main Menu')
        #self.setFixedSize(200, 200)
        loadUi('widgetConfig.ui', self)
        self.setFixedSize(self.size())
        self.agregarButton.clicked.connect(self.agregar_click)
        self.listWidget.clicked.connect(self.item_click)
        self.deleteButton.clicked.connect(self.deleteIten)
        self.saveButton.clicked.connect(self.guardarData)
        self.fileButton.clicked.connect(self.onClickLoadFileConfig)
        '''item = QListWidgetItem(self.listWidget)
        item_widget = CustomQWidget()
        item.setSizeHint(item_widget.sizeHint())
        self.listWidget.addItem(item)
        self.listWidget.setItemWidget(item, item_widget)'''

        '''
        item2 = QListWidgetItem(self.listWidget)
        item_widget2 = CustomQWidget()
        item2.setSizeHint(item_widget2.sizeHint())
        self.listWidget.addItem(item2)
        self.listWidget.setItemWidget(item2, item_widget2)'''

    def onClickLoadFileConfig(self):
        #filename = QtWidgets.QFileDialog.getOpenFileName(None, 'Test Dialog', os.getcwd(), 'All Files(*.*)')
        #print(filename)
        #QtWidgets.QFileDialog.getExistingDirectory(self, 'Select directory')
        #options = QtWidgets.QFileDialog.DontResolveSymlinks | QtWidgets.QFileDialog.ShowDirsOnly
        #directory = QtWidgets.QFileDialog.getExistingDirectory(self,"Open Folder",options=options)
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.fileName, _ = QFileDialog.getSaveFileName(self, "QFileDialog.getSaveFileName()", "",
                                                  "All Files (*);;Text Files (*.txt)", options=options)

        if self.fileName:
            self.pathFileEdit.setText(self.fileName)
            my_file = Path(self.fileName)
            if my_file.exists():
                print(self.fileName)
                connection_file = open(self.fileName, 'r')
                conn_string = json.load(connection_file)
                connection_file.close()
                print(conn_string["parametros"])
                for parametro in conn_string["parametros"]:
                    self.listWidget.addItem(parametro)


