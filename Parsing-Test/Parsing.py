"""
NAME         |TUTORIAL| EASE-OF-USE | FEATURES | TIME 100 | IMP_T 
-------------|--------|-------------|----------|----------|-------
canopy       |   +    |     +       |    +     |  +  006  | .001  
lark         |   0    |     0       |    +     |  0  017  | .037  
funcparserlib|   +    |     -       |    0     |  0  018  | .002  
parse        |   +    |     +       |    -     |  +  002  | .005  
                                                                  
TextX        |   +    |     0       |    0     |  -  032  | .220  
PyLery       |   -    |     -       |    +     |  +  001  | .012  
pe           |   0    |     +       |    -     |  -  023  | .022  
tatsu       *|   0    |     0       |    0     |  -  345  | .038  
parsimonious |   -    |     +       |    0     |  +  001  | .030  
parsy        |   +    |     +       |    -     |  +  003  | .002  
textparser   |   0    |     0       |    -     |  +  002  | .001  
pyparsing    |   -    |     0       |    0     |  +  002  | .022  
                                                                  
parsec       |   -    |     0       |    0     |  0  018  | .001  
Ply          |   -    |     -       |    0     |  +  002  | .008  
reparse      |   -    |     0       |    -     |          | .002  
Arpeggio     |   -    |     0       |    0     |  -  045  | .002  

Antlr
PyPEG
"""

"""
Canopy:
    With adding the generated module to code we can save importing time
    :
    using `` will make grammer case insensetive
    add @ before to mute
    use / for or (ordered or)
    use & before to check the next expr without consuming it
    use ! before to not match next expr

Lark:
    Complicated Tutorial and Hard to learn
    So many features

funcparserlib:
    a bit hard to learn and use
    seems to be only good for mathematical operations

parse:
    reverse of "format" built-in function
    not much features (it's hard to implement indentation parts of code)

TextX:
    Robot Example
    Messy Tutorial

PyLery:
    + time/features
    - usage/tutorial
    (json creator)

PE:
    better syntax for regex but not enough features

Parsimonious:
    just peg
    bad tutorial

Parsy:
    not enough features
    fastest parser


"""






import time
import rx7 as rx
from pprint import pprint
rx.cls()
t = rx.record()
# t = time.time
# t = time.perf_counter

















from parsy import regex, seq, string
t.lap()
year = regex("[0-9]{4}").map(int).desc("4 digit year")
month = regex("[0-9]{2}").map(int).desc("2 digit month")
day = regex("[0-9]{2}").map(int).desc("2 digit day")
dash = string("-")

fulldate = seq(year, dash, month, dash, day)

t = rx.record()
for i in range(100):
    fulldate.parse("2017-02-01")




















t.lap()
print()
print(t)