import os
import time
import shutil
import sys
import re
import argparse
import tokenize

from colored import  fg,bg,attr


class rx:
    @staticmethod
    def cls():
        os.system('cls')


    class record:
        def __init__(self):
            self.__start= time.time()
            self.laps=[]
        def lap(self,save=True, Round=15):     
            lp= round(time.time()-self.__start,Round)
            if save: self.laps.append(lp)
            return lp
        def reset(self,reset_start= False):
            self.laps= []
            if reset_start: self.__start= time.time()
        def last_lap(self, save=True):
            if save: self.laps.append(self.lap())
            return (self.lap(False)-self.laps[-1]) if self.laps else self.lap(False)
    Record = record


    class Terminal:
        run = os.system
        getoutput = __import__('subprocess').getoutput
        set_title = __import__('win32api').SetConsoleTitle
        get_title = __import__('win32api').GetConsoleTitle
    terminal = Terminal


    class style:
        def __init__(self,text,color='default',BG='black'):
            try:
                color= color.lower()
                BG=BG.lower()
                #style=style.lower()
            except:
                pass
            if color=='default':
                color=7 #188
            self.text= text     
            self.content= fg(color)+bg(BG)+text+attr(0)
        def __str__(self):
            return self.content
        def __repr__(self):
            return self.content
        def __add__(self,other):
            if type(other)!=rx.style:
                return self.content+other
            else:
                return self.content+other.content

        @staticmethod
        def print(text='', color='default', BG='default', style=0, end='\n'):

            if color=='default' and BG!='default':  # bg & !clr
                sys.stdout.write(f'{attr(style)}{bg(BG)}{text}{attr(0)}{end}')

            elif color!='default' and BG=='default':  # !bg & clr
                sys.stdout.write(f'{attr(style)}{fg(color)}{text}{attr(0)}{end}')

            elif color=='default' and BG=='default':  # !bg & !clr
                sys.stdout.write(f'{attr(style)}{text}{attr(0)}{end}')

            elif color!='default' and BG!='default':  # bg & clr
                sys.stdout.write(f'{attr(style)}{bg(BG)}{fg(color)}{text}{attr(0)}{end}')

        @staticmethod
        def switch(color='default', BG='black', style=0):
            if color == 'default':
                color = 7
            print(f'{attr(style)}{bg(BG)}{fg(color)}', end='')

        @staticmethod
        def switch_default():
            print(attr(0), end='')
        reset = switch_default

        @staticmethod
        def log_error(text, color='red', BG='default', style='bold'):
            rx.style.print(text, color, BG, style=style)
    Style = style


    class files:
        rename  = os.rename
        abspath = os.path.abspath
        exists  = os.path.exists
        mdftime = os.path.getmtime
        move    = shutil.move
        isfile = os.path.isfile
        @staticmethod
        def remove(path,force=False):
            if os.path.isfile(path):
                os.remove(path)
            else:
                if force: 
                    import shutil
                    shutil.rmtree(path)
                else:
                    try:
                        os.rmdir(path)
                    except OSError:
                        raise OSError(f"[WinError 145] The directory is not empty: '{path}'" + '\n' + ' '*23 + 
                                    '(Use force=True as an argument of remove function to remove non-empty directories.)')               
        @staticmethod
        def hide(path, mode:bool =True):
            import win32api, win32con
            if mode:
                win32api.SetFileAttributes(path,win32con.FILE_ATTRIBUTE_HIDDEN)
            else:
                win32api.SetFileAttributes(path,win32con.FILE_ATTRIBUTE_NORMAL)
        @staticmethod
        def read(path):
            with open(path) as f:
                FileR = f.read()
            return FileR
        @staticmethod
        def write(file, text='',mode='w'):
            with open(file, mode=mode) as f:
                f.write(text)

        @staticmethod
        def mkdir(path):
            try: os.mkdir(path)
            except FileExistsError: pass
    Files = files
    read  = files.read
    write = files.write


    class system:
        chdir = os.chdir
        accname = os.getlogin
        device_name = __import__('platform').node
    System = system


    class io: 
        @staticmethod
        def wait_for_input(prompt):
            answer= ''
            try:
                while not answer:
                    answer = input(prompt)
            except (EOFError,KeyboardInterrupt):
                print('EXITING...','red')
                sys.exit()
            return answer

        @staticmethod
        def selective_input(prompt,choices,default=None,error=False):
            while True:
                inp = input(prompt)
                if not inp  or  inp not in choices:
                    if error:
                        rx.style.print('Invalid input', 'red')
                    else:
                        inp = default
                        break
                else:
                    break
            return inp

        @staticmethod
        def yesno_input(prompt,default=None):
            return rx.io.selective_input(prompt,['y','yes','n','no'],default,not bool(default))

        @staticmethod
        def get_files(prompt='Enter File Name:  ', check_if_exists=True, sort= False, times=100):
            List = set()
            i = 1
            while i <= times:
                filename = rx.io.wait_for_input(prompt)
                if filename == 'end':
                    break
                pass
                if check_if_exists:
                    if rx.files.exists(filename):
                        List.add(filename)
                        i+=1
                    else:
                        rx.style.print('File Does Not Exist.')
                else:
                    i+=1
                    List.add(filename)
            if sort:
                return sorted(list(List))
            return list(List)
    SF = AF = NF = io

class IndentCheck:
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
        S, T = ' \t'


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

"""
################################################################################
# CHARS:  {✓ , ? , > , ! , X}
################
# TODO:
 #>  Load Modules:
       #> If Error happens in Loading module, .py file will remains
       #> Load modules with default Options
 #>  const keyword is not safe
 #>  Save Cache 
 #>  Define Ready_Objs from std
 #>  Extension Color for functions
 #>  Include XXX: Func1,Func2
 #>  A file to repair files (save all files in a zipfile)
 #>  "$" Family
       #> TEST  (try:x;except:pass)
 #>  Create RX App with Menu:
        #>  TERMINAL
              #> linux commands?
        #✓  Create SuperLite Module
 #>  Console support RX syntax ( '\n'.join(Syntax([line])) )
 #?  Debug Function in (--debug for debug-only && -d for run+debug)
 #?  Split line by strings, check_syntax spliteds ,connect them again
 #X  Fix Const func to accept one object
 #X  Constants Check for Error
 #X  Instead of using pip to download required modules, copy them
      (Because we couldn't find rquirements for all packages)
 #X  Debug with running linters
 #X  goto for For loops with naming For loops  (:NAME & goto NAME)
 #X  do_when Keyword for Calling specifiec function when condition comes True
 #X  Improve Exception Catching when runing file
 #!  END OF LINES ERROR IN RED  (WHAT?!)
 #✓  Check if decorator is Check_Type --> ms.Check_Type
 #✓  Array
 #✓  Constant Array __str/repr__ should be with <>
 #✓  Make object of Constant Array
###########
# NOTE:
 #>  Ready_File_Name without .rx extension?
 #>  Check for fast speed (if option of it is True)
 #>  Correct color for Options in extension (and also ignore cases)
        #> && -- ||
 #>  DEBUG (-d) is unused
 #>  do_while check for outline
 #>  Option for run translated or import it (import will ignore "if __name__ ...")
 #>  Package installer like pip? (if 3rd-party modules):
        #>  Create account (RX-Lang) in pypi to upload user packages
 #?  Combine sys.exit & cleanup
 #?  Function to check if expression is not in Quotes
 #?  NoBreak if there is python code in Base Lines
 #?  &&  ---  ||
 #?  Generate:yield(:None)
 #?  CONST at the beginning
 #?  Stop Imports
 #?  def(:None)
 #-  Copy modules to running dir
 #-  INFO['EMAIL']?
 #-  Whole code in Try-Except
 #-  New Errors Ext Color !
 #✓  How to run python file instead of os.system
###########
# BUG:
 #X  WTF!
       switch-case works fine in normal run but is not translated when loading
 #X  Check Array is defined with acceptable length
 #X  There couldnt be nested Switch-Case statements  (and Const-array?)
 #X  Errors in red Color
 #>  CONSTs:
       #!  After NameError rest of code will be ignored
 #?  Ignore module loading output error
 #X  Unable to run file with double clicking
 #X  Get Remaining Args for PROGRAM
 #X  Terminal is slow for loading code from first each time
 #X  Every Load takes 0.2
       #> Maybe with cache (check mdftime of files)
 #?  why exe doesn't accept args

########################################

# TODO (Release):
 #> Check instal:  PrependPath=1 (also for pip and scripts/*.exe)
 #> Make .exe with cxfreeze && copy .exe fileS in py/scripts dir
 #> Auto install famous 3rd-parties (requests-urllib3)
 #> ".rx" to ".exe" 

####
   #Loading Modules Are 10-1000x faster (But Tanslate Takes 0.4!)
################################################################################
"""

#] CHANGES
r"""
 C:\Users\IRANIAN\.vscode\extensions\ms-python.python-2020.8.105369\package.json   (1637)
 C:\Users\IRANIAN\.vscode\extensions\ms-python.python-2020.8.105369\snippets\python.json   (END)
 D:\Programs\Microsoft VS Code\resources\app\extensions\rx\language-configuration.json 13

 D:\Programs\Microsoft VS Code\resources\app\extensions\python\syntaxes\MagicPython.tmLanguage.json
 (1746 at the end) 276
 33    "include": "#class-declarations"
 280   "name": "storage.type.classx.python",
 1025  "class-declarations": {
 1751  "builtin-types": {
 1784   | include        (and much more)
 366   "rx-class-names": {
 362   "include": "#rx-class-names"
 1373  "function-declaration": {
 1836  "(?x)\n  (?<!\\.) \\b(\n    [A-Z]+[a-z]*Error\n  )\\b\n"        (Arithmetic | )
 #1883       | Module(-|_)(N|n)ame | (Method|Package(_|-)Version) | Func(_|-)Type(-|_)Checker | Print | (End-)?(Exit|Quit)\n
"""
#] VS Ext
r"""
 git add . && git commit
 vsce publish VERSION
 brs326qo5vgc774pezvenvixu4sj3c2lbwgqv66uwzsopcocl6ea

 Colors:
  invalid.deprecated.backtick.python   red
  support.type.exception.python        green
  support.variable.magic.python        blue light
  variable.other.constant.ruby         dodger_blue!
  storage.type.class.python            blue dark
  support.function.builtin.python      yellow
  keyword.control.flow.python          purple
"""
#] WHEN APP READY
r"""
 %USERPROFILE%
 #setx /M path "%path%;E:\ramin\Coding\GitHub\RX-Language"
 #C:\Users\IRANIAN\AppData\Roaming\ActiveState\bin;C:\Program Files (x86)\NVIDIA Corporation\PhysX\Common;C:\WINDOWS\system32;C:\WINDOWS;C:\WINDOWS\System32\Wbem;C:\WINDOWS\System32\WindowsPowerShell\v1.0\;C:\WINDOWS\System32\OpenSSH\;C:\ProgramData\chocolatey\bin;D:\Programs\Coding\Git\cmd;C:\Users\IRANIAN\AppData\Local\Programs\Python\Python37;C:\Users\IRANIAN\AppData\Local\Programs\Python\Python37\Scripts;D:\Programs\Microsoft VS Code\bin;C:\Users\IRANIAN\AppData\Local\GitHubDesktop\bin;C:\Users\IRANIAN\AppData\Roaming\npm
"""





__version__ = '1.0.0'

START_TIME = time.time()

print = rx.style.print
Error = rx.style.log_error

RX_PATH = os.path.abspath(__file__)[:-6]

CLASSES = (['files', 'system', 'random', 'record', 'style', 'terminal', 'Tuple'],
           ['Files', 'System', 'Random', 'Record', 'Style', 'Terminal', 'Tuple']
            #'internet', 'Internet'
           )

LOADED_PACKAGES = []
Lines_Added = 0



#< Make Things Ready For Running >#   0.035
def Setup_Env():
    rx.files.mkdir('__RX_LIB__')
    rx.write('__RX_LIB__/__init__.py')
    rx.files.hide('__RX_LIB__')


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
            print( 'Traceback (most recent call last):')
            print(f'  File "{File}", line {line_nom-Lines_Added}, in <module>')
            print( '    '+line_text)
            Error(f"BaseDefinedError: '{attribute}' can not be defined after setting module [OPTIONS]")
            Clean_Up(File)
            sys.exit()

    class ValueError(Exception):
        def __init__(self, 
                File,       attribute=None , value=None, line_text='', 
                line_nom=0, correct_list=[], msg=None):
            print( 'Traceback (most recent call last):')
            print(f'  File "{File}", line {line_nom-Lines_Added}, in <module>')
            print( '    '+line_text)
            if not msg:
                Error(f"ValueError: '{attribute}' can not be '{value}'. Valid Choices: {correct_list}")
            else:
                Error(f"ValueError: {msg}")
            Clean_Up(File)
            sys.exit()

    class ConstantError(Exception):
        def __init__(self,
          Line_Nom=0  , Line_Def=0, Line_Text='', 
          Attribute='', File=''   , msg=None):
            print( 'Traceback (most recent call last):')
            print(f'  File "{File}", line {Line_Nom-Lines_Added}, in <module>')
            print( '    '+Line_Text)
            end = msg if msg else f"Redefinition of '{Attribute}' (Already Defined At Line {Line_Def})"
            Error("ConstantError: "+ end)
            Clean_Up(File)
            sys.exit()

    class IndentionError(Exception):
        def __init__(self,
          Line_Nom=0, Line_Text='', File=''):
            print( 'Traceback (most recent call last):')
            print(f'  File "{File}", line {Line_Nom-Lines_Added}, in <module>')
            print( '    '+Line_Text)
            Error("IndentationError: expected an indented block")
            Clean_Up(File)
            sys.exit()

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
        def __init__(self, File, Name=None, line_text='', line_nom=0):
            print( 'Traceback (most recent call last):')
            print(f'  File "{File}", line {line_nom-Lines_Added}, in <module>')
            print( '    '+line_text)
            Error(f"ModuleNotFoundError: No module named '{Name}'")
            Clean_Up(File)
            sys.exit()

    class AttributeError(Exception):
        def __init__(self,File, Line_Nom, Line_Text, Module_Version, Attribute):
            print( 'Traceback (most recent call last):')
            print(f'  File "{File}", line {Line_Nom-Lines_Added}, in <module>')
            print( '    '+Line_Text)
            Error(f"AttributeError: module '{Module_Version}' has no attribute '{Attribute}'")
            Clean_Up(File)
            sys.exit()

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
            print( 'Traceback (most recent call last):')
            print(f'  File "{File}", line {Line_Nom-Lines_Added}, in <module>')
            print( '    '+Line_Text)
            Error(f"SyntaxError: {msg}")
            Clean_Up(File)
            sys.exit()


#< Get Arguments >#      #TODO: add (-s --start) to start menu items
def Get_Args():

    #print('ARGS:  '+str(sys.argv), 'green')
    #print(os.getcwd(),'green')

    if len(sys.argv) == 1:
        #Console()
        #Menu.menu()
        Menu.Terminal()
        sys.exit()

    #if len(sys.argv) > 3:
    #    print('Argument Parser Will be added in next versions','dodger_blue_1')
    #    sys.exit()



    parser = argparse.ArgumentParser(
        'RX', allow_abbrev=True,
        description='"RX Language Executer"',

    )

    parser.add_argument(
        '-i', '--info',
        action='store_true',
        help='Show information about running file (Verbose option in other apps)'
    )

    parser.add_argument(
        'FILE',
        metavar='FILE', type=str, nargs='?',
        help='File to execute with RX language'
    )

    parser.add_argument(
        '-o','--options',
        action='store_true',
        help='Show Options to Customize File-Run and Exit'
    )

    parser.add_argument(
        '-d',
        action='store_true',
        help='Debug file/code/syntax Before running it and print Mistakes in Red color'
    )

    parser.add_argument(
        '--debug',
        action='store_true',
        help='Debug-Only mode. This will not run file. It just Debugs it'
    )

    parser.add_argument(
        '-MT',
        action='store_true',
        help='Module Test. Not Very Usefull For Beginers'
    )

    parser.add_argument(
        '-T2P',
        action='store_true',
        help='Translate To Python'
    )

    parser.add_argument(
        'PROG_ARGS',
        action='store', 
        nargs=argparse.REMAINDER)


    args = parser.parse_args()
    #print(args.PROG_ARGS,'red')


    if args.options:
        print('BASE OPTIONS:'                                                                                                , style='bold')
        print("  OPTION NAME       DEFAULT VALUE       DESCRYPTION"                                                          , style='bold')
        print('  Module-Name       sc                  Shortcut for RX Tools and functions (also "Modulename")'                            )
        print('  Method            normal              Method of loading tools.'                                                           )
        print('                                          Valid Choices: [normal,[lite,fast]] (also "Package-Version)"'                     )
        print('  Print             stylized            Print function to use. Valid Choices: [normal,stylized]'                            )
       #print('OPTIONS:'                                                                                                     , style='bold')
       #print("  OPTION NAME       DEFAULT VALUE       DESCRYPTION"                                                                        )
        print('  Func_Type_Checker True                Check if arguments of a function are in wrong type'                                 )
       #print('                                          (REGEX:  (func|function)-?(type|arg|param)-?(scanner|checker) )'                  )
        print('  Exit              True                Exit after executing the code or not'                                               )
        print(                                                                                                                             )
       #print('"OPTIONS" SHOULD BE DEFINED AFTER "BASE OPTIONS"'                                                             , style='bold')

        sys.exit()
    elif not args.FILE:
        Menu.Console()
        #Menu()
        sys.exit()

    if args.debug:
        args.d = True


    #print('ARGS:  '+str(args))
    #sys.exit()
    return args.FILE, args.info, args.d, args.debug, args.MT, args.T2P, args.PROG_ARGS


#< Menu >#
class Menu:

    #< Interactive RX Shell >#
    @staticmethod
    def Console():
        rx.terminal.set_title('RX - Console')

        from importlib import reload

        rx.system.chdir(RX_PATH)
        PRE= ['import rx7.lite as std','print = std.style.print']
        rx.write('_Console_.py', '\n'.join(PRE)+'\n')
        import _Console_
        while True:
            try:
                new = rx.io.wait_for_input('RX:Console> ')
                if new.lower() in ('exit','quit','end'):
                    rx.files.remove('_Console_.py')
                    #sys.exit()
                    return
            except (KeyboardInterrupt,EOFError):
                rx.files.remove('_Console_.py')
                return#sys.exit()

            rx.write('_Console_.py', new+'\n', 'a')

            try:
                reload(_Console_)
            except (EOFError,KeyboardInterrupt):
                return
            except Exception as e:
                ERROR = str(e)
                if '(_Console_.py,' in ERROR:
                    ERROR = ERROR[:ERROR.index('(_Console_.py,')]
                print(str(type(e))[8:-2]+':  ' + ERROR, 'red')
                rx.write('_Console_.py', '\n'.join(rx.read('_Console_.py').splitlines()[:-1])+'\n')

            if re.search(r'^print\s*\(', rx.read('_Console_.py').splitlines()[-1].strip()):
                rx.write('_Console_.py', '\n'.join(rx.read('_Console_.py').splitlines()[:-1])+'\n')

    @staticmethod
    def Terminal():
        rx.cls()
        rx.terminal.set_title(f'RX:Terminal  |  {rx.system.device_name()}:{rx.system.accname()}')
        NOW = str(__import__('datetime').datetime.now())
        Menu_Dict = { 
           #'Terminal'   : Menu.Terminal ,
            'Console'    : Menu.Console  ,
           #'System Info': Menu.SysInfo  ,
           #'Compile'    : Menu.Compile  ,
            'Create Module Lite' : Menu.Create_SLModule
        }
        print(f"RX v{__version__} Running on {rx.system.device_name()}::{rx.system.accname()} ({NOW[:NOW.rfind('.')]})")
        while True:
            print('RX:Terminal', 'green', end='')
            print('@', end='')
            print(os.getcwd(), 'dodger_blue_1', end='')
            try:
                inp = input('> ')

                if inp.title() in Menu_Dict.keys():
                    Menu_Dict[inp.title()]()
                elif inp in ('help','commands'):
                    print('Beside all CMD commands, we also support these commands:')
                    print('  - Console')
                    print('  - System Info')
                    print('  - Compile')
                    print('  - Create Module Lite')
                elif inp in ('exit','quit'):
                    Clean_Up()
                    sys.exit()
                elif Regex:=re.search(r'cd (?P<path>.+)',inp):
                    try:
                        os.chdir(Regex.group('path'))
                    except (FileNotFoundError,NotADirectoryError):
                        print('Invalid path','red')
                elif inp == 'python':
                    rx.terminal.run('python')
                elif inp == 'cmd':
                    rx.terminal.run('cmd')
                elif inp in ('cls','clear'):
                    rx.terminal.run('cls')
                else:
                    output = rx.terminal.getoutput(inp)
                    app = inp.split(' ')[0]
                    output_list = output.splitlines()
                    if output:
                        if (f"{app} : The term '{app}' is n" in output_list[0])  or  (
                            f"'{app}' is not recognized as" in output_list[0]):
                            print('App/Command not found', 'red')
                        else:
                            print(output)
            except (EOFError,KeyboardInterrupt):
                print('Exiting...','red')
                sys.exit()

    @staticmethod
    def Create_SLModule():
        import inspect
        import rx7.lite as STD
        File = rx.io.get_files('Enter listed functions file name:  ',times=1)[0]
        output = 'MODULE.py'

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

        # Ignore Docstrings and Comments        
        if Text.strip().startswith('#'):
            continue
        elif '"""' in Text  and  not ("'''" in Text and Text.index('"""')>Text.index("'''")):
            if not '"""' in Text[Text.index('"""')+3:]:
                for line_in_str,text_in_str in enumerate(SOURCE[Line_Nom:],1):
                    if '"""' in text_in_str:
                        Skip = line_in_str
                        #print(Skip)
                        continue
        elif '"""' in Text:
            if not "'''" in Text[Text.index("'''")+3:]:
                for line_in_str,text_in_str in enumerate(SOURCE[Line_Nom:],1):
                    if "'''" in text_in_str:
                        Skip = line_in_str
                        #print(Skip)
                        continue

        #] Indent
        if Text.strip().endswith(':'):#.startswith(Keywords):
            BREAK = False
            LINE = int(Line_Nom)
            while not BREAK:
                if SOURCE[LINE-1].strip().endswith(':'):
                    BREAK = True
                else:
                    LINE += 1

            INDENT = len(re.search(r'^(?P<indent>\s*).*', Text).group('indent'))
            INDENT_START = len(re.search(r'^(?P<indent>\s*).*', SOURCE[LINE]).group('indent'))
            if INDENT_START <= INDENT:
                #print('RX_Err','red')
                raise ERRORS.IndentionError(Line_Nom+1, SOURCE[Line_Nom], FILE)


    #< OPTIONS >#
    MODULE_VERSION  = 'rx7'
    MODULE_SHORTCUT = 'std'#'sc'
    PRINT_TYPE = 'stylized'
    TYPE_SCANNER = False
    #BASED = False
    Changeable = []
    INFO = {
        'Version':'1.0.0',
        'Author':rx.system.accname(),
        'Title': FILE.split('/')[-1].split('.')[0]}
    Skip = 0

    for nom,line in enumerate(SOURCE[:10]):

        if not line.strip() or line.strip().startswith('#'):
            Changeable.append(nom)

        #] Get Shortcut Name
        elif re.search(r'^((M|m)odule(-|_)?(N|n)ame)\s*:\s*\w+',line):
            #if BASED:
            #    raise ERRORS.BaseDefinedError('Modulename', line, SOURCE[:5].index(line), FILE)
            stripped = line[line.index(':')+1:].strip()
            if re.search(r'\w+', stripped).group() == stripped:
                MODULE_SHORTCUT = str(stripped)
            else:
                raise ERRORS.ValueError(msg='Invalid Value For  modulename/module_name', File=FILE)
                        #SOURCE.remove(line)
            SOURCE[nom] = ''
            Changeable.append(nom)

        #] Get Version (Method) of Tools
        elif re.search(r'^(Method|Package(-|_)Version)\s*:\s*\w*', line):
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

        #] Print Function Method
        elif re.search(r'^Print\s*:\s*\w*', line):
            #BASED = True
            if line.strip().lower().endswith('normal'):
                PRINT_TYPE = 'normal'
            elif not line.strip().lower().endswith('stylized'):
                stripped = line[line.index(':')+1:].strip()
                raise ERRORS.ValueError(FILE, 'print', stripped, line, 
                                       SOURCE[:10].index(line), ['lite','normal'])
            SOURCE[nom] = ''
            Changeable.append(nom)

        #] Function Type Scanner          TODO: # Make it Shorter!
        elif re.search(r'^((F|f)unc(tion)?)(-|_)?((T|t)ype|(A|a)rg|(P|p)aram)(-|_)?((S|s)canner|(C|c)hecker)\s*:\s*\w*', line):
            #print("FOUND",'green')
            #BASED = True     # No Need to do it
            
            if line.endswith('True'):
                TYPE_SCANNER = True
            elif not line.strip().endswith('False'):
                stripped = line[line.index(':')+1:].strip()
                raise ERRORS.ValueError(FILE, 'func_type_checker', stripped, line, 
                                       SOURCE.index(line), "[True,False]")
            SOURCE[nom] = ''
            Changeable.append(nom)

        #] Exit at the end
        elif re.search(r'^(End(-|_))?(Exit|Quit)\s*:\s*\w*', line):
            if line.strip().lower().endswith('false'):
                SOURCE.append('__import__("getpass").getpass("Press [Enter] to Exit")')
            elif not line.strip().lower().endswith('true'):
                stripped = line[line.index(':')+1:].strip()
                raise ERRORS.ValueError(FILE, 'Exit', stripped, line, 
                                       SOURCE.index(line), "[True,False]")
            SOURCE[nom] = ''
            Changeable.append(nom)

        #] Version
        elif Regex:=re.search(r'^Version\s*:\s*(?P<Version>[0-9]+(\.[0-9]+)?(\.[0-9]+)?)', line.strip()):
            INFO['Version'] = Regex.group('Version')
            SOURCE[nom] = ''
            Changeable.append(nom)
        #] Title
        elif Regex:=re.search(r'^Title\s*:\s*(?P<Title>[^>]+)(>.+)?', line.rstrip()):
            INFO['Title'] = Regex.group('Title')
            SOURCE[nom] = ''
            Changeable.append(nom)
        #] Author
        elif Regex:=re.search(r'^Author\s*:\s*(?P<Author>.+)', line.rstrip()):
            INFO['Author'] = Regex.group('Author')
            SOURCE[nom] = ''
            Changeable.append(nom)

        else:
            break

    #print(INFO)
    
    #] Bases
    STRING = []
    STRING.append(f"import {MODULE_VERSION} as {MODULE_SHORTCUT}")
    STRING.append(f"std = {MODULE_SHORTCUT}")
    STRING.append(f"print = {MODULE_SHORTCUT+'.style.print' if PRINT_TYPE=='stylized' else 'print'}")
    #] Direct Attributes
    STRING.append(f"const = {MODULE_SHORTCUT}._Lang.Const")
    STRING.append(f"array = {MODULE_SHORTCUT}._Lang.Array")
    STRING.append(f"Check_Type = {MODULE_SHORTCUT}.Check_Type")
    for key,value in INFO.items():
        STRING.append(f"setattr(std,'{key}','{value}')")

    if len(Changeable):
        for line in Changeable:
            if line == Changeable[-1]:
                SOURCE[line] = ';'.join(STRING)
            else:
                try:
                    SOURCE[line] = STRING[0]
                    STRING = STRING[1:]
                except IndexError:
                    break
    else:
        SOURCE.insert(0, ';'.join(STRING))

    if DEBUG and not len(Changeable):
        print(f'{FILE}> No (Enough) Base-Option/Empty-lines at begining of file', 'red')


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
    threads = []

    for Line_Nom,Text in enumerate(SOURCE, 1):

        #print(str(Line_Nom)+' '+Text)

        Striped = Text.strip()
        for item in CONSTS:
            if re.search(rf'( |;|^$){item[0]}\s*(\[.+\])?\s*=\s*[^=]+', Text):  # \s*.+  {?} 
                if not Striped.startswith('def ')  and  not Striped.startswith('#'):
                    raise ERRORS.ConstantError(Line_Nom, item[1], Striped, item[0], FILE)

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
        if Text.strip().startswith('#'):
            continue
        elif '"""' in Text  and  not ("'''" in Text and Text.index('"""')>Text.index("'''")):
            if not '"""' in Text[Text.index('"""')+3:]:
                for line_in_str,text_in_str in enumerate(SOURCE[Line_Nom:],1):
                    if '"""' in text_in_str:
                        Skip = line_in_str
                        #print(Skip)
        elif '"""' in Text:
            if not "'''" in Text[Text.index("'''")+3:]:
                for line_in_str,text_in_str in enumerate(SOURCE[Line_Nom:],1):
                    if "'''" in text_in_str:
                        Skip = line_in_str
                        #print(Skip)

        #] Include
        elif Regex:=re.search(r'^(?P<Indent>\s*)include \s*(\w+,?|\*)?', Text):
            Indent = Regex.group('Indent')
            if re.search(r'^(I|i)nclude\s*\*', Text.strip()):
                Packages = list(CLASSES[0])
            else:
                Packages = re.split(r'\s*,\s*', Text)
                Packages[0]= Packages[0][len(Indent)+8:].strip()
            #SOURCE.remove(Text)
            To_Add = str(Indent)
            for package in Packages:
                if package not in CLASSES[0]+CLASSES[1]:
                    raise ERRORS.AttributeError(FILE,Line_Nom,Text,MODULE_VERSION,package)
                #SOURCE.insert(Line_Nom-1, f'{Indent}{package} = {MODULE_SHORTCUT}.{package}')
                To_Add += f'{package}={MODULE_SHORTCUT}.{package};'
            SOURCE[Line_Nom-1] = To_Add
            # continue  # do it to all?

        #] Func Type checker
        elif Striped.startswith('def ') and TYPE_SCANNER:  # Make it regex?
            if SOURCE[Line_Nom-2].strip().endswith('Check_Type'):
               SOURCE[Line_Nom-2]= re.search(r'(\s*)',Text).group(1)+f'@std.Check_Type' 
            if SOURCE[Line_Nom-2].strip().startswith('@'):
                continue
            indent = Text.index('def ')
            SOURCE.insert(Line_Nom-1, f'{" "*indent}@{MODULE_SHORTCUT}.Check_Type')
            Skip = 1
            Lines_Added += 1

        #] Switch and Case
        elif Regex:=re.search(r'^\s*(?P<indent>\s*)(S|s)witch\s+(?P<VARIABLE>\w+)\s*:', Text):
            indent = Regex.group('indent')

            rules = 0
            for nom2,line2 in enumerate(SOURCE[Line_Nom:], 1):
                if not line2:
                    continue
                if not re.search(r'^(?P<indent2>\s*)\w+', line2) and  not rules:
                    #new = len(re.search(r'^(?P<indent2>\s*)', line2).group('indent2'))
                    LAST_LINE = nom2 + Line_Nom -1
                    break
            else:
                LAST_LINE = -1

            #SOURCE.remove(Text)
            Default = False
            SOURCE[Line_Nom-1] = f'{indent}if False: pass'
            for Line,snc in enumerate(SOURCE[Line_Nom-1:LAST_LINE], Line_Nom):
                if re.search(r'^(D|d)efault\s*:\s*',snc.strip()):
                    SOURCE[Line-1] = indent+'else:'
                    Default = True
                SEARCH_VALUE = re.search(r'^(C|c)ase\s+(?P<Nobreak>(N|n)obreak)?(?P<VALUE>.+):\s*', snc.strip())
                if SEARCH_VALUE:
                    if Default:
                        raise ERRORS.SyntaxError(FILE,Line_Nom+Line,snc,
                                                 'Case is defined after default')
                    IF_EL = 'el' if not SEARCH_VALUE.group('Nobreak') else ''
                    if re.search(fr'^{IF_EL}if \w+\s+==', SOURCE[Line-1].strip()):
                        raise TypeError
                    else:
                        pass#SOURCE[Line-1] =   indent + '    ' + SOURCE[Line-1]
                    variable = Regex.group("VARIABLE")
                    value    = SEARCH_VALUE.group("VALUE")
                    SOURCE[Line-1] = f'{indent}{IF_EL}if {variable} == {value}:' #+4

        #] Load User-Defined Modules        # TODO: Better regex to get packages
        elif Regex:=re.search(r'^(?P<indent>\s*)load \s*(\w+,?)?', Text.strip()):
            t = time.time()
            Indent = Regex.group('indent')
            Packages = re.split(r'\s*,\s*', Text)
            Packages[0]= Packages[0][4:].strip()

            #SOURCE.remove(Text)
            #SOURCE[Line_Nom-1]=''
            To_Add = str(Indent)
            t2 = rx.record()
            rx.files.mkdir('__RX_LIB__')
            if not rx.files.exists('__RX_LIB__/__init__.py'):
                rx.write('__RX_LIB__/__init__.py')
            
            for package in Packages:
                if rx.files.exists(f'{package}.rx7'):
                    import threading
                    def TEST():
                        pack_out = rx.terminal.getoutput(f'python RX.py -MT {package}.rx7').strip()
                        
                        if len(pack_out):
                            #print(pack_out)
                            if re.search(r'^\w+Error', pack_out.splitlines()[-1]):
                                raise ERRORS.LoadError(package,FILE,pack_out.splitlines()[-1])
                            else:
                                raise ERRORS.LoadError(package,FILE)
                    thread = threading.Thread(target=TEST)
                    thread.start()
                    threads.append(thread)
                    LOADED_PACKAGES.append(package)
                    To_Add += f"{package}={MODULE_SHORTCUT}.import_module('__RX_LIB__/{package}.py');"
                else:
                    raise ERRORS.ModuleNotFoundError(FILE, package, Text, Line_Nom)
            #print(t2.lap())
            SOURCE[Line_Nom-1]=str(To_Add)
            print(f'Load: {time.time()-t}','green')

        #] Memory Location of Object
        elif re.search(r'''[,\(\[\{\+=: ]&\w+''', Text): #[^a-zA-Z0-9'"]
            Search=re.search(r' ?&(\w+)', Text)
            SOURCE[Line_Nom-1] = Text.replace(Search.group(),f'hex(id({Search.group(1)}))')

        #] until & unless & foreach & func
        elif Regex:=re.search(r'^until \s*(?P<Expression>.+):'  , Striped):
            SOURCE[Line_Nom-1] = f"if not ({Regex.group('Expression')}):"
        elif Regex:=re.search(r'^unless \s*(?P<Expression>.+):' , Striped):
            SOURCE[Line_Nom-1] = f"if not ({Regex.group('Expression')}):"
        elif Regex:=re.search(r'^foreach \s*(?P<Expression>.+):', Striped):
            SOURCE[Line_Nom-1] = SOURCE[Line_Nom-1].replace('foreach', 'for', 1)
        elif Regex:=re.search(r'^func \s*(?P<Expression>.+)'    , Striped):
            SOURCE[Line_Nom-1] = SOURCE[Line_Nom-1].replace('func', 'def', 1)

        #] Const Var                        # TODO: Better regex
        elif Striped.startswith('const '):
            #if Text.startswith(' '): raise LateDefine("'Const' Must Be Defined In The Main Scope")
            if Regex:=re.search(r'^(?P<Indent>\s*)const\s+(?P<VarName>\w+)\s*=\s*(?P<Value>.+)\s*', Text):
                Indent  =  Regex.group('Indent' )
                VarName =  Regex.group('VarName')
                Value   =  Regex.group('Value'  )
                SOURCE[Line_Nom-1] =  f'{Indent}{VarName} = {Value}'
                if VarName != VarName.upper()  and  DEBUG:
                    #] maybe it should be just a warning
                    print(f"{FILE}:{Line_Nom}> Constant Variable Name ({VarName}) is not UPPERCASED",'red')
                    '''
                     raise ERRORS.ConstantError(Line_Nom=Line_Nom, 
                                               Line_Text=Text.strip(), 
                                               File=FILE, 
                                               msg='Constant Variable Name Must be UPPERCASE')
                    '''
                for item in CONSTS:  #] Check if Const X is already defined
                    if VarName == item[0]:
                        raise ERRORS.ConstantError(Line_Nom, item[1], Text.strip(), item[0], FILE)
                CONSTS.add((VarName, Line_Nom))

        #] Const Array                      # TODO: Better regex
        elif Regex:=re.search(r'(?P<Indent>\s*)(?P<VarName>\w+)\s*=\s*<(?P<Content>.*)>', Text):
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
        elif Regex:=re.search(r'(?P<Indent>\s*)do\s*:\s*',Text):  #Striped.startswith('do '):
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
        elif Regex:=re.search(
                r'(?P<Indent>\s*)array (?P<VarName>\w+)\[(?P<Length>\w+)?:?(?P<Type>\w+)?\]\s*=\s*{(?P<Content>.*)}',
                Text):
            Indent  = Regex.group('Indent')
            VarName = Regex.group('VarName')
            Length  = Regex.group('Length')
            Type    = Regex.group('Type')
            Content = Regex.group('Content')

            Length  = '' if not Length  else ',size=' +Length
            Type    = '' if not Type    else ',type_='+Type

            SOURCE[Line_Nom-1] = f'{Indent}{VarName} = {MODULE_SHORTCUT}._Lang.Array({Content}{Type}{Length})'


    return SOURCE,threads


#< Verbose >#
def Add_Verbose(SOURCE, INFO):
    NOW = str(__import__('datetime').datetime.now())
    print(f'''Start  RX Language  at  "{NOW[:NOW.rindex('.')+5]}"''')
    print(f'Running  "{INFO["Title"]}" v{INFO["Version"]}  by "{INFO["Author"]}"')
    print('\n')

    SOURCE.insert(0, f'ProgramStartTime= {START_TIME}')
    EXECUTE_TIME_TEXT = 'round(__import__("time").time()-ProgramStartTime,3)'
    SOURCE.insert(-1, 'EXECUTE_TIME_TEXT='+EXECUTE_TIME_TEXT) #{EXECUTE_TIME_TEXT-.35}/
    SOURCE.insert(-1, r'''print(f'\n\nExecution Time:  {EXECUTE_TIME_TEXT}\n')''')
    #print(SOURCE[-3])

    return SOURCE


#< Clean Everything Which is Not Needed >#
def Clean_Up(File='',Lib=True):   #] 0.03
    #return
    if Lib:
        try: rx.files.remove(f'__RX_LIB__', force=True)
        except: pass
    else: pass
    try: os.remove(File)
    except: pass
    try: rx.files.remove('__pycache__', force=True)
    except: pass
    try: rx.files.remove('_Console_.py')
    except: pass




#< START OF THE CODE >#
if __name__ == "__main__":
    try:
        TIMES = {}
        TIMES['Start '] = time.time()-START_TIME #print(f'START  :: {time.time()-START_TIME}','green')
        ARGS = Get_Args()                                                            #] 0.003
            # {0:FILE , 1:info , 2:d , 3:debug, 4:MT, 5:T2P, 6:Prog_Args}  
        FILE   = ARGS[0]
        TIMES['ARGS  '] = time.time()-START_TIME
        #rx.cls()
        SOURCE = Read_File(FILE)
        SOURCE = Define_Structure(SOURCE, FILE, ARGS[2])                             #] 0.020
        INFO = SOURCE[4]
        TIMES['DefStr'] = time.time()-START_TIME
        SOURCE,threads = Syntax(SOURCE[0], SOURCE[1], SOURCE[2], SOURCE[3], FILE, ARGS[2])   #] 0.008
        TIMES['Syntax'] = time.time()-START_TIME
        if ARGS[1]:
            rx.cls()
            SOURCE = Add_Verbose(SOURCE, INFO)
        READY_FILE_NAME = '_'+FILE+'_'
        #print(Lines_Added)
        if not ARGS[3] and not ARGS[4]:
            try:
                rx.write(READY_FILE_NAME, '\n'.join(SOURCE))
            except PermissionError:
                rx.files.remove(READY_FILE_NAME)
                rx.write(READY_FILE_NAME, '\n'.join(SOURCE))
            rx.write('translated', '\n'.join(SOURCE))
            rx.files.hide(READY_FILE_NAME)
        title = rx.terminal.get_title()
        
        if ARGS[5]:
            rx.write(f'{FILE.split(".")[0]}.py', '\n'.join(SOURCE))
        if ARGS[4]:
            rx.write(f'./__RX_LIB__/{FILE.split(".")[0]}.py', '\n'.join(SOURCE))

        if not ARGS[3] and not ARGS[4] and not ARGS[5]:
        #if not all([[ARGS[3],ARGS[4]],ARGS[5]]):
            rx.terminal.set_title(f'RX - {os.path.basename(FILE)}')
            try:
                '''
                     if B_Run > 0.1:
                         print('Running Speed is Slow','red')
                     elif B_Run < 0.015:
                         print('Running Speed is Super Fast','green')
                '''
                TIMES['B_Run '] = time.time()-START_TIME
                for k,v in TIMES.items(): print(f'{k} :: {v}','green')
                import runpy
                for thread in threads:
                    thread.join()
                runpy.run_path(READY_FILE_NAME)
            except Exception as e:
                raise e
                print('Traceback (most recent call last):')
                print('  More Information in Next Updates...')
               #print(f'  File "{FILE}" in  "UNDEFINED"')
                Error(type(e).__name__+': '+str(e))
                sys.exit()

    except KeyboardInterrupt:
        #Clean_Up(File)
        Error('\nExiting Because of KeyboardInterrupt Error (Ctrl+C)')

    except Exception as E:
        if ARGS[4]:
            raise E
        raise E
        #raise E# from None
        print('Traceback (most recent call last):')
        print('  Error occured when making environment ready to run')
        print('SystemError: '+str(E), 'red', style='bold')
        print('Please report this to the RX maintainer, along with the traceback and version')

    finally:
        if not ARGS[4]:
            Clean_Up('_'+FILE+'_')
        rx.terminal.set_title(rx.terminal.get_title())  

