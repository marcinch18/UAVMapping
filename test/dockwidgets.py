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
#import sip
#sip.setapi('QString', 2)

from PySide import QtCore, QtGui




class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.textEdit = QtGui.QTextEdit()
        self.setCentralWidget(self.textEdit)

        self.createActions()
        self.createMenus()
        self.createStatusBar()
        self.createParametersDockWindow()
        self.createResPreviewDockWindow()

        self.setWindowTitle("Dock Widgets")

        self.newLetter()
        self.setUnifiedTitleAndToolBarOnMac(True)

    def newLetter(self):
        self.textEdit.clear()

        cursor = self.textEdit.textCursor()
        cursor.movePosition(QtGui.QTextCursor.Start)
        topFrame = cursor.currentFrame()
        topFrameFormat = topFrame.frameFormat()
        topFrameFormat.setPadding(16)
        topFrame.setFrameFormat(topFrameFormat)

        textFormat = QtGui.QTextCharFormat()
        boldFormat = QtGui.QTextCharFormat()
        boldFormat.setFontWeight(QtGui.QFont.Bold)
        italicFormat = QtGui.QTextCharFormat()
        italicFormat.setFontItalic(True)

        tableFormat = QtGui.QTextTableFormat()
        tableFormat.setBorder(1)
        tableFormat.setCellPadding(16)
        tableFormat.setAlignment(QtCore.Qt.AlignRight)
        cursor.insertTable(1, 1, tableFormat)
        cursor.insertText("The Firm", boldFormat)
        cursor.insertBlock()
        cursor.insertText("321 City Street", textFormat)
        cursor.insertBlock()
        cursor.insertText("Industry Park")
        cursor.insertBlock()
        cursor.insertText("Some Country")
        cursor.setPosition(topFrame.lastPosition())
        cursor.insertText(QtCore.QDate.currentDate().toString("d MMMM yyyy"),
                textFormat)
        cursor.insertBlock()
        cursor.insertBlock()
        cursor.insertText("Dear ", textFormat)
        cursor.insertText("NAME", italicFormat)   
        cursor.insertText(",", textFormat)
        for i in range(3):
            cursor.insertBlock()
        cursor.insertText("Yours sincerely,", textFormat)
        for i in range(3):
            cursor.insertBlock()
        cursor.insertText("The Boss", textFormat)
        cursor.insertBlock()
        cursor.insertText("ADDRESS", italicFormat)  

    def print_(self):
        document = self.textEdit.document()
        printer = QtGui.QPrinter()

        dlg = QtGui.QPrintDialog(printer, self)
        if dlg.exec_() != QtGui.QDialog.Accepted:
            return

        document.print_(printer)

        self.statusBar().showMessage("Ready", 2000)

    def save(self):
        filename, filtr = QtGui.QFileDialog.getSaveFileName(self,
                "Choose a file name", '.', "HTML (*.html *.htm)")
        if not filename:
            return

        file = QtCore.QFile(filename)
        if not file.open(QtCore.QFile.WriteOnly | QtCore.QFile.Text):
            QtGui.QMessageBox.warning(self, "Dock Widgets",
                    "Cannot write file %s:\n%s." % (filename, file.errorString()))
            return

        out = QtCore.QTextStream(file)
        QtGui.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
        out << self.textEdit.toHtml()
        QtGui.QApplication.restoreOverrideCursor()

        self.statusBar().showMessage("Saved '%s'" % filename, 2000)

    def undo(self):
        document = self.textEdit.document()
        document.undo()

    def insertCustomer(self, customer):
        if not customer:
            return
        customerList = customer.split(', ')
        document = self.textEdit.document()
        cursor = document.find('NAME')
        if not cursor.isNull():
            cursor.beginEditBlock()
            cursor.insertText(customerList[0])
            oldcursor = cursor
            cursor = document.find('ADDRESS')
            if not cursor.isNull():
                for i in customerList[1:]:
                    cursor.insertBlock()
                    cursor.insertText(i)
                cursor.endEditBlock()
            else:
                oldcursor.endEditBlock()

    def addParagraph(self, paragraph):
        if not paragraph:
            return
        document = self.textEdit.document()
        cursor = document.find("Yours sincerely,")
        if cursor.isNull():
            return
        cursor.beginEditBlock()
        cursor.movePosition(QtGui.QTextCursor.PreviousBlock,
                QtGui.QTextCursor.MoveAnchor, 2)
        cursor.insertBlock()
        cursor.insertText(paragraph)
        cursor.insertBlock()
        cursor.endEditBlock()

    def about(self):
        QtGui.QMessageBox.about(self, "About Dock Widgets",
                "The <b>Dock Widgets</b> example demonstrates how to use "
                "Qt's dock widgets. You can enter your own text, click a "
                "customer to add a customer name and address, and click "
                "standard paragraphs to add them.")

    def createActions(self):
        self.newLetterAct = QtGui.QAction(QtGui.QIcon(':/images/new.png'),
                "&New Letter", self, shortcut=QtGui.QKeySequence.New,
                statusTip="Create a new form letter",
                triggered=self.newLetter)

        self.saveAct = QtGui.QAction(QtGui.QIcon(':/images/save.png'),
                "&Save...", self, shortcut=QtGui.QKeySequence.Save,
                statusTip="Save the current form letter",
                triggered=self.save)

        self.printAct = QtGui.QAction(QtGui.QIcon(':/images/print.png'),
                "&Print...", self, shortcut=QtGui.QKeySequence.Print,
                statusTip="Print the current form letter",
                triggered=self.print_)

        self.undoAct = QtGui.QAction(QtGui.QIcon(':/images/undo.png'),
                "&Undo", self, shortcut=QtGui.QKeySequence.Undo,
                statusTip="Undo the last editing action", triggered=self.undo)

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
        self.fileMenu.addAction(self.newLetterAct)
        self.fileMenu.addAction(self.saveAct)
        self.fileMenu.addAction(self.printAct)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.quitAct)

        self.editMenu = self.menuBar().addMenu("&Edit")
        self.editMenu.addAction(self.undoAct)

        self.viewMenu = self.menuBar().addMenu("&View")

        self.menuBar().addSeparator()

        self.helpMenu = self.menuBar().addMenu("&Help")
        self.helpMenu.addAction(self.aboutAct)
        self.helpMenu.addAction(self.aboutQtAct)

    #def createToolBars(self):
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
        self.dockBottom = QtGui.QDockWidget("Podgląd wyników", self)
        self.paragraphsList = QtGui.QListWidget(self.dockBottom)
        self.paragraphsList.addItems((
            "Thank you for your payment which we have received today.",
            "Your order has been dispatched and should be with you within "
                "28 days.",
            "We have dispatched those items that were in stock. The rest of "
                "your order will be dispatched once all the remaining items "
                "have arrived at our warehouse. No additional shipping "
                "charges will be made.",
            "You made a small overpayment (less than $5) which we will keep "
                "on account for you, or return at your request.",
            "You made a small underpayment (less than $1), but we have sent "
                "your order anyway. We'll add this underpayment to your next "
                "bill.",
            "Unfortunately you did not send enough money. Please remit an "
                "additional $. Your order will be dispatched as soon as the "
                "complete amount has been received.",
            "You made an overpayment (more than $5). Do you wish to buy more "
                "items, or should we return the excess to you?"))

        self.dockBottom.setWidget(self.paragraphsList)
        self.addDockWidget(QtCore.Qt.BottomDockWidgetArea, self.dockBottom)


    def createParametersGroupBox(self):
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

        self.centerGroupBox = QtGui.QGroupBox("Parametry aparatu")
        layoutCenter = QtGui.QFormLayout()
        layoutCenter.addRow(QtGui.QLabel("Mianownik skali mapy:"), QtGui.QSpinBox())
        layoutCenter.addRow(QtGui.QLabel("Ogniskowa aparatu:"), QtGui.QSpinBox())
        layoutCenter.addRow(QtGui.QLabel("Czas otwarcia migawki:"), QtGui.QSpinBox())

        self.centerGroupBox.setLayout(layoutCenter)

        self.bottomGroupBox = QtGui.QGroupBox("Form layout")
        layout = QtGui.QFormLayout()
        layout.addRow(QtGui.QLabel("Wysokosc lotu:"), QtGui.QSpinBox())
        layout.addRow(QtGui.QLabel("Wysokosc lotniska:"), QtGui.QSpinBox())
        layout.addRow(QtGui.QLabel("Wysokosc minimalna terenu:"), QtGui.QSpinBox())
        layout.addRow(QtGui.QLabel("Wysokosc maksymalna terenu:"), QtGui.QSpinBox())
        layout.addRow(QtGui.QLabel("Mianownik skali mapy:"), QtGui.QSpinBox())
        layout.addRow(QtGui.QLabel("Ogniskowa aparatu:"), QtGui.QSpinBox())
        layout.addRow(QtGui.QLabel("Czas otwarcia migawki:"), QtGui.QSpinBox())
        layout.addRow(QtGui.QLabel("Line 2, long text:"), QtGui.QComboBox())
        layout.addRow(QtGui.QLabel("Line 3:"), QtGui.QSpinBox())
        self.formGroupBox.setLayout(layout)

if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
