import re
import tokenize

import rx7 as rx

from .Lib import *
from . import Errors as ERRORS



print = rx.style.print
Error = rx.style.log_error

CLASSES = (
    'date_time', 'system', 'terminal', 'style', 'io',
    'decorator', 'random', 'internet', 'files',
)
LOADED_PACKAGES = []
Lines_Added = 0





#< List of all regex patterns >#
class REGEX:

    include = re.compile(r'(?P<Indent>\s*)include \s*(?P<objects>.+)\s*')

    load = re.compile(r'(?P<indent>\s*)load \s*(?P<packages>\w+,?)?')

    _memory_loc = re.compile(r'[,\(\[\{\+=: ]&(?P<var>\w+)')

    until = re.compile(r'(?P<Indent>\s*)until \s*(?P<Expression>.+):(?P<Rest>.*)')

    unless = re.compile(r'(?P<Indent>\s*)unless \s*(?P<Expression>.+):(?P<Rest>.*)')

    foreach = re.compile(r'(?P<indent>\s*)foreach \s*(?P<iterable>.+)\[(?P<forvar>\w+)\]:\s*')

    func = re.compile(r'func \s*(?P<Expression>.+)')

    class DoWhile:
        do = re.compile(r'(?P<Indent>\s*)do\s*:\s*')
        _while = re.compile(r'while\s*\(.+\)')

    _array = re.compile(r'(?P<Indent>\s*)array \s*(?P<VarName>\w+)\s*\[\s*((?P<Length>\w+)?\s*(:?\s*(?P<Type>\w+))?\s*)?\]\s*=\s*{(?P<Content>.*)}\s*')

    class Commands:

        check = re.compile(r'(?P<Indent>\s*)\$check \s*(?P<Test>[^\s]+)(\s* then (?P<Then>.+))?( \s*anyway(s)? (?P<Anyway>.+))?')

        checkwait = re.compile(r'(?P<Indent>\s*)\$checkwait \s*(?P<Test>[^\s]+)(\s* then (?P<Then>.+))?( \s*anyway(s)? (?P<Anyway>.+))?')

        cmd = re.compile(r'(?P<Indent>\s*)\$cmd \s*(?P<Command>.+)')

        call = re.compile(r'(?P<Indent>\s*)\$call (?P<Function>.+) \s*in \s*(?P<Time>.+)')

        _clear = NotImplemented





#< Method,Module_Name,Print,Indent,Const >#
def define_structure(SOURCE, FILE, DEBUG):
    """"""
    """
    BASE OPTIONS:
      OPTION NAME        DEFAULT VALUE       DESCRYPTION"
      Lib-Name           sc                  Shortcut for RXL Tools and functions (also "Modulename")'
      Print              stylized            Print function to use. Valid Choices: [normal,stylized]'
      func-type-checker  True                Check if arguments of a function are in wrong type'
      End-Exit           True                Exit after executing the code or not'
      #Method            normal              Method of loading tools.'
      #                                        Valid Choices: [normal,[lite,fast]] (also "Package-Version)"'

    "OPTIONS" SHOULD BE DEFINED AFTER "BASE OPTIONS"'
    """
    global Lines_Added

    IndentCheck.check(FILE)


    #< OPTIONS >#
    LIB_VERSION  = 'rx7'
    LIB_SHORTCUT = 'std'
    PRINT_TYPE = 'stylized'
    TYPE_SCANNER = False
    # Allow_Reload = False
    map_defd = False
    Changeable = []
    INFO = {
        'Version':  '1.0.0',
        'Author' :  rx.system.accname(),
        'Title'  :  rx.files.basename(FILE).split(".")[0]}
    Skip = 0
    end = False

    for nom,line in enumerate(SOURCE[:20]):

        rstrip = line.rstrip()
        Stripped = line.strip()

        # if end:   # When all remaining lines are docstring
            # break
        if Skip:  # When Adding An Extra Line Like Decorators
            Skip = Skip-1
            continue
        # Ignore Docstrings and Comments
        if (not Stripped)  or  Stripped.startswith('#'):
            Changeable.append(nom)
            continue
        elif '"""' in line  and  not ("'''" in line and line.index('"""')>line.index("'''")):
            if not '"""' in line[line.index('"""')+3:]:
                for line_in_str,line_in_str in enumerate(SOURCE[nom:],1):
                    if '"""' in line_in_str:
                        Skip = line_in_str
                # if Skip > (10-nom):
                    # end = True
                continue
        elif "'''" in line:
            if not "'''" in line[line.index("'''")+3:]:
                for line_in_str,text_in_str in enumerate(SOURCE[nom:10],1):
                    if "'''" in text_in_str:
                        Skip = line_in_str
                # if Skip > (10-nom):
                    # end = True
                continue

        #] Get Shortcut Name
        elif regex:=re.match(r'Lib-?Name\s*:\s*(?P<name>.+)', rstrip, re.IGNORECASE):
            LIB_SHORTCUT = regex.group("name")
            if not re.match(r'\w+', LIB_SHORTCUT):
                raise ERRORS.ValueError(msg='Invalid Value For `Lib-Name`',
                                        File=FILE)

        #] Print Function Method
        elif regex:=re.match(r'(P|p)rint\s*:\s*(?P<type>.+)', rstrip, re.IGNORECASE):
            PRINT_TYPE = regex.group("type").lower()
            if not (PRINT_TYPE in ("normal","stylized")):
                raise ERRORS.ValueError(FILE, 'print', PRINT_TYPE, line,
                                       SOURCE.index(line), ['stylized','normal'])

        #] Function Type Scanner
        elif regex:=re.match(r'func(tion)?-?type-?checker\s*:\s*(?P<flag>.+)',rstrip,re.IGNORECASE):
            TYPE_SCANNER = regex.group("flag").capitalize()
            if TYPE_SCANNER not in ("True","False"):
                raise ERRORS.ValueError(FILE, 'func_type_checker', TYPE_SCANNER, line,
                                       SOURCE.index(line), "[True,False]")

        #] Exit at the end
        elif regex:=re.match(r'End-?Exit\s*:\s*(?P<flag>.+)', rstrip, re.IGNORECASE):
            flag = regex.group("flag").capitalize()
            if flag in ("True","False"):
                if flag == "False":
                    SOURCE.append('__import__("getpass").getpass("Press [Enter] to Exit")')
            else:
                raise ERRORS.ValueError(FILE, 'Exit', flag, line,
                                       SOURCE.index(line), "[True,False]")

        #] Reload Module
        elif regex:=re.match(r'Allow-?Reload\s*:(?P<flag>.+)', rstrip, re.IGNORECASE):
            raise NotImplementedError
            flag = regex.group("flag").capitalize()
            if flag in ("False","True")  and  flag=="True":
                Allow_Reload = True
            else:
                raise ERRORS.ValueError(FILE, 'Allow-Reload', flag, line,
                                        SOURCE.index(line)  , "[True,False]")

        #] Get Version (Method) of Tools
        elif regex:=re.match(r'Lib-?Version\s*:\s*\w+', rstrip, re.IGNORECASE):
            raise NotImplementedError
            #if BASED:
            #    raise ERRORS.BaseDefinedError('Method/Version', line, SOURCE[:5].index(line), FILE)
            StripLow = line.strip().lower()
            if StripLow.endswith('lite') or StripLow.endswith('fast'):
                LIB_VERSION = 'rx7.lite'
            elif not StripLow.endswith('normal'):
                stripped = line[line.index(':')+1:].strip()
                raise ERRORS.ValueError(FILE, 'Method', stripped, line,
                                    SOURCE[:5].index(line), ['lite','normal'])
            SOURCE[nom] = ''
            Changeable.append(nom)

        #] Consts definition
        elif regex:=re.match(r"CONSTS:", rstrip, re.IGNORECASE):
            consts = {}
            SOURCE[nom] = "class CONSTS(metaclass=std.RXL.Lang.Singleton):"
            last_line = nom
            until = nom
            indent = "  "
            while True:
                until += 1
                if (not SOURCE[until].strip()) or (SOURCE[until].lstrip().startswith("#")):
                    # print(f"Skip {until}")
                    if not SOURCE[until].strip():
                        last_line = until
                    continue
                elif len(SOURCE[until].lstrip()) == len(SOURCE[until]):
                    break

                if line_regex := re.match(r"(?P<indent>\s+)(?P<varname>\w+)\s*=\s*(?P<value>.+)",
                                          SOURCE[until]):
                    consts[line_regex.group("varname")] = line_regex.group("value")
                    SOURCE[until] = f"{indent}{line_regex.group('varname')} = " \
                                    f"std.RXL.Lang.constant(lambda:({line_regex.group('value')}))"
                    last_line = until
                    # indent = line_regex.group('indent')
                else:
                    # print(f"Unknown: {until}")
                    pass
            # text = text.encode('unicode-escape').decode().replace('\\\\', '\\')
            if SOURCE[last_line].strip():
                SOURCE[last_line] = SOURCE[last_line]+ ";  __slots__ = {}"
            else:
                if SOURCE[last_line-1]:
                    SOURCE[last_line-1] = SOURCE[last_line-1]+";  __slots__ = {}"
                else:
                    SOURCE[last_line-1] = indent+"__slots__ = {}"

            if SOURCE[until-1].strip():
                SOURCE.insert(until, "CONSTS = CONSTS()")
                Lines_Added += 1
            else:
                SOURCE[until-1] = "CONSTS = CONSTS()"

            Skip = until - nom
            continue


        #] Version
        elif Regex:=re.match(r'Version\s*:\s*(?P<Version>[0-9]+(\.[0-9]+)?(\.[0-9]+)?)',
                             rstrip, re.IGNORECASE):
            INFO['Version'] = Regex.group('Version')
        #] Title
        elif Regex:=re.match(r'Title\s*:\s*(?P<Title>[^>]+)(>.+)?',
                             rstrip, re.IGNORECASE):
            INFO['Title'] = Regex.group('Title')
        #] Author
        elif Regex:=re.match(r'Author\s*:\s*(?P<Author>.+)',
                             rstrip, re.IGNORECASE):
            INFO['Author'] = Regex.group('Author')

        elif re.search(r'^(def)|(class)\s+map\s*\(',Stripped)  or  re.search(r'^map\s*=',Stripped):
            map_defd = True

        else:
            break

        Changeable.append(nom)
        SOURCE[nom] = ''


    #] Bases
    STRING = []
    STRING.append(f"import {LIB_VERSION} as {LIB_SHORTCUT}")
    STRING.append(f"std = rx = {LIB_SHORTCUT};import importlib;"
                   "std.RXL = importlib.import_module('RXL');"
                   "std.RXL.Lang = importlib.import_module('RXL.Lang')")
    STRING.append(f"print = {LIB_SHORTCUT+'.style.print' if PRINT_TYPE=='stylized' else 'print'}")
    #] Direct Attributes
    STRING.append(F"input = {LIB_SHORTCUT}.IO.selective_input")
    STRING.append(f"Check_Type = {LIB_SHORTCUT}.Check_Type")
    #]
    if not map_defd:
        STRING.append("apply = lambda f,iterable: type(iterable)(__import__('builtins').map(f,iterable)) ; map = None")
    #] App Info
    for key,value in INFO.items():
        STRING.append(f"setattr(std,'{key}','{value}')")

    if len(Changeable):
        for line in Changeable:
            if line == Changeable[-1]:
                SOURCE[line] = ';'.join(STRING)
            else:
                try:
                    SOURCE[line] = STRING.pop(0)
                except IndexError:
                    break
    else:
        if DEBUG:
            Error(f'{FILE}> No (Enough) Base-Option/Empty-lines at begining of file',add_time=False)
        SOURCE.insert(0, ';'.join(STRING))

    return (SOURCE,
            LIB_VERSION, LIB_SHORTCUT,
            TYPE_SCANNER, INFO)





#< Syntax >#
def syntax(SOURCE,
           MODULE_VERSION ,  MODULE_SHORTCUT,
           TYPE_SCANNER   ,
           FILE           ,  DEBUG):
    global Lines_Added
    Skip = 0
    THREADS = []
    working_path = rx.files.dirname(FILE)

    for Line_Nom,Text in enumerate(SOURCE, 1):
        Stripped = Text.strip()

        #] When Adding An Extra Line Like Decorators
        if Skip:
            Skip = Skip-1
            #print(Skip)
            continue

        # Ignore Docstrings and Comments
        if Stripped.startswith('#')  or  not Stripped:
            continue
        elif '"""' in Text  and  not ("'''" in Text and Text.index('"""')>Text.index("'''")):
            if not '"""' in Text[Text.index('"""')+3:]:
                for line_in_str,text_in_str in enumerate(SOURCE[Line_Nom:],1):
                    if '"""' in text_in_str:
                        Skip = line_in_str
                        #print(Skip)
                continue
        elif "'''" in Text:
            if not "'''" in Text[Text.index("'''")+3:]:
                for line_in_str,text_in_str in enumerate(SOURCE[Line_Nom:],1):
                    if "'''" in text_in_str:
                        Skip = line_in_str
                        #print(Skip)
                continue


        if False: pass   # Just to make rest of the conditions look similar

        #] Include
        elif Stripped.startswith('include ')  or  Stripped=='include':
            Regex = REGEX.include.match(Text)
            if not Regex:
                raise ERRORS.SyntaxError(FILE,Line_Nom,Stripped,f"Wrong use of 'include'")
            attrs = dir(rx)
            Indent = Regex.group('Indent')
            items = Regex.group('objects').split(",")
            new_items = []
            # print(items)
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
            SOURCE[Line_Nom-1] = ";".join(new_items)


        #] Func Type checker
        elif (Stripped.startswith('def ') or Stripped.startswith('func '))  and  TYPE_SCANNER:  # Make it regex?
            if Stripped.startswith("func "):
                SOURCE[Line_Nom-1] = SOURCE[Line_Nom-1].replace('func', 'def', 1)
                indent = Text.index("func ")
            else:
                indent = Text.index('def ')
            # if SOURCE[Line_Nom-2].strip().endswith('Check_Type'):
            #    SOURCE[Line_Nom-2]= re.search(r'(\s*)',Text).group(1)+f'@std.Check_Type'
            if SOURCE[Line_Nom-2].strip().startswith('@'):
                continue
            SOURCE.insert(Line_Nom-1, f'{" "*indent}@{MODULE_SHORTCUT}.Check_Type')
            Skip = 1
            Lines_Added += 1


        #] Load User-Defined Modules
        elif Stripped.startswith('load ')  or  Stripped=='load':
            Regex = REGEX.load.match(Text)
            if not Regex:
                raise ERRORS.SyntaxError(FILE,Line_Nom,Stripped,f"Wrong use of 'load'")
            Packages = re.split(r'\s*,\s*', Regex.group("packages"))
            for package in Packages:
                path = f"{working_path}/{package}.rxl"
                if not rx.files.exists(path):
                    raise ERRORS.ModuleNotFoundError(FILE, package, Text, Line_Nom)
                full_path = rx.files.abspath(path)
                from .RXL import convert_source
                source = convert_source(full_path,True,DEBUG,False)
                rx.write(full_path.replace(".rxl",".py"), source)
            SOURCE[Line_Nom-1] = SOURCE[Line_Nom-1].replace("load","import",1)


        #] Memory Location of Object
        elif Regex:=re.search(r'[,\(\[\{\+=: ]&(?P<var>\w+)', Text): #[^a-zA-Z0-9'"]
            SOURCE[Line_Nom-1] = Text.replace("&"+Regex.group("var"),f'hex(id({Regex.group("var")}))')


        #] until & unless & foreach & func
        elif Stripped.startswith('until '  )  or  Stripped=='until':
            Regex = REGEX.until.match(Text)
            if not Regex:
                raise ERRORS.SyntaxError(FILE,Line_Nom,Stripped,f"Wrong use of 'until'")
            SOURCE[Line_Nom-1] = f"{Regex.group('Indent')}while not ({Regex.group('Expression')}):{Regex.group('Rest')}"
            # or i can replace "until" with "while not" (but still have to put paranthesis around condition)
        elif Stripped.startswith('unless ' )  or  Stripped=='unless':
            Regex = REGEX.unless.match(Text)
            if not Regex:
                raise ERRORS.SyntaxError(FILE,Line_Nom,Stripped,f"Wrong use of 'unless'")
            SOURCE[Line_Nom-1] = f"{Regex.group('Indent')}if not ({Regex.group('Expression')}):{Regex.group('Rest')}"
        elif Stripped.startswith('func '   )  or  Stripped=='func':
            Regex = REGEX.func.match(Text)
            if not Regex:
                raise ERRORS.SyntaxError(FILE,Line_Nom,Stripped,f"Wrong use of 'func'")
            SOURCE[Line_Nom-1] = SOURCE[Line_Nom-1].replace('func', 'def', 1)


        #] Foreach loop
        elif Stripped.startswith('foreach ')  or  Stripped=='foreach':
            Regex = REGEX.foreach.match(Text)
            if not Regex:
                raise ERRORS.SyntaxError(FILE,Line_Nom,Stripped,f"Wrong use of 'foreach'")
            indent, iterable, forvar = Regex.groups()
            modified = f"{indent}for {forvar} in {iterable}:"
            SOURCE[Line_Nom-1] = modified


        #] do_while
        elif Stripped.startswith('do '     )  or  Stripped=='do':
            if not (Regex:=REGEX.DoWhile.do.match(Text)):
                raise SyntaxError

            Indent = Regex.group('Indent')

            LN = int(Line_Nom)
            while not (Regex:=re.search(r'(?P<Indent>\s*).+', SOURCE[LN])):
                LN += 1
            Indent_Content = Regex.group('Indent')

            WHILE_LINE = 0
            LINE = int(Line_Nom)
            while not WHILE_LINE:
                try:
                    if re.search(Indent+r'while\s*\(.+\)',SOURCE[LINE]):
                        WHILE_LINE = int(LINE)
                    else:
                        LINE += 1
                except IndexError:
                    raise ERRORS.SyntaxError(FILE,Line_Nom,Text,"'do' defined without 'while'")

            i = 1
            for ln in range(Line_Nom,WHILE_LINE):
                SOURCE.insert(WHILE_LINE+i, SOURCE[ln])
                i+=1

            for ln in range(Line_Nom,WHILE_LINE):
                SOURCE[ln] = SOURCE[ln].replace(Indent_Content,'',1)

            SOURCE[Line_Nom-1] = ''
            SOURCE[WHILE_LINE] = SOURCE[WHILE_LINE]+':'


        #] Array
        elif Stripped.startswith('array '  )  or  Stripped=='array':
            raise NotImplementedError
            if not Regex:
                raise ERRORS.SyntaxError(FILE,Line_Nom,Stripped,f"Wrong use of 'array'")
            Indent  = Regex.group('Indent')
            VarName = Regex.group('VarName')
            Length  = Regex.group('Length')
            Type    = Regex.group('Type')
            Content = Regex.group('Content')

            Length  =  '' if not Length  else ', max_length='+Length
            Type    =  '' if not Length  else ', type_='+Length


            # SOURCE[Line_Nom-1] = f'{Indent}{VarName} = {MODULE_SHORTCUT}._Lang.Array({Content},{Type},{Length})'
            SOURCE[Line_Nom-1] = f'{Indent}{VarName} = {MODULE_SHORTCUT}.RXL.array({Content}{Type}{Length})'


        #] $Commands

        #] $check
        elif Stripped.startswith('$check ')  or  Stripped=='$check':
            Regex = REGEX.Commands.check.match(Text)
            if not Regex:
                raise ERRORS.SyntaxError(FILE,Line_Nom,Stripped,f"Wrong use of '$check'")
            Indent   =   Regex.group('Indent')
            needed_lines = 2
            if Regex.group("Then"):
                #print('Then True')
                needed_lines += 1
                else_ =  f'{Indent}else: {Regex.group("Then")}'
            else:
                else_ = ''
            if Regex.group('Anyway'):
                #print('Anyway True')
                needed_lines += 1
                finally_ =  f'{Indent}finally: {Regex.group("Anyway")}'
            else:
                #print('Anyway False')
                finally_ = ''

            nofound = True
            line = int(Line_Nom)
            pos_lines = 0
            free_lines = []
            free_lines.append(line-1)
            while (nofound and line!=len(SOURCE)):
                if  SOURCE[line].strip() or pos_lines>=needed_lines:
                    nofound = False
                else:
                    free_lines.append(line)
                    pos_lines+=1
                line+=1
            line = int(Line_Nom-2)
            pre_lines = 0
            nofound = True
            while (nofound and line!=1):
                if SOURCE[line].strip() or len(free_lines)>=needed_lines:
                    nofound = False
                else:
                    free_lines.append(line)
                    pre_lines+=1
                line-=1

            if len(free_lines)<needed_lines:
                #print(free_lines,'red')
                ERRORS.RaiseError('SpaceError',f"'$check' should have one extra blank line around it " +
                                               f"per any extra keywords ({needed_lines-1} lines needed)",
                                  Text,Line_Nom,FILE)

            free_lines.sort()
            Indent   =   Regex.group('Indent')
            try_     =   f'{Indent}try: {Regex.group("Test")}'
            except_  =   f'{Indent}except: pass'

            SOURCE[free_lines[0]] =  Indent+try_
            SOURCE[free_lines[1]] =  Indent+except_
            if else_:
                SOURCE[free_lines[2]] =  Indent+else_
            if finally_:
                SOURCE[free_lines[3]] =  Indent+finally_

            Lines_Added += needed_lines

        elif Stripped.startswith('$checkwait ')  or  Stripped=='$checkwait':

            Regex = REGEX.Commands.checkwait.match(Text)
            if not Regex:
                raise ERRORS.SyntaxError(FILE,Line_Nom,Stripped,f"Wrong use of '$checkwait'")
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
            while (nofound and line!=len(SOURCE)):
                if  SOURCE[line].strip() or pos_lines>=needed_lines:
                    nofound = False
                else:
                    free_lines.append(line)
                    pos_lines+=1
                line+=1
            line = int(Line_Nom-2)
            pre_lines = 0
            nofound = True
            while (nofound and line!=1):
                if SOURCE[line].strip() or len(free_lines)>=needed_lines:
                    nofound = False
                else:
                    free_lines.append(line)
                    pre_lines+=1
                line-=1

            if len(free_lines)<needed_lines:
                #print(free_lines,'red')
                ERRORS.RaiseError('SpaceError',f"'$check' should have one extra blank line around it " +
                                               f"per any extra keywords ({needed_lines-1} lines needed)",
                                  Text,Line_Nom,FILE)

            free_lines.sort()
            Indent   =   Regex.group('Indent')
            try_     =   f' {Indent}try: {Regex.group("Test")}'
            except_  =   f' {Indent}except: pass'

            SOURCE[free_lines[0]] =  Indent+"while True:"
            SOURCE[free_lines[1]] =  Indent+try_+";break"
            SOURCE[free_lines[2]] =  Indent+except_
            if else_:
                SOURCE[free_lines[3]] =  Indent+else_
            if finally_:
                SOURCE[free_lines[4]] =  Indent+finally_

            Lines_Added += needed_lines

        #] $CMD
        elif Stripped.startswith('$cmd '   )  or  Stripped=='$cmd' :
            Regex = REGEX.Commands.cmd.match(Text)
            if not Regex:
                raise ERRORS.SyntaxError(FILE,Line_Nom,Stripped,f"Wrong use of '$cmd'")
            SOURCE[Line_Nom-1] = f'{Regex.group("Indent")}std.terminal.run("{Regex.group("Command") if Regex else "cmd"}")'

        #] $CALL
        elif Stripped.startswith('$call '  )  or  Stripped=='$call':
            Regex = REGEX.Commands.call.match(Text)
            if not Regex:
                raise ERRORS.SyntaxError(FILE,Line_Nom,Stripped,f"Wrong use of '$call'")
            Indent = Regex.group('Indent'  )
            Delay  = Regex.group('Time'    )
            Func   = Regex.group('Function')
            SOURCE[Line_Nom-1] = f"{Indent}std.call({Func},delay={Delay})"

        #] $CLEAR
        elif Stripped in ('$cls','$clear'):
            SOURCE[Line_Nom-1] = f"{' '*Text.index('$')}std.cls()"

        #print(f"{Line_Nom} :: {time.time()-t} {Striped[:5]}",'red')
    return SOURCE,THREADS





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
