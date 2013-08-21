cp-logic
========

Some tools for classical propositional logic - my bachelor thesis.

## Prerequisites
* Python 2.7
* [Pyside](http://qt-project.org/wiki/PySideDownloads), the QT library for Python

## Getting started
To get started, just enter

    python main.py

in the directory containing the Python code.
If you're using multiple versions of Python, you may specify the version by entering

    python2.7 main.py

You should then see a window open like this (depending on your operating system):
[[toolbox.png]]

You can now enter one of the examples or test

## Examples

    p0 AND p1
    nnf(p0 AND p1 IMPL p2)
    A = p0 OR p1 OR NOT (p2 AND NOT p3)
    sat(A)
    l(A)
    B = NOT p0 AND NOT p1 IMPL (p2 OR NOT p3)
    nnf(B)
    sufo(B)
    C = p0 AND p1 AND p2 AND NOT p3 AND NOT p4 AND p5
    pedantic(C)
    latex(C)
    sat(p0 AND NOT p1)

## Documentation

### Formula-Class
* `l()`: Returns the length of a given formula
* `sufo()`: Returns all subformulas from a given formula
* `latex()`: Returns a latex representation of a given formula
* `pedantic()`: Returns a pedantic (binary) representation of a given formula
* `nnf()`: Returns a formula in negation normal form
* `cnf()`: Returns a formula in conjunctive normal form

### Tools-Class
* `sat()`: Returns, if possible, a valid valuation for the given formula
* `dchains()`: Use D-chains to prove formula
* `resolution()`: Apply resolution

### UML


### Examples
To start the tests, enter

    python tests.py
