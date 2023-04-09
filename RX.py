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


Lines_Added = 0
TIMES = {}
CACHE_DIR = "__pycache__"





#< List of all errors >#
class ERRORS:
    #TRACEBACK = 'Traceback (most recent call last):'
    class RaiseError(Exception):
        def __init__(self, title, msg, line_text, line_nom, File):
            print( 'Traceback (most recent call last):')
            print(f'  File "{File}", line {line_nom-Lines_Added}, in <module>')
            print( '    '+line_text)
            Error(str(title)+': '+str(msg))
            # Clean_Up(File)
            sys.exit()

    class BaseDefinedError(Exception):
        def __init__(self, attribute, line_text, line_nom, File):
            ERRORS.RaiseError(
                'BaseDefinedError',
                f"BaseDefinedError: '{attribute}' can not be defined after setting module [OPTIONS]",
                line_text,line_nom,File
            )

    class ValueError(Exception):
        def __init__(self,
                File,       attribute=None , value=None, Line_Text='',
                Line_Nom=0, correct_list=[], msg=None):
            MSG = msg if msg else f"'{attribute}' can not be '{value}'. Valid Choices: {correct_list}"
            raise ERRORS.RaiseError(
                  'ValueError', MSG,
                  Line_Text,Line_Nom,File
                  )

    class ConstantError(Exception):
        def __init__(self,
          Line_Nom=0  , Line_Def=0, Line_Text='',
          Attribute='', File=''   , msg=None):
            MSG = msg if msg else f"Redefinition of '{Attribute}' (Already Defined At Line {Line_Def})"
            raise ERRORS.RaiseError(
                  'ConstantError', MSG,
                  Line_Text,Line_Nom,File
                  )

    class IndentationError(Exception):
        def __init__(self,
          Line_Nom=0, Line_Text='', File=''):
            raise ERRORS.RaiseError(
                  'IndentationError', 'expected an indented block',
                  Line_Text,Line_Nom,File
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
            # Clean_Up(File)
            sys.exit()

    class ModuleNotFoundError(Exception):
        def __init__(self, File, Name=None, Line_Text='', Line_Nom=0):
            raise ERRORS.RaiseError(
                  'ModuleNotFoundError', f"No module named '{Name}'",
                  Line_Text,Line_Nom,File
                  )

    class AttributeError(Exception):
        def __init__(self,File, Line_Nom, Line_Text, Module_Version, Attribute, Type='module'):
            raise ERRORS.RaiseError(
                  'AttributeError', f"{Type} '{Module_Version}' has no attribute '{Attribute}'",
                  Line_Text,Line_Nom,File
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
            # Clean_Up(File)
            sys.exit()

    class SyntaxError(Exception):
        def __init__(self,File, Line_Nom, Line_Text, msg):
            raise ERRORS.RaiseError(
                  'SyntaxError', msg,
                  Line_Text,Line_Nom,File
                  )



#< List of all regex patterns >#
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



#< Processing arguments and tasks >#
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
            task_args = [args.file, args.cache, args.debug, args.verbose, args.compile]
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
            "console"  :  Tasks.Console,
            "translate":  Tasks.translate_only,
            "compile"  :  NotImplemented,
            "runfile"  :  Tasks.runfile,
        }
        return tasks_dict[task](*args)



#< Implementation of tasks >#
class Tasks:

    #] Interactive RX Shell
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
        raise NotImplementedError
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
    def compile(FILE=None):
        raise NotImplementedError
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


    @staticmethod
    def translate_only(path:str, cache, debug, verbose, compile):
        source = convert_source(path, cache, debug, verbose)
        py_file_path = path.removesuffix(".rx")+".py"
        # if rx.files.exists(py_file_path):
            # print(f"{py_file_path} Already exists...")
            # if replace:=rx.io.yesno_input("Replace it? "):
                # rx.write(py_file_path, source)
        # else:
        rx.write(py_file_path, source)

        if compile:
            raise NotImplementedError
        TIMES["TRANSLATE_ONLY"] = time.time()-START_TIME


    @staticmethod
    def runfile(path, cache, debug, verbose):
        source = convert_source(path, cache, debug, verbose)
        ready_file_name = convert_file_name(path)

        rx.write(ready_file_name, source)

        if verbose:
            #rx.cls()
            NOW = str(__import__('datetime').datetime.now())
            # probably consider changing next line from "NOW" to "START_TIME"
            print(f'''Start  RX Language  at  "{NOW[:NOW.rindex('.')+5]}"''')
            # print(f'Running  "{INFO["Title"]}" v{INFO["Version"]}  by "{INFO["Author"]}"')
            print('\n')

        TIMES['B_Run '] = time.time()-START_TIME
        for k,v in TIMES.items(): print(f'{k} :: {v}','green')

        import runpy
        try:
            runpy.run_path(ready_file_name)
        except Exception as e:
            raise e
            print('Traceback (most recent call last):')
            print('  More Information in Next Updates...')
           #print(f'  File "{FILE}" in  "UNDEFINED"')
            Error(type(e).__name__+': '+str(e))
            sys.exit()
        finally:
            pass
            # os.remove(ready_file_name)

        if verbose:
            EXECUTION_TIME_TEXT = round(time.time()-START_TIME,3)
            print(f'\n\nExecution Time:  {EXECUTION_TIME_TEXT}\n')
            #print(START_TIME)
            #print(EXECUTION_TIME_TEXT)





#< Make Things Ready For Running >#
def Setup_Env():     #]  0.000 (with .hide():0.003)
    if not rx.files.exists(CACHE_DIR):
        rx.files.mkdir(CACHE_DIR)
        # rx.files.hide(CACHE_DIR)
        return False
    return True



#< Check cache availablity >#
def get_cache(cache:bool, path:str, debug:bool, verbose:bool):
    if not cache:
        return False

    ready_file_name = convert_file_name(path)
    full_ready_path = f"./{CACHE_DIR}/{ready_file_name}"

    cache_file =  rx.files.exists(full_ready_path)
    if cache_file:
        if debug or verbose:
            print("[*] Found Cache")
        source = rx.files.read(full_ready_path).split("\n")
        cache_id = int(source.pop(0))
        if cache_id == int(rx.files.mdftime(path)):
            return "\n".join(source)
        else:
            print("[*] Cache does not match with latest version of file")
    else:
        if debug:
            print("[*] No Cache were found")
    return False


#< Save cache of `path` >#
def save_cache(path, source):
    id = str(int(rx.files.mdftime(path)))
    source = id + "\n" + source
    rx.write(f"./{CACHE_DIR}/{convert_file_name(rx.files.basename(path))}",source)



#< Translate Source (and write cache) >#
def translate(source:list, path:str, cache:bool, debug:bool, verbose:bool):
    # global TIMES, Lines_Added
    source, module_version, module_shortcut, \
        type_scanner, info = Grammar.define_structure(source, path, debug)
    TIMES['DefStr'] = time.time()-START_TIME

    source, threads = Grammar.syntax(source, module_version, module_shortcut,
                             type_scanner, path, debug)
    TIMES['DefStr'] = time.time()-START_TIME

    source = '\n'.join(source)
    rx.write('translated', source)

    return source,threads,info



#< Translate >#
def convert_source(path, cache, debug, verbose):
    source = get_cache(cache, path, debug, verbose)
    threads = []
    info = {}
    if not source:
        source = rx.read(path).split("\n")
        source,threads,info = translate(source, path, cache, debug, verbose)
        if cache:
            if debug:
                print("[*] Creating Cache")
            save_cache(path, source)
    for thread in threads:
        thread.join()

    return source





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
        print(TIMES)


    except KeyboardInterrupt:
        Error('\nExiting Because of KeyboardInterrupt Error (Ctrl+C)')


    except Exception as E:
        raise E# from None
        print('Traceback (most recent call last):')
        print('  Error occured when making environment ready to run')
        print('SystemError: '+str(E), 'red', style='bold')
        print('Please report this in https://github.com/Ramin-RX7/RX-Language/issues, along with the traceback and version')


    finally:
        pass
        # rx.terminal.set_title(title)
