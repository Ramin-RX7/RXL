import os
import time
import sys

from addict import Addict
from tap import Tap

from .Lib import *
from . import Grammar





__version__ = '0.0.1'

START_TIME = time.time()

print = rx.style.print
Error = rx.style.log_error

RX_PATH = os.path.abspath(__file__)[:-7]


Lines_Added = 0
TIMES = {}
CACHE_DIR = "__pycache__"
CONSOLE_FILE = "_console_.py"





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
        #create_mini_std
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
        # if len(sys.argv) == 1:
            # task = "console"
            # task_args = []
        if args.file:
            if args.translate_only:
                task = "translate"
                task_args = [args.file, args.cache, args.debug, args.verbose, args.compile]
            elif args.compile:
                task = "compile"
                task_args = [args.file]
            else:
                task = "runfile"
                task_args = [args.file, args.cache, args.debug, args.verbose]

        else:
            task = "console"
            task_args = []

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
        raise NotImplementedError


    #] Create a module with custom std files
    @staticmethod
    def Create_Mini_Std():
        raise NotImplementedError


    #] Compiling .rx given file to bytecode
    @staticmethod
    def compile(file=None):
        raise NotImplementedError


    #] only translating file to python code (if compile==True also compiles it)
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


    #] running the file given as terminal argument
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

        try:
            import runpy
            # runpy.run_path(ready_file_name)
            rx.terminal.run(f"python {ready_file_name}")
        except Exception as e:
            raise e
            print('Traceback (most recent call last):')
            print('  More Information in Next Updates...')
           #print(f'  File "{FILE}" in  "UNDEFINED"')
            Error(type(e).__name__+': '+str(e))
            sys.exit()
        finally:
            os.remove(ready_file_name)

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
def get_cache(cache:str, path:str, debug:bool, verbose:bool):
    if cache is False:
        return False

    ready_file_name = convert_file_name(path)
    full_ready_path = f"./{cache}/{ready_file_name}"

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
def save_cache(path, source, cache_dir):
    id = str(int(rx.files.mdftime(path)))
    source = id + "\n" + source
    rx.write(f"./{cache_dir}/{convert_file_name(rx.files.basename(path))}",source)



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
    if cache:
        cache = CACHE_DIR
    source = get_cache(cache, path, debug, verbose)
    threads = []
    info = {}
    if not source:
        source = rx.read(path).split("\n")
        source,threads,info = translate(source, path, cache, debug, verbose)
        if cache:
            if debug:
                print("[*] Creating Cache")
            save_cache(path, source, cache)
    for thread in threads:
        thread.join()

    return source





#< START OF THE CODE >#
# if __name__ == "__main__":
def main():
    try:
        TIMES['Start '] = time.time()-START_TIME

        Setup_Env()
        TIMES['SetEnv'] = time.time()-START_TIME

        ARGS  = ArgumentParser.parse_args()
        # print(ARGS)
        TASK,TASK_ARGS = ArgumentParser.detect_task(Addict(ARGS))
        TIMES['ARGS  '] = time.time()-START_TIME
        ArgumentParser.run_task(TASK,TASK_ARGS)
        # print(TIMES)


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
