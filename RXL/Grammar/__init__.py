import re
import tokenize
from typing import Callable
from threading import Thread

import rx7 as rx

from .. import Errors as ERRORS
from .source import Source
from .regex import REGEX,get_regex


print = rx.style.print
Error = rx.style.log_error

CLASSES = (
    'date_time', 'system', 'terminal', 'style', 'io',
    'decorator', 'random', 'internet', 'files',
)
LOADED_PACKAGES = []


grammars = {
    "include" : True,
    # "load"  : True  ,
    "until"   : True,
    "unless"  : True,
    "func"    : True,
    "foreach" : True,
    "array"   : True,
    "$cmd"    : True,
    "$call"   : True,
    "$check"  : False,
    "$cls"    : True,
    "$clear"  : True
}



def get_skips(source:Source, index_line:str, stripped:str):
    if (not stripped) or stripped.startswith('#'):
            return 1
    if ('"""' in stripped  and
        not (("'''" in stripped)  and
        (stripped.index('"""')>stripped.index("'''")))):
        if not '"""' in stripped[stripped.index('"""')+3:]:
            for line_in_str,text_in_str in enumerate(source[index_line+1:],2):
                if '"""' in text_in_str:
                    skip = line_in_str
            return skip
    elif "'''" in stripped:
        if not "'''" in stripped[stripped.index("'''")+3:]:
            for line_in_str,text_in_str in enumerate(source[index_line+1:],2):
                if "'''" in text_in_str:
                    skip = line_in_str
            return skip
    return 0




#< Method,Module_Name,Print,Indent,Const >#
def define_structure(source:Source, file:str, debug:bool, configs:dict):
    Changeable = []
    for nom,line in enumerate(source[:15]):
        Stripped = line.strip()
        #] Skips
        if source.skip:
            source.skip -= 1
            continue
        elif skips := get_skips(source, nom, Stripped):
            source.skip = skips - 1
            Changeable += list(range(nom,nom+skips))
            continue

        #] Consts definition
        elif regex:=re.match(r"CONSTS:", Stripped, re.IGNORECASE):
            consts = {}
            source[nom] = "class CONSTS(metaclass=std.RXL.Lang.Singleton):"
            last_line = nom
            until = nom
            indent = "  "
            while True:
                until += 1
                if (not source[until].strip()) or (source[until].lstrip().startswith("#")):
                    # print(f"Skip {until}")
                    if not source[until].strip():
                        last_line = until
                    continue
                elif len(source[until].lstrip()) == len(source[until]):
                    break

                if line_regex := re.match(r"(?P<indent>\s+)(?P<varname>\w+)\s*=\s*(?P<value>.+)",
                                          source[until]):
                    consts[line_regex.group("varname")] = line_regex.group("value")
                    source[until] = f"{indent}{line_regex.group('varname')} = " \
                                    f"std.RXL.Lang.constant(lambda:({line_regex.group('value')}))"
                    last_line = until
                    # indent = line_regex.group('indent')
                else:
                    # print(f"Unknown: {until}")
                    pass
            # text = text.encode('unicode-escape').decode().replace('\\\\', '\\')
            if source[last_line].strip():
                source[last_line] = source[last_line]+ ";  __slots__ = {}"
            else:
                if source[last_line-1]:
                    source[last_line-1] = source[last_line-1]+";  __slots__ = {}"
                else:
                    source[last_line-1] = indent+"__slots__ = {}"

            if source[until-1].strip():
                source.insert(until, "CONSTS = CONSTS()")
                source.lines_added += 1
            else:
                source[until-1] = "CONSTS = CONSTS()"
            break

        else:
            break


    configs["structure"]['lib_version'] = "rx7"
    LIB_NAME = configs["structure"]["lib_name"]
    #] Bases
    STRUCTURES = [
       f"import {configs['structure']['lib_version']} as {LIB_NAME}",
       f"std = rx = {LIB_NAME}",
        "import importlib",
        "std.RXL = importlib.import_module('RXL')",
        "std.RXL.Lang = importlib.import_module('RXL.Lang')",
        "std.RXL.NewFeatures = importlib.import_module('RXL.NewFeatures')",
        "del importlib"
        "std.array = std.RXL.NewFeatures.array",
       f"input = {LIB_NAME}.IO.selective_input",
       f"Check_Type = {LIB_NAME}.Check_Type",
        "apply = std.RXL.Lang.apply; map = NotImplemented"
    ]
    match configs["structure"]['print']:
        case 'stylized':
            STRUCTURES.append(f"print = {LIB_NAME}.style.print")
        case 'pprint':
            STRUCTURES.append(f"print = {LIB_NAME}.style.pprint")
        case _:
            pass
    #] App Info
    for key,value in configs['info'].items():
        STRUCTURES.append(f"setattr(std,'{key}',{value})")

    if len(Changeable):
        for line_nom in Changeable:
            if not STRUCTURES:
                break
            if line_nom == Changeable[-1]:
                source[line_nom] = ';'.join(STRUCTURES)
                break
            else:
                source[line_nom] = STRUCTURES.pop(0)
    else:
        if debug:
            Error(f'{file}> Not (Enough) Empty-lines at begining of file',add_time=False)
        source.insert(0, ';'.join(STRUCTURES))

    if not configs["structure"]["end_exit"]:
        source.append(f'{LIB_NAME}.io.getpass("Press [Enter] to Exit")')

    return source





#< Syntax >#
def check_synta(source:Source, file:str, debug:bool, configs:dict) -> tuple[Source,list[Thread]]:

    threads = []
    working_path = rx.files.dirname(file)

    source:Source[str] = Source(source, file)
    for Line_Nom,Text in enumerate(source, 1):
        Stripped = Text.strip()

        #] Check for skips
        if source.skip:
            source.skip -= 1
            continue
        if skips := get_skips(source,Line_Nom-1, Stripped):
            if skips is True:
                continue
            source.skip = skips
            continue


        for name,regex_check in grammars.items():
            if Stripped.startswith(f'{name} ')  or  Stripped==name:
                if regex_check:
                    Regex = get_regex(name, Text, file, Line_Nom)
                else:
                    Regex = Text
                source.call_syntax_f(name, Line_Nom, Regex)
                break


        #] Memory Location of Object
        if Regex:=re.search(r'[,\(\[\{\+=: ]&(?P<var>.+)', Text): #[^a-zA-Z0-9'"]
            source[Line_Nom-1] = Text.replace("&"+Regex.group("var"),f'hex(id({Regex.group("var")}))')

        #] Func Type checker
        elif (Stripped.startswith('def ') or Stripped.startswith('func '))  and  configs["structure"]["func_type_checker"]:  # Make it regex?
            if Stripped.startswith("func "):
                source[Line_Nom-1] = source[Line_Nom-1].replace('func', 'def', 1)
                indent = Text.index("func ")
            else:
                indent = Text.index('def ')
            # if SOURCE[Line_Nom-2].strip().endswith('Check_Type'):
            #    SOURCE[Line_Nom-2]= re.search(r'(\s*)',Text).group(1)+f'@std.Check_Type'
            if source[Line_Nom-2].strip().startswith('@'):
                continue
            source.insert(Line_Nom-1, f'{" "*indent}@std.Check_Type')
            source.skip = 1
            source.lines_added += 1

        #] do_while
        elif Stripped.startswith('do '     )  or  Stripped=='do':
            if not (Regex:=REGEX.DoWhile.do.match(Text)):
                raise SyntaxError

            Indent = Regex.group('Indent')

            LN = int(Line_Nom)
            while not (Regex:=re.search(r'(?P<Indent>\s*).+', source[LN])):
                LN += 1
            Indent_Content = Regex.group('Indent')

            WHILE_LINE = 0
            LINE = int(Line_Nom)
            while not WHILE_LINE:
                try:
                    if re.search(Indent+r'while\s*\(.+\)',source[LINE]):
                        WHILE_LINE = int(LINE)
                    else:
                        LINE += 1
                except IndexError:
                    raise ERRORS.SyntaxError(file,Line_Nom,Text,"'do' defined without 'while'")

            i = 1
            for ln in range(Line_Nom,WHILE_LINE):
                source.insert(WHILE_LINE+i, source[ln])
                i+=1

            for ln in range(Line_Nom,WHILE_LINE):
                source[ln] = source[ln].replace(Indent_Content,'',1)

            source[Line_Nom-1] = ''
            source[WHILE_LINE] = source[WHILE_LINE]+':'

        #] Load User-Defined Modules
        elif Stripped.startswith('load ' )  or  Stripped=='load':
            Regex = get_regex('load', Text, file, Line_Nom)
            Packages = re.split(r'\s*,\s*', Regex.group("packages"))
            for package in Packages:
                path = f"{working_path}/{package}.rxl"
                if not rx.files.exists(path):
                    raise ERRORS.ModuleNotFoundError(file, package, Text, Line_Nom)
                full_path = rx.files.abspath(path)
                from ..RXL import convert_source
                source = convert_source(full_path,True,debug,False)
                rx.write(full_path.removesuffix(".rxl")+".py", source)
            source[Line_Nom-1] = source[Line_Nom-1].replace("load","import",1)

        elif Stripped.startswith('$checkwait ')  or  Stripped=='$checkwait':
            raise NotImplementedError
            Regex = REGEX.Commands.checkwait.match(Text)
            if not Regex:
                raise ERRORS.SyntaxError(file,Line_Nom,Stripped,f"Wrong use of '$checkwait'")
            needed_lines = 3
            if Regex.group("Then"):
                #print('Then True')
                needed_lines += 1
                else_ =  f' {Indent}else: {Regex.group("Then")}'
            else:
                else_ = ''
            if Regex.group('Anyway'):
                #print('Anyway True')
                needed_lines += 1
                finally_ =  f' {Indent}finally: {Regex.group("Anyway")}'
            else:
                #print('Anyway False')
                finally_ = ''

            nofound = True
            line = int(Line_Nom)
            pos_lines = 0
            free_lines = []
            free_lines.append(line-1)
            while (nofound and line!=len(source)):
                if  source[line].strip() or pos_lines>=needed_lines:
                    nofound = False
                else:
                    free_lines.append(line)
                    pos_lines+=1
                line+=1
            line = int(Line_Nom-2)
            pre_lines = 0
            nofound = True
            while (nofound and line!=1):
                if source[line].strip() or len(free_lines)>=needed_lines:
                    nofound = False
                else:
                    free_lines.append(line)
                    pre_lines+=1
                line-=1

            if len(free_lines)<needed_lines:
                #print(free_lines,'red')
                ERRORS.RaiseError('SpaceError',f"'$check' should have one extra blank line around it " +
                                               f"per any extra keywords ({needed_lines-1} lines needed)",
                                  Text,Line_Nom,file)

            free_lines.sort()
            Indent   =   Regex.group('Indent')
            try_     =   f' {Indent}try: {Regex.group("Test")}'
            except_  =   f' {Indent}except: pass'

            source[free_lines[0]] =  Indent+"while True:"
            source[free_lines[1]] =  Indent+try_+";break"
            source[free_lines[2]] =  Indent+except_
            if else_:
                source[free_lines[3]] =  Indent+else_
            if finally_:
                source[free_lines[4]] =  Indent+finally_

            source.lines_added += needed_lines

        #print(f"{Line_Nom} :: {time.time()-t} {Striped[:5]}",'red')
    return source,threads





class IndentCheck:
    """
    This Class is a copy of tabnanny module in standard library
    About half of the methods that are not used are deleted from the code
    SOURCE: https://github.com/python/cpython/blob/3.10/Lib/tabnanny.py
    """
    class NannyNag(Exception):
        def __init__(self, lineno, msg, line):
            self.lineno, self.msg, self.line = lineno, msg, line
        def get_lineno(self):
            return self.lineno
        def get_msg(self):
            return self.msg
        def get_line(self):
            return self.line


    @staticmethod
    def check(file):
        try:
            f = tokenize.open(file)
        except OSError as msg:
            return (False,f"I/O Error: {msg}")

        try:
            IndentCheck.process_tokens(tokenize.generate_tokens(f.readline))
        except tokenize.TokenError as msg:
            return (False,f"Token Error: {msg}")
        except IndentationError as msg:
            return (False,f"Indentation Error: {msg}")
        except IndentCheck.NannyNag as nag:
            badline = nag.get_lineno()
            line = nag.get_line()
            if ' ' in file: file = '"' + file + '"'
            else: print(file, badline, repr(line))
            return (False,)
        finally:
            f.close()

        return (True,True)


    class Whitespace:
        S, T = ' ','\t'

        def __init__(self, ws):
            self.raw  = ws
            S, T = IndentCheck.Whitespace.S, IndentCheck.Whitespace.T
            count = []
            b = n = nt = 0
            for ch in self.raw:
                if ch == S:
                    n = n + 1
                    b = b + 1
                elif ch == T:
                    n = n + 1
                    nt = nt + 1
                    if b >= len(count):
                        count = count + [0] * (b - len(count) + 1)
                    count[b] = count[b] + 1
                    b = 0
                else:
                    break
            self.n    = n
            self.nt   = nt
            self.norm = tuple(count), b
            self.is_simple = len(count) <= 1

        def longest_run_of_spaces(self):
            count, trailing = self.norm
            return max(len(count)-1, trailing)

        def indent_level(self, tabsize):
            count, trailing = self.norm
            il = 0
            for i in range(tabsize, len(count)):
                il = il + i//tabsize * count[i]
            return trailing + tabsize * (il + self.nt)

        def equal(self, other):
            return self.norm == other.norm

        def not_equal_witness(self, other):
            n = max(self.longest_run_of_spaces(),
                    other.longest_run_of_spaces()) + 1
            a = []
            for ts in range(1, n+1):
                if self.indent_level(ts) != other.indent_level(ts):
                    a.append( (ts,
                            self.indent_level(ts),
                            other.indent_level(ts)) )
            return a

        def less(self, other):
            if self.n >= other.n:
                return False
            if self.is_simple and other.is_simple:
                return self.nt <= other.nt
            n = max(self.longest_run_of_spaces(),
                    other.longest_run_of_spaces()) + 1
            for ts in range(2, n+1):
                if self.indent_level(ts) >= other.indent_level(ts):
                    return False
            return True

        def not_less_witness(self, other):
            n = max(self.longest_run_of_spaces(),
                    other.longest_run_of_spaces()) + 1
            a = []
            for ts in range(1, n+1):
                if self.indent_level(ts) >= other.indent_level(ts):
                    a.append( (ts,
                            self.indent_level(ts),
                            other.indent_level(ts)) )
            return a


    @staticmethod
    def format_witnesses(w):
        firsts = (str(tup[0]) for tup in w)
        prefix = "at tab size"
        if len(w) > 1:
            prefix = prefix + "s"
        return prefix + " " + ', '.join(firsts)


    @staticmethod
    def process_tokens(tokens):
        INDENT = tokenize.INDENT
        DEDENT = tokenize.DEDENT
        NEWLINE = tokenize.NEWLINE
        JUNK = tokenize.COMMENT, tokenize.NL
        indents = [IndentCheck.Whitespace("")]
        check_equal = 0

        for (type, token, start, end, line) in tokens:
            if type == NEWLINE:
                check_equal = 1

            elif type == INDENT:
                check_equal = 0
                thisguy = IndentCheck.Whitespace(token)
                if not indents[-1].less(thisguy):
                    witness = indents[-1].not_less_witness(thisguy)
                    msg = "indent not greater e.g. " + IndentCheck.format_witnesses(witness)
                    raise IndentCheck.NannyNag(start[0], msg, line)
                indents.append(thisguy)

            elif type == DEDENT:
                check_equal = 1

                del indents[-1]

            elif check_equal and type not in JUNK:
                check_equal = 0
                thisguy = IndentCheck.Whitespace(line)
                if not indents[-1].equal(thisguy):
                    witness = indents[-1].not_equal_witness(thisguy)
                    msg = "indent not equal e.g. " + IndentCheck.format_witnesses(witness)
                    raise IndentCheck.NannyNag(start[0], msg, line)
