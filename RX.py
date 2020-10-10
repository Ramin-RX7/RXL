import sys
import re
import time


START_TIME = time.time()

import rx7.lite as rx




print = rx.style.print






#< CHANGES >#
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
"""
#< VS Ext >#
r"""
 git add . && git commit
 vsce publish VERSION
 
 Colors:
  invalid.deprecated.backtick.python   red
  support.type.exception.python        green
  support.variable.magic.python        blue light
  variable.other.constant.ruby         dodger_blue!
  storage.type.class.python            blue dark
  support.function.builtin.python      yellow
  keyword.control.flow.python          purple
"""
#< WHEN APP READY >#
r"""
 %USERPROFILE%
 #setx /M path "%path%;E:\ramin\Coding\GitHub\RX-Language"
 #C:\Users\IRANIAN\AppData\Roaming\ActiveState\bin;C:\Program Files (x86)\NVIDIA Corporation\PhysX\Common;C:\WINDOWS\system32;C:\WINDOWS;C:\WINDOWS\System32\Wbem;C:\WINDOWS\System32\WindowsPowerShell\v1.0\;C:\WINDOWS\System32\OpenSSH\;C:\ProgramData\chocolatey\bin;D:\Programs\Coding\Git\cmd;C:\Users\IRANIAN\AppData\Local\Programs\Python\Python37;C:\Users\IRANIAN\AppData\Local\Programs\Python\Python37\Scripts;D:\Programs\Microsoft VS Code\bin;C:\Users\IRANIAN\AppData\Local\GitHubDesktop\bin;C:\Users\IRANIAN\AppData\Roaming\npm
"""

"""
################################################################################

#### EXT: RUN FILE
# TODO:
 #>  Improve Exception Catching when runing file
 #>  reindent->rx for indent checking or opposite?
 #>  Load Packages
 #?  Errors in red Color
 #X  Catch Error in Running file
 #X  Do_While loop
 #!  END OF LINES ERROR IN RED
###########
# NOTE:
 #>  Option for run translated or import it (import will ignore "if __name__ ...")
 #>  CONST at the beginning?
 #>  Stop Imports?
 #>  New Errors Ext Color
 #>  Package installer like pip? (if 3rd-party modules)
 #?  Improve switch & case
###########
# XXX!:
 #>  CONSTs:
       #>  After NameError rest of code will be ignored
 #>  No Support for args
 #!  Terminal is slow for loading code from first each time
 #!  0.35 seconds are spent for what
 #!  why exe doesn't accept args
 #✓  if if statement is more than 1 line it will be indent error

########################################

# Release TODO:
 #> Check instal:  PrependPath=1
 #> Make .exe with cxfreeze && copy .exe fileS in py/scripts dir
 #> Auto install famous 3rd-parties (requests-urllib3)
 #> ".rx" to ".exe" 

################################################################################
"""






RX_PATH = rx.files.abspath(__file__)[:-6]

CLASSES = ('files'  , 'system' , #'datetime' ,
           'random' , 'style'  , #'internet' , 
           'record' , 'Tuple'  , 'terminal' ,)


#< List of all errors >#
class ERRORS:
    class BaseDefinedError(Exception):
        def __init__(self, attribute, line_text, line_nom, File):
            #super().__init__(f"Already Defined {attribute}")
            print( 'Traceback (most recent call last):')
            print(f'  File "{File}", line {line_nom}, in <module>')
            print( '    '+line_text)
            print(f"BaseDefinedError: '{attribute}' can not be defined after setting module [OPTIONS]")
            sys.exit()

    class NameError(Exception):
        def __init__(self, 
                File, attribute=None, value=None, line_text='', 
                line_nom=0, correct_list=[], msg=None):
            print( 'Traceback (most recent call last):')
            print(f'  File "{File}", line {line_nom}, in <module>')
            print( '    '+line_text)
            if not msg:
                print(f"NameError: '{attribute}' can not be {value}. Valid Choices: {correct_list}")
            else:
                print(f"NameError: {msg}")
            sys.exit()
    
    class ConstantError(Exception):
        def __init__(self,
          Line_Nom=0, Line_Def=0, Line_Text='', Attribute='', File='', msg=None):
            print( 'Traceback (most recent call last):')
            print(f'  File "{File}", line {Line_Nom}, in <module>')
            print( '    '+Line_Text)
            end = msg if msg else f"Redefinition of '{Attribute}' (Already Defined At Line {Line_Def})"
            print("ConstantError: "+ end)
            sys.exit()

    class IndentionError(Exception):
        def __init__(self,
          Line_Nom=0, Line_Text='', File=''):
            print( 'Traceback (most recent call last):')
            print(f'  File "{File}", line {Line_Nom}, in <module>')
            print( '    '+Line_Text)
            print("IndentationError: expected an indented block")
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
            sys.exit()

    class ModuleNotFoundError(Exception):
        def __init__(self, File, Name=None, line_text='', line_nom=0):
            print( 'Traceback (most recent call last):')
            print(f'  File "{File}", line {line_nom}, in <module>')
            print( '    '+line_text)
            print(f"ModuleNotFoundError: No module named '{Name}'")
            sys.exit()

    class AttributeError(Exception):
        def __init__(self,File, Line_Nom, Line_Text, Module_Version, Attribute):
            print('Traceback (most recent call last):')
            print(f'  File "{File}", line {Line_Nom}, in <module>')
            print('    '+Line_Text)
            print(f"AttributeError: module '{Module_Version}' has no attribute '{Attribute}'")
            sys.exit()


#< Get Arguments >#
def Get_Args():

    print('ARGS:  '+str(sys.argv))
    
    if len(sys.argv) == 1:
        Console()

    if len(sys.argv) > 3:
        print('Argument Parser Will be added in next versions','dodger_blue_1')
        sys.exit()

    import argparse

    parser = argparse.ArgumentParser(
        'RX', allow_abbrev=True,
        description='"RX Language Executer"',

    )

    parser.add_argument(
        '-i', '--info',
        action='store_true',
        help='Show information about running file'
    )

    parser.add_argument(
        'FILE',
        metavar='FILE', type=str, nargs='?',
        help='File to execute with RX language'
    )

    parser.add_argument(
        '-o','--options',
        action='store_true'
    )


    args = parser.parse_args()
    
    if args.options:
        print('BASE OPTIONS:', style='bold')
        print("  OPTION NAME       DEFAULT VALUE       DESCRYPTION", style='bold')
        print('  ModuleName        sc                  Shortcut for RX Tools and functions (also "Module_Name")')
        print('  Method            normal              Method of loading tools.')
        print('                                          Valid Choices: [normal,[lite,fast]] (also Version)')
        print('OPTIONS:', style='bold')
        print("  OPTION NAME       DEFAULT VALUE       DESCRYPTION")
        print('  func_type_checker True                Check if argument of a function is in wrong type')
        print('                                          (REGEX:  (func|function)_?(type|arg|param)_?(scanner|checker) )')
        print('  Exit              True                Exit after executing the code or not')
        print()
        print('"OPTIONS" SHOULD BE DEFINED AFTER "BASE OPTIONS"', style='bold')

        sys.exit()

    #print('ARGS:  '+str(args))
    return args.FILE, args.info


#< Interactive RX Shell >#
def Console():
    def wait_for_input(prompt):
        '''
        Prompt  input(prompt)  until sth is given
        '''
        answer= ''
        while not answer:
            answer = input(prompt)
        return answer

    from importlib import reload
    
    rx.system.chdir(RX_PATH)

    PRE= ['import rx7.lite as sc','print = sc.style.print']
    rx.write('Console.py', '\n'.join(PRE)+'\n')
    import Console
    while True:
        try:
            new = wait_for_input('RX:Console> ')
            if new.lower() in ('exit','quit','end'):
                rx.files.remove('Console.py')
                sys.exit()
        except (KeyboardInterrupt,EOFError):
            rx.files.remove('Console.py')
            sys.exit()

        rx.write('Console.py', new+'\n', 'a')
        
        try:
            reload(Console)
        except Exception as e:
            ERROR = str(e)
            if '(Console.py,' in ERROR:
                ERROR = ERROR[:ERROR.index('(Console.py,')]
            print(str(type(e))[8:-2]+':  ' + ERROR, 'red')
            rx.write('Console.py', '\n'.join(rx.read('Console.py').splitlines()[:-1])+'\n', 'w')

        if re.search(r'^print\s*\(', rx.read('Console.py').splitlines()[-1].strip()):
            rx.write('Console.py', '\n'.join(rx.read('Console.py').splitlines()[:-1])+'\n')


#< Reading File >#
def Read_File(filepath):
    if rx.files.exists(filepath):
        with open(filepath) as f:
            SOURCE = f.read().split('\n')
        return SOURCE + ['\n']
    print(f"RX: can't open file '{filepath}': [Errno 2] No such file") #or directory
    sys.exit()


#< Module Name and Version  <Method,Module_Name,Print,Indent,Const> >#
def Define_Structure(SOURCE, FILE):
    #] Checking Indentation
    #INDENT_OUTPUT = rx.terminal.getoutput(f'python {RX_PATH}\\reindent.py -d -n '+FILE)
    INDENT_OUTPUT = rx.terminal.getoutput(f'python -m reindent -d -n '+FILE)
    if len(INDENT_OUTPUT):
        print('REINDENT')
        INDENT_OUTPUT = INDENT_OUTPUT.split('\n')
        if INDENT_OUTPUT[-1].startswith('tokenize.TokenError'):
            raise ERRORS.UndefinedError('SyntaxError: a parantheses is still open',FILE)
        elif INDENT_OUTPUT[-1].startswith('IndentationError'):
            LINE = INDENT_OUTPUT[-4]
            LINE_NOM = LINE[LINE.index('line ')+5:]
            raise ERRORS.IndentionError(LINE_NOM, INDENT_OUTPUT[-3][4:],FILE)
        else:
            raise ERRORS.UndefinedError
        LINE = INDENT_OUTPUT[-4]
        LINE_NOM = LINE[LINE.index('line ')+5:]
        raise ERRORS.IndentionError(LINE_NOM, INDENT_OUTPUT[-3][4:],FILE)


    #< Const Vars && Indents >#
    CONSTS = set()
    Keywords = ('for', 'while', 'if', 'else', 'elif', 'except')
    #INDENT = 0

    for Line_Nom,Text in enumerate(SOURCE, 1):
        
        if Text.strip().startswith('#'):
            continue

        #] Const Var
        if Text.strip().startswith('Const '):
            #if Text.startswith(' '): raise LateDefine("'Const' Must Be Defined In The Main Scope")
            if re.search(r'^Const\s+([A-Za-z]|_)+\s*=\s*', Text.strip()):
                INDENT = re.search(r'Const\s+([A-Za-z]|_)+\s*=\s*', Text).start()
                striped = Text.strip()
                SOURCE.remove(Text)
                SOURCE.insert(Line_Nom-1, INDENT*' ' + striped[striped.index(' ')+1:])
                CONST = striped[striped.index(' '):striped.index('=')].strip()
                if CONST != CONST.upper():
                    raise ERRORS.ConstantError(Line_Nom=Line_Nom, 
                                               Line_Text=Text.strip(), 
                                               File=FILE, 
                                               msg='Constant Variable Name Must be UPPERCASE')
                for item in CONSTS: #] Check if Const X is already defined
                    if CONST == item[0]:
                        raise ERRORS.ConstantError(Line_Nom, item[1], Text.strip(), item[0], FILE)
                CONSTS.add((CONST, Line_Nom))

        #] Const Array
        elif re.search(r'^\w+\s*=\s*<.+>', Text.strip()):
            search = re.search(r'(?P<Indent>\s*)(?P<VarName>\w+)\s*=\s*<(?P<Content>.*)>', Text)
            Content = search.group('Content')
            TYPE_ERROR = False
            try:
                Content = eval(Content)
                if type(Content) != tuple:
                    TYPE_ERROR = True
            except NameError:
                pass
            except Exception as e:
                raise e from None
            #else:
            VarName = search.group('VarName')
            if TYPE_ERROR:
                #raise TypeError(f"ArrayConst can not be '{type(Content)}' type (Use 'Const' keyword)")
                Type_Content = str(type(Content))[8:-2]
                print(f"'<>' is for Arrays, Try to use 'Const' keyword for type ",'red', end='')
                print(f"'{Type_Content}'  ({FILE}:{Line_Nom}:{VarName})", 'red')#, style='bold')
            CONSTS.add((VarName, Line_Nom))
            SOURCE[Line_Nom-1] = f'{VarName} = {Content}'


        for item in CONSTS:
            if re.search(rf'( |;){item}\s*(\[.+\])?\s*=\s*.+', Text):  # \s*.+  {?} 
                if not Text.strip().startswith('def')  and  not Text.strip().startswith('#'):
                    raise ERRORS.ConstantError(Line_Nom, item[1], Text.strip(), item[0], FILE)

        #] Indent
        if Text.strip().startswith(Keywords):
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
                print('RX')
                raise ERRORS.IndentionError(Line_Nom+1, SOURCE[Line_Nom], FILE)


    #< OPTIONS >#
    MODULE_VERSION  = 'rx7'
    MODULE_SHORTCUT = 'sc'
    PRINT_TYPE = 'print'
    TYPE_SCANNER = True
    BASED = False

    for line in SOURCE[:5]:

        #< Get Shortcut Name >#
        if re.search(r'^(ModuleName|Module_Name)\s*:\s*\w*',line):
            if BASED:
                raise ERRORS.BaseDefinedError('Modulename', line, SOURCE[:5].index(line), FILE)
            stripped = line[line.index(':')+1:].strip()
            if re.search(r'\w+', stripped).group() == stripped:
                MODULE_SHORTCUT = str(stripped)
                print(MODULE_SHORTCUT,'red')
            else:
                raise ERRORS.NameError(msg='Invalid Value For  modulename/module_name', File=FILE)
            SOURCE.remove(line)

        #< Get Version (Method) of Tools >#
        elif re.search(r'^(Method|Version)\s*:\s*\w*', line):
            StripLow = line.strip().lower()
            if BASED:
                raise ERRORS.BaseDefinedError('Method/Version', line, SOURCE[:5].index(line), FILE)
            pass
            if StripLow.endswith('lite') or StripLow.endswith('fast'):
                MODULE_VERSION = 'rx7.lite'
            elif not StripLow.endswith('normal'):
                stripped = line[line.index(':')+1:].strip()
                raise ERRORS.NameError(FILE, 'method', stripped, line, SOURCE[:5].index(line), ['lite','normal'])
            SOURCE.remove(line)

        #< Print Function Method >#
        elif re.search(r'^Print\s*:\s*\w*', line):
            BASED = True
            if line.strip().lower().endswith('stylized'):
                PRINT_TYPE = f'{MODULE_SHORTCUT}.style.print'
            elif not line.strip().lower().endswith('normal'):
                stripped = line[line.index(':')+1:].strip()
                raise ERRORS.NameError(FILE, 'print', stripped, line, SOURCE[:5].index(line), ['lite','normal'])
            SOURCE.remove(line)

        #< Function Type Scanner >#
        elif re.search(r'^((F|f)unc|(F|f)unction)_?((T|t)ype|(A|a)rg|(P|p)aram)_?((S|s)canner|(C|c)hecker)\s*:\s*\w*', line):
            BASED = True
            if line.endswith('False'):
                TYPE_SCANNER = False
            elif not line.strip().endswith('True'):
                raise ERRORS.NameError(FILE, 'func_type_checker', stripped, line, SOURCE[:5].index(line), "[True,False]")
            SOURCE.remove(line)

        #< Exit at the end >#
        elif re.search(r'^(Exit|Quit)\s*:\s*\w*', line):
            if line.strip().lower().endswith('false'):
                #SOURCE.append('__import__("os").system('pause')')
                #SOURCE[SOURCE.index(line)] = ''
                SOURCE.append('__import__("getpass").getpass("Press [Enter] to Exit")')
            elif not line.strip().lower().endswith('true'):
                stripped = line[line.index(':')+1:].strip()
                raise ERRORS.NameError(FILE, 'Exit', stripped, line, SOURCE[:5].index(line), ['True','False'])

    SOURCE[0] = f'import {MODULE_VERSION} as {MODULE_SHORTCUT}'
    SOURCE.insert(1,f'print = {PRINT_TYPE}')
    SOURCE.insert(2,'')


    #print(CONSTS)
    return (SOURCE, 
            MODULE_VERSION, MODULE_SHORTCUT,
            TYPE_SCANNER, CONSTS,)


#< Syntax >#
def Syntax(SOURCE, 
           MODULE_VERSION ,  MODULE_SHORTCUT,
           TYPE_SCANNER   ,  CONSTS, 
           FILE):

    Skip = False
    for Line_Nom,Text in enumerate(SOURCE, 1):
        
        #print(str(Line_Nom)+' '+Text)

        #< When Adding An Extra Line Like Decorators >#
        if Skip or Text.strip().startswith('#'):
            Skip = False
            continue

        #< Importing Tools :  <include,load> >#
        if re.search(r'^(I|i)nclude \s*(\w+,?)?', Text.strip()):
            if re.search(r'^Include \s*\*', Text):
                Packages = list(CLASSES)
            else:
                Packages = re.split(r'\s*,\s*', Text)
                Packages[0]= Packages[0][8:].strip()
            #print(Packages)
            SOURCE.remove(Text)
            for package in Packages:
                if package not in CLASSES:
                    raise ERRORS.AttributeError(FILE,Line_Nom,Line_Text,MODULE_VERSION,package)
                SOURCE.insert(Line_Nom-1, f'{package} = {MODULE_SHORTCUT}.{package}')
            continue

        #] Func Type checker
        elif Text.strip().startswith('def ') and TYPE_SCANNER:
            indent = Text.index('def ')
            SOURCE.insert(Line_Nom-1, f'{" "*indent}@{MODULE_SHORTCUT}.Check_Type')
            Skip = True

        #] Switch and Case
        elif re.search(r'^\s*(S|s)witch\s+\w+\s*:\s*', Text):
            SEARCH = re.search(r'^(?P<indent>\s*)(S|s)witch\s+(?P<VARIABLE>\w+)\s*:\s*', Text)
            indent = len(SEARCH.group('indent'))
            
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

            SOURCE.remove(Text)
            for Line,snc in enumerate(SOURCE[Line_Nom-1:LAST_LINE], Line_Nom):
                SEARCH_VALUE = re.search(r'^(C|c)ase\s+(?P<VALUE>.+):\s*', snc.strip())
                if SEARCH_VALUE:
                    if re.search(r'^elif \w+\s+==', SOURCE[Line-1].strip()):
                        raise TypeError
                    else:
                        pass#SOURCE[Line-1] =   ' '*(indent+4) + SOURCE[Line-1]
                    
                    SOURCE[Line-1] = f'{(indent)*" "}elif {SEARCH.group("VARIABLE")} == {SEARCH_VALUE.group("VALUE")}:' #+4
            SOURCE.insert(Line_Nom-1, f'{(indent)*" "}if False:pass')
            
        #] Load User-Defined Modules
        elif re.search(r'^(L|l)oad \s*(\w+,?)?', Text.strip()):
            Packages = re.split(r'\s*,\s*', Text)
            Packages[0]= Packages[0][4:].strip()
            
            print(Packages)
            #sys.exit()
            SOURCE.remove(Text)
            for package in Packages:
                if rx.files.exists(f'{package}.rx7'):
                    SOURCE.insert(Line_Nom-1,f"{MODULE_SHORTCUT}.files.rename('{package}.rx7','{package}.py');import {package};{MODULE_SHORTCUT}.files.rename('{package}.py','{package}.rx7')")
                else:
                    raise ERRORS.ModuleNotFoundError(FILE, package, Text, Line_Nom)
                




    return SOURCE


#< Verbose >#
def Add_Verbose(SOURCE, FILE, VERBOSE):
    if VERBOSE:
        import datetime
        print(f'Start RX Language at "{datetime.datetime.now()}"')
        print(f'Running  {FILE}')
        print('\n')

        SOURCE.insert(0, f'ProgramStartTime= {START_TIME}')
        EXECUTE_TIME_TEXT = 'round(__import__("time").time()-ProgramStartTime,3)'
        SOURCE.insert(-1, 'EXECUTE_TIME_TEXT='+EXECUTE_TIME_TEXT) #{EXECUTE_TIME_TEXT-.35}/
        SOURCE.insert(-1, r'''print(f'\n\nExecution Time:  {EXECUTE_TIME_TEXT}\n')''')
        #print(SOURCE[-3])

    return SOURCE






#< START OF THE CODE >#
if __name__ == "__main__":
    try:
        ARGS = Get_Args()
        FILE   = ARGS[0]
        rx.cls()
        SOURCE = Read_File(FILE)
        SOURCE = Define_Structure(SOURCE, FILE)
        SOURCE = Syntax(SOURCE[0], SOURCE[1], SOURCE[2], SOURCE[3], SOURCE[4], FILE)
        SOURCE = Add_Verbose(SOURCE, FILE, ARGS[1])


        rx.write('_RX_Py.py', '\n'.join(SOURCE))
        rx.write('translated', '\n'.join(SOURCE))
        rx.files.hide('_RX_Py.py')


        import os
        #os.system('python _RX_Py.py')

        try:
            #print(time.time()-START_TIME,'red',style='bold')
            #t=time.time()
            import _RX_Py
            #print(time.time()-t,'red',style='bold')
        except Exception as E:
            raise E
            print('Traceback (most recent call last):','red')
            print('  More Information Soon...','red')
            print(str(type(E))[8:-2]+': '+str(E), 'red', style='bold')
        finally:
            rx.files.remove('_RX_Py.py')
            '''
            print('Traceback (most recent call last):')
            print(f'  File "{FILE}" in  "UNDEFINED"')
            print(e, 'red')
            sys.exit()
            '''
            
    except KeyboardInterrupt:
        print('\nExiting Because of KeyboardInterrupt Error (Ctrl+C)','red')
