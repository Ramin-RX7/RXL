import rx7 as rx
from .. import Errors as ERRORS
from .regex import REGEX



class Source(list):
    def __init__(self, __iterable, file):
        super().__init__(__iterable)
        self.lines_added = 0
        self.file = file




    def call_syntax_f(self, name, line_nom, regex):
        if name.startswith("$"):
            name = name[1:]
        # print(name)
        eval(f"self.{name}")(line_nom,regex)


    def include(self, line_nom, regex):
        CLASSES = (
            'date_time', 'system', 'terminal', 'style', 'io',
            'decorator', 'random', 'internet', 'files',
        )
        attrs = dir(rx)
        Indent = regex.group('Indent')
        items = regex.group('objects').split(",")
        new_items = []
        for item in items:
            if item.startswith("*"):
                class_ = item[1:]
                if class_ in CLASSES:
                    new_items.append(f"from rx7.{class_} import *")
                else:
                    raise AttributeError("Class not found to get all")
            elif ":" in item:
                class_ = item[:item.index(":")].strip()
                if class_ not in CLASSES:
                    raise AttributeError("Class not found to get some")
                new_item = f"from rx7.{class_} import "
                items_inside = item[item.index(":")+1:].replace(" ","").split("/")
                for item_inside in items_inside:
                    if item_inside in dir(eval(f"rx.{class_}")):
                        new_item += item_inside + ","
                    else:
                        raise AttributeError("Not in class")
                new_items.append(new_item[:-1])  # [:-1] to remove last `,`
            elif item in attrs:
                new_items.append(f"from rx7 import {item}")
            else:
                raise AttributeError("Not found in standard library")
        self[line_nom-1] = Indent+";".join(new_items)


    def load(self, line_nom, regex):
        ...


    def until(self, line_nom, regex):
        self[line_nom-1] = f"{regex.group('Indent')}while not ({regex.group('Expression')}):{regex.group('Rest')}"


    def unless(self, line_nom, regex):
        self[line_nom-1] = f"{regex.group('Indent')}if not ({regex.group('Expression')}):{regex.group('Rest')}"


    def func(self, line_nom, regex):
        self[line_nom-1].replace('func', 'def', 1)


    def foreach(self, line_nom, regex):
        indent, iterable, forvar = regex.groups()
        modified = f"{indent}for {forvar} in {iterable}:"
        self[line_nom-1] = modified


    def array(self, line_nom, regex):
        Indent  = regex.group('Indent')
        VarName = regex.group('VarName')
        Length  = regex.group('Length')
        Type    = regex.group('Type')
        Content = regex.group('Content')
        Length  =  '' if not Length  else ', max_length='+Length
        Type    =  '' if not Type    else ', type_='+Type
        # if not any([Length, Type]):
            # raise ERRORS.SyntaxError("length and type of the array elements should be set")
        self[line_nom-1] = f'{Indent}{VarName} = std.array(({Content},){Type}{Length})'


    def cmd(self, line_nom, regex):
        self[line_nom-1] = f'{regex.group("Indent")}std.terminal.run("{regex.group("Command") if regex else "cmd"}")'


    def call(self, line_nom, regex):
        Indent = regex.group('Indent'  )
        Delay  = regex.group('Time'    )
        Func   = regex.group('Function')
        self[line_nom-1] = f"{Indent}std.call({Func},delay={Delay})"


    def check(self, line_nom, text):
        Regex = (
            REGEX.Commands.Check.thenanyway.match(text) or
            REGEX.Commands.Check.anyway.match(text) or
            REGEX.Commands.Check.then.match(text) or
            REGEX.Commands.Check.ignore.match(text)
        )
        if not Regex:
            raise ERRORS.SyntaxError(self.file,line_nom,text,f"Wrong use of '$check'")
        regex_dict = Regex.groupdict()
        Indent   =   regex_dict.get('Indent', '')
        needed_lines = 2
        if regex_dict.get('Then', ''):
            needed_lines += 1
            else_ =  f'{Indent}else: {regex_dict["Then"]}'
        else:
            else_ = ''
        if regex_dict.get('Anyway', ''):
            needed_lines += 1
            finally_ =  f'{Indent}finally: {regex_dict["Anyway"]}'
        else:
            finally_ = ''

        nofound = True
        line = int(line_nom)
        pos_lines = 0
        free_lines = []
        free_lines.append(line-1)
        while (nofound and line!=len(self)):
            if  self[line].strip() or pos_lines>=needed_lines:
                nofound = False
            else:
                free_lines.append(line)
                pos_lines+=1
            line+=1
        line = int(line_nom-2)
        pre_lines = 0
        nofound = True
        while (nofound and line!=1):
            if self[line].strip() or len(free_lines)>=needed_lines:
                nofound = False
            else:
                free_lines.append(line)
                pre_lines+=1
            line-=1

        if len(free_lines)<needed_lines:
            ERRORS.RaiseError('SpaceError',f"'$check' should have one extra blank line around it " +
                                           f"per any extra keywords ({needed_lines-1} lines needed)",
                              text,line_nom,self.file,self.lines_added)

        free_lines.sort()
        Indent   =   Regex.group('Indent')
        try_     =   f'{Indent}try: {Regex.group("Test")}'
        except_  =   f'{Indent}except: pass'

        self[free_lines[0]] =  Indent+try_
        self[free_lines[1]] =  Indent+except_
        if else_:
            self[free_lines[2]] =  Indent+else_
        if finally_:
            l = 3 if else_ else 2
            self[free_lines[l]] =  Indent+finally_

        self.lines_added += needed_lines
