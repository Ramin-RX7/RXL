"""
in all "TreeNodeN".init:: super(...) can be changed to TreeNode(...)
"""

__all__ = ["Load","Include","Until","Unless","Const","Array"]

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
class ParseError(SyntaxError):
    pass
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
        parser = grammar.Parser(input, actions, types)
        return parser.parse()





class Load:

    class TreeNode1(TreeNode):
        def __init__(self, text, offset, elements):
            super(Load.TreeNode1, self).__init__(text, offset, elements)
            self.indent = elements[0]
            self.pkg_name = elements[3]


    class Grammar(object):
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
            index2 = self._offset
            address1 = self._read_spaces()
            if address1 is FAILURE:
                address1 = TreeNode(self._input[index2:index2], index2, [])
                self._offset = index2
            if address1 is not FAILURE:
                elements0.append(address1)
                address2 = FAILURE
                chunk0, max0 = None, self._offset + 5
                if max0 <= self._input_size:
                    chunk0 = self._input[self._offset:max0]
                if chunk0 == 'load ':
                    address2 = TreeNode(self._input[self._offset:self._offset + 5], self._offset, [])
                    self._offset = self._offset + 5
                else:
                    address2 = FAILURE
                    if self._offset > self._failure:
                        self._failure = self._offset
                        self._expected = []
                    if self._offset == self._failure:
                        self._expected.append(('LOAD::load', '"load "'))
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
                        address4 = self._read_pkg_name()
                        if address4 is not FAILURE:
                            elements0.append(address4)
                            address5 = FAILURE
                            index4 = self._offset
                            address5 = self._read_spaces()
                            if address5 is FAILURE:
                                address5 = TreeNode(self._input[index4:index4], index4, [])
                                self._offset = index4
                            if address5 is not FAILURE:
                                elements0.append(address5)
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
                address0 = Load.TreeNode1(self._input[index1:self._offset], index1, elements0)
                self._offset = self._offset
            self._cache['load'][index0] = (address0, self._offset)
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
                        self._expected.append(('LOAD::spaces', '" "'))
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
                    if chunk1 is not None and Load.Grammar.REGEX_2.search(chunk1):
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


    class Parser(Grammar):
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
            tree = self._read_load()
            if tree is not FAILURE and self._offset == self._input_size:
                return tree
            if not self._expected:
                self._failure = self._offset
                self._expected.append(('LOAD', '<EOF>'))
            raise ParseError(format_error(self._input, self._failure, self._expected))



class Include:

    class TreeNode1(TreeNode):
        def __init__(self, text, offset, elements):
            super(Include.TreeNode1, self).__init__(text, offset, elements)
            self.indent = elements[0]
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
            address1 = self._read_spaces()
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
                    address3 = self._read_spaces()
                    if address3 is FAILURE:
                        address3 = TreeNode(self._input[index3:index3], index3, [])
                        self._offset = index3
                    if address3 is not FAILURE:
                        elements0.append(address3)
                        address4 = FAILURE
                        address4 = self._read_pkg_name()
                        if address4 is not FAILURE:
                            elements0.append(address4)
                            address5 = FAILURE
                            index4 = self._offset
                            address5 = self._read_spaces()
                            if address5 is FAILURE:
                                address5 = TreeNode(self._input[index4:index4], index4, [])
                                self._offset = index4
                            if address5 is not FAILURE:
                                elements0.append(address5)
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
                address0 = Include.TreeNode1(self._input[index1:self._offset], index1, elements0)
                self._offset = self._offset
            self._cache['include'][index0] = (address0, self._offset)
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
                        self._expected.append(('INCLUDE::spaces', '" "'))
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


    class Parser(Grammar):
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
            tree = self._read_include()
            if tree is not FAILURE and self._offset == self._input_size:
                return tree
            if not self._expected:
                self._failure = self._offset
                self._expected.append(('INCLUDE', '<EOF>'))
            raise ParseError(format_error(self._input, self._failure, self._expected))



class Until:
    class TreeNode1(TreeNode):
        def __init__(self, text, offset, elements):
            super(Until.TreeNode1, self).__init__(text, offset, elements)
            self.indent = elements[0]
            self.expr = elements[3]
            self.rest = elements[5]


    class Grammar(object):
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
                        self._expected.append(('UNTIL::spaces', '" "'))
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


    class Parser(Grammar):
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
            tree = self._read_until()
            if tree is not FAILURE and self._offset == self._input_size:
                return tree
            if not self._expected:
                self._failure = self._offset
                self._expected.append(('UNTIL', '<EOF>'))
            raise ParseError(format_error(self._input, self._failure, self._expected))



class Unless:
    class TreeNode1(TreeNode):
        def __init__(self, text, offset, elements):
            super(Unless.TreeNode1, self).__init__(text, offset, elements)
            self.indent = elements[0]
            self.expr = elements[3]
            self.rest = elements[5]


    class Grammar(object):
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
                        self._expected.append(('UNLESS::spaces', '" "'))
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


    class Parser(Grammar):
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
            tree = self._read_unless()
            if tree is not FAILURE and self._offset == self._input_size:
                return tree
            if not self._expected:
                self._failure = self._offset
                self._expected.append(('UNLESS', '<EOF>'))
            raise ParseError(format_error(self._input, self._failure, self._expected))



class Const:
    class TreeNode1(TreeNode):
        def __init__(self, text, offset, elements):
            super(Const.TreeNode1, self).__init__(text, offset, elements)
            self.indent = elements[0]
            self.varname = elements[3]
            self.var = elements[3]
            self.value = elements[7]


    class Grammar(object):
        REGEX_1 = re.compile('^[a-zA-Z_]')
        REGEX_2 = re.compile('^[a-zA-Z0-9_]')

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
                if chunk0 is not None and Const.Grammar.REGEX_1.search(chunk0):
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
                    if chunk1 is not None and Const.Grammar.REGEX_2.search(chunk1):
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


    class Parser(Grammar):
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
            tree = self._read_const()
            if tree is not FAILURE and self._offset == self._input_size:
                return tree
            if not self._expected:
                self._failure = self._offset
                self._expected.append(('CONST', '<EOF>'))
            raise ParseError(format_error(self._input, self._failure, self._expected))



class Array:
    class TreeNode1(TreeNode):
        def __init__(self, text, offset, elements):
            super(Array.TreeNode1, self).__init__(text, offset, elements)
            self.indent = elements[0]
            self.s = elements[14]
            self.varname = elements[3]
            self.var = elements[3]
            self.options = elements[6]
            self.values = elements[12]


    class TreeNode2(TreeNode):
        def __init__(self, text, offset, elements):
            super(Array.TreeNode2, self).__init__(text, offset, elements)
            self.s = elements[1]


    class TreeNode3(TreeNode):
        def __init__(self, text, offset, elements):
            super(Array.TreeNode3, self).__init__(text, offset, elements)
            self.s = elements[2]
            self.len = elements[1]


    class TreeNode4(TreeNode):
        def __init__(self, text, offset, elements):
            super(Array.TreeNode4, self).__init__(text, offset, elements)
            self.s = elements[1]
            self.type = elements[2]
            self.var = elements[2]


    class Grammar(object):
        REGEX_1 = re.compile('^[^}]')
        REGEX_2 = re.compile('^[a-zA-Z_]')
        REGEX_3 = re.compile('^[a-zA-Z0-9_]')
        REGEX_4 = re.compile('^[a-zA-Z0-9_]')

        def _read_array(self):
            address0, index0 = FAILURE, self._offset
            cached = self._cache['array'].get(index0)
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
                if chunk0 == 'array ':
                    address2 = TreeNode(self._input[self._offset:self._offset + 6], self._offset, [])
                    self._offset = self._offset + 6
                else:
                    address2 = FAILURE
                    if self._offset > self._failure:
                        self._failure = self._offset
                        self._expected = []
                    if self._offset == self._failure:
                        self._expected.append(('ARRAY::array', '"array "'))
                if address2 is not FAILURE:
                    elements0.append(address2)
                    address3 = FAILURE
                    address3 = self._read_s()
                    if address3 is not FAILURE:
                        elements0.append(address3)
                        address4 = FAILURE
                        address4 = self._read_var()
                        if address4 is not FAILURE:
                            elements0.append(address4)
                            address5 = FAILURE
                            address5 = self._read_s()
                            if address5 is not FAILURE:
                                elements0.append(address5)
                                address6 = FAILURE
                                chunk1, max1 = None, self._offset + 1
                                if max1 <= self._input_size:
                                    chunk1 = self._input[self._offset:max1]
                                if chunk1 == '[':
                                    address6 = TreeNode(self._input[self._offset:self._offset + 1], self._offset, [])
                                    self._offset = self._offset + 1
                                else:
                                    address6 = FAILURE
                                    if self._offset > self._failure:
                                        self._failure = self._offset
                                        self._expected = []
                                    if self._offset == self._failure:
                                        self._expected.append(('ARRAY::array', '"["'))
                                if address6 is not FAILURE:
                                    elements0.append(address6)
                                    address7 = FAILURE
                                    address7 = self._read_options()
                                    if address7 is not FAILURE:
                                        elements0.append(address7)
                                        address8 = FAILURE
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
                                                self._expected.append(('ARRAY::array', '"]"'))
                                        if address8 is not FAILURE:
                                            elements0.append(address8)
                                            address9 = FAILURE
                                            address9 = self._read_s()
                                            if address9 is not FAILURE:
                                                elements0.append(address9)
                                                address10 = FAILURE
                                                chunk3, max3 = None, self._offset + 1
                                                if max3 <= self._input_size:
                                                    chunk3 = self._input[self._offset:max3]
                                                if chunk3 == '=':
                                                    address10 = TreeNode(self._input[self._offset:self._offset + 1], self._offset, [])
                                                    self._offset = self._offset + 1
                                                else:
                                                    address10 = FAILURE
                                                    if self._offset > self._failure:
                                                        self._failure = self._offset
                                                        self._expected = []
                                                    if self._offset == self._failure:
                                                        self._expected.append(('ARRAY::array', '"="'))
                                                if address10 is not FAILURE:
                                                    elements0.append(address10)
                                                    address11 = FAILURE
                                                    address11 = self._read_s()
                                                    if address11 is not FAILURE:
                                                        elements0.append(address11)
                                                        address12 = FAILURE
                                                        chunk4, max4 = None, self._offset + 1
                                                        if max4 <= self._input_size:
                                                            chunk4 = self._input[self._offset:max4]
                                                        if chunk4 == '{':
                                                            address12 = TreeNode(self._input[self._offset:self._offset + 1], self._offset, [])
                                                            self._offset = self._offset + 1
                                                        else:
                                                            address12 = FAILURE
                                                            if self._offset > self._failure:
                                                                self._failure = self._offset
                                                                self._expected = []
                                                            if self._offset == self._failure:
                                                                self._expected.append(('ARRAY::array', '"{"'))
                                                        if address12 is not FAILURE:
                                                            elements0.append(address12)
                                                            address13 = FAILURE
                                                            index2, elements1, address14 = self._offset, [], None
                                                            while True:
                                                                chunk5, max5 = None, self._offset + 1
                                                                if max5 <= self._input_size:
                                                                    chunk5 = self._input[self._offset:max5]
                                                                if chunk5 is not None and Array.Grammar.REGEX_1.search(chunk5):
                                                                    address14 = TreeNode(self._input[self._offset:self._offset + 1], self._offset, [])
                                                                    self._offset = self._offset + 1
                                                                else:
                                                                    address14 = FAILURE
                                                                    if self._offset > self._failure:
                                                                        self._failure = self._offset
                                                                        self._expected = []
                                                                    if self._offset == self._failure:
                                                                        self._expected.append(('ARRAY::array', '[^}]'))
                                                                if address14 is not FAILURE:
                                                                    elements1.append(address14)
                                                                else:
                                                                    break
                                                            if len(elements1) >= 0:
                                                                address13 = TreeNode(self._input[index2:self._offset], index2, elements1)
                                                                self._offset = self._offset
                                                            else:
                                                                address13 = FAILURE
                                                            if address13 is not FAILURE:
                                                                elements0.append(address13)
                                                                address15 = FAILURE
                                                                chunk6, max6 = None, self._offset + 1
                                                                if max6 <= self._input_size:
                                                                    chunk6 = self._input[self._offset:max6]
                                                                if chunk6 == '}':
                                                                    address15 = TreeNode(self._input[self._offset:self._offset + 1], self._offset, [])
                                                                    self._offset = self._offset + 1
                                                                else:
                                                                    address15 = FAILURE
                                                                    if self._offset > self._failure:
                                                                        self._failure = self._offset
                                                                        self._expected = []
                                                                    if self._offset == self._failure:
                                                                        self._expected.append(('ARRAY::array', '"}"'))
                                                                if address15 is not FAILURE:
                                                                    elements0.append(address15)
                                                                    address16 = FAILURE
                                                                    address16 = self._read_s()
                                                                    if address16 is not FAILURE:
                                                                        elements0.append(address16)
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
            index2 = self._offset
            index3, elements1 = self._offset, []
            address2 = FAILURE
            address2 = self._read_s()
            if address2 is not FAILURE:
                elements1.append(address2)
                address3 = FAILURE
                index4 = self._offset
                address3 = self._read_w()
                if address3 is FAILURE:
                    address3 = TreeNode(self._input[index4:index4], index4, [])
                    self._offset = index4
                if address3 is not FAILURE:
                    elements1.append(address3)
                    address4 = FAILURE
                    address4 = self._read_s()
                    if address4 is not FAILURE:
                        elements1.append(address4)
                        address5 = FAILURE
                        index5 = self._offset
                        index6, elements2 = self._offset, []
                        address6 = FAILURE
                        chunk0, max0 = None, self._offset + 1
                        if max0 <= self._input_size:
                            chunk0 = self._input[self._offset:max0]
                        if chunk0 == ':':
                            address6 = TreeNode(self._input[self._offset:self._offset + 1], self._offset, [])
                            self._offset = self._offset + 1
                        else:
                            address6 = FAILURE
                            if self._offset > self._failure:
                                self._failure = self._offset
                                self._expected = []
                            if self._offset == self._failure:
                                self._expected.append(('ARRAY::options', '":"'))
                        if address6 is not FAILURE:
                            elements2.append(address6)
                            address7 = FAILURE
                            address7 = self._read_s()
                            if address7 is not FAILURE:
                                elements2.append(address7)
                                address8 = FAILURE
                                address8 = self._read_var()
                                if address8 is not FAILURE:
                                    elements2.append(address8)
                                else:
                                    elements2 = None
                                    self._offset = index6
                            else:
                                elements2 = None
                                self._offset = index6
                        else:
                            elements2 = None
                            self._offset = index6
                        if elements2 is None:
                            address5 = FAILURE
                        else:
                            address5 = Array.TreeNode4(self._input[index6:self._offset], index6, elements2)
                            self._offset = self._offset
                        if address5 is FAILURE:
                            address5 = TreeNode(self._input[index5:index5], index5, [])
                            self._offset = index5
                        if address5 is not FAILURE:
                            elements1.append(address5)
                        else:
                            elements1 = None
                            self._offset = index3
                    else:
                        elements1 = None
                        self._offset = index3
                else:
                    elements1 = None
                    self._offset = index3
            else:
                elements1 = None
                self._offset = index3
            if elements1 is None:
                address1 = FAILURE
            else:
                address1 = Array.TreeNode3(self._input[index3:self._offset], index3, elements1)
                self._offset = self._offset
            if address1 is FAILURE:
                address1 = TreeNode(self._input[index2:index2], index2, [])
                self._offset = index2
            if address1 is not FAILURE:
                elements0.append(address1)
                address9 = FAILURE
                address9 = self._read_s()
                if address9 is not FAILURE:
                    elements0.append(address9)
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
                if chunk0 is not None and Array.Grammar.REGEX_2.search(chunk0):
                    address2 = TreeNode(self._input[self._offset:self._offset + 1], self._offset, [])
                    self._offset = self._offset + 1
                else:
                    address2 = FAILURE
                    if self._offset > self._failure:
                        self._failure = self._offset
                        self._expected = []
                    if self._offset == self._failure:
                        self._expected.append(('ARRAY::var', '[a-zA-Z_]'))
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
                    if chunk1 is not None and Array.Grammar.REGEX_3.search(chunk1):
                        address4 = TreeNode(self._input[self._offset:self._offset + 1], self._offset, [])
                        self._offset = self._offset + 1
                    else:
                        address4 = FAILURE
                        if self._offset > self._failure:
                            self._failure = self._offset
                            self._expected = []
                        if self._offset == self._failure:
                            self._expected.append(('ARRAY::var', '[a-zA-Z0-9_]'))
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

        def _read_w(self):
            address0, index0 = FAILURE, self._offset
            cached = self._cache['w'].get(index0)
            if cached:
                self._offset = cached[1]
                return cached[0]
            chunk0, max0 = None, self._offset + 1
            if max0 <= self._input_size:
                chunk0 = self._input[self._offset:max0]
            if chunk0 is not None and Array.Grammar.REGEX_4.search(chunk0):
                address0 = TreeNode(self._input[self._offset:self._offset + 1], self._offset, [])
                self._offset = self._offset + 1
            else:
                address0 = FAILURE
                if self._offset > self._failure:
                    self._failure = self._offset
                    self._expected = []
                if self._offset == self._failure:
                    self._expected.append(('ARRAY::w', '[a-zA-Z0-9_]'))
            self._cache['w'][index0] = (address0, self._offset)
            return address0


    class Parser(Grammar):
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
            tree = self._read_array()
            if tree is not FAILURE and self._offset == self._input_size:
                return tree
            if not self._expected:
                self._failure = self._offset
                self._expected.append(('ARRAY', '<EOF>'))
            raise ParseError(format_error(self._input, self._failure, self._expected))


















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


    class Parser(Grammar):
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
            tree = self._read_untiless()
            if tree is not FAILURE and self._offset == self._input_size:
                return tree
            if not self._expected:
                self._failure = self._offset
                self._expected.append(('UNTILESS', '<EOF>'))
            raise ParseError(format_error(self._input, self._failure, self._expected))





