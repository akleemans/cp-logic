cp-logic
========

Some tools for classical propositional logic - my bachelor thesis.

## Examples

    nnf(p0 AND p1 IMPL p2)
    sat(p0 AND NOT (p0 AND p1))

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



## Todo
### Up next
* Design mockup
* 

### Further stuff


## Arbeit
* Doku (UML, Klassenbeschreibungen, Algorithmen)
* Design / Mockup / Printscreens
* User tests
* Performance tests
