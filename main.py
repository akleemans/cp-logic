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
            
    def menu_to_nnf(self):
        formula = self.lineEdit.text()
        formula = 'nnf(' + formula + ')'
        self.lineEdit.setText(formula)
        print 'Menu: to_nnf()'
        
    def menu_dchains(self):
        formula = self.lineEdit.text()
        formula = 'dchains(' + formula + ')'
        self.lineEdit.setText(formula)
        print 'Menu: to_dchains()'

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = MyApplication()
    window.show()
    sys.exit(app.exec_())
