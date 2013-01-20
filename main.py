#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on 17.01.2013

@author: adrianus
'''

import sys
from PySide.QtGui import *
from PySide.QtCore import *
from gui import *
from formula import *
#from exceptions import FormulaInvalidError

class MyApplication(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyApplication, self).__init__(parent)
        self.setupUi(self)
        self.listWidget.addItem(u'\u0393\u2080: p\u2080 ∧ p\u2081 ∧ (¬ p\u2082 ∨ ⊥)\n\u0393\u2081: p\u2080 ∧ p\u2081 , ¬ p\u2082 ∨ ⊥\n\u0393\u2082: ...')

    def buttonPressed(self):
        formula = self.lineEdit.text()
        try:
            f = Formula(formula)
        except FormulaInvalidError, e:
            self.listWidget.addItem('[Error: ' + e.value + ']')
        else:
            print f.formula
            self.listWidget.addItem(f.formula)
            
    def menu_loadformula(self):
        raise NotImplementedError
            
    def menu_nnf(self):
        self.lineEdit.setText('nnf(' + self.lineEdit.text() + ')')
        
    def menu_dchains(self):
        self.lineEdit.setText('dchains(' + self.lineEdit.text() + ')')
        
    def menu_cnf(self):
        self.lineEdit.setText('cnf(' + self.lineEdit.text() + ')')
        
    def menu_length(self):
        self.lineEdit.setText('l(' + self.lineEdit.text() + ')')
        
    def menu_generate(self):
        self.lineEdit.setText('generate(' + self.lineEdit.text() + ')')
        
    def menu_sat(self):
        self.lineEdit.setText('sat(' + self.lineEdit.text() + ')')
        
    def menu_sufo(self):
        self.lineEdit.setText('sufo(' + self.lineEdit.text() + ')')
        
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = MyApplication()
    window.show()
    sys.exit(app.exec_())
