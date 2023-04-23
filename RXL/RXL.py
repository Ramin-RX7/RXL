import time
import sys

from addict import Addict
from tap import Tap

from .Lib import rx,convert_file_name
from . import Grammar





__version__ = '0.0.1'

START_TIME = time.time()

print = rx.style.print
Error = rx.style.log_error

RX_PATH = rx.files.dirname(rx.files.abspath(__file__))


Lines_Added = 0
TIMES = {}
CACHE_DIR = "__pycache__"
CONSOLE_FILE = "_console_.py"
WORKING_PATH = ...





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
        file    : str  =  None      # path to `RXL` file to run
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
                    description='"RX Language app"',
                    underscores_to_dashes=True,
                    # allow_abbrev=True,
                ).parse_args(
                    known_only=True
        )
        return parser.as_dict()


    @staticmethod
    def empty_asdict() -> dict:
        """
        Returns a dictionary of how argument shoud be when no arguments are given from terminal
        """
        # return {'module_test': False, 'debug': False, 'cache': True, 'verbose': False,
        #         'file': None, 'compile': False, 'translate_only': False}
        return ArgumentParser.Parser(underscores_to_dashes=True).parse_args({}).as_dict()



#< Implementation of tasks >#
class Tasks:

    #] Interactive RXL Shell
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
        """
        --standalone   (creates a `myfile.dist` directory that contains all files to run on any machine)
        --onefile
        --follow-imports
        --disable-console
        --windows-icon-from-ico  --linux-icon
        --file-version  --product-version
        --copyright  --trademark
        """


    #] only translating file to python code (if compile==True also compiles it)
    @staticmethod
    def translate_only(path:str, cache:bool, debug:bool, verbose:bool, compile:bool) -> bool:
        """only translates the script (does not run it), also compiles it if compile is true

        Args:
            path (str): path to the file
            cache (bool): wether should use cache or not
            debug (bool): debug flag
            verbose (bool): verbose flag
            compile (bool): compile flag

        Returns:
            bool: true if it runs successfully
        """
        path = rx.files.abspath(path)
        set_working_path(rx.files.dirname(path))

        source = convert_source(path, cache, debug, verbose)
        py_file_path = path.removesuffix(".rx")+".py"
        # if rx.files.exists(py_file_path):
            # print(f"{py_file_path} Already exists...")
            # if replace:=rx.io.yesno_input("Replace it? "):
                # rx.write(py_file_path, source)
        # else:
        rx.write(py_file_path, source)

        if compile:
            Tasks.compile()

        TIMES["TRANSLATE_ONLY"] = time.time()-START_TIME
        return True

    #] running the file given as terminal argument
    @staticmethod
    def runfile(path:str, cache:bool, debug:bool, verbose:bool) -> bool:
        """runs the given file (path)

        Args:
            path (str): path to file that should be run
            cache (bool): cache flag
            debug (bool): debug flag
            verbose (bool): verbose flag

        Raises:
            e: the exception that will be raised when running python on file

        Returns:
            bool: true if it runs successfully
        """
        path = rx.files.abspath(path)
        set_working_path(rx.files.dirname(path))

        source = convert_source(path, cache, debug, verbose)
        ready_file_name = convert_file_name(path)

        rx.write(ready_file_name, source)

        if verbose:
            #rx.cls()
            NOW = str(__import__('datetime').datetime.now())
            # probably consider changing next line from "NOW" to "START_TIME"
            print(f'''Start `RXL` at "{NOW[:NOW.rindex('.')+5]}"''')
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
            Error(type(e).__name__+': '+str(e))
            sys.exit()
        finally:
            rx.files.remove(ready_file_name)

        if verbose:
            EXECUTION_TIME_TEXT = round(time.time()-START_TIME,3)
            print(f'\n\nExecution Time:  {EXECUTION_TIME_TEXT}\n')
            #print(START_TIME)
            #print(EXECUTION_TIME_TEXT)

        return True


    @staticmethod
    def detect_task(args:Addict) -> tuple:
        """detects what task shoud be run from given arguments

        Args:
            args (Addict): dotted-dictionary of parsed arguments of terminal

        Returns:
            tuple: task:str, task_args:list of args that needs to be passed to task function
        """
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
    def run_task(task:str,args:list) -> bool:
        """calls the given task function with passing *args to it

        Args:
            task (str): name of the task
            args (list): list of arguments that are needed for the task's function

        Returns:
            bool: whether the task ran successfully or not
        """
        tasks_dict = {
            "console"  :  Tasks.Console,
            "translate":  Tasks.translate_only,
            "compile"  :  NotImplemented,
            "runfile"  :  Tasks.runfile,
        }
        return tasks_dict[task](*args)



#< Make Things Ready For Running >#
def Setup_Env() -> None:     #]  0.000 (with .hide():0.003)
    """Setups the environment for RXL to run."""
    if not rx.files.exists(CACHE_DIR):
        rx.files.mkdir(CACHE_DIR)
        # rx.files.hide(CACHE_DIR)


def set_working_path(path) -> None:
    """Set `WORKING_PATH` to path"""
    global WORKING_PATH
    WORKING_PATH = path



#< Check cache availablity >#
def get_cache(cache:bool, path:str, debug:bool, verbose:bool) -> str|None:
    """check to see if suitable cache can be found for `path` to use

    Args:
        cache (bool): cache flag from terminal
        path (str): path to the file to check for cache
        debug (bool): debug flag from terminal
        verbose (bool): verbose flag from terminal

    Returns:
        str|None: if cache is true and a suitable cache exists returns source for path else None
    """
    if cache is False:
        return None

    full_ready_path = f"{WORKING_PATH}/{CACHE_DIR}/{convert_file_name(rx.files.basename(path))}"
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
    TIMES["CACHE "] = time.time()-START_TIME
    return None


#< Save cache of `path` >#
def save_cache(path:str, source:str, cache_dir:str=CACHE_DIR) -> None:
    """Save cache for given path with given source in cache_dir

    Args:
        path (str): path to file that requests to be cached
        source (str): source of the file (translated)
        cache_dir (str, optional): relative dir to path to save cache file. Defaults to CACHE_DIR.
    """
    id = str(int(rx.files.mdftime(path)))
    source = id + "\n" + source
    rx.write(f"{WORKING_PATH}/{cache_dir}/{convert_file_name(rx.files.basename(path))}",source)



#< Translate Source (and write cache) >#
def translate(source:list, path:str, cache:bool, debug:bool, verbose:bool) -> tuple:
    """transalte given source (that comes from path)

    Args:
        source (list): list of lines of the given path
        path (str): path to the file that source comes from
        cache (bool): cache flag from terminal
        debug (bool): debug flag from terminal
        verbose (bool): verbose flag from terminal

    Returns:
        tuple: translated source, list of threads created during translation, info of app
    """
    source, lib_version, lib_shortcut, \
        type_scanner, info = Grammar.define_structure(source, path, debug)
    TIMES['DefStr'] = time.time()-START_TIME

    source, threads = Grammar.syntax(source, lib_version, lib_shortcut,
                             type_scanner, path, debug)
    TIMES['Syntax'] = time.time()-START_TIME

    source = '\n'.join(source)
    rx.write('translated', source)

    return source,threads,info



#< Translate >#
def convert_source(path:str, cache:bool, debug:bool, verbose:bool) -> str:
    """gets the translated source for path. waits for all threads to join

    Args:
        path (str): path to the file to convert the source
        cache (bool): cache flag from terminal
        debug (bool): debug flag from terminal
        verbose (bool): verbose flag from terminal

    Returns:
        str: translated source for path
    """
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
# if __name__ == "__main__":
def main():
    """Main function of the module that will be run from script of the package

    Raises:
        All errors will be raised right now as RXL is still in alpha stages
    """
    try:
        TIMES['Start '] = time.time()-START_TIME

        Setup_Env()
        TIMES['SetEnv'] = time.time()-START_TIME

        ARGS  = ArgumentParser.parse_args()
        # print(ARGS)
        TASK,TASK_ARGS = Tasks.detect_task(Addict(ARGS))
        TIMES['ARGS  '] = time.time()-START_TIME
        Tasks.run_task(TASK,TASK_ARGS)
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
