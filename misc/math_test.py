
import sys

from PyQt4.QtGui import *


app = QApplication(sys.argv)

listWidget = QListWidget()

for i in range(10):
    item = QListWidgetItem("Item %i" % i)

listWidget.addItem(item)


listWidget.show()

sys.exit(app.exec_())