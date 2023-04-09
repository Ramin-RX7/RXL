import re
from . import *
from . import Errors as ERRORS

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





#< Method,Module_Name,Print,Indent,Const >#
def define_structure(SOURCE, FILE, DEBUG):
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
def syntax(SOURCE,
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
