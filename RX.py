import sys
import re

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




CLASSES = ('files'   , 'system', 'datetime',
           'internet', 'random', 'style'   , 
           'record'  , 'Tuple' , 'terminal')


#< Get Arguments >#
def Get_Args():
    if len(sys.argv) == 1:
        print('Console Will be added in next versions','dodger_blue_1')
        sys.exit()

    if len(sys.argv) > 2:
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
        metavar='FILE',
        type=str,
        help='File to execute with RX language'
    )

    parser.add_argument(
        '-',
        metavar='--options',
        action='store_true',
        help='Show options of RX language interpreter',
    )



    # Execute the parse_args() method
    args = parser.parse_args()
    
    if args.options:
        print("OPTION NAME       DEFAULT VALUE       DESCRYPTION")
        print()
        print('modulename        sc                  Shortcut for RX Tools and functions')


        sys.exit()

    print('ARGS:  '+str(args))


#< Reading File >#
def Read_File():
    with open(sys.argv[1]) as f:
        SOURCE = f.read().split('\n')
    return SOURCE


#< Module Name and Version  <method,module_name,print> >#
def Define_Structure(SOURCE):

    class DefinedError(Exception):
        def __init__(self, attribute, line_text, line_nom):
            #super().__init__(f"Already Defined {attribute}")
            print('Traceback (most recent call last):')
            print(f'  File "{sys.argv[1]}", line {line_nom}, in <module>')
            print('    '+line_text)
            print(f"DefinedError: '{attribute}' can not be defined after setting module [OPTIONS]")
            sys.exit()

    class NameError(Exception):
        def __init__(self, attribute=None, value=None, line_text='', line_nom=0, correct_list=[], msg=None):
            #super().__init__(f"Already Defined {attribute}")
            print('Traceback (most recent call last):')
            print(f'  File "{sys.argv[1]}", line {line_nom}, in <module>')
            print('    '+line_text)
            if not msg:
                print(f"NameError: '{attribute}' can not be ")
            else:
                print(f"NameError: {msg}")
            sys.exit()

    MODULE_VERSION  = 'rx7'
    MODULE_SHORTCUT = 'sc'
    PRINT_TYPE = 'print'
    TYPE_SCANNER = True
    BASED = False
    for line in SOURCE[:5]:

        #< Get Shortcut Name >#
        if re.search(r'^(ModuleName|Module_Name)\s*:\s*',line):
            if BASED:
                raise DefinedError('Modulename', line, SOURCE[:5].index(line))
            stripped = line[line.index(':')+1:].strip()
            if re.search(r'\w+', stripped).group() == stripped:
                MODULE_SHORTCUT = str(stripped)
            else:
                raise NameError(msg='Invalid Value For  modulename/module_name')

        #< Get Version (Method) of Tools >#
        elif re.search(r'^(Method|Version)\s*:\s*\w*', line):
            StripLow = line.strip().lower()
            if BASED:
                raise DefinedError('Method/Version', line, SOURCE[:5].index(line))
            if StripLow.endswith('lite') or StripLow.endswith('fast'):
                MODULE_VERSION = 'rx7.lite'
            elif not StripLow.endswith('normal'):
                stripped = line[line.index(':')+1:].strip()
                raise NameError('method', stripped, line, SOURCE[:5].index(line), ['lite','normal'])

        #< Print Function Method >#
        elif re.search(r'^Print\s*:\s*\w*', line):
            BASED = True
            if line.strip().lower().endswith('stylized'):
                PRINT_TYPE = f'{MODULE_SHORTCUT}.style.print'
            elif not line.strip().lower().endswith('normal'):
                stripped = line[line.index(':')+1:].strip()
                raise NameError('print', stripped, line, SOURCE[:5].index(line), ['lite','normal'])

        #< Function Type Scanner >#
        elif re.search(r'^(func|function)_?(type|arg|param)_?(scanner|checker)\s*:\s*\w*', line):
            BASED = True
            if line.strip().endswith('True'):
                TYPE_SCANNER = True
            elif line.endswith('False'):
                TYPE_SCANNER = False
            else:
                raise NameError('metho', stripped, line, SOURCE[:5].index(line), ['lite','normal'])
        
        SOURCE.remove(line)


    SOURCE[0] = f'import {MODULE_VERSION} as {MODULE_SHORTCUT}'
    SOURCE.insert(1,f'print = {PRINT_TYPE}')
    SOURCE.insert(2,'')

    return SOURCE, MODULE_SHORTCUT, TYPE_SCANNER, MODULE_VERSION


#< Syntax >#
def Syntax(SOURCE, MODULE_SHORTCUT, TYPE_SCANNER, MODULE_VERSION):
    Skip = False
    for Line_Nom,Text in enumerate(SOURCE, 1):
        
        #< When Adding An Extra Line Like Decorators >#
        if Skip:
            Skip = False
            continue
        
        #print(str(Line_Nom)+' '+Text)

        #< Importing Tools :  <include,load> >#
        if re.search(r'^(Load|Include) \s*(\w+,?)?', Text.strip()):
            if re.search(r'^Include \s*\*', Text):
                Packages = list(CLASSES)
            else:
                Packages = re.split(r'\s*,\s*', Text)
                Packages[0]= Packages[0][4:].strip() if Packages[0].startswith('Load') else Packages[0][8:].strip()
            print(Packages)
            SOURCE.remove(Text)
            for package in Packages:
                if package not in CLASSES:
                    print('Traceback (most recent call last):')
                    print(f'  File "{sys.argv[1]}", line {Line_Nom}, in <module>')
                    print('    '+Text)
                    print(f"AttributeError: module '{MODULE_VERSION}' has no attribute '{package}'")
                    sys.exit()
                SOURCE.insert(Line_Nom-1, f'{package} = {MODULE_SHORTCUT}.{package}')
            continue

        # Func annot checker
        elif Text.strip().startswith('def '):
            if TYPE_SCANNER:
                indent = Text.index('def ')
                SOURCE.insert(Line_Nom-1, f'{" "*indent}@{MODULE_SHORTCUT}.check_type')
            Skip = True
    


    return SOURCE


# START OF THE CODE:
Get_Args()
SOURCE = Read_File()
SOURCE = Define_Structure(SOURCE)
SOURCE = Syntax(SOURCE[0], SOURCE[1], SOURCE[2], SOURCE[3])

rx.write('result.txt', '\n'.join(SOURCE))
import os
#os.system('python result.txt')
