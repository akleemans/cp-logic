# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui.ui'
#
# Created: Sun Jan 20 19:51:52 2013
#      by: pyside-uic 0.2.13 running on PySide 1.1.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(680, 500)
        MainWindow.setMinimumSize(QtCore.QSize(680, 500))
        MainWindow.setMaximumSize(QtCore.QSize(680, 500))
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.lineEdit = QtGui.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(10, 421, 581, 20))
        self.lineEdit.setObjectName("lineEdit")
        self.pushButton = QtGui.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(599, 419, 80, 23))
        self.pushButton.setObjectName("pushButton")
        self.listWidget = QtGui.QListWidget(self.centralwidget)
        self.listWidget.setGeometry(QtCore.QRect(5, 8, 671, 401))
        self.listWidget.setObjectName("listWidget")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 680, 25))
        self.menubar.setObjectName("menubar")
        self.menuDatei = QtGui.QMenu(self.menubar)
        self.menuDatei.setObjectName("menuDatei")
        self.menu = QtGui.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        self.menuTools = QtGui.QMenu(self.menubar)
        self.menuTools.setObjectName("menuTools")
        self.menuFormula = QtGui.QMenu(self.menubar)
        self.menuFormula.setObjectName("menuFormula")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionConvert_to_NNF = QtGui.QAction(MainWindow)
        self.actionConvert_to_NNF.setObjectName("actionConvert_to_NNF")
        self.actionConvert_to_CNF = QtGui.QAction(MainWindow)
        self.actionConvert_to_CNF.setObjectName("actionConvert_to_CNF")
        self.actionD_Chains = QtGui.QAction(MainWindow)
        self.actionD_Chains.setObjectName("actionD_Chains")
        self.actionLoad_formula = QtGui.QAction(MainWindow)
        self.actionLoad_formula.setObjectName("actionLoad_formula")
        self.actionInfo = QtGui.QAction(MainWindow)
        self.actionInfo.setObjectName("actionInfo")
        self.actionNNF = QtGui.QAction(MainWindow)
        self.actionNNF.setObjectName("actionNNF")
        self.actionCNF = QtGui.QAction(MainWindow)
        self.actionCNF.setObjectName("actionCNF")
        self.actionLength = QtGui.QAction(MainWindow)
        self.actionLength.setObjectName("actionLength")
        self.actionSAT_naive = QtGui.QAction(MainWindow)
        self.actionSAT_naive.setObjectName("actionSAT_naive")
        self.actionGenerate = QtGui.QAction(MainWindow)
        self.actionGenerate.setObjectName("actionGenerate")
        self.actionSubformulas = QtGui.QAction(MainWindow)
        self.actionSubformulas.setObjectName("actionSubformulas")
        self.menuDatei.addAction(self.actionLoad_formula)
        self.menu.addAction(self.actionInfo)
        self.menuTools.addAction(self.actionSAT_naive)
        self.menuTools.addAction(self.actionD_Chains)
        self.menuFormula.addAction(self.actionLength)
        self.menuFormula.addAction(self.actionSubformulas)
        self.menuFormula.addSeparator()
        self.menuFormula.addAction(self.actionNNF)
        self.menuFormula.addAction(self.actionCNF)
        self.menuFormula.addSeparator()
        self.menuFormula.addAction(self.actionGenerate)
        self.menubar.addAction(self.menuDatei.menuAction())
        self.menubar.addAction(self.menuFormula.menuAction())
        self.menubar.addAction(self.menuTools.menuAction())
        self.menubar.addAction(self.menu.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL("clicked()"), MainWindow.buttonPressed)
        QtCore.QObject.connect(self.actionNNF, QtCore.SIGNAL("activated()"), MainWindow.menu_nnf)
        QtCore.QObject.connect(self.actionD_Chains, QtCore.SIGNAL("activated()"), MainWindow.menu_dchains)
        QtCore.QObject.connect(self.actionCNF, QtCore.SIGNAL("activated()"), MainWindow.menu_cnf)
        QtCore.QObject.connect(self.actionLoad_formula, QtCore.SIGNAL("activated()"), MainWindow.menu_loadformula)
        QtCore.QObject.connect(self.actionSAT_naive, QtCore.SIGNAL("activated()"), MainWindow.menu_sat)
        QtCore.QObject.connect(self.actionLength, QtCore.SIGNAL("activated()"), MainWindow.menu_length)
        QtCore.QObject.connect(self.actionGenerate, QtCore.SIGNAL("activated()"), MainWindow.menu_generate)
        QtCore.QObject.connect(self.actionSubformulas, QtCore.SIGNAL("activated()"), MainWindow.menu_sufo)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Toolbox Classical Propositional Logic", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("MainWindow", "Go", None, QtGui.QApplication.UnicodeUTF8))
        self.menuDatei.setTitle(QtGui.QApplication.translate("MainWindow", "File", None, QtGui.QApplication.UnicodeUTF8))
        self.menu.setTitle(QtGui.QApplication.translate("MainWindow", "?", None, QtGui.QApplication.UnicodeUTF8))
        self.menuTools.setTitle(QtGui.QApplication.translate("MainWindow", "Tools", None, QtGui.QApplication.UnicodeUTF8))
        self.menuFormula.setTitle(QtGui.QApplication.translate("MainWindow", "Formula", None, QtGui.QApplication.UnicodeUTF8))
        self.actionConvert_to_NNF.setText(QtGui.QApplication.translate("MainWindow", "Convert to NNF", None, QtGui.QApplication.UnicodeUTF8))
        self.actionConvert_to_CNF.setText(QtGui.QApplication.translate("MainWindow", "Convert to CNF", None, QtGui.QApplication.UnicodeUTF8))
        self.actionD_Chains.setText(QtGui.QApplication.translate("MainWindow", "D-Chains", None, QtGui.QApplication.UnicodeUTF8))
        self.actionLoad_formula.setText(QtGui.QApplication.translate("MainWindow", "Load formula...", None, QtGui.QApplication.UnicodeUTF8))
        self.actionInfo.setText(QtGui.QApplication.translate("MainWindow", "Info", None, QtGui.QApplication.UnicodeUTF8))
        self.actionNNF.setText(QtGui.QApplication.translate("MainWindow", "NNF", None, QtGui.QApplication.UnicodeUTF8))
        self.actionCNF.setText(QtGui.QApplication.translate("MainWindow", "CNF", None, QtGui.QApplication.UnicodeUTF8))
        self.actionLength.setText(QtGui.QApplication.translate("MainWindow", "Length", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSAT_naive.setText(QtGui.QApplication.translate("MainWindow", "SAT (naive)", None, QtGui.QApplication.UnicodeUTF8))
        self.actionGenerate.setText(QtGui.QApplication.translate("MainWindow", "Generate formula", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSubformulas.setText(QtGui.QApplication.translate("MainWindow", "Subformulas", None, QtGui.QApplication.UnicodeUTF8))

