import sys
import re
import time

START_TIME = time.time()

import rx7.lite as rx

print = rx.style.print

#rx.cls()



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
"""
#< VS Ext >#
r"""
 git add . && git commit
 vsce publish VERSION
"""
#< WHEN APP READY >#
r"""
 %USERPROFILE%
 #setx /M path "%path%;E:\ramin\Coding\GitHub\RX-Language"
 #C:\Users\IRANIAN\AppData\Roaming\ActiveState\bin;C:\Program Files (x86)\NVIDIA Corporation\PhysX\Common;C:\WINDOWS\system32;C:\WINDOWS;C:\WINDOWS\System32\Wbem;C:\WINDOWS\System32\WindowsPowerShell\v1.0\;C:\WINDOWS\System32\OpenSSH\;C:\ProgramData\chocolatey\bin;D:\Programs\Coding\Git\cmd;C:\Users\IRANIAN\AppData\Local\Programs\Python\Python37;C:\Users\IRANIAN\AppData\Local\Programs\Python\Python37\Scripts;D:\Programs\Microsoft VS Code\bin;C:\Users\IRANIAN\AppData\Local\GitHubDesktop\bin;C:\Users\IRANIAN\AppData\Roaming\npm
"""




# TODO:
#   CONST Variable
#   Stop Imports
#   Add <>




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
          Line_Nom, Line_Def, Line_Text, Attribute, File):
            print( 'Traceback (most recent call last):')
            print(f'  File "{File}", line {Line_Nom}, in <module>')
            print( '    '+Line_Text)
            print(f"ConstantError: Redefinition of '{Attribute}' (Already Defined At Line {Line_Def})")
            sys.exit()

#< Get Arguments >#
def Get_Args():
    print(sys.argv)
    if len(sys.argv) == 1:
        print('Console Will be added in next versions','dodger_blue_1')
        sys.exit()

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


#< Reading File >#
def Read_File(filepath):
    if rx.files.exists(filepath):
        with open(filepath) as f:
            SOURCE = f.read().split('\n')
        return SOURCE + ['\n']
    print(f"RX: can't open file '{filepath}': [Errno 2] No such file") #or directory


#< Module Name and Version  <method,module_name,print> >#
def Define_Structure(SOURCE, FILE):

    MODULE_VERSION  = 'rx7'
    MODULE_SHORTCUT = 'sc'
    PRINT_TYPE = 'print'
    TYPE_SCANNER = True
    BASED = False

    CONSTS = set()
    for Line_Nom,Text in enumerate(SOURCE, 1):
        if Text.strip().startswith('Const '):
            #if Text.startswith(' '): raise LateDefine("'Const' Must Be Defined In The Main Scope")
            if re.search(r'^Const\s+([A-Z]|_)+\s*=\s*', Text.strip()):
                INDENT = re.search(r'Const\s+([A-Z]|_)+\s*=\s*', Text).start()
                striped = Text.strip()
                SOURCE.remove(Text)
                SOURCE.insert(Line_Nom-1, INDENT*' ' + striped[striped.index(' ')+1:])
                CONST = striped[striped.index(' '):striped.index('=')].strip()
                if CONST != CONST.upper():
                    raise ERRORS.ConstantError(Line_Nom, CONST[1], Text.strip(), CONST[0], FILE)
                for item in CONSTS:
                    if CONST == item[0]:
                        raise ERRORS.ConstantError(Line_Nom, item[1], Text.strip(), item[0], FILE)                    
                CONSTS.add((CONST, Line_Nom))
    print(CONSTS)


    for line in SOURCE[:5]:

        #< Get Shortcut Name >#
        if re.search(r'^(ModuleName|Module_Name)\s*:\s*\w*',line):
            if BASED:
                raise ERRORS.BaseDefinedError('Modulename', line, SOURCE[:5].index(line), FILE)
            stripped = line[line.index(':')+1:].strip()
            if re.search(r'\w+', stripped).group() == stripped:
                MODULE_SHORTCUT = str(stripped)
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
        elif re.search(r'^(func|function)_?(type|arg|param)_?(scanner|checker)\s*:\s*\w*', line):
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

    return SOURCE, MODULE_SHORTCUT, TYPE_SCANNER, MODULE_VERSION, CONSTS


#< Syntax >#
def Syntax(SOURCE, MODULE_SHORTCUT, TYPE_SCANNER, MODULE_VERSION, FILE, CONSTS):
    Skip = False
    for Line_Nom,Text in enumerate(SOURCE, 1):
        
        #print(str(Line_Nom)+' '+Text)


        #< When Adding An Extra Line Like Decorators >#
        if Skip:
            Skip = False
            continue

        if True:
            #< Check Constants >#
            for CONST in CONSTS:
                if (CONST[0] in Text) and ('=' in Text) and (not re.search(r'def \w+\(', Text)):
                    if re.search(CONST[0] + r'\s*=\s*', Text):
                        #if 'Const' in Text:
                            raise ERRORS.ConstantError(Line_Nom, CONST[1], Text.strip(), CONST[0], FILE)
                        #raise TypeError('Can not change Constant')
      
        pass

        #< Importing Tools :  <include,load> >#
        if re.search(r'^(Load|Include) \s*(\w+,?)?', Text.strip()):
            if re.search(r'^Include \s*\*', Text):
                Packages = list(CLASSES)
            else:
                Packages = re.split(r'\s*,\s*', Text)
                Packages[0]= Packages[0][4:].strip() if Packages[0].startswith('Load') else Packages[0][8:].strip()
            #print(Packages)
            SOURCE.remove(Text)
            for package in Packages:
                if package not in CLASSES:
                    print('Traceback (most recent call last):')
                    print(f'  File "{FILE}", line {Line_Nom}, in <module>')
                    print('    '+Text)
                    print(f"AttributeError: module '{MODULE_VERSION}' has no attribute '{package}'")
                    sys.exit()
                SOURCE.insert(Line_Nom-1, f'{package} = {MODULE_SHORTCUT}.{package}')
            continue

        # Func annot checker
        elif Text.strip().startswith('def '):
            if TYPE_SCANNER:
                indent = Text.index('def ')
                SOURCE.insert(Line_Nom-1, f'{" "*indent}@{MODULE_SHORTCUT}.Check_Type')
            Skip = True
    

    print(CONSTS)
    return SOURCE


#< Verbose >#
def Add_Verbose(SOURCE, FILE, VERBOSE):
    if VERBOSE:
        import datetime
        print(f'Start RX Language at "{datetime.datetime.now()}"')
        print(f'Running  {FILE}')
        print('\n')

        SOURCE.insert(0, f'ProgramStartTime= {START_TIME}')
        EXECUTE_TIME_TEXT = '{round(__import__("time").time()-ProgramStartTime,3)}'
        SOURCE.insert(-2, fr'''print(f'\n\nExecution Time:  {EXECUTE_TIME_TEXT}\n')''')


    return SOURCE






# START OF THE CODE:
ARGS = Get_Args()
FILE   = ARGS[0]
SOURCE = Read_File(FILE)
SOURCE = Define_Structure(SOURCE, FILE)
SOURCE = Syntax(SOURCE[0], SOURCE[1], SOURCE[2], SOURCE[3], FILE, SOURCE[4])
SOURCE = Add_Verbose(SOURCE, FILE, ARGS[1])

rx.write('result.txt', '\n'.join(SOURCE))
#rx.files.hide('result.txt')

import os
#os.system('python result.txt')
