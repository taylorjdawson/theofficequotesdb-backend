import sys

from PyQt5.QtWidgets import QApplication, QPushButton, QLineEdit
from PyQt5.QtWidgets import QGroupBox, QDialog, QVBoxLayout, \
    QGridLayout, QTextEdit, QProgressBar

from DeployableServer.ElasticSearchClient import ElasticSearchClient


class App(QDialog):
    def __init__(self):
        super().__init__()
        self.title = 'ES Tester'
        self.left = 1100
        self.top = 900
        self.width = 1200
        self.height = 700
        self.initUI()


    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.createGridLayout()

        windowLayout = QVBoxLayout()
        windowLayout.addWidget(self.horizontalGroupBox)
        self.setLayout(windowLayout)

        self.show()

    def createGridLayout(self):
        self.es = ElasticSearchClient()
        self.horizontalGroupBox = QGroupBox()
        self.layout = QGridLayout()
        self.layout.setSpacing(10)
        # layout.setColumnStretch(0, 4)
        # layout.setColumnStretch(2, 4)

        self.textbox = QLineEdit(self)
        self.search_btn = QPushButton('Search')
        self.reindex_btn = QPushButton('Reindex')
        self.indexProgress = QProgressBar(self)

        self.indexProgress.setGeometry(200, 80, 250, 20)
        self.indexProgress.setVisible(False)
        self.search_results = QTextEdit(self)
        self.search_results.setReadOnly(True)

        self.layout.addWidget(self.indexProgress, 3, 0)
        self.layout.addWidget(self.textbox, 0, 0)
        self.layout.addWidget(self.reindex_btn,2,0,1,1)
        self.layout.addWidget(self.search_btn, 0, 1,1,1)
        self.layout.addWidget(self.search_results, 1, 0,1,2)

        self.horizontalGroupBox.setLayout(self.layout)

        # self.worker = Worker(self.es)
        # self.worker.updateProgress.connect(self.setProgress)

        self.search_btn.clicked.connect(self.searchBtnClick)
        self.indexProgress.setValue(0)
        self.reindex_btn.clicked.connect(self.reindex)

        # self.worker.started.connect(self.disableBtns)
        # self.worker.finished.connect(self.enableBtns)


    def searchBtnClick(self):
        self.search_results.clear()
        text = self.textbox.text()
        results = self.es.search(text)
        for res in results:
            self.search_results.insertHtml(res + '<br>')

    def setProgress(self, progress):
        self.indexProgress.setValue(progress)

    def enableBtns(self):
        self.search_btn.setDisabled(False)
        self.reindex_btn.setDisabled(False)

    def disableBtns(self):
        self.search_btn.setDisabled(True)
        self.reindex_btn.setDisabled(True)

# self.es.indexES()

    def reindex(self):
        self.disableBtns()
        self.es.indexES()
        self.enableBtns()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())