#!/usr/bin/env python

############################################################################
#
#  Copyright (C) 2004-2005 Trolltech AS. All rights reserved.
#
#  This file is part of the example classes of the Qt Toolkit.
#
#  This file may be used under the terms of the GNU General Public
#  License version 2.0 as published by the Free Software Foundation
#  and appearing in the file LICENSE.GPL included in the packaging of
#  this file.  Please review the following information to ensure GNU
#  General Public Licensing requirements will be met:
#  http://www.trolltech.com/products/qt/opensource.html
#
#  If you are unsure which license is appropriate for your use, please
#  review the following information:
#  http://www.trolltech.com/products/qt/licensing.html or contact the
#  sales department at sales@trolltech.com.
#
#  This file is provided AS IS with NO WARRANTY OF ANY KIND, INCLUDING THE
#  WARRANTY OF DESIGN, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.
#
############################################################################

# This is only needed for Python v2 but is harmless for Python v3.
# import sip
# sip.setapi('QString', 2)

from PySide import QtCore, QtGui,QtWebKit
from PySide.QtGui import QApplication, QWidget, QVBoxLayout, QPushButton

from  PySide.QtWebKit import QWebView


class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()


        self.setCentralWidget(self.getMapView())

        self.createActions()
        self.createMenus()
        self.createStatusBar()
        self.createParametersDockWindow()
        self.createResPreviewDockWindow()

        self.setWindowTitle("Dock Widgets")

        self.setUnifiedTitleAndToolBarOnMac(True)

    def about(self):
        QtGui.QMessageBox.about(self, "About Dock Widgets",
                                "The <b>Dock Widgets</b> example demonstrates how to use "
                                "Qt's dock widgets. You can enter your own text, click a "
                                "customer to add a customer name and address, and click "
                                "standard paragraphs to add them.")

    def createActions(self):
        self.quitAct = QtGui.QAction("&Quit", self, shortcut="Ctrl+Q",
                                     statusTip="Quit the application", triggered=self.close)

        self.aboutAct = QtGui.QAction("&About", self,
                                      statusTip="Show the application's About box",
                                      triggered=self.about)

        self.aboutQtAct = QtGui.QAction("About &Qt", self,
                                        statusTip="Show the Qt library's About box",
                                        triggered=QtGui.qApp.aboutQt)

    def createMenus(self):
        self.fileMenu = self.menuBar().addMenu("&File")

        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.quitAct)

        self.editMenu = self.menuBar().addMenu("&Edit")

        self.viewMenu = self.menuBar().addMenu("&View")

        self.menuBar().addSeparator()

        self.helpMenu = self.menuBar().addMenu("&Help")
        self.helpMenu.addAction(self.aboutAct)
        self.helpMenu.addAction(self.aboutQtAct)

    # def createToolBars(self):
    #    self.fileToolBar = self.addToolBar("File")
    #    self.fileToolBar.addAction(self.newLetterAct)
    #    self.fileToolBar.addAction(self.saveAct)
    #    self.fileToolBar.addAction(self.printAct)

    #    self.editToolBar = self.addToolBar("Edit")
    #    self.editToolBar.addAction(self.undoAct)

    def createStatusBar(self):
        self.statusBar().showMessage("Ready")

    def createParametersDockWindow(self):
        self.dockPropertiees = QtGui.QDockWidget("Parametry", self)
        self.dockPropertiees.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea | QtCore.Qt.RightDockWidgetArea)

        self.createParametersGroupBox()
        self.dockPropertiees.setWidget(self.formGroupBox)
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.dockPropertiees)

    def createResPreviewDockWindow(self):
        self.dockBottom = QtGui.QDockWidget("Podglad wynikow", self)
        self.paragraphsList = QtGui.QListWidget(self.dockBottom)
        self.paragraphsList.addItems((
            "Test .",
        ))

        self.dockBottom.setWidget(self.paragraphsList)
        self.addDockWidget(QtCore.Qt.BottomDockWidgetArea, self.dockBottom)

    def createParametersGroupBox(self):
        self.formGroupBox = QtGui.QGroupBox("Parametry")

        self.topGroupBox = QtGui.QGroupBox("Wysokosci")
        layoutTop = QtGui.QFormLayout()
        layoutTop.addRow(QtGui.QLabel("Lotu:"), QtGui.QSpinBox())
        layoutTop.addRow(QtGui.QLabel("Lotniska:"), QtGui.QSpinBox())
        layoutTop.addRow(QtGui.QLabel("Minimalna terenu:"), QtGui.QSpinBox())
        layoutTop.addRow(QtGui.QLabel("Maksymalna terenu:"), QtGui.QSpinBox())

        self.topGroupBox.setLayout(layoutTop)

        self.centerGroupBox = QtGui.QGroupBox("Parametry oblotu")
        layoutCenter = QtGui.QFormLayout()
        layoutCenter.addRow(QtGui.QLabel("Mianownik skali mapy:"), QtGui.QSpinBox())
        layoutCenter.addRow(QtGui.QLabel("Predkosc lotu:"), QtGui.QSpinBox())
        layoutCenter.addRow(QtGui.QLabel("Pokrycie podluzne:"), QtGui.QSpinBox())
        layoutCenter.addRow(QtGui.QLabel("Pokrycie poprzeczne:"), QtGui.QSpinBox())
        self.centerGroupBox.setLayout(layoutCenter)

        self.centerGroupBox2 = QtGui.QGroupBox("Parametry aparatu")
        layoutCenter2 = QtGui.QFormLayout()
        layoutCenter2.addRow(QtGui.QLabel("Mianownik skali mapy:"), QtGui.QSpinBox())
        layoutCenter2.addRow(QtGui.QLabel("Ogniskowa aparatu:"), QtGui.QSpinBox())
        layoutCenter2.addRow(QtGui.QLabel("Czas otwarcia migawki:"), QtGui.QSpinBox())

        self.centerGroupBox2.setLayout(layoutCenter2)

        self.bottomGroupBox = QtGui.QGroupBox("Form layout")
        layoutBottom = QtGui.QFormLayout()
        layoutBottom.addRow(QtGui.QLabel("Wysokosc lotu:"), QtGui.QSpinBox())
        layoutBottom.addRow(QtGui.QLabel("Wysokosc lotniska:"), QtGui.QSpinBox())
        layoutBottom.addRow(QtGui.QLabel("Wysokosc minimalna terenu:"), QtGui.QSpinBox())
        layoutBottom.addRow(QtGui.QLabel("Wysokosc maksymalna terenu:"), QtGui.QSpinBox())
        layoutBottom.addRow(QtGui.QLabel("Mianownik skali mapy:"), QtGui.QSpinBox())
        layoutBottom.addRow(QtGui.QLabel("Ogniskowa aparatu:"), QtGui.QSpinBox())
        layoutBottom.addRow(QtGui.QLabel("Czas otwarcia migawki:"), QtGui.QSpinBox())
        # layout.addRow(QtGui.QLabel("Line 2, long text:"), QtGui.QComboBox())
        # layout.addRow(QtGui.QLabel("Line 3:"), QtGui.QSpinBox())
        self.bottomGroupBox.setLayout(layoutBottom)

        formLayout = QtGui.QVBoxLayout()
        formLayout.addWidget(self.topGroupBox)
        formLayout.addWidget(self.centerGroupBox)
        formLayout.addWidget(self.centerGroupBox2)
        formLayout.addWidget(self.bottomGroupBox)

        self.formGroupBox.setLayout(formLayout)


    def getMapView(self):
        # Create and fill a QWebView
        self.view = QGoogleMap()
        return self.view


from os.path import abspath,dirname

class QGoogleMap(QWebView):

    def __init__(self):
        super(QGoogleMap, self).__init__()

        self.initialized = False
        self.loadFinished.connect(self.onLoadFinished)
        self.page().mainFrame().addToJavaScriptWindowObject(
            "qtWidget", self)

        basePath = abspath(dirname(__file__))
        url = 'file:///' + basePath + '/maps/googleapi.html'
        self.setUrl(QtCore.QUrl(url))


    def onLoadFinished(self, ok):
        if self.initialized: return
        if not ok:
            print("Error initializing Google Maps")
        self.initialized = True
        self.centerAt(0, 0)
        self.setZoom(1)


    def waitUntilReady(self):
        while not self.initialized:
            QtGui.QApplication.processEvents()


    def geocode(self, location):
        return GeoCoder(self).geocode(location)


    def runScript(self, script):
        return self.page().mainFrame().evaluateJavaScript(script)


    def centerAt(self, latitude, longitude):
        self.runScript("gmap_setCenter({},{})".format(latitude, longitude))


    def setZoom(self, zoom):
        self.runScript("gmap_setZoom({})".format(zoom))


    def center(self):
        center = self.runScript("gmap_getCenter()")
        return center.lat, center.lng


    def centerAtAddress(self, location):
        try:
            latitude, longitude = self.geocode(location)
        except GeoCoder.NotFoundError:
            return None
        self.centerAt(latitude, longitude)
        return latitude, longitude


    def addMarkerAtAddress(self, location, **extra):
        if 'title' not in extra:
            extra['title'] = location
        try:
            latitude, longitude = self.geocode(location)
        except GeoCoder.NotFoundError:
            return None
        return self.addMarker(location, latitude, longitude, **extra)


    def addMarker(self, key, latitude, longitude, **extra):
        return self.runScript(
            "gmap_addMarker("
            "key={!r}, "
            "latitude={}, "
            "longitude={}, "
            "{}"
            "); "
                .format(key, latitude, longitude, json.dumps(extra)))


    def moveMarker(self, key, latitude, longitude):
        return self.runScript(
            "gmap_moveMarker({!r}, {}, {});".format(key, latitude, longitude))


    def setMarkerOptions(self, keys, **extra):
        return self.runScript(
            "gmap_changeMarker("
            "key={!r}, "
            "{}"
            "); "
                .format(keys, json.dumps(extra)))


    def deleteMarker(self, key):
        return self.runScript(
            "gmap_deleteMarker("
            "key={!r} "
            "); "
                .format(key))


if __name__ == '__main__':
    import sys

    app = QtGui.QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
