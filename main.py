#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Main class for the cp-logic package.
Loads the UI and the formula class.

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
        self.listWidget.addItem('Welcome to cp-logic! Try entering something like this (double-click on entry):')
        self.listWidget.addItem('p0 AND (NOT p1 OR p2)')
        #self.listWidget.addItem('A = p0 OR p1 IMPL p2 AND p0')
        #self.listWidget.addItem('l(A)')
        #self.listWidget.addItem('B = (NOT p0 AND p1) AND (p0 OR p2) OR (NOT p2 AND p3)')
        #self.listWidget.addItem('sat(B)')
        self.listWidget.addItem('----------------------------------------------------------------------------------')
        self.formulas = []
        
    def entry_clicked(self, b):
        text = b.text()
        if text.find(']') != -1:
            text = text.split('] ')[1]
        self.lineEdit.setText(text.replace('>', '').strip())
        
    def build_formula(self, formula, name):
        ''' Returns formula, if existing, else builds a new one '''
        if len(formula) == 1:
            for f in self.formulas:
                if f.name == formula:
                    return f
            raise ValueError
        else: # build new formula
            try:
                f = Formula(formula, name)
            except FormulaInvalidError, e:
                return '[Error: ' + e.value + ']'
            else:
                formula = f.formula
                if name != '_anon': # check if variable already exists
                    for i in range(len(self.formulas)):
                        if self.formulas[i].name == name:
                            del self.formulas[i]
                    self.formulas.append(f)

            return f
    
    def analyze_input(self, text):
        functions = ['l', 'sufo', 'nnf', 'cnf', 'sat', 'latex', 'pedantic']
        anon = '_anon'
        
        if text.split('(')[0] in functions:             # function
            function = text.split('(')[0]
            formula = text[text.find('(')+1:-1]
            try:
                f = self.build_formula(formula, '_anon')
            except ValueError, e:
               return '[Error: meta-variable ' + formula + ' not found]'
            
            # length
            if function == 'l':
                name = f.name
                if name == anon: name = f.formula
                return 'l(' + name + ') = ' + str(f.length())
                
            # sat
            elif function == 'sat':
                try:
                    satisfiable = f.sat()
                except AttributeError, e:
                    return '[Error: formula invalid]'
                except FormulaInvalidError, e:
                    return '[Error: ' + e.value + ']'
                except TimeOutError, e:
                    return '[Error: ' + e.value + ']'
                
                if satisfiable[0]: s = 'satisfiable with ' +  ', '.join(x for x in satisfiable[1])
                else: s = 'not satisfiable'
                name = f.name
                if name == anon: name = f.formula
                #return 'sat(' + name + ') is ' + s
                return '...is ' + s
                
            # latex
            elif function == 'latex':
                name = f.name
                if name == anon: name = f.formula
                return f.latex()
                
            # pedantic
            elif function == 'pedantic':
                name = f.name
                if name == anon: name = f.formula
                return f.formula_pedantic
            
            # nnf
            elif function == 'nnf':
                name = f.name
                if name == anon: name = f.formula
                return f.formula_nnf
                
            # sufo
            elif function == 'sufo':
                name = f.name
                if name == anon: name = f.formula
                subformulas = f.sufo()
                return 'Found the following ' + str(len(subformulas)) +' subformulas:\n' + '\n'.join(subformulas)
            # ...
                
        elif text.find('=') != -1:                      # assignment
            parts = text.split('=')
            name = parts[0].strip()
            formula = parts[1].strip()
            f = self.build_formula(formula, name)
            if isinstance(f, basestring): 
                return f
            else:
                return name + ' = ' + f.formula
        
        else:                                           # plain formula
        
            try:
                f = self.build_formula(text, '_anon')
            except ValueError, e:
               return '[Error: meta-variable ' + text + ' not found]'
                
            if isinstance(f, basestring): 
                return f
            else:
                return f.formula
    
    def buttonPressed(self):
        entry = ''
        text = self.lineEdit.text()
        self.listWidget.addItem('>> ' + text)
        
        entry = self.analyze_input(text)
        
        self.listWidget.addItem('[' + str(self.count) + ']   ' + entry)
        self.listWidget.addItem('')
        self.listWidget.scrollToBottom()
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
        self.lineEdit.setText('generate(10)')
        
    def menu_sat(self):
        self.lineEdit.setText('sat(' + self.lineEdit.text() + ')')
        
    def menu_sufo(self):
        self.lineEdit.setText('sufo(' + self.lineEdit.text() + ')')
        
    def menu_latex(self):
        self.lineEdit.setText('latex(' + self.lineEdit.text() + ')')
    
    def menu_pedantic(self):
        self.lineEdit.setText('pedantic(' + self.lineEdit.text() + ')')
        
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = MyApplication()
    window.show()
    sys.exit(app.exec_())
