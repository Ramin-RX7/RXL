"""
in all "TreeNodeN".init:: super(...) can be changed to TreeNode(...)
"""

__all__ = ["Load","Include","Until","Unless","Const","Array",
           "C_Check","C_Cmd", "C_Call", "C_Clear"]

from collections import defaultdict
import re



FAILURE = object()
class TreeNode(object):
    def __init__(self, text, offset, elements):
        self.text = text
        self.offset = offset
        self.elements = elements
    def __iter__(self):
        for el in self.elements:
            yield el
class ParseError(SyntaxError): pass
def format_error(input, offset, expected):
    lines = input.split('\n')
    line_no, position = 0, 0
    while position <= offset:
        position += len(lines[line_no]) + 1
        line_no += 1

    line = lines[line_no - 1]
    message = 'Line ' + str(line_no) + ': expected one of:\n\n'

    for pair in expected:
        message += '    - ' + pair[1] + ' from ' + pair[0] + '\n'

    number = str(line_no)
    while len(number) < 6:
        number = ' ' + number

    message += '\n' + number + ' | ' + line + '\n'
    message += ' ' * (len(line) + 10 + offset - position)
    return message + '^'
def parse(input,grammar, actions=None, types=None):
    class Parser(grammar.Grammar):
        def __init__(self, input, actions, types):
            self._input = input
            self._input_size = len(input)
            self._actions = actions
            self._types = types
            self._offset = 0
            self._cache = defaultdict(dict)
            self._failure = 0
            self._expected = []

        def parse(self):
            tree = eval(f"self._read_{grammar.__name__.lower()}()")
            if tree is not FAILURE and self._offset == self._input_size:
                return tree
            if not self._expected:
                self._failure = self._offset
                self._expected.append((grammar.__name__, '<EOF>'))
            raise ParseError(format_error(self._input, self._failure, self._expected))

    parser = Parser(input, actions, types)
    return parser.parse()






class Grammar_Base:
    def _read_spaces(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['spaces'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1, elements0, address1 = self._offset, [], None
        while True:
            chunk0, max0 = None, self._offset + 1
            if max0 <= self._input_size:
                chunk0 = self._input[self._offset:max0]
            if chunk0 == ' ':
                address1 = TreeNode(self._input[self._offset:self._offset + 1], self._offset, [])
                self._offset = self._offset + 1
            else:
                address1 = FAILURE
                if self._offset > self._failure:
                    self._failure = self._offset
                    self._expected = []
                if self._offset == self._failure:
                    self._expected.append(('Grammar_Base::spaces', '" "'))
            if address1 is not FAILURE:
                elements0.append(address1)
            else:
                break
        if len(elements0) >= 0:
            address0 = TreeNode(self._input[index1:self._offset], index1, elements0)
            self._offset = self._offset
        else:
            address0 = FAILURE
        self._cache['spaces'][index0] = (address0, self._offset)
        return address0

    def _read_s(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['s'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1, elements0, address1 = self._offset, [], None
        while True:
            chunk0, max0 = None, self._offset + 1
            if max0 <= self._input_size:
                chunk0 = self._input[self._offset:max0]
            if chunk0 == ' ':
                address1 = TreeNode(self._input[self._offset:self._offset + 1], self._offset, [])
                self._offset = self._offset + 1
            else:
                address1 = FAILURE
                if self._offset > self._failure:
                    self._failure = self._offset
                    self._expected = []
                if self._offset == self._failure:
                    self._expected.append(('CONST::s', '" "'))
            if address1 is not FAILURE:
                elements0.append(address1)
            else:
                break
        if len(elements0) >= 0:
            address0 = TreeNode(self._input[index1:self._offset], index1, elements0)
            self._offset = self._offset
        else:
            address0 = FAILURE
        self._cache['s'][index0] = (address0, self._offset)
        return address0

    Var_beginning = re.compile('^[a-zA-Z_]')
    Var_rest      = re.compile('^[a-zA-Z0-9_]')




class Load:

    class TreeNode1(TreeNode):
        def __init__(self, text, offset, elements):
            super(Load.TreeNode1, self).__init__(text, offset, elements)
            self.s = elements[3]
            self.pkgs = elements[2]
            self.pkg_names = elements[2]


    class TreeNode2(TreeNode):
        def __init__(self, text, offset, elements):
            super(Load.TreeNode2, self).__init__(text, offset, elements)
            self.pkg_name = elements[0]


    class TreeNode3(TreeNode):
        def __init__(self, text, offset, elements):
            super(TreeNode3, self).__init__(text, offset, elements)
            self.s = elements[2]
            self.pkg_name = elements[3]



    class Grammar(Grammar_Base,object):
        REGEX_1 = re.compile('^[a-zA-Z_]')
        REGEX_2 = re.compile('^[a-zA-Z0-9_]')

        def _read_load(self):
            address0, index0 = FAILURE, self._offset
            cached = self._cache['load'].get(index0)
            if cached:
                self._offset = cached[1]
                return cached[0]
            index1, elements0 = self._offset, []
            address1 = FAILURE
            chunk0, max0 = None, self._offset + 5
            if max0 <= self._input_size:
                chunk0 = self._input[self._offset:max0]
            if chunk0 == 'load ':
                address1 = TreeNode(self._input[self._offset:self._offset + 5], self._offset, [])
                self._offset = self._offset + 5
            else:
                address1 = FAILURE
                if self._offset > self._failure:
                    self._failure = self._offset
                    self._expected = []
                if self._offset == self._failure:
                    self._expected.append(('LOAD::load', '"load "'))
            if address1 is not FAILURE:
                elements0.append(address1)
                address2 = FAILURE
                address2 = self._read_s()
                if address2 is not FAILURE:
                    elements0.append(address2)
                    address3 = FAILURE
                    address3 = self._read_pkg_names()
                    if address3 is not FAILURE:
                        elements0.append(address3)
                        address4 = FAILURE
                        address4 = self._read_s()
                        if address4 is not FAILURE:
                            elements0.append(address4)
                        else:
                            elements0 = None
                            self._offset = index1
                    else:
                        elements0 = None
                        self._offset = index1
                else:
                    elements0 = None
                    self._offset = index1
            else:
                elements0 = None
                self._offset = index1
            if elements0 is None:
                address0 = FAILURE
            else:
                address0 = Load.TreeNode1(self._input[index1:self._offset], index1, elements0)
                self._offset = self._offset
            self._cache['load'][index0] = (address0, self._offset)
            return address0

        def _read_pkg_names(self):
            address0, index0 = FAILURE, self._offset
            cached = self._cache['pkg_names'].get(index0)
            if cached:
                self._offset = cached[1]
                return cached[0]
            index1, elements0 = self._offset, []
            address1 = FAILURE
            address1 = self._read_pkg_name()
            if address1 is not FAILURE:
                elements0.append(address1)
                address2 = FAILURE
                index2, elements1, address3 = self._offset, [], None
                while True:
                    index3, elements2 = self._offset, []
                    address4 = FAILURE
                    address4 = self._read_s()
                    if address4 is not FAILURE:
                        elements2.append(address4)
                        address5 = FAILURE
                        chunk0, max0 = None, self._offset + 1
                        if max0 <= self._input_size:
                            chunk0 = self._input[self._offset:max0]
                        if chunk0 == ',':
                            address5 = TreeNode(self._input[self._offset:self._offset + 1], self._offset, [])
                            self._offset = self._offset + 1
                        else:
                            address5 = FAILURE
                            if self._offset > self._failure:
                                self._failure = self._offset
                                self._expected = []
                            if self._offset == self._failure:
                                self._expected.append(('LOAD::pkg_names', '","'))
                        if address5 is not FAILURE:
                            elements2.append(address5)
                            address6 = FAILURE
                            address6 = self._read_s()
                            if address6 is not FAILURE:
                                elements2.append(address6)
                                address7 = FAILURE
                                address7 = self._read_pkg_name()
                                if address7 is not FAILURE:
                                    elements2.append(address7)
                                else:
                                    elements2 = None
                                    self._offset = index3
                            else:
                                elements2 = None
                                self._offset = index3
                        else:
                            elements2 = None
                            self._offset = index3
                    else:
                        elements2 = None
                        self._offset = index3
                    if elements2 is None:
                        address3 = FAILURE
                    else:
                        address3 = TreeNode3(self._input[index3:self._offset], index3, elements2)
                        self._offset = self._offset
                    if address3 is not FAILURE:
                        elements1.append(address3)
                    else:
                        break
                if len(elements1) >= 0:
                    address2 = TreeNode(self._input[index2:self._offset], index2, elements1)
                    self._offset = self._offset
                else:
                    address2 = FAILURE
                if address2 is not FAILURE:
                    elements0.append(address2)
                else:
                    elements0 = None
                    self._offset = index1
            else:
                elements0 = None
                self._offset = index1
            if elements0 is None:
                address0 = FAILURE
            else:
                address0 = Load.TreeNode2(self._input[index1:self._offset], index1, elements0)
                self._offset = self._offset
            self._cache['pkg_names'][index0] = (address0, self._offset)
            return address0

        def _read_pkg_name(self):
            address0, index0 = FAILURE, self._offset
            cached = self._cache['pkg_name'].get(index0)
            if cached:
                self._offset = cached[1]
                return cached[0]
            index1, elements0 = self._offset, []
            address1 = FAILURE
            index2, elements1, address2 = self._offset, [], None
            while True:
                chunk0, max0 = None, self._offset + 1
                if max0 <= self._input_size:
                    chunk0 = self._input[self._offset:max0]
                if chunk0 is not None and Load.Grammar.REGEX_1.search(chunk0):
                    address2 = TreeNode(self._input[self._offset:self._offset + 1], self._offset, [])
                    self._offset = self._offset + 1
                else:
                    address2 = FAILURE
                    if self._offset > self._failure:
                        self._failure = self._offset
                        self._expected = []
                    if self._offset == self._failure:
                        self._expected.append(('LOAD::pkg_name', '[a-zA-Z_]'))
                if address2 is not FAILURE:
                    elements1.append(address2)
                else:
                    break
            if len(elements1) >= 1:
                address1 = TreeNode(self._input[index2:self._offset], index2, elements1)
                self._offset = self._offset
            else:
                address1 = FAILURE
            if address1 is not FAILURE:
                elements0.append(address1)
                address3 = FAILURE
                index3, elements2, address4 = self._offset, [], None
                while True:
                    chunk1, max1 = None, self._offset + 1
                    if max1 <= self._input_size:
                        chunk1 = self._input[self._offset:max1]
                    if chunk1 is not None and Grammar.REGEX_2.search(chunk1):
                        address4 = TreeNode(self._input[self._offset:self._offset + 1], self._offset, [])
                        self._offset = self._offset + 1
                    else:
                        address4 = FAILURE
                        if self._offset > self._failure:
                            self._failure = self._offset
                            self._expected = []
                        if self._offset == self._failure:
                            self._expected.append(('LOAD::pkg_name', '[a-zA-Z0-9_]'))
                    if address4 is not FAILURE:
                        elements2.append(address4)
                    else:
                        break
                if len(elements2) >= 0:
                    address3 = TreeNode(self._input[index3:self._offset], index3, elements2)
                    self._offset = self._offset
                else:
                    address3 = FAILURE
                if address3 is not FAILURE:
                    elements0.append(address3)
                else:
                    elements0 = None
                    self._offset = index1
            else:
                elements0 = None
                self._offset = index1
            if elements0 is None:
                address0 = FAILURE
            else:
                address0 = TreeNode(self._input[index1:self._offset], index1, elements0)
                self._offset = self._offset
            self._cache['pkg_name'][index0] = (address0, self._offset)
            return address0

        def _read_s(self):
            address0, index0 = FAILURE, self._offset
            cached = self._cache['s'].get(index0)
            if cached:
                self._offset = cached[1]
                return cached[0]
            index1, elements0, address1 = self._offset, [], None
            while True:
                chunk0, max0 = None, self._offset + 1
                if max0 <= self._input_size:
                    chunk0 = self._input[self._offset:max0]
                if chunk0 == ' ':
                    address1 = TreeNode(self._input[self._offset:self._offset + 1], self._offset, [])
                    self._offset = self._offset + 1
                else:
                    address1 = FAILURE
                    if self._offset > self._failure:
                        self._failure = self._offset
                        self._expected = []
                    if self._offset == self._failure:
                        self._expected.append(('LOAD::s', '" "'))
                if address1 is not FAILURE:
                    elements0.append(address1)
                else:
                    break
            if len(elements0) >= 0:
                address0 = TreeNode(self._input[index1:self._offset], index1, elements0)
                self._offset = self._offset
            else:
                address0 = FAILURE
            self._cache['s'][index0] = (address0, self._offset)
            return address0



class Include:

    class TreeNode1(TreeNode):
        def __init__(self, text, offset, elements):
            super(Include.TreeNode1, self).__init__(text, offset, elements)
            self.indent = elements[0]
            self.pkgs = elements[3]


    class TreeNode2(TreeNode):
        def __init__(self, text, offset, elements):
            super(Include.TreeNode2, self).__init__(text, offset, elements)
            self.s = elements[0]
            self.pkg_name = elements[1]


    class TreeNode3(TreeNode):
        def __init__(self, text, offset, elements):
            super(Include.TreeNode3, self).__init__(text, offset, elements)
            self.s = elements[2]
            self.pkg_name = elements[3]


    class Grammar(object):
        REGEX_1 = re.compile('^[a-zA-Z_]')
        REGEX_2 = re.compile('^[a-zA-Z0-9_]')

        def _read_include(self):
            address0, index0 = FAILURE, self._offset
            cached = self._cache['include'].get(index0)
            if cached:
                self._offset = cached[1]
                return cached[0]
            index1, elements0 = self._offset, []
            address1 = FAILURE
            index2 = self._offset
            address1 = self._read_s()
            if address1 is FAILURE:
                address1 = TreeNode(self._input[index2:index2], index2, [])
                self._offset = index2
            if address1 is not FAILURE:
                elements0.append(address1)
                address2 = FAILURE
                chunk0, max0 = None, self._offset + 8
                if max0 <= self._input_size:
                    chunk0 = self._input[self._offset:max0]
                if chunk0 == 'include ':
                    address2 = TreeNode(self._input[self._offset:self._offset + 8], self._offset, [])
                    self._offset = self._offset + 8
                else:
                    address2 = FAILURE
                    if self._offset > self._failure:
                        self._failure = self._offset
                        self._expected = []
                    if self._offset == self._failure:
                        self._expected.append(('INCLUDE::include', '"include "'))
                if address2 is not FAILURE:
                    elements0.append(address2)
                    address3 = FAILURE
                    index3 = self._offset
                    address3 = self._read_s()
                    if address3 is FAILURE:
                        address3 = TreeNode(self._input[index3:index3], index3, [])
                        self._offset = index3
                    if address3 is not FAILURE:
                        elements0.append(address3)
                        address4 = FAILURE
                        index4, elements1 = self._offset, []
                        address5 = FAILURE
                        address5 = self._read_s()
                        if address5 is not FAILURE:
                            elements1.append(address5)
                            address6 = FAILURE
                            address6 = self._read_pkg_name()
                            if address6 is not FAILURE:
                                elements1.append(address6)
                                address7 = FAILURE
                                index5, elements2, address8 = self._offset, [], None
                                while True:
                                    index6, elements3 = self._offset, []
                                    address9 = FAILURE
                                    address9 = self._read_s()
                                    if address9 is not FAILURE:
                                        elements3.append(address9)
                                        address10 = FAILURE
                                        chunk1, max1 = None, self._offset + 1
                                        if max1 <= self._input_size:
                                            chunk1 = self._input[self._offset:max1]
                                        if chunk1 == ',':
                                            address10 = TreeNode(self._input[self._offset:self._offset + 1], self._offset, [])
                                            self._offset = self._offset + 1
                                        else:
                                            address10 = FAILURE
                                            if self._offset > self._failure:
                                                self._failure = self._offset
                                                self._expected = []
                                            if self._offset == self._failure:
                                                self._expected.append(('INCLUDE::include', '","'))
                                        if address10 is not FAILURE:
                                            elements3.append(address10)
                                            address11 = FAILURE
                                            address11 = self._read_s()
                                            if address11 is not FAILURE:
                                                elements3.append(address11)
                                                address12 = FAILURE
                                                address12 = self._read_pkg_name()
                                                if address12 is not FAILURE:
                                                    elements3.append(address12)
                                                else:
                                                    elements3 = None
                                                    self._offset = index6
                                            else:
                                                elements3 = None
                                                self._offset = index6
                                        else:
                                            elements3 = None
                                            self._offset = index6
                                    else:
                                        elements3 = None
                                        self._offset = index6
                                    if elements3 is None:
                                        address8 = FAILURE
                                    else:
                                        address8 = Include.TreeNode3(self._input[index6:self._offset], index6, elements3)
                                        self._offset = self._offset
                                    if address8 is not FAILURE:
                                        elements2.append(address8)
                                    else:
                                        break
                                if len(elements2) >= 0:
                                    address7 = TreeNode(self._input[index5:self._offset], index5, elements2)
                                    self._offset = self._offset
                                else:
                                    address7 = FAILURE
                                if address7 is not FAILURE:
                                    elements1.append(address7)
                                    address13 = FAILURE
                                    index7 = self._offset
                                    chunk2, max2 = None, self._offset + 1
                                    if max2 <= self._input_size:
                                        chunk2 = self._input[self._offset:max2]
                                    if chunk2 == ',':
                                        address13 = TreeNode(self._input[self._offset:self._offset + 1], self._offset, [])
                                        self._offset = self._offset + 1
                                    else:
                                        address13 = FAILURE
                                        if self._offset > self._failure:
                                            self._failure = self._offset
                                            self._expected = []
                                        if self._offset == self._failure:
                                            self._expected.append(('INCLUDE::include', '","'))
                                    if address13 is FAILURE:
                                        address13 = TreeNode(self._input[index7:index7], index7, [])
                                        self._offset = index7
                                    if address13 is not FAILURE:
                                        elements1.append(address13)
                                    else:
                                        elements1 = None
                                        self._offset = index4
                                else:
                                    elements1 = None
                                    self._offset = index4
                            else:
                                elements1 = None
                                self._offset = index4
                        else:
                            elements1 = None
                            self._offset = index4
                        if elements1 is None:
                            address4 = FAILURE
                        else:
                            address4 = Include.TreeNode2(self._input[index4:self._offset], index4, elements1)
                            self._offset = self._offset
                        if address4 is not FAILURE:
                            elements0.append(address4)
                        else:
                            elements0 = None
                            self._offset = index1
                    else:
                        elements0 = None
                        self._offset = index1
                else:
                    elements0 = None
                    self._offset = index1
            else:
                elements0 = None
                self._offset = index1
            if elements0 is None:
                address0 = FAILURE
            else:
                address0 = Include.TreeNode1(self._input[index1:self._offset], index1, elements0)
                self._offset = self._offset
            self._cache['include'][index0] = (address0, self._offset)
            return address0

        def _read_s(self):
            address0, index0 = FAILURE, self._offset
            cached = self._cache['s'].get(index0)
            if cached:
                self._offset = cached[1]
                return cached[0]
            index1, elements0, address1 = self._offset, [], None
            while True:
                chunk0, max0 = None, self._offset + 1
                if max0 <= self._input_size:
                    chunk0 = self._input[self._offset:max0]
                if chunk0 == ' ':
                    address1 = TreeNode(self._input[self._offset:self._offset + 1], self._offset, [])
                    self._offset = self._offset + 1
                else:
                    address1 = FAILURE
                    if self._offset > self._failure:
                        self._failure = self._offset
                        self._expected = []
                    if self._offset == self._failure:
                        self._expected.append(('INCLUDE::s', '" "'))
                if address1 is not FAILURE:
                    elements0.append(address1)
                else:
                    break
            if len(elements0) >= 0:
                address0 = TreeNode(self._input[index1:self._offset], index1, elements0)
                self._offset = self._offset
            else:
                address0 = FAILURE
            self._cache['s'][index0] = (address0, self._offset)
            return address0

        def _read_pkg_name(self):
            address0, index0 = FAILURE, self._offset
            cached = self._cache['pkg_name'].get(index0)
            if cached:
                self._offset = cached[1]
                return cached[0]
            index1, elements0 = self._offset, []
            address1 = FAILURE
            index2, elements1, address2 = self._offset, [], None
            while True:
                chunk0, max0 = None, self._offset + 1
                if max0 <= self._input_size:
                    chunk0 = self._input[self._offset:max0]
                if chunk0 is not None and Include.Grammar.REGEX_1.search(chunk0):
                    address2 = TreeNode(self._input[self._offset:self._offset + 1], self._offset, [])
                    self._offset = self._offset + 1
                else:
                    address2 = FAILURE
                    if self._offset > self._failure:
                        self._failure = self._offset
                        self._expected = []
                    if self._offset == self._failure:
                        self._expected.append(('INCLUDE::pkg_name', '[a-zA-Z_]'))
                if address2 is not FAILURE:
                    elements1.append(address2)
                else:
                    break
            if len(elements1) >= 1:
                address1 = TreeNode(self._input[index2:self._offset], index2, elements1)
                self._offset = self._offset
            else:
                address1 = FAILURE
            if address1 is not FAILURE:
                elements0.append(address1)
                address3 = FAILURE
                index3, elements2, address4 = self._offset, [], None
                while True:
                    chunk1, max1 = None, self._offset + 1
                    if max1 <= self._input_size:
                        chunk1 = self._input[self._offset:max1]
                    if chunk1 is not None and Include.Grammar.REGEX_2.search(chunk1):
                        address4 = TreeNode(self._input[self._offset:self._offset + 1], self._offset, [])
                        self._offset = self._offset + 1
                    else:
                        address4 = FAILURE
                        if self._offset > self._failure:
                            self._failure = self._offset
                            self._expected = []
                        if self._offset == self._failure:
                            self._expected.append(('INCLUDE::pkg_name', '[a-zA-Z0-9_]'))
                    if address4 is not FAILURE:
                        elements2.append(address4)
                    else:
                        break
                if len(elements2) >= 0:
                    address3 = TreeNode(self._input[index3:self._offset], index3, elements2)
                    self._offset = self._offset
                else:
                    address3 = FAILURE
                if address3 is not FAILURE:
                    elements0.append(address3)
                else:
                    elements0 = None
                    self._offset = index1
            else:
                elements0 = None
                self._offset = index1
            if elements0 is None:
                address0 = FAILURE
            else:
                address0 = TreeNode(self._input[index1:self._offset], index1, elements0)
                self._offset = self._offset
            self._cache['pkg_name'][index0] = (address0, self._offset)
            return address0




class Until:
    class TreeNode1(TreeNode):
        def __init__(self, text, offset, elements):
            super(Until.TreeNode1, self).__init__(text, offset, elements)
            self.indent = elements[0]
            self.expr = elements[3]
            self.rest = elements[5]


    class Grammar(Grammar_Base,object):
        REGEX_1 = re.compile('^[^:]')

        def _read_until(self):
            address0, index0 = FAILURE, self._offset
            cached = self._cache['until'].get(index0)
            if cached:
                self._offset = cached[1]
                return cached[0]
            index1, elements0 = self._offset, []
            address1 = FAILURE
            index2 = self._offset
            address1 = self._read_spaces()
            if address1 is FAILURE:
                address1 = TreeNode(self._input[index2:index2], index2, [])
                self._offset = index2
            if address1 is not FAILURE:
                elements0.append(address1)
                address2 = FAILURE
                chunk0, max0 = None, self._offset + 6
                if max0 <= self._input_size:
                    chunk0 = self._input[self._offset:max0]
                if chunk0 == 'until ':
                    address2 = TreeNode(self._input[self._offset:self._offset + 6], self._offset, [])
                    self._offset = self._offset + 6
                else:
                    address2 = FAILURE
                    if self._offset > self._failure:
                        self._failure = self._offset
                        self._expected = []
                    if self._offset == self._failure:
                        self._expected.append(('UNTIL::until', '"until "'))
                if address2 is not FAILURE:
                    elements0.append(address2)
                    address3 = FAILURE
                    index3 = self._offset
                    address3 = self._read_spaces()
                    if address3 is FAILURE:
                        address3 = TreeNode(self._input[index3:index3], index3, [])
                        self._offset = index3
                    if address3 is not FAILURE:
                        elements0.append(address3)
                        address4 = FAILURE
                        index4, elements1, address5 = self._offset, [], None
                        while True:
                            chunk1, max1 = None, self._offset + 1
                            if max1 <= self._input_size:
                                chunk1 = self._input[self._offset:max1]
                            if chunk1 is not None and Until.Grammar.REGEX_1.search(chunk1):
                                address5 = TreeNode(self._input[self._offset:self._offset + 1], self._offset, [])
                                self._offset = self._offset + 1
                            else:
                                address5 = FAILURE
                                if self._offset > self._failure:
                                    self._failure = self._offset
                                    self._expected = []
                                if self._offset == self._failure:
                                    self._expected.append(('UNTIL::until', '[^:]'))
                            if address5 is not FAILURE:
                                elements1.append(address5)
                            else:
                                break
                        if len(elements1) >= 1:
                            address4 = TreeNode(self._input[index4:self._offset], index4, elements1)
                            self._offset = self._offset
                        else:
                            address4 = FAILURE
                        if address4 is not FAILURE:
                            elements0.append(address4)
                            address6 = FAILURE
                            chunk2, max2 = None, self._offset + 1
                            if max2 <= self._input_size:
                                chunk2 = self._input[self._offset:max2]
                            if chunk2 == ':':
                                address6 = TreeNode(self._input[self._offset:self._offset + 1], self._offset, [])
                                self._offset = self._offset + 1
                            else:
                                address6 = FAILURE
                                if self._offset > self._failure:
                                    self._failure = self._offset
                                    self._expected = []
                                if self._offset == self._failure:
                                    self._expected.append(('UNTIL::until', '":"'))
                            if address6 is not FAILURE:
                                elements0.append(address6)
                                address7 = FAILURE
                                index5, elements2, address8 = self._offset, [], None
                                while True:
                                    if self._offset < self._input_size:
                                        address8 = TreeNode(self._input[self._offset:self._offset + 1], self._offset, [])
                                        self._offset = self._offset + 1
                                    else:
                                        address8 = FAILURE
                                        if self._offset > self._failure:
                                            self._failure = self._offset
                                            self._expected = []
                                        if self._offset == self._failure:
                                            self._expected.append(('UNTIL::until', '<any char>'))
                                    if address8 is not FAILURE:
                                        elements2.append(address8)
                                    else:
                                        break
                                if len(elements2) >= 0:
                                    address7 = TreeNode(self._input[index5:self._offset], index5, elements2)
                                    self._offset = self._offset
                                else:
                                    address7 = FAILURE
                                if address7 is not FAILURE:
                                    elements0.append(address7)
                                else:
                                    elements0 = None
                                    self._offset = index1
                            else:
                                elements0 = None
                                self._offset = index1
                        else:
                            elements0 = None
                            self._offset = index1
                    else:
                        elements0 = None
                        self._offset = index1
                else:
                    elements0 = None
                    self._offset = index1
            else:
                elements0 = None
                self._offset = index1
            if elements0 is None:
                address0 = FAILURE
            else:
                address0 = Until.TreeNode1(self._input[index1:self._offset], index1, elements0)
                self._offset = self._offset
            self._cache['until'][index0] = (address0, self._offset)
            return address0



class Unless:
    class TreeNode1(TreeNode):
        def __init__(self, text, offset, elements):
            super(Unless.TreeNode1, self).__init__(text, offset, elements)
            self.indent = elements[0]
            self.expr = elements[3]
            self.rest = elements[5]


    class Grammar(Grammar_Base,object):
        REGEX_1 = re.compile('^[^:]')

        def _read_unless(self):
            address0, index0 = FAILURE, self._offset
            cached = self._cache['unless'].get(index0)
            if cached:
                self._offset = cached[1]
                return cached[0]
            index1, elements0 = self._offset, []
            address1 = FAILURE
            index2 = self._offset
            address1 = self._read_spaces()
            if address1 is FAILURE:
                address1 = TreeNode(self._input[index2:index2], index2, [])
                self._offset = index2
            if address1 is not FAILURE:
                elements0.append(address1)
                address2 = FAILURE
                chunk0, max0 = None, self._offset + 7
                if max0 <= self._input_size:
                    chunk0 = self._input[self._offset:max0]
                if chunk0 == 'unless ':
                    address2 = TreeNode(self._input[self._offset:self._offset + 7], self._offset, [])
                    self._offset = self._offset + 7
                else:
                    address2 = FAILURE
                    if self._offset > self._failure:
                        self._failure = self._offset
                        self._expected = []
                    if self._offset == self._failure:
                        self._expected.append(('UNLESS::unless', '"unless "'))
                if address2 is not FAILURE:
                    elements0.append(address2)
                    address3 = FAILURE
                    index3 = self._offset
                    address3 = self._read_spaces()
                    if address3 is FAILURE:
                        address3 = TreeNode(self._input[index3:index3], index3, [])
                        self._offset = index3
                    if address3 is not FAILURE:
                        elements0.append(address3)
                        address4 = FAILURE
                        index4, elements1, address5 = self._offset, [], None
                        while True:
                            chunk1, max1 = None, self._offset + 1
                            if max1 <= self._input_size:
                                chunk1 = self._input[self._offset:max1]
                            if chunk1 is not None and Unless.Grammar.REGEX_1.search(chunk1):
                                address5 = TreeNode(self._input[self._offset:self._offset + 1], self._offset, [])
                                self._offset = self._offset + 1
                            else:
                                address5 = FAILURE
                                if self._offset > self._failure:
                                    self._failure = self._offset
                                    self._expected = []
                                if self._offset == self._failure:
                                    self._expected.append(('UNLESS::unless', '[^:]'))
                            if address5 is not FAILURE:
                                elements1.append(address5)
                            else:
                                break
                        if len(elements1) >= 1:
                            address4 = TreeNode(self._input[index4:self._offset], index4, elements1)
                            self._offset = self._offset
                        else:
                            address4 = FAILURE
                        if address4 is not FAILURE:
                            elements0.append(address4)
                            address6 = FAILURE
                            chunk2, max2 = None, self._offset + 1
                            if max2 <= self._input_size:
                                chunk2 = self._input[self._offset:max2]
                            if chunk2 == ':':
                                address6 = TreeNode(self._input[self._offset:self._offset + 1], self._offset, [])
                                self._offset = self._offset + 1
                            else:
                                address6 = FAILURE
                                if self._offset > self._failure:
                                    self._failure = self._offset
                                    self._expected = []
                                if self._offset == self._failure:
                                    self._expected.append(('UNLESS::unless', '":"'))
                            if address6 is not FAILURE:
                                elements0.append(address6)
                                address7 = FAILURE
                                index5, elements2, address8 = self._offset, [], None
                                while True:
                                    if self._offset < self._input_size:
                                        address8 = TreeNode(self._input[self._offset:self._offset + 1], self._offset, [])
                                        self._offset = self._offset + 1
                                    else:
                                        address8 = FAILURE
                                        if self._offset > self._failure:
                                            self._failure = self._offset
                                            self._expected = []
                                        if self._offset == self._failure:
                                            self._expected.append(('UNLESS::unless', '<any char>'))
                                    if address8 is not FAILURE:
                                        elements2.append(address8)
                                    else:
                                        break
                                if len(elements2) >= 0:
                                    address7 = TreeNode(self._input[index5:self._offset], index5, elements2)
                                    self._offset = self._offset
                                else:
                                    address7 = FAILURE
                                if address7 is not FAILURE:
                                    elements0.append(address7)
                                else:
                                    elements0 = None
                                    self._offset = index1
                            else:
                                elements0 = None
                                self._offset = index1
                        else:
                            elements0 = None
                            self._offset = index1
                    else:
                        elements0 = None
                        self._offset = index1
                else:
                    elements0 = None
                    self._offset = index1
            else:
                elements0 = None
                self._offset = index1
            if elements0 is None:
                address0 = FAILURE
            else:
                address0 = Unless.TreeNode1(self._input[index1:self._offset], index1, elements0)
                self._offset = self._offset
            self._cache['unless'][index0] = (address0, self._offset)
            return address0



class Const:
    class TreeNode1(TreeNode):
        def __init__(self, text, offset, elements):
            super(Const.TreeNode1, self).__init__(text, offset, elements)
            self.indent = elements[0]
            self.varname = elements[3]
            self.var = elements[3]
            self.value = elements[7]


    class Grammar(Grammar_Base,object):

        def _read_const(self):
            address0, index0 = FAILURE, self._offset
            cached = self._cache['const'].get(index0)
            if cached:
                self._offset = cached[1]
                return cached[0]
            index1, elements0 = self._offset, []
            address1 = FAILURE
            index2 = self._offset
            address1 = self._read_s()
            if address1 is FAILURE:
                address1 = TreeNode(self._input[index2:index2], index2, [])
                self._offset = index2
            if address1 is not FAILURE:
                elements0.append(address1)
                address2 = FAILURE
                chunk0, max0 = None, self._offset + 6
                if max0 <= self._input_size:
                    chunk0 = self._input[self._offset:max0]
                if chunk0 == 'const ':
                    address2 = TreeNode(self._input[self._offset:self._offset + 6], self._offset, [])
                    self._offset = self._offset + 6
                else:
                    address2 = FAILURE
                    if self._offset > self._failure:
                        self._failure = self._offset
                        self._expected = []
                    if self._offset == self._failure:
                        self._expected.append(('CONST::const', '"const "'))
                if address2 is not FAILURE:
                    elements0.append(address2)
                    address3 = FAILURE
                    index3 = self._offset
                    address3 = self._read_s()
                    if address3 is FAILURE:
                        address3 = TreeNode(self._input[index3:index3], index3, [])
                        self._offset = index3
                    if address3 is not FAILURE:
                        elements0.append(address3)
                        address4 = FAILURE
                        address4 = self._read_var()
                        if address4 is not FAILURE:
                            elements0.append(address4)
                            address5 = FAILURE
                            index4 = self._offset
                            address5 = self._read_s()
                            if address5 is FAILURE:
                                address5 = TreeNode(self._input[index4:index4], index4, [])
                                self._offset = index4
                            if address5 is not FAILURE:
                                elements0.append(address5)
                                address6 = FAILURE
                                chunk1, max1 = None, self._offset + 1
                                if max1 <= self._input_size:
                                    chunk1 = self._input[self._offset:max1]
                                if chunk1 == '=':
                                    address6 = TreeNode(self._input[self._offset:self._offset + 1], self._offset, [])
                                    self._offset = self._offset + 1
                                else:
                                    address6 = FAILURE
                                    if self._offset > self._failure:
                                        self._failure = self._offset
                                        self._expected = []
                                    if self._offset == self._failure:
                                        self._expected.append(('CONST::const', '"="'))
                                if address6 is not FAILURE:
                                    elements0.append(address6)
                                    address7 = FAILURE
                                    index5 = self._offset
                                    address7 = self._read_s()
                                    if address7 is FAILURE:
                                        address7 = TreeNode(self._input[index5:index5], index5, [])
                                        self._offset = index5
                                    if address7 is not FAILURE:
                                        elements0.append(address7)
                                        address8 = FAILURE
                                        index6, elements1, address9 = self._offset, [], None
                                        while True:
                                            if self._offset < self._input_size:
                                                address9 = TreeNode(self._input[self._offset:self._offset + 1], self._offset, [])
                                                self._offset = self._offset + 1
                                            else:
                                                address9 = FAILURE
                                                if self._offset > self._failure:
                                                    self._failure = self._offset
                                                    self._expected = []
                                                if self._offset == self._failure:
                                                    self._expected.append(('CONST::const', '<any char>'))
                                            if address9 is not FAILURE:
                                                elements1.append(address9)
                                            else:
                                                break
                                        if len(elements1) >= 1:
                                            address8 = TreeNode(self._input[index6:self._offset], index6, elements1)
                                            self._offset = self._offset
                                        else:
                                            address8 = FAILURE
                                        if address8 is not FAILURE:
                                            elements0.append(address8)
                                        else:
                                            elements0 = None
                                            self._offset = index1
                                    else:
                                        elements0 = None
                                        self._offset = index1
                                else:
                                    elements0 = None
                                    self._offset = index1
                            else:
                                elements0 = None
                                self._offset = index1
                        else:
                            elements0 = None
                            self._offset = index1
                    else:
                        elements0 = None
                        self._offset = index1
                else:
                    elements0 = None
                    self._offset = index1
            else:
                elements0 = None
                self._offset = index1
            if elements0 is None:
                address0 = FAILURE
            else:
                address0 = Const.TreeNode1(self._input[index1:self._offset], index1, elements0)
                self._offset = self._offset
            self._cache['const'][index0] = (address0, self._offset)
            return address0

        def _read_var(self):
            address0, index0 = FAILURE, self._offset
            cached = self._cache['var'].get(index0)
            if cached:
                self._offset = cached[1]
                return cached[0]
            index1, elements0 = self._offset, []
            address1 = FAILURE
            index2, elements1, address2 = self._offset, [], None
            while True:
                chunk0, max0 = None, self._offset + 1
                if max0 <= self._input_size:
                    chunk0 = self._input[self._offset:max0]
                if chunk0 is not None and self.Var_beginning.search(chunk0):
                    address2 = TreeNode(self._input[self._offset:self._offset + 1], self._offset, [])
                    self._offset = self._offset + 1
                else:
                    address2 = FAILURE
                    if self._offset > self._failure:
                        self._failure = self._offset
                        self._expected = []
                    if self._offset == self._failure:
                        self._expected.append(('CONST::var', '[a-zA-Z_]'))
                if address2 is not FAILURE:
                    elements1.append(address2)
                else:
                    break
            if len(elements1) >= 1:
                address1 = TreeNode(self._input[index2:self._offset], index2, elements1)
                self._offset = self._offset
            else:
                address1 = FAILURE
            if address1 is not FAILURE:
                elements0.append(address1)
                address3 = FAILURE
                index3, elements2, address4 = self._offset, [], None
                while True:
                    chunk1, max1 = None, self._offset + 1
                    if max1 <= self._input_size:
                        chunk1 = self._input[self._offset:max1]
                    if chunk1 is not None and self.Var_rest.search(chunk1):
                        address4 = TreeNode(self._input[self._offset:self._offset + 1], self._offset, [])
                        self._offset = self._offset + 1
                    else:
                        address4 = FAILURE
                        if self._offset > self._failure:
                            self._failure = self._offset
                            self._expected = []
                        if self._offset == self._failure:
                            self._expected.append(('CONST::var', '[a-zA-Z0-9_]'))
                    if address4 is not FAILURE:
                        elements2.append(address4)
                    else:
                        break
                if len(elements2) >= 0:
                    address3 = TreeNode(self._input[index3:self._offset], index3, elements2)
                    self._offset = self._offset
                else:
                    address3 = FAILURE
                if address3 is not FAILURE:
                    elements0.append(address3)
                else:
                    elements0 = None
                    self._offset = index1
            else:
                elements0 = None
                self._offset = index1
            if elements0 is None:
                address0 = FAILURE
            else:
                address0 = TreeNode(self._input[index1:self._offset], index1, elements0)
                self._offset = self._offset
            self._cache['var'][index0] = (address0, self._offset)
            return address0



class Array:
    class TreeNode1(TreeNode):
        def __init__(self, text, offset, elements):
            super(Array.TreeNode1, self).__init__(text, offset, elements)
            self.s = elements[5]
            self.options = elements[3]
            self.values = elements[7]


    class TreeNode2(TreeNode):
        def __init__(self, text, offset, elements):
            super(Array.TreeNode2, self).__init__(text, offset, elements)
            self.type_ = elements[0]
            self.max_length = elements[2]




    class Grammar(object):
        REGEX_1 = re.compile('^[a-zA-Z0-9]')

        def _read_array(self):
            address0, index0 = FAILURE, self._offset
            cached = self._cache['array'].get(index0)
            if cached:
                self._offset = cached[1]
                return cached[0]
            index1, elements0 = self._offset, []
            address1 = FAILURE
            chunk0, max0 = None, self._offset + 6
            if max0 <= self._input_size:
                chunk0 = self._input[self._offset:max0]
            if chunk0 == 'array ':
                address1 = TreeNode(self._input[self._offset:self._offset + 6], self._offset, [])
                self._offset = self._offset + 6
            else:
                address1 = FAILURE
                if self._offset > self._failure:
                    self._failure = self._offset
                    self._expected = []
                if self._offset == self._failure:
                    self._expected.append(('ARRAY::array', '"array "'))
            if address1 is not FAILURE:
                elements0.append(address1)
                address2 = FAILURE
                address2 = self._read_s()
                if address2 is not FAILURE:
                    elements0.append(address2)
                    address3 = FAILURE
                    chunk1, max1 = None, self._offset + 1
                    if max1 <= self._input_size:
                        chunk1 = self._input[self._offset:max1]
                    if chunk1 == '[':
                        address3 = TreeNode(self._input[self._offset:self._offset + 1], self._offset, [])
                        self._offset = self._offset + 1
                    else:
                        address3 = FAILURE
                        if self._offset > self._failure:
                            self._failure = self._offset
                            self._expected = []
                        if self._offset == self._failure:
                            self._expected.append(('ARRAY::array', '"["'))
                    if address3 is not FAILURE:
                        elements0.append(address3)
                        address4 = FAILURE
                        address4 = self._read_options()
                        if address4 is not FAILURE:
                            elements0.append(address4)
                            address5 = FAILURE
                            chunk2, max2 = None, self._offset + 1
                            if max2 <= self._input_size:
                                chunk2 = self._input[self._offset:max2]
                            if chunk2 == ']':
                                address5 = TreeNode(self._input[self._offset:self._offset + 1], self._offset, [])
                                self._offset = self._offset + 1
                            else:
                                address5 = FAILURE
                                if self._offset > self._failure:
                                    self._failure = self._offset
                                    self._expected = []
                                if self._offset == self._failure:
                                    self._expected.append(('ARRAY::array', '"]"'))
                            if address5 is not FAILURE:
                                elements0.append(address5)
                                address6 = FAILURE
                                address6 = self._read_s()
                                if address6 is not FAILURE:
                                    elements0.append(address6)
                                    address7 = FAILURE
                                    chunk3, max3 = None, self._offset + 1
                                    if max3 <= self._input_size:
                                        chunk3 = self._input[self._offset:max3]
                                    if chunk3 == '<':
                                        address7 = TreeNode(self._input[self._offset:self._offset + 1], self._offset, [])
                                        self._offset = self._offset + 1
                                    else:
                                        address7 = FAILURE
                                        if self._offset > self._failure:
                                            self._failure = self._offset
                                            self._expected = []
                                        if self._offset == self._failure:
                                            self._expected.append(('ARRAY::array', '"<"'))
                                    if address7 is not FAILURE:
                                        elements0.append(address7)
                                        address8 = FAILURE
                                        index2, elements1, address9 = self._offset, [], None
                                        while True:
                                            index3, elements2 = self._offset, []
                                            address10 = FAILURE
                                            index4 = self._offset
                                            chunk4, max4 = None, self._offset + 1
                                            if max4 <= self._input_size:
                                                chunk4 = self._input[self._offset:max4]
                                            if chunk4 == '>':
                                                address10 = TreeNode(self._input[self._offset:self._offset + 1], self._offset, [])
                                                self._offset = self._offset + 1
                                            else:
                                                address10 = FAILURE
                                                if self._offset > self._failure:
                                                    self._failure = self._offset
                                                    self._expected = []
                                                if self._offset == self._failure:
                                                    self._expected.append(('ARRAY::array', '">"'))
                                            self._offset = index4
                                            if address10 is FAILURE:
                                                address10 = TreeNode(self._input[self._offset:self._offset], self._offset, [])
                                                self._offset = self._offset
                                            else:
                                                address10 = FAILURE
                                            if address10 is not FAILURE:
                                                elements2.append(address10)
                                                address11 = FAILURE
                                                if self._offset < self._input_size:
                                                    address11 = TreeNode(self._input[self._offset:self._offset + 1], self._offset, [])
                                                    self._offset = self._offset + 1
                                                else:
                                                    address11 = FAILURE
                                                    if self._offset > self._failure:
                                                        self._failure = self._offset
                                                        self._expected = []
                                                    if self._offset == self._failure:
                                                        self._expected.append(('ARRAY::array', '<any char>'))
                                                if address11 is not FAILURE:
                                                    elements2.append(address11)
                                                else:
                                                    elements2 = None
                                                    self._offset = index3
                                            else:
                                                elements2 = None
                                                self._offset = index3
                                            if elements2 is None:
                                                address9 = FAILURE
                                            else:
                                                address9 = TreeNode(self._input[index3:self._offset], index3, elements2)
                                                self._offset = self._offset
                                            if address9 is not FAILURE:
                                                elements1.append(address9)
                                            else:
                                                break
                                        if len(elements1) >= 1:
                                            address8 = TreeNode(self._input[index2:self._offset], index2, elements1)
                                            self._offset = self._offset
                                        else:
                                            address8 = FAILURE
                                        if address8 is not FAILURE:
                                            elements0.append(address8)
                                            address12 = FAILURE
                                            chunk5, max5 = None, self._offset + 1
                                            if max5 <= self._input_size:
                                                chunk5 = self._input[self._offset:max5]
                                            if chunk5 == '>':
                                                address12 = TreeNode(self._input[self._offset:self._offset + 1], self._offset, [])
                                                self._offset = self._offset + 1
                                            else:
                                                address12 = FAILURE
                                                if self._offset > self._failure:
                                                    self._failure = self._offset
                                                    self._expected = []
                                                if self._offset == self._failure:
                                                    self._expected.append(('ARRAY::array', '">"'))
                                            if address12 is not FAILURE:
                                                elements0.append(address12)
                                            else:
                                                elements0 = None
                                                self._offset = index1
                                        else:
                                            elements0 = None
                                            self._offset = index1
                                    else:
                                        elements0 = None
                                        self._offset = index1
                                else:
                                    elements0 = None
                                    self._offset = index1
                            else:
                                elements0 = None
                                self._offset = index1
                        else:
                            elements0 = None
                            self._offset = index1
                    else:
                        elements0 = None
                        self._offset = index1
                else:
                    elements0 = None
                    self._offset = index1
            else:
                elements0 = None
                self._offset = index1
            if elements0 is None:
                address0 = FAILURE
            else:
                address0 = Array.TreeNode1(self._input[index1:self._offset], index1, elements0)
                self._offset = self._offset
            self._cache['array'][index0] = (address0, self._offset)
            return address0

        def _read_options(self):
            address0, index0 = FAILURE, self._offset
            cached = self._cache['options'].get(index0)
            if cached:
                self._offset = cached[1]
                return cached[0]
            index1, elements0 = self._offset, []
            address1 = FAILURE
            index2, elements1, address2 = self._offset, [], None
            while True:
                index3, elements2 = self._offset, []
                address3 = FAILURE
                index4 = self._offset
                chunk0, max0 = None, self._offset + 1
                if max0 <= self._input_size:
                    chunk0 = self._input[self._offset:max0]
                if chunk0 == ':':
                    address3 = TreeNode(self._input[self._offset:self._offset + 1], self._offset, [])
                    self._offset = self._offset + 1
                else:
                    address3 = FAILURE
                    if self._offset > self._failure:
                        self._failure = self._offset
                        self._expected = []
                    if self._offset == self._failure:
                        self._expected.append(('ARRAY::options', '":"'))
                self._offset = index4
                if address3 is FAILURE:
                    address3 = TreeNode(self._input[self._offset:self._offset], self._offset, [])
                    self._offset = self._offset
                else:
                    address3 = FAILURE
                if address3 is not FAILURE:
                    elements2.append(address3)
                    address4 = FAILURE
                    if self._offset < self._input_size:
                        address4 = TreeNode(self._input[self._offset:self._offset + 1], self._offset, [])
                        self._offset = self._offset + 1
                    else:
                        address4 = FAILURE
                        if self._offset > self._failure:
                            self._failure = self._offset
                            self._expected = []
                        if self._offset == self._failure:
                            self._expected.append(('ARRAY::options', '<any char>'))
                    if address4 is not FAILURE:
                        elements2.append(address4)
                    else:
                        elements2 = None
                        self._offset = index3
                else:
                    elements2 = None
                    self._offset = index3
                if elements2 is None:
                    address2 = FAILURE
                else:
                    address2 = TreeNode(self._input[index3:self._offset], index3, elements2)
                    self._offset = self._offset
                if address2 is not FAILURE:
                    elements1.append(address2)
                else:
                    break
            if len(elements1) >= 0:
                address1 = TreeNode(self._input[index2:self._offset], index2, elements1)
                self._offset = self._offset
            else:
                address1 = FAILURE
            if address1 is not FAILURE:
                elements0.append(address1)
                address5 = FAILURE
                chunk1, max1 = None, self._offset + 1
                if max1 <= self._input_size:
                    chunk1 = self._input[self._offset:max1]
                if chunk1 == ':':
                    address5 = TreeNode(self._input[self._offset:self._offset + 1], self._offset, [])
                    self._offset = self._offset + 1
                else:
                    address5 = FAILURE
                    if self._offset > self._failure:
                        self._failure = self._offset
                        self._expected = []
                    if self._offset == self._failure:
                        self._expected.append(('ARRAY::options', '":"'))
                if address5 is not FAILURE:
                    elements0.append(address5)
                    address6 = FAILURE
                    index5, elements3, address7 = self._offset, [], None
                    while True:
                        index6, elements4 = self._offset, []
                        address8 = FAILURE
                        index7 = self._offset
                        chunk2, max2 = None, self._offset + 1
                        if max2 <= self._input_size:
                            chunk2 = self._input[self._offset:max2]
                        if chunk2 == ']':
                            address8 = TreeNode(self._input[self._offset:self._offset + 1], self._offset, [])
                            self._offset = self._offset + 1
                        else:
                            address8 = FAILURE
                            if self._offset > self._failure:
                                self._failure = self._offset
                                self._expected = []
                            if self._offset == self._failure:
                                self._expected.append(('ARRAY::options', '"]"'))
                        self._offset = index7
                        if address8 is FAILURE:
                            address8 = TreeNode(self._input[self._offset:self._offset], self._offset, [])
                            self._offset = self._offset
                        else:
                            address8 = FAILURE
                        if address8 is not FAILURE:
                            elements4.append(address8)
                            address9 = FAILURE
                            if self._offset < self._input_size:
                                address9 = TreeNode(self._input[self._offset:self._offset + 1], self._offset, [])
                                self._offset = self._offset + 1
                            else:
                                address9 = FAILURE
                                if self._offset > self._failure:
                                    self._failure = self._offset
                                    self._expected = []
                                if self._offset == self._failure:
                                    self._expected.append(('ARRAY::options', '<any char>'))
                            if address9 is not FAILURE:
                                elements4.append(address9)
                            else:
                                elements4 = None
                                self._offset = index6
                        else:
                            elements4 = None
                            self._offset = index6
                        if elements4 is None:
                            address7 = FAILURE
                        else:
                            address7 = TreeNode(self._input[index6:self._offset], index6, elements4)
                            self._offset = self._offset
                        if address7 is not FAILURE:
                            elements3.append(address7)
                        else:
                            break
                    if len(elements3) >= 0:
                        address6 = TreeNode(self._input[index5:self._offset], index5, elements3)
                        self._offset = self._offset
                    else:
                        address6 = FAILURE
                    if address6 is not FAILURE:
                        elements0.append(address6)
                    else:
                        elements0 = None
                        self._offset = index1
                else:
                    elements0 = None
                    self._offset = index1
            else:
                elements0 = None
                self._offset = index1
            if elements0 is None:
                address0 = FAILURE
            else:
                address0 = Array.TreeNode2(self._input[index1:self._offset], index1, elements0)
                self._offset = self._offset
            self._cache['options'][index0] = (address0, self._offset)
            return address0

        def _read_s(self):
            address0, index0 = FAILURE, self._offset
            cached = self._cache['s'].get(index0)
            if cached:
                self._offset = cached[1]
                return cached[0]
            index1, elements0, address1 = self._offset, [], None
            while True:
                chunk0, max0 = None, self._offset + 1
                if max0 <= self._input_size:
                    chunk0 = self._input[self._offset:max0]
                if chunk0 == ' ':
                    address1 = TreeNode(self._input[self._offset:self._offset + 1], self._offset, [])
                    self._offset = self._offset + 1
                else:
                    address1 = FAILURE
                    if self._offset > self._failure:
                        self._failure = self._offset
                        self._expected = []
                    if self._offset == self._failure:
                        self._expected.append(('ARRAY::s', '" "'))
                if address1 is not FAILURE:
                    elements0.append(address1)
                else:
                    break
            if len(elements0) >= 0:
                address0 = TreeNode(self._input[index1:self._offset], index1, elements0)
                self._offset = self._offset
            else:
                address0 = FAILURE
            self._cache['s'][index0] = (address0, self._offset)
            return address0

        def _read_w(self):
            address0, index0 = FAILURE, self._offset
            cached = self._cache['w'].get(index0)
            if cached:
                self._offset = cached[1]
                return cached[0]
            index1, elements0, address1 = self._offset, [], None
            while True:
                chunk0, max0 = None, self._offset + 1
                if max0 <= self._input_size:
                    chunk0 = self._input[self._offset:max0]
                if chunk0 is not None and Array.Grammar.REGEX_1.search(chunk0):
                    address1 = TreeNode(self._input[self._offset:self._offset + 1], self._offset, [])
                    self._offset = self._offset + 1
                else:
                    address1 = FAILURE
                    if self._offset > self._failure:
                        self._failure = self._offset
                        self._expected = []
                    if self._offset == self._failure:
                        self._expected.append(('ARRAY::w', '[a-zA-Z0-9]'))
                if address1 is not FAILURE:
                    elements0.append(address1)
                else:
                    break
            if len(elements0) >= 1:
                address0 = TreeNode(self._input[index1:self._offset], index1, elements0)
                self._offset = self._offset
            else:
                address0 = FAILURE
            self._cache['w'][index0] = (address0, self._offset)
            return address0







class C_Check:
    class TreeNode1(TreeNode):
        def __init__(self, text, offset, elements):
            super(C_Check.TreeNode1, self).__init__(text, offset, elements)
            self.indent = elements[0]
            self.s = elements[4]
            self.test = elements[3]
            self.then = elements[5]
            self.anyway = elements[6]


    class TreeNode2(TreeNode):
        def __init__(self, text, offset, elements):
            super(C_Check.TreeNode2, self).__init__(text, offset, elements)
            self.s = elements[1]
            self.thenin = elements[2]


    class TreeNode3(TreeNode):
        def __init__(self, text, offset, elements):
            super(C_Check.TreeNode3, self).__init__(text, offset, elements)
            self.s = elements[4]
            self.anywayin = elements[5]



    class Grammar(object):
        def _read_c_check(self):
            address0, index0 = FAILURE, self._offset
            cached = self._cache['c_check'].get(index0)
            if cached:
                self._offset = cached[1]
                return cached[0]
            index1, elements0 = self._offset, []
            address1 = FAILURE
            address1 = self._read_s()
            if address1 is not FAILURE:
                elements0.append(address1)
                address2 = FAILURE
                chunk0, max0 = None, self._offset + 7
                if max0 <= self._input_size:
                    chunk0 = self._input[self._offset:max0]
                if chunk0 == '$check ':
                    address2 = TreeNode(self._input[self._offset:self._offset + 7], self._offset, [])
                    self._offset = self._offset + 7
                else:
                    address2 = FAILURE
                    if self._offset > self._failure:
                        self._failure = self._offset
                        self._expected = []
                    if self._offset == self._failure:
                        self._expected.append(('C_CHECK::c_check', '"$check "'))
                if address2 is not FAILURE:
                    elements0.append(address2)
                    address3 = FAILURE
                    address3 = self._read_s()
                    if address3 is not FAILURE:
                        elements0.append(address3)
                        address4 = FAILURE
                        index2, elements1, address5 = self._offset, [], None
                        while True:
                            index3, elements2 = self._offset, []
                            address6 = FAILURE
                            index4 = self._offset
                            index5 = self._offset
                            chunk1, max1 = None, self._offset + 6
                            if max1 <= self._input_size:
                                chunk1 = self._input[self._offset:max1]
                            if chunk1 == ' then ':
                                address6 = TreeNode(self._input[self._offset:self._offset + 6], self._offset, [])
                                self._offset = self._offset + 6
                            else:
                                address6 = FAILURE
                                if self._offset > self._failure:
                                    self._failure = self._offset
                                    self._expected = []
                                if self._offset == self._failure:
                                    self._expected.append(('C_CHECK::c_check', '" then "'))
                            if address6 is FAILURE:
                                self._offset = index5
                                chunk2, max2 = None, self._offset + 8
                                if max2 <= self._input_size:
                                    chunk2 = self._input[self._offset:max2]
                                if chunk2 == ' anyway ':
                                    address6 = TreeNode(self._input[self._offset:self._offset + 8], self._offset, [])
                                    self._offset = self._offset + 8
                                else:
                                    address6 = FAILURE
                                    if self._offset > self._failure:
                                        self._failure = self._offset
                                        self._expected = []
                                    if self._offset == self._failure:
                                        self._expected.append(('C_CHECK::c_check', '" anyway "'))
                                if address6 is FAILURE:
                                    self._offset = index5
                                    chunk3, max3 = None, self._offset + 9
                                    if max3 <= self._input_size:
                                        chunk3 = self._input[self._offset:max3]
                                    if chunk3 == ' anyways ':
                                        address6 = TreeNode(self._input[self._offset:self._offset + 9], self._offset, [])
                                        self._offset = self._offset + 9
                                    else:
                                        address6 = FAILURE
                                        if self._offset > self._failure:
                                            self._failure = self._offset
                                            self._expected = []
                                        if self._offset == self._failure:
                                            self._expected.append(('C_CHECK::c_check', '" anyways "'))
                                    if address6 is FAILURE:
                                        self._offset = index5
                            self._offset = index4
                            if address6 is FAILURE:
                                address6 = TreeNode(self._input[self._offset:self._offset], self._offset, [])
                                self._offset = self._offset
                            else:
                                address6 = FAILURE
                            if address6 is not FAILURE:
                                elements2.append(address6)
                                address7 = FAILURE
                                if self._offset < self._input_size:
                                    address7 = TreeNode(self._input[self._offset:self._offset + 1], self._offset, [])
                                    self._offset = self._offset + 1
                                else:
                                    address7 = FAILURE
                                    if self._offset > self._failure:
                                        self._failure = self._offset
                                        self._expected = []
                                    if self._offset == self._failure:
                                        self._expected.append(('C_CHECK::c_check', '<any char>'))
                                if address7 is not FAILURE:
                                    elements2.append(address7)
                                else:
                                    elements2 = None
                                    self._offset = index3
                            else:
                                elements2 = None
                                self._offset = index3
                            if elements2 is None:
                                address5 = FAILURE
                            else:
                                address5 = TreeNode(self._input[index3:self._offset], index3, elements2)
                                self._offset = self._offset
                            if address5 is not FAILURE:
                                elements1.append(address5)
                            else:
                                break
                        if len(elements1) >= 1:
                            address4 = TreeNode(self._input[index2:self._offset], index2, elements1)
                            self._offset = self._offset
                        else:
                            address4 = FAILURE
                        if address4 is not FAILURE:
                            elements0.append(address4)
                            address8 = FAILURE
                            address8 = self._read_s()
                            if address8 is not FAILURE:
                                elements0.append(address8)
                                address9 = FAILURE
                                index6 = self._offset
                                index7, elements3 = self._offset, []
                                address10 = FAILURE
                                chunk4, max4 = None, self._offset + 5
                                if max4 <= self._input_size:
                                    chunk4 = self._input[self._offset:max4]
                                if chunk4 == 'then ':
                                    address10 = TreeNode(self._input[self._offset:self._offset + 5], self._offset, [])
                                    self._offset = self._offset + 5
                                else:
                                    address10 = FAILURE
                                    if self._offset > self._failure:
                                        self._failure = self._offset
                                        self._expected = []
                                    if self._offset == self._failure:
                                        self._expected.append(('C_CHECK::c_check', '"then "'))
                                if address10 is not FAILURE:
                                    elements3.append(address10)
                                    address11 = FAILURE
                                    address11 = self._read_s()
                                    if address11 is not FAILURE:
                                        elements3.append(address11)
                                        address12 = FAILURE
                                        index8, elements4, address13 = self._offset, [], None
                                        while True:
                                            index9, elements5 = self._offset, []
                                            address14 = FAILURE
                                            index10 = self._offset
                                            index11, elements6 = self._offset, []
                                            address15 = FAILURE
                                            chunk5, max5 = None, self._offset + 7
                                            if max5 <= self._input_size:
                                                chunk5 = self._input[self._offset:max5]
                                            if chunk5 == ' anyway':
                                                address15 = TreeNode(self._input[self._offset:self._offset + 7], self._offset, [])
                                                self._offset = self._offset + 7
                                            else:
                                                address15 = FAILURE
                                                if self._offset > self._failure:
                                                    self._failure = self._offset
                                                    self._expected = []
                                                if self._offset == self._failure:
                                                    self._expected.append(('C_CHECK::c_check', '" anyway"'))
                                            if address15 is not FAILURE:
                                                elements6.append(address15)
                                                address16 = FAILURE
                                                index12 = self._offset
                                                chunk6, max6 = None, self._offset + 1
                                                if max6 <= self._input_size:
                                                    chunk6 = self._input[self._offset:max6]
                                                if chunk6 == 's':
                                                    address16 = TreeNode(self._input[self._offset:self._offset + 1], self._offset, [])
                                                    self._offset = self._offset + 1
                                                else:
                                                    address16 = FAILURE
                                                    if self._offset > self._failure:
                                                        self._failure = self._offset
                                                        self._expected = []
                                                    if self._offset == self._failure:
                                                        self._expected.append(('C_CHECK::c_check', '"s"'))
                                                if address16 is FAILURE:
                                                    address16 = TreeNode(self._input[index12:index12], index12, [])
                                                    self._offset = index12
                                                if address16 is not FAILURE:
                                                    elements6.append(address16)
                                                    address17 = FAILURE
                                                    chunk7, max7 = None, self._offset + 1
                                                    if max7 <= self._input_size:
                                                        chunk7 = self._input[self._offset:max7]
                                                    if chunk7 == ' ':
                                                        address17 = TreeNode(self._input[self._offset:self._offset + 1], self._offset, [])
                                                        self._offset = self._offset + 1
                                                    else:
                                                        address17 = FAILURE
                                                        if self._offset > self._failure:
                                                            self._failure = self._offset
                                                            self._expected = []
                                                        if self._offset == self._failure:
                                                            self._expected.append(('C_CHECK::c_check', '" "'))
                                                    if address17 is not FAILURE:
                                                        elements6.append(address17)
                                                    else:
                                                        elements6 = None
                                                        self._offset = index11
                                                else:
                                                    elements6 = None
                                                    self._offset = index11
                                            else:
                                                elements6 = None
                                                self._offset = index11
                                            if elements6 is None:
                                                address14 = FAILURE
                                            else:
                                                address14 = TreeNode(self._input[index11:self._offset], index11, elements6)
                                                self._offset = self._offset
                                            self._offset = index10
                                            if address14 is FAILURE:
                                                address14 = TreeNode(self._input[self._offset:self._offset], self._offset, [])
                                                self._offset = self._offset
                                            else:
                                                address14 = FAILURE
                                            if address14 is not FAILURE:
                                                elements5.append(address14)
                                                address18 = FAILURE
                                                if self._offset < self._input_size:
                                                    address18 = TreeNode(self._input[self._offset:self._offset + 1], self._offset, [])
                                                    self._offset = self._offset + 1
                                                else:
                                                    address18 = FAILURE
                                                    if self._offset > self._failure:
                                                        self._failure = self._offset
                                                        self._expected = []
                                                    if self._offset == self._failure:
                                                        self._expected.append(('C_CHECK::c_check', '<any char>'))
                                                if address18 is not FAILURE:
                                                    elements5.append(address18)
                                                else:
                                                    elements5 = None
                                                    self._offset = index9
                                            else:
                                                elements5 = None
                                                self._offset = index9
                                            if elements5 is None:
                                                address13 = FAILURE
                                            else:
                                                address13 = TreeNode(self._input[index9:self._offset], index9, elements5)
                                                self._offset = self._offset
                                            if address13 is not FAILURE:
                                                elements4.append(address13)
                                            else:
                                                break
                                        if len(elements4) >= 1:
                                            address12 = TreeNode(self._input[index8:self._offset], index8, elements4)
                                            self._offset = self._offset
                                        else:
                                            address12 = FAILURE
                                        if address12 is not FAILURE:
                                            elements3.append(address12)
                                        else:
                                            elements3 = None
                                            self._offset = index7
                                    else:
                                        elements3 = None
                                        self._offset = index7
                                else:
                                    elements3 = None
                                    self._offset = index7
                                if elements3 is None:
                                    address9 = FAILURE
                                else:
                                    address9 = C_Check.TreeNode2(self._input[index7:self._offset], index7, elements3)
                                    self._offset = self._offset
                                if address9 is FAILURE:
                                    address9 = TreeNode(self._input[index6:index6], index6, [])
                                    self._offset = index6
                                if address9 is not FAILURE:
                                    elements0.append(address9)
                                    address19 = FAILURE
                                    index13 = self._offset
                                    index14, elements7 = self._offset, []
                                    address20 = FAILURE
                                    address20 = self._read_s()
                                    if address20 is not FAILURE:
                                        elements7.append(address20)
                                        address21 = FAILURE
                                        chunk8, max8 = None, self._offset + 6
                                        if max8 <= self._input_size:
                                            chunk8 = self._input[self._offset:max8]
                                        if chunk8 == 'anyway':
                                            address21 = TreeNode(self._input[self._offset:self._offset + 6], self._offset, [])
                                            self._offset = self._offset + 6
                                        else:
                                            address21 = FAILURE
                                            if self._offset > self._failure:
                                                self._failure = self._offset
                                                self._expected = []
                                            if self._offset == self._failure:
                                                self._expected.append(('C_CHECK::c_check', '"anyway"'))
                                        if address21 is not FAILURE:
                                            elements7.append(address21)
                                            address22 = FAILURE
                                            index15 = self._offset
                                            chunk9, max9 = None, self._offset + 1
                                            if max9 <= self._input_size:
                                                chunk9 = self._input[self._offset:max9]
                                            if chunk9 == 's':
                                                address22 = TreeNode(self._input[self._offset:self._offset + 1], self._offset, [])
                                                self._offset = self._offset + 1
                                            else:
                                                address22 = FAILURE
                                                if self._offset > self._failure:
                                                    self._failure = self._offset
                                                    self._expected = []
                                                if self._offset == self._failure:
                                                    self._expected.append(('C_CHECK::c_check', '"s"'))
                                            if address22 is FAILURE:
                                                address22 = TreeNode(self._input[index15:index15], index15, [])
                                                self._offset = index15
                                            if address22 is not FAILURE:
                                                elements7.append(address22)
                                                address23 = FAILURE
                                                chunk10, max10 = None, self._offset + 1
                                                if max10 <= self._input_size:
                                                    chunk10 = self._input[self._offset:max10]
                                                if chunk10 == ' ':
                                                    address23 = TreeNode(self._input[self._offset:self._offset + 1], self._offset, [])
                                                    self._offset = self._offset + 1
                                                else:
                                                    address23 = FAILURE
                                                    if self._offset > self._failure:
                                                        self._failure = self._offset
                                                        self._expected = []
                                                    if self._offset == self._failure:
                                                        self._expected.append(('C_CHECK::c_check', '" "'))
                                                if address23 is not FAILURE:
                                                    elements7.append(address23)
                                                    address24 = FAILURE
                                                    address24 = self._read_s()
                                                    if address24 is not FAILURE:
                                                        elements7.append(address24)
                                                        address25 = FAILURE
                                                        index16, elements8, address26 = self._offset, [], None
                                                        while True:
                                                            if self._offset < self._input_size:
                                                                address26 = TreeNode(self._input[self._offset:self._offset + 1], self._offset, [])
                                                                self._offset = self._offset + 1
                                                            else:
                                                                address26 = FAILURE
                                                                if self._offset > self._failure:
                                                                    self._failure = self._offset
                                                                    self._expected = []
                                                                if self._offset == self._failure:
                                                                    self._expected.append(('C_CHECK::c_check', '<any char>'))
                                                            if address26 is not FAILURE:
                                                                elements8.append(address26)
                                                            else:
                                                                break
                                                        if len(elements8) >= 1:
                                                            address25 = TreeNode(self._input[index16:self._offset], index16, elements8)
                                                            self._offset = self._offset
                                                        else:
                                                            address25 = FAILURE
                                                        if address25 is not FAILURE:
                                                            elements7.append(address25)
                                                        else:
                                                            elements7 = None
                                                            self._offset = index14
                                                    else:
                                                        elements7 = None
                                                        self._offset = index14
                                                else:
                                                    elements7 = None
                                                    self._offset = index14
                                            else:
                                                elements7 = None
                                                self._offset = index14
                                        else:
                                            elements7 = None
                                            self._offset = index14
                                    else:
                                        elements7 = None
                                        self._offset = index14
                                    if elements7 is None:
                                        address19 = FAILURE
                                    else:
                                        address19 = C_Check.TreeNode3(self._input[index14:self._offset], index14, elements7)
                                        self._offset = self._offset
                                    if address19 is FAILURE:
                                        address19 = TreeNode(self._input[index13:index13], index13, [])
                                        self._offset = index13
                                    if address19 is not FAILURE:
                                        elements0.append(address19)
                                    else:
                                        elements0 = None
                                        self._offset = index1
                                else:
                                    elements0 = None
                                    self._offset = index1
                            else:
                                elements0 = None
                                self._offset = index1
                        else:
                            elements0 = None
                            self._offset = index1
                    else:
                        elements0 = None
                        self._offset = index1
                else:
                    elements0 = None
                    self._offset = index1
            else:
                elements0 = None
                self._offset = index1
            if elements0 is None:
                address0 = FAILURE
            else:
                address0 = C_Check.TreeNode1(self._input[index1:self._offset], index1, elements0)
                self._offset = self._offset
            self._cache['c_check'][index0] = (address0, self._offset)
            return address0

        def _read_s(self):
            address0, index0 = FAILURE, self._offset
            cached = self._cache['s'].get(index0)
            if cached:
                self._offset = cached[1]
                return cached[0]
            index1, elements0, address1 = self._offset, [], None
            while True:
                chunk0, max0 = None, self._offset + 1
                if max0 <= self._input_size:
                    chunk0 = self._input[self._offset:max0]
                if chunk0 == ' ':
                    address1 = TreeNode(self._input[self._offset:self._offset + 1], self._offset, [])
                    self._offset = self._offset + 1
                else:
                    address1 = FAILURE
                    if self._offset > self._failure:
                        self._failure = self._offset
                        self._expected = []
                    if self._offset == self._failure:
                        self._expected.append(('C_CHECK::s', '" "'))
                if address1 is not FAILURE:
                    elements0.append(address1)
                else:
                    break
            if len(elements0) >= 0:
                address0 = TreeNode(self._input[index1:self._offset], index1, elements0)
                self._offset = self._offset
            else:
                address0 = FAILURE
            self._cache['s'][index0] = (address0, self._offset)
            return address0




class C_Cmd:
    class TreeNode1(TreeNode):
        def __init__(self, text, offset, elements):
            super(C_Cmd.TreeNode1, self).__init__(text, offset, elements)
            self.indent = elements[0]
            self.s = elements[0]


    class TreeNode2(TreeNode):
        def __init__(self, text, offset, elements):
            super(C_Cmd.TreeNode2, self).__init__(text, offset, elements)
            self.command = elements[1]



    class Grammar(object):
        def _read_cmd(self):
            address0, index0 = FAILURE, self._offset
            cached = self._cache['cmd'].get(index0)
            if cached:
                self._offset = cached[1]
                return cached[0]
            index1, elements0 = self._offset, []
            address1 = FAILURE
            address1 = self._read_s()
            if address1 is not FAILURE:
                elements0.append(address1)
                address2 = FAILURE
                chunk0, max0 = None, self._offset + 4
                if max0 <= self._input_size:
                    chunk0 = self._input[self._offset:max0]
                if chunk0 == '$cmd':
                    address2 = TreeNode(self._input[self._offset:self._offset + 4], self._offset, [])
                    self._offset = self._offset + 4
                else:
                    address2 = FAILURE
                    if self._offset > self._failure:
                        self._failure = self._offset
                        self._expected = []
                    if self._offset == self._failure:
                        self._expected.append(('C_CMD::cmd', '"$cmd"'))
                if address2 is not FAILURE:
                    elements0.append(address2)
                    address3 = FAILURE
                    index2 = self._offset
                    index3, elements1 = self._offset, []
                    address4 = FAILURE
                    index4, elements2, address5 = self._offset, [], None
                    while True:
                        chunk1, max1 = None, self._offset + 1
                        if max1 <= self._input_size:
                            chunk1 = self._input[self._offset:max1]
                        if chunk1 == ' ':
                            address5 = TreeNode(self._input[self._offset:self._offset + 1], self._offset, [])
                            self._offset = self._offset + 1
                        else:
                            address5 = FAILURE
                            if self._offset > self._failure:
                                self._failure = self._offset
                                self._expected = []
                            if self._offset == self._failure:
                                self._expected.append(('C_CMD::cmd', '" "'))
                        if address5 is not FAILURE:
                            elements2.append(address5)
                        else:
                            break
                    if len(elements2) >= 1:
                        address4 = TreeNode(self._input[index4:self._offset], index4, elements2)
                        self._offset = self._offset
                    else:
                        address4 = FAILURE
                    if address4 is not FAILURE:
                        elements1.append(address4)
                        address6 = FAILURE
                        index5, elements3, address7 = self._offset, [], None
                        while True:
                            if self._offset < self._input_size:
                                address7 = TreeNode(self._input[self._offset:self._offset + 1], self._offset, [])
                                self._offset = self._offset + 1
                            else:
                                address7 = FAILURE
                                if self._offset > self._failure:
                                    self._failure = self._offset
                                    self._expected = []
                                if self._offset == self._failure:
                                    self._expected.append(('C_CMD::cmd', '<any char>'))
                            if address7 is not FAILURE:
                                elements3.append(address7)
                            else:
                                break
                        if len(elements3) >= 0:
                            address6 = TreeNode(self._input[index5:self._offset], index5, elements3)
                            self._offset = self._offset
                        else:
                            address6 = FAILURE
                        if address6 is not FAILURE:
                            elements1.append(address6)
                        else:
                            elements1 = None
                            self._offset = index3
                    else:
                        elements1 = None
                        self._offset = index3
                    if elements1 is None:
                        address3 = FAILURE
                    else:
                        address3 = C_Cmd.TreeNode2(self._input[index3:self._offset], index3, elements1)
                        self._offset = self._offset
                    if address3 is FAILURE:
                        address3 = TreeNode(self._input[index2:index2], index2, [])
                        self._offset = index2
                    if address3 is not FAILURE:
                        elements0.append(address3)
                    else:
                        elements0 = None
                        self._offset = index1
                else:
                    elements0 = None
                    self._offset = index1
            else:
                elements0 = None
                self._offset = index1
            if elements0 is None:
                address0 = FAILURE
            else:
                address0 = C_Cmd.TreeNode1(self._input[index1:self._offset], index1, elements0)
                self._offset = self._offset
            self._cache['cmd'][index0] = (address0, self._offset)
            return address0

        def _read_s(self):
            address0, index0 = FAILURE, self._offset
            cached = self._cache['s'].get(index0)
            if cached:
                self._offset = cached[1]
                return cached[0]
            index1, elements0, address1 = self._offset, [], None
            while True:
                chunk0, max0 = None, self._offset + 1
                if max0 <= self._input_size:
                    chunk0 = self._input[self._offset:max0]
                if chunk0 == ' ':
                    address1 = TreeNode(self._input[self._offset:self._offset + 1], self._offset, [])
                    self._offset = self._offset + 1
                else:
                    address1 = FAILURE
                    if self._offset > self._failure:
                        self._failure = self._offset
                        self._expected = []
                    if self._offset == self._failure:
                        self._expected.append(('C_CMD::s', '" "'))
                if address1 is not FAILURE:
                    elements0.append(address1)
                else:
                    break
            if len(elements0) >= 0:
                address0 = TreeNode(self._input[index1:self._offset], index1, elements0)
                self._offset = self._offset
            else:
                address0 = FAILURE
            self._cache['s'][index0] = (address0, self._offset)
            return address0




class C_Call:
    class TreeNode1(TreeNode):
        def __init__(self, text, offset, elements):
            super(C_Call.TreeNode1, self).__init__(text, offset, elements)
            self.indent = elements[0]
            self.s = elements[5]
            self.func = elements[2]
            self.delay = elements[6]





    class Grammar(object):
        REGEX_1 = re.compile('^[a-zA-Z_]')
        REGEX_2 = re.compile('^[a-zA-Z0-9_]')

        def _read_c_call(self):
            address0, index0 = FAILURE, self._offset
            cached = self._cache['c_call'].get(index0)
            if cached:
                self._offset = cached[1]
                return cached[0]
            index1, elements0 = self._offset, []
            address1 = FAILURE
            address1 = self._read_s()
            if address1 is not FAILURE:
                elements0.append(address1)
                address2 = FAILURE
                chunk0, max0 = None, self._offset + 6
                if max0 <= self._input_size:
                    chunk0 = self._input[self._offset:max0]
                if chunk0 == '$call ':
                    address2 = TreeNode(self._input[self._offset:self._offset + 6], self._offset, [])
                    self._offset = self._offset + 6
                else:
                    address2 = FAILURE
                    if self._offset > self._failure:
                        self._failure = self._offset
                        self._expected = []
                    if self._offset == self._failure:
                        self._expected.append(('C_CALL::c_call', '"$call "'))
                if address2 is not FAILURE:
                    elements0.append(address2)
                    address3 = FAILURE
                    index2, elements1, address4 = self._offset, [], None
                    while True:
                        index3, elements2 = self._offset, []
                        address5 = FAILURE
                        index4 = self._offset
                        chunk1, max1 = None, self._offset + 3
                        if max1 <= self._input_size:
                            chunk1 = self._input[self._offset:max1]
                        if chunk1 == ' in':
                            address5 = TreeNode(self._input[self._offset:self._offset + 3], self._offset, [])
                            self._offset = self._offset + 3
                        else:
                            address5 = FAILURE
                            if self._offset > self._failure:
                                self._failure = self._offset
                                self._expected = []
                            if self._offset == self._failure:
                                self._expected.append(('C_CALL::c_call', '" in"'))
                        self._offset = index4
                        if address5 is FAILURE:
                            address5 = TreeNode(self._input[self._offset:self._offset], self._offset, [])
                            self._offset = self._offset
                        else:
                            address5 = FAILURE
                        if address5 is not FAILURE:
                            elements2.append(address5)
                            address6 = FAILURE
                            if self._offset < self._input_size:
                                address6 = TreeNode(self._input[self._offset:self._offset + 1], self._offset, [])
                                self._offset = self._offset + 1
                            else:
                                address6 = FAILURE
                                if self._offset > self._failure:
                                    self._failure = self._offset
                                    self._expected = []
                                if self._offset == self._failure:
                                    self._expected.append(('C_CALL::c_call', '<any char>'))
                            if address6 is not FAILURE:
                                elements2.append(address6)
                            else:
                                elements2 = None
                                self._offset = index3
                        else:
                            elements2 = None
                            self._offset = index3
                        if elements2 is None:
                            address4 = FAILURE
                        else:
                            address4 = TreeNode(self._input[index3:self._offset], index3, elements2)
                            self._offset = self._offset
                        if address4 is not FAILURE:
                            elements1.append(address4)
                        else:
                            break
                    if len(elements1) >= 1:
                        address3 = TreeNode(self._input[index2:self._offset], index2, elements1)
                        self._offset = self._offset
                    else:
                        address3 = FAILURE
                    if address3 is not FAILURE:
                        elements0.append(address3)
                        address7 = FAILURE
                        index5, elements3, address8 = self._offset, [], None
                        while True:
                            chunk2, max2 = None, self._offset + 1
                            if max2 <= self._input_size:
                                chunk2 = self._input[self._offset:max2]
                            if chunk2 == ' ':
                                address8 = TreeNode(self._input[self._offset:self._offset + 1], self._offset, [])
                                self._offset = self._offset + 1
                            else:
                                address8 = FAILURE
                                if self._offset > self._failure:
                                    self._failure = self._offset
                                    self._expected = []
                                if self._offset == self._failure:
                                    self._expected.append(('C_CALL::c_call', '" "'))
                            if address8 is not FAILURE:
                                elements3.append(address8)
                            else:
                                break
                        if len(elements3) >= 1:
                            address7 = TreeNode(self._input[index5:self._offset], index5, elements3)
                            self._offset = self._offset
                        else:
                            address7 = FAILURE
                        if address7 is not FAILURE:
                            elements0.append(address7)
                            address9 = FAILURE
                            chunk3, max3 = None, self._offset + 3
                            if max3 <= self._input_size:
                                chunk3 = self._input[self._offset:max3]
                            if chunk3 == 'in ':
                                address9 = TreeNode(self._input[self._offset:self._offset + 3], self._offset, [])
                                self._offset = self._offset + 3
                            else:
                                address9 = FAILURE
                                if self._offset > self._failure:
                                    self._failure = self._offset
                                    self._expected = []
                                if self._offset == self._failure:
                                    self._expected.append(('C_CALL::c_call', '"in "'))
                            if address9 is not FAILURE:
                                elements0.append(address9)
                                address10 = FAILURE
                                address10 = self._read_s()
                                if address10 is not FAILURE:
                                    elements0.append(address10)
                                    address11 = FAILURE
                                    index6, elements4, address12 = self._offset, [], None
                                    while True:
                                        if self._offset < self._input_size:
                                            address12 = TreeNode(self._input[self._offset:self._offset + 1], self._offset, [])
                                            self._offset = self._offset + 1
                                        else:
                                            address12 = FAILURE
                                            if self._offset > self._failure:
                                                self._failure = self._offset
                                                self._expected = []
                                            if self._offset == self._failure:
                                                self._expected.append(('C_CALL::c_call', '<any char>'))
                                        if address12 is not FAILURE:
                                            elements4.append(address12)
                                        else:
                                            break
                                    if len(elements4) >= 1:
                                        address11 = TreeNode(self._input[index6:self._offset], index6, elements4)
                                        self._offset = self._offset
                                    else:
                                        address11 = FAILURE
                                    if address11 is not FAILURE:
                                        elements0.append(address11)
                                    else:
                                        elements0 = None
                                        self._offset = index1
                                else:
                                    elements0 = None
                                    self._offset = index1
                            else:
                                elements0 = None
                                self._offset = index1
                        else:
                            elements0 = None
                            self._offset = index1
                    else:
                        elements0 = None
                        self._offset = index1
                else:
                    elements0 = None
                    self._offset = index1
            else:
                elements0 = None
                self._offset = index1
            if elements0 is None:
                address0 = FAILURE
            else:
                address0 = C_Call.TreeNode1(self._input[index1:self._offset], index1, elements0)
                self._offset = self._offset
            self._cache['c_call'][index0] = (address0, self._offset)
            return address0

        def _read_s(self):
            address0, index0 = FAILURE, self._offset
            cached = self._cache['s'].get(index0)
            if cached:
                self._offset = cached[1]
                return cached[0]
            index1, elements0, address1 = self._offset, [], None
            while True:
                chunk0, max0 = None, self._offset + 1
                if max0 <= self._input_size:
                    chunk0 = self._input[self._offset:max0]
                if chunk0 == ' ':
                    address1 = TreeNode(self._input[self._offset:self._offset + 1], self._offset, [])
                    self._offset = self._offset + 1
                else:
                    address1 = FAILURE
                    if self._offset > self._failure:
                        self._failure = self._offset
                        self._expected = []
                    if self._offset == self._failure:
                        self._expected.append(('C_CALL::s', '" "'))
                if address1 is not FAILURE:
                    elements0.append(address1)
                else:
                    break
            if len(elements0) >= 0:
                address0 = TreeNode(self._input[index1:self._offset], index1, elements0)
                self._offset = self._offset
            else:
                address0 = FAILURE
            self._cache['s'][index0] = (address0, self._offset)
            return address0

        def _read_variable(self):
            address0, index0 = FAILURE, self._offset
            cached = self._cache['variable'].get(index0)
            if cached:
                self._offset = cached[1]
                return cached[0]
            index1, elements0 = self._offset, []
            address1 = FAILURE
            index2, elements1, address2 = self._offset, [], None
            while True:
                chunk0, max0 = None, self._offset + 1
                if max0 <= self._input_size:
                    chunk0 = self._input[self._offset:max0]
                if chunk0 is not None and Grammar.REGEX_1.search(chunk0):
                    address2 = TreeNode(self._input[self._offset:self._offset + 1], self._offset, [])
                    self._offset = self._offset + 1
                else:
                    address2 = FAILURE
                    if self._offset > self._failure:
                        self._failure = self._offset
                        self._expected = []
                    if self._offset == self._failure:
                        self._expected.append(('C_CALL::variable', '[a-zA-Z_]'))
                if address2 is not FAILURE:
                    elements1.append(address2)
                else:
                    break
            if len(elements1) >= 1:
                address1 = TreeNode(self._input[index2:self._offset], index2, elements1)
                self._offset = self._offset
            else:
                address1 = FAILURE
            if address1 is not FAILURE:
                elements0.append(address1)
                address3 = FAILURE
                index3 = self._offset
                index4, elements2, address4 = self._offset, [], None
                while True:
                    chunk1, max1 = None, self._offset + 1
                    if max1 <= self._input_size:
                        chunk1 = self._input[self._offset:max1]
                    if chunk1 is not None and Grammar.REGEX_2.search(chunk1):
                        address4 = TreeNode(self._input[self._offset:self._offset + 1], self._offset, [])
                        self._offset = self._offset + 1
                    else:
                        address4 = FAILURE
                        if self._offset > self._failure:
                            self._failure = self._offset
                            self._expected = []
                        if self._offset == self._failure:
                            self._expected.append(('C_CALL::variable', '[a-zA-Z0-9_]'))
                    if address4 is not FAILURE:
                        elements2.append(address4)
                    else:
                        break
                if len(elements2) >= 0:
                    address3 = TreeNode(self._input[index4:self._offset], index4, elements2)
                    self._offset = self._offset
                else:
                    address3 = FAILURE
                if address3 is FAILURE:
                    address3 = TreeNode(self._input[index3:index3], index3, [])
                    self._offset = index3
                if address3 is not FAILURE:
                    elements0.append(address3)
                else:
                    elements0 = None
                    self._offset = index1
            else:
                elements0 = None
                self._offset = index1
            if elements0 is None:
                address0 = FAILURE
            else:
                address0 = TreeNode(self._input[index1:self._offset], index1, elements0)
                self._offset = self._offset
            self._cache['variable'][index0] = (address0, self._offset)
            return address0




class C_Clear:

    class TreeNode1(TreeNode):
        def __init__(self, text, offset, elements):
            super(C_Clear.TreeNode1, self).__init__(text, offset, elements)
            self.indent = elements[0]
            self.s = elements[0]




    class Grammar(object):
        def _read_c_clear(self):
            address0, index0 = FAILURE, self._offset
            cached = self._cache['c_clear'].get(index0)
            if cached:
                self._offset = cached[1]
                return cached[0]
            index1 = self._offset
            index2, elements0 = self._offset, []
            address1 = FAILURE
            address1 = self._read_s()
            if address1 is not FAILURE:
                elements0.append(address1)
                address2 = FAILURE
                chunk0, max0 = None, self._offset + 1
                if max0 <= self._input_size:
                    chunk0 = self._input[self._offset:max0]
                if chunk0 == '$':
                    address2 = TreeNode(self._input[self._offset:self._offset + 1], self._offset, [])
                    self._offset = self._offset + 1
                else:
                    address2 = FAILURE
                    if self._offset > self._failure:
                        self._failure = self._offset
                        self._expected = []
                    if self._offset == self._failure:
                        self._expected.append(('C_CLEAR::c_clear', '"$"'))
                if address2 is not FAILURE:
                    elements0.append(address2)
                    address3 = FAILURE
                    chunk1, max1 = None, self._offset + 5
                    if max1 <= self._input_size:
                        chunk1 = self._input[self._offset:max1]
                    if chunk1 == 'clear':
                        address3 = TreeNode(self._input[self._offset:self._offset + 5], self._offset, [])
                        self._offset = self._offset + 5
                    else:
                        address3 = FAILURE
                        if self._offset > self._failure:
                            self._failure = self._offset
                            self._expected = []
                        if self._offset == self._failure:
                            self._expected.append(('C_CLEAR::c_clear', '"clear"'))
                    if address3 is not FAILURE:
                        elements0.append(address3)
                    else:
                        elements0 = None
                        self._offset = index2
                else:
                    elements0 = None
                    self._offset = index2
            else:
                elements0 = None
                self._offset = index2
            if elements0 is None:
                address0 = FAILURE
            else:
                address0 = C_Clear.TreeNode1(self._input[index2:self._offset], index2, elements0)
                self._offset = self._offset
            if address0 is FAILURE:
                self._offset = index1
                chunk2, max2 = None, self._offset + 3
                if max2 <= self._input_size:
                    chunk2 = self._input[self._offset:max2]
                if chunk2 == 'cls':
                    address0 = TreeNode(self._input[self._offset:self._offset + 3], self._offset, [])
                    self._offset = self._offset + 3
                else:
                    address0 = FAILURE
                    if self._offset > self._failure:
                        self._failure = self._offset
                        self._expected = []
                    if self._offset == self._failure:
                        self._expected.append(('C_CLEAR::c_clear', '"cls"'))
                if address0 is FAILURE:
                    self._offset = index1
            self._cache['c_clear'][index0] = (address0, self._offset)
            return address0

        def _read_s(self):
            address0, index0 = FAILURE, self._offset
            cached = self._cache['s'].get(index0)
            if cached:
                self._offset = cached[1]
                return cached[0]
            index1, elements0, address1 = self._offset, [], None
            while True:
                chunk0, max0 = None, self._offset + 1
                if max0 <= self._input_size:
                    chunk0 = self._input[self._offset:max0]
                if chunk0 == ' ':
                    address1 = TreeNode(self._input[self._offset:self._offset + 1], self._offset, [])
                    self._offset = self._offset + 1
                else:
                    address1 = FAILURE
                    if self._offset > self._failure:
                        self._failure = self._offset
                        self._expected = []
                    if self._offset == self._failure:
                        self._expected.append(('C_CLEAR::s', '" "'))
                if address1 is not FAILURE:
                    elements0.append(address1)
                else:
                    break
            if len(elements0) >= 0:
                address0 = TreeNode(self._input[index1:self._offset], index1, elements0)
                self._offset = self._offset
            else:
                address0 = FAILURE
            self._cache['s'][index0] = (address0, self._offset)
            return address0

















class Until_Unless:
    class TreeNode1(TreeNode):
        def __init__(self, text, offset, elements):
            super(Until_Unless.TreeNode1, self).__init__(text, offset, elements)
            self.indent = elements[0]
            self.action = elements[1]
            self.expr = elements[4]
            self.rest = elements[6]


    class Grammar(object):
        def _read_untiless(self):
            address0, index0 = FAILURE, self._offset
            cached = self._cache['untiless'].get(index0)
            if cached:
                self._offset = cached[1]
                return cached[0]
            index1, elements0 = self._offset, []
            address1 = FAILURE
            index2 = self._offset
            address1 = self._read_spaces()
            if address1 is FAILURE:
                address1 = TreeNode(self._input[index2:index2], index2, [])
                self._offset = index2
            if address1 is not FAILURE:
                elements0.append(address1)
                address2 = FAILURE
                index3 = self._offset
                chunk0, max0 = None, self._offset + 5
                if max0 <= self._input_size:
                    chunk0 = self._input[self._offset:max0]
                if chunk0 == 'until':
                    address2 = TreeNode(self._input[self._offset:self._offset + 5], self._offset, [])
                    self._offset = self._offset + 5
                else:
                    address2 = FAILURE
                    if self._offset > self._failure:
                        self._failure = self._offset
                        self._expected = []
                    if self._offset == self._failure:
                        self._expected.append(('UNTILESS::untiless', '"until"'))
                if address2 is FAILURE:
                    self._offset = index3
                    chunk1, max1 = None, self._offset + 6
                    if max1 <= self._input_size:
                        chunk1 = self._input[self._offset:max1]
                    if chunk1 == 'unless':
                        address2 = TreeNode(self._input[self._offset:self._offset + 6], self._offset, [])
                        self._offset = self._offset + 6
                    else:
                        address2 = FAILURE
                        if self._offset > self._failure:
                            self._failure = self._offset
                            self._expected = []
                        if self._offset == self._failure:
                            self._expected.append(('UNTILESS::untiless', '"unless"'))
                    if address2 is FAILURE:
                        self._offset = index3
                if address2 is not FAILURE:
                    elements0.append(address2)
                    address3 = FAILURE
                    chunk2, max2 = None, self._offset + 1
                    if max2 <= self._input_size:
                        chunk2 = self._input[self._offset:max2]
                    if chunk2 == ' ':
                        address3 = TreeNode(self._input[self._offset:self._offset + 1], self._offset, [])
                        self._offset = self._offset + 1
                    else:
                        address3 = FAILURE
                        if self._offset > self._failure:
                            self._failure = self._offset
                            self._expected = []
                        if self._offset == self._failure:
                            self._expected.append(('UNTILESS::untiless', '" "'))
                    if address3 is not FAILURE:
                        elements0.append(address3)
                        address4 = FAILURE
                        index4 = self._offset
                        address4 = self._read_spaces()
                        if address4 is FAILURE:
                            address4 = TreeNode(self._input[index4:index4], index4, [])
                            self._offset = index4
                        if address4 is not FAILURE:
                            elements0.append(address4)
                            address5 = FAILURE
                            index5, elements1, address6 = self._offset, [], None
                            while True:
                                if self._offset < self._input_size:
                                    address6 = TreeNode(self._input[self._offset:self._offset + 1], self._offset, [])
                                    self._offset = self._offset + 1
                                else:
                                    address6 = FAILURE
                                    if self._offset > self._failure:
                                        self._failure = self._offset
                                        self._expected = []
                                    if self._offset == self._failure:
                                        self._expected.append(('UNTILESS::untiless', '<any char>'))
                                if address6 is not FAILURE:
                                    elements1.append(address6)
                                else:
                                    break
                            if len(elements1) >= 1:
                                address5 = TreeNode(self._input[index5:self._offset], index5, elements1)
                                self._offset = self._offset
                            else:
                                address5 = FAILURE
                            if address5 is not FAILURE:
                                elements0.append(address5)
                                address7 = FAILURE
                                chunk3, max3 = None, self._offset + 1
                                if max3 <= self._input_size:
                                    chunk3 = self._input[self._offset:max3]
                                if chunk3 == ':':
                                    address7 = TreeNode(self._input[self._offset:self._offset + 1], self._offset, [])
                                    self._offset = self._offset + 1
                                else:
                                    address7 = FAILURE
                                    if self._offset > self._failure:
                                        self._failure = self._offset
                                        self._expected = []
                                    if self._offset == self._failure:
                                        self._expected.append(('UNTILESS::untiless', '":"'))
                                if address7 is not FAILURE:
                                    elements0.append(address7)
                                    address8 = FAILURE
                                    index6, elements2, address9 = self._offset, [], None
                                    while True:
                                        if self._offset < self._input_size:
                                            address9 = TreeNode(self._input[self._offset:self._offset + 1], self._offset, [])
                                            self._offset = self._offset + 1
                                        else:
                                            address9 = FAILURE
                                            if self._offset > self._failure:
                                                self._failure = self._offset
                                                self._expected = []
                                            if self._offset == self._failure:
                                                self._expected.append(('UNTILESS::untiless', '<any char>'))
                                        if address9 is not FAILURE:
                                            elements2.append(address9)
                                        else:
                                            break
                                    if len(elements2) >= 0:
                                        address8 = TreeNode(self._input[index6:self._offset], index6, elements2)
                                        self._offset = self._offset
                                    else:
                                        address8 = FAILURE
                                    if address8 is not FAILURE:
                                        elements0.append(address8)
                                    else:
                                        elements0 = None
                                        self._offset = index1
                                else:
                                    elements0 = None
                                    self._offset = index1
                            else:
                                elements0 = None
                                self._offset = index1
                        else:
                            elements0 = None
                            self._offset = index1
                    else:
                        elements0 = None
                        self._offset = index1
                else:
                    elements0 = None
                    self._offset = index1
            else:
                elements0 = None
                self._offset = index1
            if elements0 is None:
                address0 = FAILURE
            else:
                address0 = Until_Unless.TreeNode1(self._input[index1:self._offset], index1, elements0)
                self._offset = self._offset
            self._cache['untiless'][index0] = (address0, self._offset)
            return address0

        def _read_spaces(self):
            address0, index0 = FAILURE, self._offset
            cached = self._cache['spaces'].get(index0)
            if cached:
                self._offset = cached[1]
                return cached[0]
            index1, elements0, address1 = self._offset, [], None
            while True:
                chunk0, max0 = None, self._offset + 1
                if max0 <= self._input_size:
                    chunk0 = self._input[self._offset:max0]
                if chunk0 == ' ':
                    address1 = TreeNode(self._input[self._offset:self._offset + 1], self._offset, [])
                    self._offset = self._offset + 1
                else:
                    address1 = FAILURE
                    if self._offset > self._failure:
                        self._failure = self._offset
                        self._expected = []
                    if self._offset == self._failure:
                        self._expected.append(('UNTILESS::spaces', '" "'))
                if address1 is not FAILURE:
                    elements0.append(address1)
                else:
                    break
            if len(elements0) >= 0:
                address0 = TreeNode(self._input[index1:self._offset], index1, elements0)
                self._offset = self._offset
            else:
                address0 = FAILURE
            self._cache['spaces'][index0] = (address0, self._offset)
            return address0



