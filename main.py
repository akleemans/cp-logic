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

class MyApplication(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyApplication, self).__init__(parent)
        self.setupUi(self)
        self.count = 0
        #self.listWidget.addItem(u'\u0393\u2080: p\u2080 ∧ p\u2081 ∧ (¬ p\u2082 ∨ ⊥)\n\u0393\u2081: p\u2080 ∧ p\u2081 , ¬ p\u2082 ∨ ⊥\n\u0393\u2082: ...')
        welcome = '''Welcome to cp-logic! Try entering something like this:
p0 AND (NOT p1 OR p2)
A = p0 OR p1 IMPL p2 AND p0
l(A)
---------------------------------------------
'''
        self.listWidget.addItem(welcome)
        self.formulas = []
        
    def buttonPressed(self):
        entry = ''
        text = self.lineEdit.text()
        parts = text.split('(')
        functions = ['l', 'sufo', 'nnf', 'cnf']
        function = ''
        name = '_anon'
        
        if parts[0] in functions:                       # function
            function = parts[0]
            formula = text[text.find('(')+1:-1]
        else:
            parts = self.lineEdit.text().split('=')     # assignment
            if len(parts) == 1:
                formula = parts[0]
            elif len(parts) == 2:
                name = parts[0].strip()
                formula = parts[1].strip()
            else:
                entry = '[Error: Only one "=" allowed]'
        
        # analyze formula
        if len(formula) == 1:
            for f in self.formulas:
                if f.name == formula:
                    name = formula
                    formula = f.formula
                    break
            if function == '': self.listWidget.addItem(formula)
        else:
            try:
                f = Formula(formula, name)
            except FormulaInvalidError, e:
                entry = '[Error: ' + e.value + ']'
            else:
                formula = f.formula
                if name != '_anon':
                    # check if variable already exists
                    for i in range(len(self.formulas)):
                        if self.formulas[i].name == name:
                            del self.formulas[i]
                    self.formulas.append(f)
                    entry = name + ' = ' + formula
                else:
                    if function == '': entry = formula
        
        # function
        if name == '_anon':
            name = formula
        if function != '':
            if function == 'l':
                entry = 'l(' + name + ') = ' + str(f.length())
            #elif function == 'sufo':
            #    ...
        
        self.listWidget.addItem('[' + str(self.count) + '] ' + entry)
        self.count += 1
            
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
