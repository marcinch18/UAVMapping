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

#from PySide import QtCore, QtGui, QtWebKit
#from PySide.QtGui import QApplication, QWidget, QVBoxLayout, QPushButton

from  PySide.QtWebKit import QWebView
#from os.path import abspath, dirname
from calcs.inzFlightCalculator import FlightCalculator
from qgmap import *

class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.centralDialog = TabDialog()
        self.setCentralWidget(self.centralDialog)

        self.createActions()
        self.createMenus()
        self.createStatusBar()
        self.createButtons()
        self.createParametersDockWindow()
        self.createResPreviewDockWindow()
        self.createConncetions()

        self.setWindowTitle("Program do Obliczania Nalotu Fotogrametrycznego")

        self.setUnifiedTitleAndToolBarOnMac(True)
        self.centralDialog.cameraTab.focalLEdit.setText(self.hlSbox.text())

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
        self.createParametersGroupBox()

        self.dockProperties = QtGui.QDockWidget("Parametry", self)
        self.dockProperties.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea | QtCore.Qt.RightDockWidgetArea)

        self.propDockGroupBox = QtGui.QGroupBox("Dane Wyjsciowe")
        self.propDockLayout = QtGui.QVBoxLayout()

        self.propDockLayout.addWidget(self.formGroupBox)
        self.propDockLayout.addWidget(self.calculateButton)
        self.propDockGroupBox.setLayout(self.propDockLayout)

        scrollArea = QtGui.QScrollArea()
        scrollArea.setBackgroundRole(QtGui.QPalette.Dark)
        scrollArea.setWidget(self.propDockGroupBox)

        self.dockProperties.setWidget(scrollArea)
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.dockProperties)

    def createResPreviewDockWindow(self):
        self.dockBottom = QtGui.QDockWidget("Podglad wynikow", self)
        self.resPrevText = QtGui.QTextEdit(self.dockBottom)

        self.dockBottom.setWidget(self.resPrevText)
        self.addDockWidget(QtCore.Qt.BottomDockWidgetArea, self.dockBottom)


    def createParametersGroupBox(self):
        self.formGroupBox = QtGui.QGroupBox("Parametry")

        self.topGroupBox = QtGui.QGroupBox("Wysokosci")
        layoutTop = QtGui.QFormLayout()
        self.hlSbox = QtGui.QLineEdit("150")
        self.hltnSbox = QtGui.QLineEdit("124")
        self.hmintSbox = QtGui.QLineEdit("239")
        self.hmaxtSbox = QtGui.QLineEdit("269")
        layoutTop.addRow(QtGui.QLabel("Wysokosc Fotografowania [m]:"), self.hlSbox)
        layoutTop.addRow(QtGui.QLabel("Wysokosc Lotniska [m]:"), self.hltnSbox)
        layoutTop.addRow(QtGui.QLabel("Wysokosc Minimalna terenu [m]:"), self.hmintSbox)
        layoutTop.addRow(QtGui.QLabel("Wysokosc Maksymalna terenu [m]:"), self.hmaxtSbox)

        self.topGroupBox.setLayout(layoutTop)

        self.centerGroupBox = QtGui.QGroupBox("Parametry oblotu")
        layoutCenter = QtGui.QFormLayout()
        self.msklzSbox = QtGui.QLineEdit("2000")
        self.prlSbox = QtGui.QLineEdit("22")
        self.pokpodSbox = QtGui.QLineEdit("60")
        self.pokpopSbox = QtGui.QLineEdit("25")
        layoutCenter.addRow(QtGui.QLabel("Mianownik skali mapy:"), self.msklzSbox)
        layoutCenter.addRow(QtGui.QLabel("Predkosc lotu [m/s]:"), self.prlSbox)
        layoutCenter.addRow(QtGui.QLabel("Pokrycie podluzne [%]:"), self.pokpodSbox)
        layoutCenter.addRow(QtGui.QLabel("Pokrycie poprzeczne [%]:"), self.pokpopSbox)
        self.centerGroupBox.setLayout(layoutCenter)

        self.centerGroupBox2 = QtGui.QGroupBox("Parametry aparatu")
        layoutCenter2 = QtGui.QFormLayout()
        self.ognaparSbox = QtGui.QLineEdit("80")
        self.czotmigSbox = QtGui.QLineEdit("0.002")
        self.pikselRSbox = QtGui.QLineEdit("6")
        self.predaparSbox = QtGui.QLineEdit("1.2")
        self.szermatSbox = QtGui.QLineEdit("36.7")
        self.dlgmatSbox = QtGui.QLineEdit("49.1")
        self.szermatpixSbox = QtGui.QLineEdit("6132")
        self.dlgmatpixSbox = QtGui.QLineEdit("8176")
        layoutCenter2.addRow(QtGui.QLabel("Ogniskowa aparatu [mm]:"), self.ognaparSbox)
        layoutCenter2.addRow(QtGui.QLabel("Czas otwarcia migawki [s]:"), self.czotmigSbox)
        layoutCenter2.addRow(QtGui.QLabel("Rozmiar piksela [um]:"), self.pikselRSbox)
        layoutCenter2.addRow(QtGui.QLabel("Predkosc aparatu [s]:"), self.predaparSbox)
        layoutCenter2.addRow(QtGui.QLabel("Szerokosc matrycy,a [mm]:"), self.szermatSbox)
        layoutCenter2.addRow(QtGui.QLabel("Dlugosc matrycy,b [mm]:"), self.dlgmatSbox)
        layoutCenter2.addRow(QtGui.QLabel("Szerokosc matrycy,pa [pix]:"), self.szermatpixSbox)
        layoutCenter2.addRow(QtGui.QLabel("Dlugosc matrycy,pb [pix]:"), self.dlgmatpixSbox)
        self.centerGroupBox2.setLayout(layoutCenter2)

        self.bottomGroupBox = QtGui.QGroupBox("Parametry mapy")
        layoutBottom = QtGui.QFormLayout()
        self.lxmapySbox = QtGui.QLineEdit("4000")
        self.lymapySbox = QtGui.QLineEdit("4000")
        layoutBottom.addRow(QtGui.QLabel("Wymiar Lx mapy [m]:"), self.lxmapySbox)
        layoutBottom.addRow(QtGui.QLabel("Wymiar Ly mapy [m]:"), self.lymapySbox)
        # layout.addRow(QtGui.QLabel("Line 2, long text:"), QtGui.QComboBox())
        # layout.addRow(QtGui.QLabel("Line 3:"), QtGui.QLineEdit())
        self.bottomGroupBox.setLayout(layoutBottom)

        formLayout = QtGui.QVBoxLayout()
        formLayout.addWidget(self.topGroupBox)
        formLayout.addWidget(self.centerGroupBox)
        formLayout.addWidget(self.centerGroupBox2)
        formLayout.addWidget(self.bottomGroupBox)

        self.formGroupBox.setLayout(formLayout)


    def createButtons(self):
        self.calculateButton = QtGui.QPushButton()
        self.calculateButton.setText("Oblicz")

    def createConncetions(self):
        QtCore.QObject.connect(self.calculateButton, QtCore.SIGNAL('clicked()'), self.getResults)



    def getResults(self):
        if self.predaparSbox.text() != "":
            lzd1 = (60.0 / float(self.predaparSbox.text()))
            ognAp = float(self.ognaparSbox.text()) / 1000
            rozmPix = float(self.pikselRSbox.text()) / 10e6
            S = FlightCalculator(V=self.prlSbox.text(), hfp=self.hlSbox.text(), hmin=self.hmintSbox.text(),
                                 hmax=self.hmaxtSbox.text(), hltn=self.hltnSbox.text(), M=self.msklzSbox.text(),
                                 ck=ognAp, ce=self.czotmigSbox.text(), a=self.szermatSbox.text(),
                                 b=self.dlgmatSbox.text(), pa=self.szermatpixSbox.text(), pb=self.dlgmatpixSbox.text(),
                                 pixelS=rozmPix, Ly=self.lymapySbox.text(), Lx=self.lxmapySbox.text(),
                                 p=self.pokpodSbox.text(), q=self.pokpopSbox.text(), lzd=lzd1)

            # S.calculateVariable(True,hfp=h)
            S.calculateAll()
            self.resPrevText.clear()
            res = str(S.results.items())
            res = res.replace("), (", "\n")
            res = res.replace("dict_items([(", "Wyniki:\n")
            res = res.replace(")])", "\n---Koniec---")
            self.resPrevText.setText(res)




class TabDialog(QtGui.QDialog):
    def __init__(self, parent=None):
        super(TabDialog, self).__init__(parent)

        self.cameraTab = CameraTab()
        self.mapTab = MapTab()
        tabWidget = QtGui.QTabWidget()
        tabWidget.addTab(self.mapTab, "Widok Mapy")
        tabWidget.addTab(self.cameraTab, "Obliczenia Kamery")
        mainLayout = QtGui.QVBoxLayout()
        mainLayout.addWidget(tabWidget)
        #mainLayout.addWidget(buttonBox)
        self.setLayout(mainLayout)
        #tabWidget.addTab(PermissionsTab(fileInfo), "Permissions")


class MapTab(QtGui.QWidget):
    def __init__(self, parent=None):
        super(MapTab, self).__init__(parent)
        # Create and fill a QWebView
        self.view = GoogleMapView()
        #self.hgroupbox = QtGui.QGroupBox()

        self.addressEdit = QtGui.QLineEdit()
        self.coordsEdit = QtGui.QLineEdit()
        layout = QtGui.QFormLayout()
        layout.addRow('Address:', self.addressEdit)
        layout.addRow('Coords:', self.coordsEdit)
        layout.addRow(self.view)

        self.coordsEdit.editingFinished.connect(lambda: self.view.goCoords(self.coordsEdit))
        self.addressEdit.editingFinished.connect(lambda: self.view.goAddress( self.addressEdit,self.coordsEdit))
        self.setLayout(layout)

class CameraTab(QtGui.QWidget):
    def __init__(self, parent=None):
        super(CameraTab, self).__init__(parent)
        self.hfotoEdit = QtGui.QLineEdit()
        self.focalLEdit = QtGui.QLineEdit()
        self.NcamEdit = QtGui.QLineEdit()
        self.cocEdit = QtGui.QLineEdit()
        self.hfotoEdit.isReadOnly()
        self.calculateCamButton = QtGui.QPushButton("Oblicz")
        QtCore.QObject.connect(self.calculateCamButton, QtCore.SIGNAL('clicked()'), self.getCameraParameters)

        inputGroupBox = QtGui.QGroupBox("Parametry kamery ")
        layout = QtGui.QFormLayout()
        layout.addRow("Wysokosc fotografowania [m]",self.hfotoEdit)
        layout.addRow("Ogniskowa aparatu [mm]",self.focalLEdit)
        layout.addRow("Liczba przeslony [-]",self.NcamEdit)
        layout.addRow("Krazek rozmycia [mm]",self.cocEdit)

        inputGroupBox.setLayout(layout)

        outputGroupBox = QtGui.QGroupBox("Wyniki obliczen: ")
        outlayout = QtGui.QGridLayout()
        self.outputText = QtGui.QTextEdit()
        outlayout.addWidget(self.outputText)
        outputGroupBox.setLayout(outlayout)
        self.finalLayout =  QtGui.QVBoxLayout()
        self.finalLayout.addWidget(inputGroupBox)
        self.finalLayout.addWidget(self.calculateCamButton)
        self.finalLayout.addWidget(outputGroupBox)

        self.setLayout(self.finalLayout)

    def addResultsLayout(self):

        text = "Odleglosc hiperfokalna [m]: %s" % self.hyperfocalL + "\n"
        text = text  + ("Poczatek glebi ostrosci [m]: %s" % self.strOfFocL)+ "\n"
        text = text  + ("Koniec glebi ostrosci [m]: %s" % self.endOfFocL)+ "\n"
        text = text  + "Glebia ostrosci [m]: %s" % self.DOF+ "\n"
        self.outputText.setText(text)



    def getCameraParameters(self):
        self.getHyperfocalL()
        self.getStartOfFocal()
        self.getEndOfFocal()
        self.getDOF()

        self.addResultsLayout()

    def getHyperfocalL(self):
        f2=float(self.focalLEdit.text())*float(self.focalLEdit.text())*1e-6
        N=float(self.NcamEdit.text())*1e-3
        CoC=float(self.cocEdit.text())*1e-3
        self.hyperfocalL = f2/(N*CoC)*1e-3

    def getStartOfFocal(self):
        hfoto = float(self.hfotoEdit.text())
        self.strOfFocL = self.hyperfocalL * hfoto / (self.hyperfocalL + hfoto)

    def getEndOfFocal(self):
        hfoto = float(self.hfotoEdit.text())
        self.endOfFocL = self.hyperfocalL * hfoto / (self.hyperfocalL - hfoto)

    def getDOF(self):
        self.DOF = self.endOfFocL - self.strOfFocL

class GoogleMapView(QWebView):
    def __init__(self):
        super(GoogleMapView, self).__init__()


        self.gmap = QGoogleMap(self)
        self.createConnections()

        #self.gmap.setSizePolicy(
        #    QtGui.QSizePolicy.MinimumExpanding,
        #    QtGui.QSizePolicy.MinimumExpanding)

        self.gmap.waitUntilReady()

        self.gmap.centerAt(50.9412313855822,20.419464111328125)
        self.gmap.setZoom(12)
        coords = self.gmap.centerAtAddress("DW748 17-25, 26-067, Poland")
        # Many icons at: https://sites.google.com/site/gmapsdevelopment/
        self.gmap.addMarker("MyDragableMark", *coords, **dict(
            draggable=True,
            title="Move me!"
        ))

        self.gmap.createPolyline()

    def createConnections(self):
        self.gmap.mapMoved.connect(self.onMapMoved)
        self.gmap.markerMoved.connect(self.onMarkerMoved)
        self.gmap.mapClicked.connect(self.onMapLClick)
        self.gmap.mapDoubleClicked.connect(self.onMapDClick)
        self.gmap.mapRightClicked.connect(self.onMapRClick)
        self.gmap.markerClicked.connect(self.onMarkerLClick)
        self.gmap.markerDoubleClicked.connect(self.onMarkerDClick)
        self.gmap.markerRightClicked.connect(self.onMarkerRClick)

    def goCoords(self,coordsIn):
        def resetError(self):
            self.coordsEdit.setStyleSheet('')

        try:
            latitude, longitude = coordsIn.text().split(",")
        except ValueError:
            coordsIn.setStyleSheet("color: red;")
            QtCore.QTimer.singleShot(500, resetError)
        else:
            self.gmap.centerAt(latitude, longitude)
            self.gmap.moveMarker("MyDragableMark", latitude, longitude)

    def goAddress(self,address,coordsIn):
        def resetError():
            address.setStyleSheet('')

        coords = self.gmap.centerAtAddress(address.text())
        if coords is None:
            address.setStyleSheet("color: red;")
            QtCore.QTimer.singleShot(500, resetError)
            return
        self.gmap.moveMarker("MyDragableMark", *coords)
        coordsIn.setText("{}, {}".format(*coords))

    def onMarkerMoved(self,key, latitude, longitude):
        print("Moved!!", key, latitude, longitude)
        self.coordsEdit.setText("{}, {}".format(latitude, longitude))

    def onMarkerRClick(self,key):
        print("RClick on ", key)
        self.gmap.setMarkerOptions(key, draggable=False)

    def onMarkerLClick(self,key):
        print("LClick on ", key)

    def onMarkerDClick(self,key):
        print("DClick on ", key)
        self.gmap.setMarkerOptions(key, draggable=True)

    def onMapMoved(self,latitude, longitude):
        print("Moved to ", latitude, longitude)

    def onMapRClick(self,latitude, longitude):
        print("RClick on ", latitude, longitude)

    def onMapLClick(self,latitude, longitude):
        print("LClick on ", latitude, longitude)

    def onMapDClick(self,latitude, longitude):
        print("DClick on ", latitude, longitude)


if __name__ == '__main__':
    import sys

    app = QtGui.QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
