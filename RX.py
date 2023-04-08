import os
import time
import sys
import re
from typing import Literal

from addict import Addict
from tap import Tap
from colored import  fg,bg,attr

from RXL import *






__version__ = '0.0.1'

START_TIME = time.time()

print = rx.style.print
Error = rx.style.log_error

RX_PATH = os.path.abspath(__file__)[:-6]

CLASSES = (
           ['Files'   , 'System', 'Random'    , 'Record', 'Style'   ,
            'Terminal', 'Tuple' , 'Decorator' , 'IO'    , 'Internet',
            'Date_Time'],
           ['files'   , 'system', 'random'    , 'record', 'style'   ,
            'terminal', 'Tuple' , 'decorator' , 'io'    , 'internet',
            'date_time'],
           )

LOADED_PACKAGES = []
Lines_Added = 0
TIMES = {}
CACHE_DIR = "__pycache__"



#< Make Things Ready For Running >#
def Setup_Env():     #]  0.000 (with .hide():0.003)
    if not rx.files.exists(CACHE_DIR):
        rx.files.mkdir(CACHE_DIR)
        # rx.files.hide('__RX_LC__')
        return False
    return True



#< List of all errors >#
class ERRORS:
    #TRACEBACK = 'Traceback (most recent call last):'
    class RaiseError(Exception):
        def __init__(self, title, msg, line_text, line_nom, File):
            print( 'Traceback (most recent call last):')
            print(f'  File "{File}", line {line_nom-Lines_Added}, in <module>')
            print( '    '+line_text)
            Error(str(title)+': '+str(msg))
            Clean_Up(File)
            sys.exit()

    class BaseDefinedError(Exception):
        def __init__(self, attribute, line_text, line_nom, File):
            ERRORS.RaiseError(
                'BaseDefinedError',
                f"BaseDefinedError: '{attribute}' can not be defined after setting module [OPTIONS]",
                line_text,line_nom,FILE
            )

    class ValueError(Exception):
        def __init__(self,
                File,       attribute=None , value=None, Line_Text='',
                Line_Nom=0, correct_list=[], msg=None):
            MSG = msg if msg else f"'{attribute}' can not be '{value}'. Valid Choices: {correct_list}"
            raise ERRORS.RaiseError(
                  'ValueError', MSG,
                  Line_Text,Line_Nom,FILE
                  )

    class ConstantError(Exception):
        def __init__(self,
          Line_Nom=0  , Line_Def=0, Line_Text='',
          Attribute='', File=''   , msg=None):
            MSG = msg if msg else f"Redefinition of '{Attribute}' (Already Defined At Line {Line_Def})"
            raise ERRORS.RaiseError(
                  'ConstantError', MSG,
                  Line_Text,Line_Nom,FILE
                  )

    class IndentationError(Exception):
        def __init__(self,
          Line_Nom=0, Line_Text='', File=''):
            raise ERRORS.RaiseError(
                  'IndentationError', 'expected an indented block',
                  Line_Text,Line_Nom,FILE
                  )

    class UndefinedError(Exception):
        def __init__(self, msg='', File=''):
            print( 'Traceback (most recent call last):')
            print(f'  File "{File}", in/out <module>')
            print( 'UndefinedError: Something Went Wrong. ')#, end='')
            if msg:
                print('  Possible Error: ','red')
                print('    '+msg, 'red')
            else:
                print('  Please Check Your code for Possible Issues','red')
                print('  If You are Sure It is a Bug Please Report This to the Maintainer','red')
            Clean_Up(File)
            sys.exit()

    class ModuleNotFoundError(Exception):
        def __init__(self, File, Name=None, Line_Text='', Line_Nom=0):
            raise ERRORS.RaiseError(
                  'ModuleNotFoundError', f"No module named '{Name}'",
                  Line_Text,Line_Nom,FILE
                  )

    class AttributeError(Exception):
        def __init__(self,File, Line_Nom, Line_Text, Module_Version, Attribute, Type='module'):
            raise ERRORS.RaiseError(
                  'AttributeError', f"{Type} '{Module_Version}' has no attribute '{Attribute}'",
                  Line_Text,Line_Nom,FILE
                  )

    class LoadError(Exception):
        def __init__(self, Module, File, error=False):
            print( 'Traceback (most recent call last):')
            print(f'  Loading Module "{Module}" Resulted in an Error', 'red' if error else 'default')
            if error:
                print(error)
            else:
                print(f'    Module {Module} Returned Output When Loading')
                Error(f'LoadError: Make Sure There is No Print/Output in Module "{Module}"')
            Clean_Up(File)
            sys.exit()

    class SyntaxError(Exception):
        def __init__(self,File, Line_Nom, Line_Text, msg):
            raise ERRORS.RaiseError(
                  'SyntaxError', msg,
                  Line_Text,Line_Nom,FILE
                  )



class REGEX:

    _INCLUDE = ...

    class _SwitchCase:
        switch = re.compile(r'(?P<indent>\s*)switch\s+(?P<VARIABLE>\w+)\s*:')
        default = re.compile(r'^default\s*:\s*')
        case = re.compile(r'case\s+(?P<Nobreak>(nobreak)?)(?P<VALUE>.+):')

    load = re.compile(r'(?P<indent>\s*)load \s*(\w+,?)?')

    memory_loc = re.compile(r'[,\(\[\{\+=: ]&(?P<var>\w+)')

    until = re.compile(r'(?P<Indent>\s*)until \s*(?P<Expression>.+):(?P<Rest>.*)')

    unless = re.compile(r'(?P<Indent>\s*)unless \s*(?P<Expression>.+):(?P<Rest>.*)')

    foreach = re.compile(r'foreach \s*(?P<Expression>.+):')

    func = re.compile(r'func \s*(?P<Expression>.+)')

    const = re.compile(r'(?P<Indent>\s*)const\s+(?P<VarName>\w+)\s*=\s*(?P<Value>.+)\s*')

    const_array = re.compile(r'(?P<Indent>\s*)(?P<VarName>\w+)\s*=\s*<(?P<Content>.*)>')

    class DoWhile:
        do = re.compile(r'(?P<Indent>\s*)do\s*:\s*')
        while_ = re.compile(r'while\s*\(.+\)')

    array = re.compile(r'(?P<Indent>\s*)array \s*(?P<VarName>\w+)\s*\[\s*((?P<Length>\w+)?\s*(:?\s*(?P<Type>\w+))?\s*)?\]\s*=\s*{(?P<Content>.*)}\s*')

    class Commands:

        check = re.compile(r'(?P<Indent>\s*)\$check \s*(?P<Test>[^\s]+)(\s* then (?P<Then>.+))?( \s*anyway(s)? (?P<Anyway>.+))?')

        checkwait = re.compile("r'(?P<Indent>\s*)\$checkwait \s*(?P<Test>[^\s]+)(\s* then (?P<Then>.+))?( \s*anyway(s)? (?P<Anyway>.+))?'")

        cmd = re.compile(r'(?P<Indent>\s*)\$cmd \s*(?P<Command>.+)')

        call = re.compile(r'(?P<Indent>\s*)\$call (?P<Function>.+) \s*in \s*(?P<Time>.+)')

        _clear = NotImplemented


#< Get Arguments >#
class ArgumentParser:
    """
    All the methods related to parsing arguments of terminal should be implemented here
    """
    class Parser(Tap):
        """
        Base class for terminal argument parser

        All arguments and options are defined here
        """
        file    : str  =  None      # path to `RX` file to run
        cache   : bool =  True      # whether to use cache or not (using this will prevent using cache)
        verbose : bool =  False     # Verbose (Prints information when running RXL)
        debug   : bool =  False     # Debug file/code/syntax Before running it and print Mistakes in Red color
        compile : bool =  False     # Goes to `compile` menu
        translate_only: bool = False    # Translate file to python (without running it)
        #create_lite
        _module_test  : bool = False    # Module test (Internal use only)
        # file_args : list[str]         # arguments to pass to given file
            # instead we use `self.extra_args`


        def configure(self):
            self.add_argument("file", nargs="?")
            self.add_argument("-c", "--cache")
            self.add_argument("-v", "--verbose")
            self.add_argument("-d", "--debug")
            self.add_argument("-t", "--translate-only")
            # self.add_argument('file_args',nargs=argparse.REMAINDER)

        def process_args(self):
            if self.file and  not rx.files.exists(self.file):
                Error(f"can't open file '{rx.files.abspath(self.file)}':  No such file or directory",
                      add_time=False)
                exit()
            if not self.file and (self.translate_only or self.compile):
                Error(f"`file` should be specified when `--translate-only` or `--compile` arguments are given",
                      add_time=False)
                exit()
            if self.compile:
                raise NotImplementedError
                try:
                    import pyinstaller
                except ModuleNotFoundError:
                    Error("")


    @staticmethod
    def parse_args() -> dict:
        """Returns parsed arguments of terminal"""
        parser = ArgumentParser.Parser(
                    prog = "RXL",
                    description='"RX Language complete app"',
                    underscores_to_dashes=True,
                    # allow_abbrev=True,
                ).parse_args(
                    known_only=True
        )
        return parser.as_dict()


    @staticmethod
    def empty_asdict():
        # return {'module_test': False, 'debug': False, 'cache': True, 'verbose': False, 'file': None, 'compile': False, 'translate_only': False}
        return ArgumentParser.Parser(underscores_to_dashes=True).parse_args({})


    @staticmethod
    def detect_task(args:Addict):
        """Returns what task should be done. also returns needed arguments"""
        if len(sys.argv) == 1:
            task = "console"
            task_args = []
        elif args.translate_only:
            task = "translate"
            task_args = [args.file, args.cache, args.compile, args.debug]
        elif args.compile:
            task = "compile"
            task_args = [args.file]
        else:
            task = "runfile"
            task_args = [args.file, args.cache, args.debug, args.verbose]

        return (task,task_args)

    @staticmethod
    def run_task(task:str,args:list):
        """Runs the given task from function with giving the required arguments"""
        tasks_dict = {
            "console"  :  Menu.Console,
            "translate":  translate,
            "compile"  :  NotImplemented,
            "runfile"  :  NotImplemented,
        }
        return tasks_dict[task](*args)



#< Menu >#
class Menu:

    #< Interactive RX Shell >#
    @staticmethod
    def Console():
        rx.terminal.set_title('RX - Console')

        from importlib import reload

        #rx.system.chdir(RX_PATH)
        CWD = rx.system.cwd()

        PRE= ['import rx7 as rx','std=rx','print = std.style.print']
        rx.write(f'{CWD}/_Console_.py', '\n'.join(PRE)+'\n')
        import _Console_
        # _Console_ = __import__("_Console_") importlib.import_module("_Console_")
        while True:
            try:
                new = rx.io.wait_for_input('RX:Console> ')
                if new.lower() in ('exit','quit','end'):
                    rx.files.remove(f'{CWD}/_Console_.py')
                    return
            except (KeyboardInterrupt,EOFError):
                rx.files.remove(f'{CWD}/_Console_.py')
                return

            rx.write(f'{CWD}/_Console_.py', new+'\n', 'a')

            try:
                reload(_Console_)
            except (EOFError,KeyboardInterrupt):
                return
            except Exception as e:
                ERROR = str(e)
                if '(_Console_.py,' in ERROR:
                    ERROR = ERROR[:ERROR.index('(_Console_.py,')]
                print(str(type(e))[8:-2]+':  ' + ERROR, 'red')
                rx.write(f'{CWD}/_Console_.py', '\n'.join(rx.read(f'{CWD}/_Console_.py').splitlines()[:-1])+'\n')

            if re.match(r'print\s*\(', rx.read(f'{CWD}/_Console_.py').splitlines()[-1].strip()):
                rx.write(f'{CWD}/_Console_.py', '\n'.join(rx.read(f'{CWD}/_Console_.py').splitlines()[:-1])+'\n')


    @staticmethod
    def Create_SLModule():
        import inspect
        import rx7 as STD  #lite
        File = rx.io.get_files('Enter listed functions file name:  ',times=1)[0]
        output = 'RXSL.py'

        Main = 'import os,time,sys,subprocess,random,shutil\n\n'

        Files      = 'class Files:'
        Terminal   = 'class Terminal:'
        Record     = 'class Record:'
        Random     = 'class Random:'
        IO         = 'class IO:'
        Style      = 'class Style:'
        Decorator  = 'class Decorator:'
        System     = 'class System:'
        # files.isdir
        classes = {'files':Files,'terminal':Terminal,'record':Record,
                'random':Random, 'io':IO,'style':Style,
                'decorator':Decorator,'system':System
                }
        classes_names = list(classes.keys())

        for line in rx.read(File).split('\n'):
            if line:
                for cls in classes_names:
                    if line.startswith(cls):
                        try:
                            classes[cls] += '\n'+inspect.getsource(eval('STD.'+line))
                        except AttributeError:
                            print(f"Warning:  '{line[line.index('.')+1:]}' not found in STD.{cls}",'red')
                        break
                else:
                    try:
                        Main += inspect.getsource(eval('STD.'+line))+'\n'
                    except (NameError):
                        print(f"Warning:  '{line}' not found in STD.",'red')

        for name,cls in classes.items():
            if not len(cls.split('\n'))==1:
                Main += '\n\n'+cls+'\n'+f'{name} = {name.capitalize()}'+'\n'

        rx.write(output,Main)
        print(f'Module has been created successfully', 'green')

    @staticmethod
    def Compile(FILE=None):
        File = FILE if FILE else rx.io.get_files('Enter File Path:  ',times=1)[0]
        File = rx.files.abspath(File)
        #print(File)
        rx.terminal.run(f'python rx.py -T2P {File}')
        File = File[:File.rindex('.')]+'.py'

        Compiler = rx.io.selective_input('Compiler? [1-cx_freeze,2-pyinstaller]  ',
                                         choices={'1':'cxfreeze','2':'pyinstaller'},error=True)
        Icon = input('Icon Path:  ')
        Path = input('Path to save file:  ')

        if Compiler == 'cxfreeze':
            Icon = '--icon '+Icon if Icon else ''
            Path = '--target-dir '+Path if Path else ''
            Default_Args = '-s'
            Onefile  = ''
            Windowed = ''
        if Compiler == 'pyinstaller':
            Icon = '-i '+Icon if Icon else ''
            Path = '--specpath '+Path if Path else ''
            Onefile  = rx.io.selective_input('Onefile? [1-One File, 2-One Directory]  ',
                                             choices=['1','2'],error=True)
            Onefile  = '--onefile' if Onefile=='1' else '--onedir'
            Windowed = rx.io.selective_input('Window? [1-Console,2-Hide Console]  ',
                                             choices=['1','2'],error=True)
            Windowed = '--console' if Windowed=='1' else '--windowed'
            Default_Args = '-y'
        Args = input('Enter other arguments:  ')
        rx.terminal.run(f"{Compiler} {File} {Path} {Icon} {Default_Args} {Onefile} {Windowed} {Args}")
        print("\n\n[*] Done")
        print("Press Enter to Continue")
        rx.io.getpass("")
        print()



#< Reading File >#
def Read_File(filepath):
    if filepath and rx.files.exists(filepath):
        with open(filepath) as f:
            SOURCE = f.read().split('\n')
        return SOURCE + ['\n']
    print(os.path.abspath(filepath), 'red')
    print(f"RX> can't open file '{filepath}': No such file", 'red') #or directory
    sys.exit()



#< Method,Module_Name,Print,Indent,Const >#
def Define_Structure(SOURCE, FILE, DEBUG):
    """"""
    """
    BASE OPTIONS:
      OPTION NAME       DEFAULT VALUE       DESCRYPTION"
      Module-Name       sc                  Shortcut for RX Tools and functions (also "Modulename")'
      Method            normal              Method of loading tools.'
                                              Valid Choices: [normal,[lite,fast]] (also "Package-Version)"'
      Print             stylized            Print function to use. Valid Choices: [normal,stylized]'
    OPTIONS:'
      OPTION NAME       DEFAULT VALUE       DESCRYPTION"
      Func_Type_Checker True                Check if arguments of a function are in wrong type'
                                              (REGEX:  (func|function)-?(type|arg|param)-?(scanner|checker) )'
      Exit              True                Exit after executing the code or not'

    "OPTIONS" SHOULD BE DEFINED AFTER "BASE OPTIONS"'
    """
    #] Checking Indentation
     # {???}autopep8 -i script.py
     # import IndentCheck
    IndentCheck.check(FILE)
    Skip = 0
    for Line_Nom,Text in enumerate(SOURCE, 1):
        #] When Adding An Extra Line Like Decorators
        if Skip:
            Skip = Skip-1
            continue

        Stripped = Text.strip()

        # Ignore Docstrings and Comments
        if Stripped.startswith('#'):
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

        #] Indent
        if Stripped.endswith(':'):#.startswith(Keywords):
            BREAK = False
            LINE = int(Line_Nom)
            while not BREAK:
                if SOURCE[LINE-1].strip().endswith(':'):
                    BREAK = True
                else:
                    LINE += 1

            INDENT = len(re.match(r'(?P<indent>\s*).*', Text).group('indent'))
            INDENT_START = len(re.match(r'(?P<indent>\s*).*', SOURCE[LINE]).group('indent'))
            if INDENT_START <= INDENT:
                #print('RX_Err','red')
                raise ERRORS.IndentationError(Line_Nom+1, SOURCE[Line_Nom], FILE)

        pass
        if re.search(r'^(def)|(class)\s+map\s*\(',Stripped)  or  re.search(r'map\s*=\s*lambda\s+.+:',Stripped):
            map_defd = True
        else:
            map_defd = False

    #< OPTIONS >#
    MODULE_VERSION  = 'rx7'
    MODULE_SHORTCUT = 'std'#'sc'
    PRINT_TYPE = 'stylized'
    TYPE_SCANNER = False
    Allow_Reload = False
    Changeable = []
    INFO = {
        'Version':'1.0.0',
        'Author':rx.system.accname(),
        'Title': FILE.split('/')[-1].split('.')[0]}
    Skip = 0

    for nom,line in enumerate(SOURCE[:10]):

        r''' Normal|Lite
            #] Get Version (Method) of Tools
            elif re.match(r'(Method|Package(-|_)Version)\s*:\s*\w+', line):
                #if BASED:
                #    raise ERRORS.BaseDefinedError('Method/Version', line, SOURCE[:5].index(line), FILE)
                StripLow = line.strip().lower()
                if StripLow.endswith('lite') or StripLow.endswith('fast'):
                    MODULE_VERSION = 'rx7.lite'
                elif not StripLow.endswith('normal'):
                    stripped = line[line.index(':')+1:].strip()
                    raise ERRORS.ValueError(FILE, 'Method', stripped, line,
                                        SOURCE[:5].index(line), ['lite','normal'])
                SOURCE[nom] = ''
                Changeable.append(nom)
        '''
        rstrip = line.rstrip()

        if not line.strip() or line.strip().startswith('#'):
            pass

        #] Get Shortcut Name
        elif regex:=re.match(r'Module-?Name\s*:\s*(?P<name>.+)',
                             rstrip, re.IGNORECASE):
            MODULE_SHORTCUT = regex.group("name")
            if not re.match(r'\w+', MODULE_SHORTCUT):
                raise ERRORS.ValueError(msg='Invalid Value For  modulename/module_name',
                                        File=FILE)

        #] Print Function Method
        elif regex:=re.match(r'Print\s*:\s*(?P<type>.+)',
                             rstrip, re.IGNORECASE):
            PRINT_TYPE = regex.group("type").lower()
            if not (PRINT_TYPE in ("normal","stylized")):
                raise ERRORS.ValueError(FILE, 'print', PRINT_TYPE, line,
                                       SOURCE.index(line), ['lite','normal'])

        #] Function Type Scanner
        elif regex:=re.match(r'func(tion)?-?type-?checker\s*:\s*(?P<flag>.+)',
                             rstrip,re.IGNORECASE):
            #r'(Func(tion)?)(-|_)?(Type|Arg|Param)(-|_)?(Scanner|Checker)\s*:\s*\w+\s*'
            TYPE_SCANNER = regex.group("flag").capitalize()
            if TYPE_SCANNER not in ("True","False"):
                raise ERRORS.ValueError(FILE, 'func_type_checker', TYPE_SCANNER, line,
                                       SOURCE.index(line), "[True,False]")

        #] Exit at the end
        elif regex:=re.match(r'End-?(Exit|Quit)\s*:\s*(?P<flag>.+)',
                      rstrip, re.IGNORECASE):
            flag = regex.group("flag").capitalize()
            if flag in ("True","False"):
                if flag == "False":
                    SOURCE.append('__import__("getpass").getpass("Press [Enter] to Exit")')
            else:
                raise ERRORS.ValueError(FILE, 'Exit', flag, line,
                                       SOURCE.index(line), "[True,False]")

        #] Exit at the end
        elif regex:=re.match(r'Save-?Cache\s*:\s*(?P<flag>.+)', rstrip, re.IGNORECASE):
            flag = regex.group("flag").capitalize()
            if flag in ("True","False")  and  flag=='False':
                ABSPATH = os.path.dirname(rx.files.abspath(FILE))
                SOURCE.insert(-1,f'std.files.remove("{ABSPATH}/__RX_LC__",force=True)')
            else:
                raise ERRORS.ValueError(FILE, 'SaveCache', flag, line,
                                       SOURCE.index(line), "[True,False]")

        #] Reload Module
        elif regex:=re.match(r'Allow-?Reload\s*:(?P<flag>.+)', rstrip, re.IGNORECASE):
            flag = regex.group("flag").capitalize()
            if flag in ("False","True")  and  flag=="True":
                Allow_Reload = True
            else:
                raise ERRORS.ValueError(FILE, 'Allow-Reload', flag, line,
                                        SOURCE.index(line)  , "[True,False]")

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

        else:
            break

        Changeable.append(nom)
        SOURCE[nom] = ''

    #print(INFO)

    #] Bases
    STRING = []
    STRING.append(f"import {MODULE_VERSION} as {MODULE_SHORTCUT}")
    STRING.append(f"std = rx = {MODULE_SHORTCUT};std.RXL = __import__('RXL')")
    STRING.append(f"print = {MODULE_SHORTCUT+'.style.print' if PRINT_TYPE=='stylized' else 'print'}")
    #] Direct Attributes
    STRING.append(F"input = {MODULE_SHORTCUT}.Input")
    STRING.append(f"Check_Type = {MODULE_SHORTCUT}.Check_Type")
    #] Other ones
    if not map_defd:
        STRING.append("apply = __builtins__['map'] ; map = None")
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
        SOURCE.insert(0, ';'.join(STRING))

    if DEBUG and not len(Changeable):
        print(f'{FILE}> No (Enough) Base-Option/Empty-lines at begining of file', 'red')

    # rx.files.write(f'./__RX_LC__/_{os.path.basename(FILE)}_info_',str(rx.files.mdftime(FILE)))

    #print(CONSTS)
    return (SOURCE,
            MODULE_VERSION, MODULE_SHORTCUT,
            TYPE_SCANNER, INFO)



#< Syntax >#
def Syntax(SOURCE,
           MODULE_VERSION ,  MODULE_SHORTCUT,
           TYPE_SCANNER   ,
           FILE           ,  DEBUG):

    global Lines_Added
    '''
     #print(TYPE_SCANNER,'red')
     Keywords = ('if' , 'elif' , 'except' , 'def',
                'for', 'while', 'foreach', 'until', 'unless',
                'try', 'else' , 'switch' , 'class', 'case',
                )
    '''
    CONSTS = set()
    Skip = 0
    THREADS = []

    for Line_Nom,Text in enumerate(SOURCE, 1):
        #t = time.time()
        #print(str(Line_Nom)+' '+Text)

        Stripped = Text.strip()

        #] && --- ||
        '''
         nnoo = False
         while not nnoo:
             if '&&' in Text  and  Text[:Text.index('&&')].count("'")%2==0:
                 Text.replace('&&','and',1)
             else:
                 nnoo = True
        '''

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

        #] Check for Constant re-definition/change
        for item in CONSTS:
            if re.search(rf'( |;|^$){item[0]}\s*(\[.+\])?\s*=\s*[^=]+', Text):  # \s*.+  {?}
                if not Stripped.startswith('def ')  and  not Stripped.startswith('#'):
                    raise ERRORS.ConstantError(Line_Nom, item[1], Stripped, item[0], FILE)

        if False: pass  #Just to make rest of the conditions look similar

        #] Include
        elif Stripped.startswith('include ')  or  Stripped=='include':
            Regex=re.match(r'(?P<Indent>\s*)include \s*(?P<objects>.+)\s*', Text)
            if not Regex:
                raise ERRORS.SyntaxError(FILE,Line_Nom,Stripped,f"Wrong use of 'include'")
            Indent = Regex.group('Indent')
            OBJECTS = Regex.group('objects')
            To_Add = str(Indent)

            if OBJECTS == '*':
                Type = 'Class'
                Packages = list(CLASSES[0])
            elif not ':' in OBJECTS:
                Type = 'Class'
                Packages = re.split(r'\s*,\s*', Text)
                Packages[0]= Packages[0][len(Indent)+8:].strip()
            elif Reg2:=re.search(r'(?P<CLASS>\w+)\s*:\s*(?P<OBJECTS>.+)',OBJECTS):
                Type = 'Object'
                import rx7# as RX_M
                global RX_M
                RX_M = rx7
                CLASS = Reg2.group('CLASS')
                OBJ2  = Reg2.group('OBJECTS')

                method_list = [func for func in dir(eval(f'RX_M.{CLASS}')) if (
                    callable(getattr(eval(f'RX_M.{CLASS}'), func))  and  not func.startswith("__"))]
                if CLASS not in CLASSES[0]+CLASSES[1]:
                    raise ERRORS.AttributeError(FILE,Line_Nom,Text,MODULE_VERSION,package)
                OBJ_of_OBJS2 = re.split(r'\s*,\s*',OBJ2)
                for obj in OBJ_of_OBJS2:
                    if not obj in method_list:
                        raise ERRORS.AttributeError(FILE,Line_Nom,Text,MODULE_VERSION,obj,'class')
                    To_Add += f'{obj}={MODULE_SHORTCUT}.{CLASS}.{obj};'
            else:
                raise ERRORS.RaiseError('IncludeError',
                        "Syntax is not recognized for 'include'. (Make sure it is true, then report it)",
                        Text,Line_Nom,FILE)

            if Type == 'Class':
                for package in Packages:
                    if package not in CLASSES[0]+CLASSES[1]:
                        raise ERRORS.AttributeError(FILE,Line_Nom,Text,MODULE_VERSION,package)
                    #SOURCE.insert(Line_Nom-1, f'{Indent}{package} = {MODULE_SHORTCUT}.{package}')
                    To_Add += f'{package}={MODULE_SHORTCUT}.{package};'

            SOURCE[Line_Nom-1] = To_Add
            # continue  # do it to all?

        #] Func Type checker
        elif Stripped.startswith('def ')   and  TYPE_SCANNER:  # Make it regex?
            if SOURCE[Line_Nom-2].strip().endswith('Check_Type'):
               SOURCE[Line_Nom-2]= re.search(r'(\s*)',Text).group(1)+f'@std.Check_Type'
            if SOURCE[Line_Nom-2].strip().startswith('@'):
                continue
            indent = Text.index('def ')
            SOURCE.insert(Line_Nom-1, f'{" "*indent}@{MODULE_SHORTCUT}.Check_Type')
            Skip = 1
            Lines_Added += 1

        #] Load User-Defined Modules        # TODO: Better regex to get packages
        elif Stripped.startswith('load ')  or  Stripped=='load':
            #elif Regex:=re.match(r'(?P<indent>\s*)load \s*(\w+,?)?', Text):
            Regex = re.match(r'(?P<indent>\s*)load \s*(\w+,?)?', Text)
            if not Regex:
                raise ERRORS.SyntaxError(FILE,Line_Nom,Stripped,f"Wrong use of 'load'")
            #t = time.time()
            Indent = Regex.group('indent')
            Packages = re.split(r'\s*,\s*', Text)
            Packages[0]= Packages[0][4:].strip()

            #SOURCE.remove(Text)
            #SOURCE[Line_Nom-1]=''
            To_Add = str(Indent)
            #rx.files.mkdir('__RX_LC__')
            #if not rx.files.exists('__RX_LC__/__init__.py'):
            #    rx.write('__RX_LC__/__init__.py')

            for package in Packages:
                if rx.files.exists(f'{package}.rx7'):
                    import threading
                    #print(package,'green')
                    def TEST():
                        pack_out = rx.terminal.getoutput(f'python RX.py -MT {package}.rx7').strip()

                        if len(pack_out):
                            #print(pack_out)
                            if re.match(r'\w+Error', pack_out.splitlines()[-1]):
                                raise ERRORS.LoadError(package,FILE,pack_out.splitlines()[-1])
                            else:
                                raise ERRORS.LoadError(package,FILE)
                    thread = threading.Thread(target=TEST)
                    thread.start()
                    THREADS.append(thread)
                    LOADED_PACKAGES.append(package)
                    To_Add += f"{package}={MODULE_SHORTCUT}.import_module('__RX_LC__/{package}');"
                else:
                    raise ERRORS.ModuleNotFoundError(FILE, package, Text, Line_Nom)
            SOURCE[Line_Nom-1]=str(To_Add)
            #print(f'Load: {time.time()-t}','green')

        #] Memory Location of Object
        elif Regex:=re.search(r'[,\(\[\{\+=: ]&(?P<var>\w+)', Text): #[^a-zA-Z0-9'"]
            SOURCE[Line_Nom-1] = Text.replace("&"+Regex.group("var"),f'hex(id({Regex.group("var")}))')

        #] until & unless & foreach & func
        elif Stripped.startswith('until '  )  or  Stripped=='until':
            #elif Regex:=re.match(r'(?P<Indent>\s*)until \s*(?P<Expression>.+):'  , Text):
            Regex=re.match(r'(?P<Indent>\s*)until \s*(?P<Expression>.+):(?P<Rest>.*)'  , Text)
            if not Regex:
                raise ERRORS.SyntaxError(FILE,Line_Nom,Stripped,f"Wrong use of 'until'")
            SOURCE[Line_Nom-1] = f"{Regex.group('Indent')}while not ({Regex.group('Expression')}):{Regex.group('Rest')}"
            # or i can replace "until" with "while not" (but still have to put paranthesis around condition)
        elif Stripped.startswith('unless ' )  or  Stripped=='unless':
            #elif Regex:=re.match(r'(?P<Indent>\s*)unless \s*(?P<Expression>.+):' , Text):
            Regex=re.match(r'(?P<Indent>\s*)unless \s*(?P<Expression>.+):(?P<Rest>.*)' , Text)
            if not Regex:
                raise ERRORS.SyntaxError(FILE,Line_Nom,Stripped,f"Wrong use of 'unless'")
            SOURCE[Line_Nom-1] = f"{Regex.group('Indent')}if not ({Regex.group('Expression')}):{Regex.group('Rest')}"
        elif Stripped.startswith('foreach ')  or  Stripped=='foreach':
            #elif Regex:=re.match(r'foreach \s*(?P<Expression>.+):', Striped):
            Regex=re.match(r'foreach \s*(?P<Expression>.+):', Stripped)
            if not Regex:
                raise ERRORS.SyntaxError(FILE,Line_Nom,Stripped,f"Wrong use of 'foreach'")
            SOURCE[Line_Nom-1] = SOURCE[Line_Nom-1].replace('foreach', 'for', 1)
        elif Stripped.startswith('func '   )  or  Stripped=='func':
            #elif Regex:=re.match(r'func \s*(?P<Expression>.+)'    , Striped):
            Regex=re.match(r'func \s*(?P<Expression>.+)'    , Stripped)
            if not Regex:
                raise ERRORS.SyntaxError(FILE,Line_Nom,Stripped,f"Wrong use of 'func'")
            SOURCE[Line_Nom-1] = SOURCE[Line_Nom-1].replace('func', 'def', 1)

        #] Const Var                        # TODO: Better regex
        elif Stripped.startswith('const '  )  or  Stripped=='const':
            #if Text.startswith(' '): raise LateDefine("'Const' Must Be Defined In The Main Scope")
            if Regex:=re.match(r'(?P<Indent>\s*)const\s+(?P<VarName>\w+)\s*=\s*(?P<Value>.+)\s*', Text):
                Indent  =  Regex.group('Indent' )
                VarName =  Regex.group('VarName')
                Value   =  Regex.group('Value'  )
                SOURCE[Line_Nom-1] =  f'{Indent}{VarName} = {Value}'
                if VarName != VarName.upper()  and  DEBUG:
                    #] maybe it should be just a warning
                    print(f"{FILE}:{Line_Nom}> Constant Variable Name ({VarName}) is not UPPERCASED",'red')
                    '''
                     raise ERRORS.ConstantError(Line_Nom=Line_Nom,
                                               Line_Text=Stripped,
                                               File=FILE,
                                               msg='Constant Variable Name Must be UPPERCASE')
                    '''
                for item in CONSTS:  #] Check if Const X is already defined
                    if VarName == item[0]:
                        raise ERRORS.ConstantError(Line_Nom, item[1], Stripped, item[0], FILE)
                CONSTS.add((VarName, Line_Nom))

        #] Const Array
        elif Regex:=re.match(r'(?P<Indent>\s*)(?P<VarName>\w+)\s*=\s*<(?P<Content>.*)>', Text):
            Content = Regex.group('Content')
            VarName = Regex.group('VarName')
            '''
            TYPE_ERROR = False
            try:
                Content = eval(Content)
                if type(Content) != tuple:
                    TYPE_ERROR = True
            except NameError:
                pass
            except Exception as e:
                ERRORS.RaiseError(str(type(e).__name__),e,Text,Line_Nom,FILE)

            if TYPE_ERROR:
                #raise TypeError(f"ArrayConst can not be '{type(Content)}' type (Use 'Const' keyword)")
                Type_Content = str(type(Content))[8:-2]
                if DEBUG:
                    print(f"'<>' is for Arrays, Try to use 'Const' keyword for type ",'red', end='')
                    print(f"'{Type_Content}'  ({FILE}:{Line_Nom}:{VarName})", 'red')#, style='bold')
            '''
            if VarName != VarName.upper()  and  DEBUG:
                print(f"{FILE}:{Line_Nom}> Constant Variable Name ({VarName}) is not UPPERCASED",'red')
            CONSTS.add((VarName, Line_Nom))
            Indent = Regex.group('Indent')
            SOURCE[Line_Nom-1] = f'{Indent}{VarName} = {MODULE_SHORTCUT}._Lang.Const({Content})'

        #] do_while
        elif Regex:=re.match(r'(?P<Indent>\s*)do\s*:\s*',Text):
            #elif Striped.startswith('do '     )  or  Striped=='do':
            if not Regex:
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
            #"array " s "[" s type_:.* s ":" s max_length:.* s "]" s "<" values:[^>]* ">"
            Regex=re.search(r'''[^a-zA-Z0-9_]array \s*
                               \s*\[\s*(?P<Type>.+)?\s*:\s*(?P<Length>.+)?\s*\]\s*<(?P<Content>.*)>''',
                           Text,re.VERBOSE)
            continue
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


        #] $check
        elif Stripped.startswith('$check ')  or  Stripped=='$check':
            Regex=re.match(r'(?P<Indent>\s*)\$check \s*(?P<Test>[^\s]+)(\s* then (?P<Then>.+))?( \s*anyway(s)? (?P<Anyway>.+))?',Text)
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

            Regex=re.match(r'(?P<Indent>\s*)\$checkwait \s*(?P<Test>[^\s]+)(\s* then (?P<Then>.+))?( \s*anyway(s)? (?P<Anyway>.+))?',Text)
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
            Regex = re.match(r'(?P<Indent>\s*)\$cmd \s*(?P<Command>.+)',Text)
            if not Regex:
                raise ERRORS.SyntaxError(FILE,Line_Nom,Stripped,f"Wrong use of '$cmd'")
            SOURCE[Line_Nom-1] = f'{Regex.group("Indent")}std.terminal.run("{Regex.group("Command") if Regex else "cmd"}")'

        #] $CALL
        elif Stripped.startswith('$call '  )  or  Stripped=='$call':
            Regex = re.match(r'(?P<Indent>\s*)\$call (?P<Function>.+) \s*in \s*(?P<Time>.+)',Text)
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



#< Clean Everything Which is Not Needed >#
def Clean_Up(File='',Lib=True):   #] 0.03
    #return
    #if Lib:
    #    try: rx.files.remove(f'__RX_LC__', force=True)
    #    except: pass
    #else: pass
    try: os.remove('_'+File+'_')
    except: pass
    # try: rx.files.remove('__pycache__', force=True)
    # except: pass
    try: rx.files.remove('_Console_.py')
    except: pass



#< Running _FILE_ >#
def RUN(READY_FILE_NAME,THREADS=[]):
    # rx.terminal.set_title(f'RX - {os.path.basename(FILE)}')
    try:
        for thread in THREADS:
            thread.join()
        TIMES['B_Run '] = time.time()-START_TIME
        if TIMES['B_Run '] >  0.5 + 0.3*len(THREADS):
            print('Running Speed is Slow','red')
        elif TIMES['B_Run '] < 0.01:
            pass#print('Running Speed is Super Fast','green')
        for k,v in TIMES.items(): print(f'{k} :: {v}','green')
        print(f"B_Run  :: {TIMES['B_Run ']}",'green')
        # return
        import runpy
        runpy.run_path(READY_FILE_NAME)
    except Exception as e:
        raise e
        print('Traceback (most recent call last):')
        print('  More Information in Next Updates...')
       #print(f'  File "{FILE}" in  "UNDEFINED"')
        Error(type(e).__name__+': '+str(e))
        sys.exit()



#< Check cache availablity >#
def Cache_Check(cache:bool, path:str, debug:bool, verbose:bool):
    if not cache:
        return False

    ready_file_name = convert_file_name(path)
    full_ready_path = f"./{CACHE_DIR}/{ready_file_name}"

    cache_file =  bool(rx.files.exists(full_ready_path))
    if cache_file:
        if debug or verbose:
            print("[*] Found Cache")
        source = rx.files.read(full_ready_path).split("\n")
        cache_id = int(source.pop(0))
        if cache_id == int(rx.files.mdftime(path)):
            return source
        else:
            print("[*] Cache does not match with latest version of file")
    else:
        if debug:
            print("[*] No Cache were found")
    return False



#< Translate Source (and write cache) >#
def Convert_Source(path:str, source:list, cache:bool, debug:bool, verbose:bool):
    # global TIMES, Lines_Added

    source, module_version, module_shortcut, \
        type_scanner, info = Define_Structure(source, path, debug)
    #-> SOURCE,MODULE_VERSION, MODULE_SHORTCUT,TYPE_SCANNER, INFO
    TIMES['DefStr'] = time.time()-START_TIME

    source, threads = Syntax(source, module_version, module_shortcut,
                             type_scanner, path, debug)

    ready_file_name = convert_file_name(path)

    rx.write('translated', '\n'.join(source))

    if cache:
        if debug:
            print("[*] Creating Cache")
        cached_source = [str(int(rx.files.mdftime()))] + source
        full_ready_path = f"./{CACHE_DIR}/{ready_file_name}"
        try:
            rx.write(full_ready_path, '\n'.join(cached_source))
        except PermissionError:
            rx.files.remove(full_ready_path)
            rx.write(full_ready_path, '\n'.join(cached_source))

    return source,threads,info


#< Starting Code >#
def Start_Lang():
    if ADD_VERBOSE:
        #rx.cls()
        NOW = str(__import__('datetime').datetime.now())
        # probably consider changing next line from "NOW" to "START_TIME"
        print(f'''Start  RX Language  at  "{NOW[:NOW.rindex('.')+5]}"''')
        print(f'Running  "{INFO["Title"]}" v{INFO["Version"]}  by "{INFO["Author"]}"')
        print('\n')
    RUN(READY_FILE_NAME,THREADS)
    if ADD_VERBOSE:
        EXECUTION_TIME_TEXT = round(__import__("time").time()-START_TIME,3)
        print(f'\n\nExecution Time:  {EXECUTION_TIME_TEXT}\n')
        #print(START_TIME)
        #print(EXECUTION_TIME_TEXT)


#< Translate >#
def translate(path, cache, debug, verbose):
    source = Cache_Check(cache, path, debug, verbose)
    threads = []
    if source:
        pass
    else:
        source,threads,info = Convert_Source(path, source, cache, debug, verbose)





#< START OF THE CODE >#
if __name__ == "__main__":
    try:
        TIMES['Start '] = time.time()-START_TIME

        Setup_Env()
        TIMES['SetEnv'] = time.time()-START_TIME

        ARGS  = ArgumentParser.parse_args()
        TASK,TASK_ARGS = ArgumentParser.detect_task(Addict(ARGS))
        TIMES['ARGS  '] = time.time()-START_TIME
        # print(TIMES)
        ArgumentParser.run_task(TASK,TASK_ARGS)


    except KeyboardInterrupt:
        #Clean_Up(File)
        Error('\nExiting Because of KeyboardInterrupt Error (Ctrl+C)')


    except Exception as E:
        raise E# from None
        print('Traceback (most recent call last):')
        print('  Error occured when making environment ready to run')
        print('SystemError: '+str(E), 'red', style='bold')
        print('Please report this in https://github.com/Ramin-RX7/RX-Language/issues, along with the traceback and version')


    finally:
        try:
            if not MT:
                Clean_Up(FILE)
        except:
            pass
        # rx.terminal.set_title(title)
