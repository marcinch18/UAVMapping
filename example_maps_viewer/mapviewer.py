from PySide.QtGui import QApplication,QWidget,QVBoxLayout,QPushButton

from  PySide.QtWebKit import QWebView
from PySide import QtCore
from os.path import abspath,dirname



class QGoogleMap(QWebView):

    def __init__(self):
        super(QGoogleMap, self).__init__()


        basePath = abspath(dirname(__file__))
        basePath = basePath.replace("\\","/")
        url = 'file://' + basePath + '/maps/simple.html'


# Create an application
app = QApplication([])

# And a window
win = QWidget()
win.setWindowTitle('QWebView Interactive Demo')

# And give it a layout
layout = QVBoxLayout()
win.setLayout(layout)

# Create and fill a QWebView
view = QWebView()
basePath = abspath(dirname(__file__))
basePath = basePath.replace("\\","/")
url = 'file://' + basePath + '/maps/simple.html'
view.setUrl("file:///C:/Users/Marcin/Documents/AGATA/inzynierka2016/inzProgram/v1901/maps/simple.html")


# Add the QWebView and button to the layout
layout.addWidget(view)


# Show the window and run the app
win.show()
app.exec_()