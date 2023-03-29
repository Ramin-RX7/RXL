"""
Grammer is PEG type.
$ canopy "grammer.peg" --lang python

  import grammer
  grammer.parse(text)
    => returns tree[nodes]
 - Accessing to nodes:
    tree.elements[x].text
    # each element can have more nodes it self
    tree.rule_name.text
    # it can goes deeper
 - Comments start with "#"
 - Case-Insensitive strings are between ``
 - Regex (out of strings):  . [] ? + * {n}{n,m}{n,}
 - Labelled Nodes (Named):  name:expr  ::  makes new node named "name" in tree (not in elements)
    (all referenced rules also make nodes in tree)
 - Add "@" before expr to mute it
 - To make ordered-or: "/"
 - To check but not consume: "&" before expr
     "!" before expr to match anything but expr
 - Actions:
      grammer:
          %func_name after a rule
      python:
          class Actions:
            def func_name(self,input, start, end, elements):
              return ...   #int(elements[0])+int(elements[2])
          parse(...,actions=Actions())
      #Extensions:
        (Adds methods to tree)
        grammer:
            root  <-  named_one:"foo" named_two:"bar" <Extension>
        python:
            class Types:
              class Extension(object):
                def convert(self):
                  return ...    #int(self.named_one.text) + int(self.named_two)
            tree.parse(..., types=Types).convert()
"""


# from lib2to3.pgen2 import grammar
import time
import rx7 as rx
from pprint import pprint





rx.cls()
# t = time.time
# t = time.perf_counter
t = rx.record()



import Grammar
from Grammar import *



source = [
    "include raminrx",
    "load adsf",
    "array  [adsf:asdf]<asdf>",

    "const myx =    help",
    "until myx: ",
    "    unless   help    :",
]
grammars = [Include,Load,Array,Const,Until,Unless]

for i,line in enumerate(source):
    for j,grmr in enumerate(grammars):
        try:
            a = Grammar.parse(line,grmr)
        except:
            pass# print("Error")
        else:
            print("\n")
            print(i,j)
            for k in a.elements:
                print(k.text, end="|")
















t.lap()
print()
print(t)
