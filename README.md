cp-logic
========

Some tools for classical propositional logic - my bachelor thesis.

## Prerequisites
* Python 2.7
* [Pyside](http://qt-project.org/wiki/PySideDownloads), the QT library for Python
* [Pygame](http://www.pygame.org/download.shtml)

Note: For Ubuntu, simply enter

    sudo add-apt-repository ppa:pyside
    sudo apt-get update
    sudo apt-get install python-pyside

to install Pyside and

    sudo apt-get install python-pygame

to install Pygame.
For other OS see the link above (binary libraries for Windows, MAC and Linux are provided).

## Getting started
To get started, just enter

    python main.py

in the directory containing the Python code.
If you're using multiple versions of Python, you may specify the version by entering

    python2.7 main.py

You should then see a window open like this (depending on your operating system):
![](https://raw.github.com/captainfox/cp-logic/master/toolbox.png?login=captainfox&token=7ebb4cd1faeb4ee5c28e1fe7605bbbbd)

You can now enter one of the examples or test

## Examples

When entering a formula, you can enter either in plain ASCII or copy-paste Unicode.
The tokens you can use are listed here:

| ASCII token  | symbol | meaning                                                             |
|:-------------|:-------|:--------------------------------------------------------------------|
| `p0`         |  p₀    | A basic proposition. Must contain an index number.                  |
| `AND`        |  ∧     | logical AND                                                         |
| `OR`         |  ∨     | logical OR                                                          |
| `NOT`        |  ¬     | logical NOT                                                         |
| `IMPL`       |  →     | implication                                                         |
| `TOP`        |  ⊤     | TOP (always evaluated as true)                                      |
| `BOTTOM`     |  ⊥     | BOTTOM (always evaluated as false)                                  |
| `( )`        |  ( )   | brackets, can be used to structure the formula                      |
| `A`          |  A     | capital letters always stand for metavariables                      |

### Defining a formula

You can either just enter a formula right away

    p0 AND p1
    p3 OR NOT (p1 AND TOP)

or you can make an assignment to a so-called meta-variable.
You can use the capital letters A-Z for storing formulas.

    A = NOT p0 AND (p1 AND p2 IMPL NOT p1)
    B = p3 OR NOT (p2 AND p4)

Metavariables will always be evaluated first, so you can use them along or even in the middle of other formulas:

    C = A AND NOT B

### Change form

Once you have some formulas stored (or you can also enter them directly), you can change their forms.
For example, the **normal negation** form can be obtained with

    nnf(p0 AND p1 IMPL p2)

which will result in `(¬p₀ ∨ ¬p₁) ∨ p₂`. You can also assign it directly to another variable:

    D = nnf(A OR p2)

For further investigation, it's important to have a binary tree of a given formula.
There's an intern representation of the formulat called `pedantic`, which you can also call explicitly.

    C = pedantic(B)

The **conjunctive normal** form you get with

    cnf(D)

Here too you can use the 'form-modifiers' directly in the middle of a formula, they will be evaluated first:

    C = cnf(A) OR NOT nnf(NOT B OR p0)

### Apply a function

For a simple satisfiability test, use

    sat(A)

which will return if A is satisfiable and if yes, which valuation it satisfies.

For the clause set (which will be obtained through CNF) enter

    clause_set(A)

which will provide the corresponding set in set notation.
For the length, enter

    length(A)

and the elements of the formula will be counted and shown as an integer.

Formulas can also be divided and subdivided in their subformulas.
For a given formula, all subformulas are shown using

    sufo(B)

Note that here and also with other functions, the result of the function strongly depends on the form of the formula.
For example

    sufo(p0 IMPL p1)

and

    sufo(nnf(p0 IMPL p1))

will result in a different set of subformulas.

If you want to evaluate how a certain formula without propositions evaluates, you can simply enter

    evaluate(⊤ ∧ ( ⊥ ∨ ⊥ ))

which will then be resolved to a single `True` or `False`-Value.

For a representation that you can copy-paste into LaTeX, use the `latex`-command:

    latex(C)

### Resolution

For checking which clauses belong to a formula, you can enter

    clause_set(A)

to get all clauses corresponding to the formula A.
You can also apply resolution directly:

    resolution(A)

The program will then, according to the rules of resolution, try to generate the empty set.
The sets will be shown, and also if the empty set could be found (which means the formula is not satisfiable) or not (formula satisfiable).

### Deduction chains

For building up series of deduction chains, short dchains, you can use the command

    dchains(A, B, C, ...)

where A, B and C are metavariables or formulas, entered directly. The system will provide a graphical output similar to this one:

![1](../blob/master/tree.png?raw=true)
![2](../master/tree.png?raw=true)
![3](https://raw.github.com/captainfox/cp-logic/master/tree.png)

Click on a node for more information, which chain exactly the node is representing.

The color of each node represents wether the underlying chain is an axiom or not:
 * **red**: chain is not an axiom
 * **blue**: chain is the *identity*-axiom of PSC
 * **green**: chain is the *true*-axiom of PSC
 * **black**: undefined

### Nesting

Functions are nestable to the first degree.
If a function is specified with a certain form (cnf, nnf, pedantic) it will be resolved first before the function is applied.

    length(nnf(A))
    sufo(cnf(A))
    latex(pedantic(A))

## Documentation

### Available Functions

| function       | meaning                                                                      |
|:---------------|:-----------------------------------------------------------------------------|
| `length()`     | Returns the length of a given formula                                        |
| `sufo()`       | Returns all subformulas from a given formula                                 |
| `latex()`      | Returns a latex representation of a given formula                            |
| `pedantic()`   | Returns a pedantic (binary) representation of a given formula                |
| `nnf()`        | Returns a formula in negation normal form                                    |
| `cnf()`        | Returns a formula in conjunctive normal form                                 |
| `sat()`        | Returns, if possible, a valid valuation for the given formula                |
| `clause_set()` | Calculates the corresponding clause set for a given formula                  |
| `evaluate()`   | Evaluate a formula (without propositions)                                    |
| `resolution()` | Apply resolution                                                             |
| `dchains()`    | Use D-chains to prove formula                                                |

### UML
![](https://raw.github.com/captainfox/cp-logic/master/UML.png)

### Tests
To run the tests provided, enter

    python tests.py
