"""
        #] Switch and Case
        elif False and (Stripped.startswith('switch ')  or  Stripped==('switch')):
            #elif Regex:=re.match(r'(?P<indent>\s*)(S|s)witch\s+(?P<VARIABLE>\w+)\s*:', Text):
            Regex = re.match(r'(?P<indent>\s*)switch\s+(?P<VARIABLE>\w+)\s*:', Stripped)
            if not Regex: raise SyntaxError

            indent = Regex.group('indent')
            rules = 0  #?
            for nom2,line2 in enumerate(SOURCE[Line_Nom:], 1):
                if not line2:
                    continue
                if not re.match(r'(?P<indent2>\s*).+', line2) and  not rules:
                    #new = len(re.search(r'^(?P<indent2>\s*)', line2).group('indent2'))
                    LAST_LINE = nom2 + Line_Nom -1
                    break
            else:
                LAST_LINE = -1

            #SOURCE.remove(Text)
            Default = False
            SOURCE[Line_Nom-1] = f'{indent}if False: pass'
            for Line,snc in enumerate(SOURCE[Line_Nom-1:LAST_LINE], Line_Nom):
                if re.match(r'^default\s*:',snc.strip()):
                    SOURCE[Line-1] = indent+'else:'
                    Default = True
                SEARCH_VALUE = re.match(r'case\s+(?P<Nobreak>(nobreak)?)(?P<VALUE>.+):', snc.strip())
                if SEARCH_VALUE:
                    if Default:
                        raise ERRORS.SyntaxError(FILE,Line_Nom+Line,snc,
                                                 'Case is defined after default')
                    IF_EL = 'el' if not SEARCH_VALUE.group('Nobreak') else ''
                    if re.match(fr'{IF_EL}if \w+\s+==', SOURCE[Line-1].strip()):
                        raise TypeError
                    else:
                        pass#SOURCE[Line-1] =   indent + '    ' + SOURCE[Line-1]
                    variable = Regex.group("VARIABLE")
                    value    = SEARCH_VALUE.group("VALUE")
                    SOURCE[Line-1] = f'{indent}{IF_EL}if {variable} == {value}:' #+4

"""

"""
    @staticmethod
    def Console():
        raise NotImplementedError
        # rx.terminal.set_title('RX - Console')

        from importlib import reload

        CWD = rx.system.cwd()

        PRE= ['import rx7 as rx','std=rx','print = std.style.print']
        rx.write(f'{CWD}/{CONSOLE_FILE}', '\n'.join(PRE)+'\n')
        # import _Console_   importlib.import_module("_Console_")
        _Console_ = __import__(CONSOLE_FILE)
        while True:
            try:
                new = rx.io.wait_for_input('RX:Console> ')
                if new.lower() in ('exit','quit','end'):
                    rx.files.remove(f'{CWD}/{CONSOLE_FILE}')
                    return
            except (KeyboardInterrupt,EOFError):
                rx.files.remove(f'{CWD}/{CONSOLE_FILE}')
                return

            rx.write(f'{CWD}/{CONSOLE_FILE}', new+'\n', 'a')

            try:
                reload(_Console_)
            except (EOFError,KeyboardInterrupt):
                return
            except Exception as e:
                ERROR = str(e)
                if f'({CONSOLE_FILE},' in ERROR:
                    ERROR = ERROR[:ERROR.index(f'(CONSOLE_FILE,')]
                print(str(type(e))[8:-2]+':  ' + ERROR, 'red')
                rx.write(f'{CWD}/{CONSOLE_FILE}', '\n'.join(rx.read(f'{CWD}/{CONSOLE_FILE}').splitlines()[:-1])+'\n')

            if re.match(r'print\s*\(', rx.read(f'{CWD}/{CONSOLE_FILE}').splitlines()[-1].strip()):
                rx.write(f'{CWD}/{CONSOLE_FILE}', '\n'.join(rx.read(f'{CWD}/{CONSOLE_FILE}').splitlines()[:-1])+'\n')


    @staticmethod
    def Create_Mini_Std():
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

"""
"""
    class Constant:
        def __new__(cls,*args,array=True):
            cls._init = False
            return super(_Lang.Constant, cls).__new__(cls)
        def __init__(self,*args,array=True):
            '''
            if array:
                self.__members =  args
            else:
                if len(args) > 1:
                    raise ValueError
                self.__members = args[0]
            '''
            self.__members = args
            self._init = True

        def __str__(self):
            #if len(self.__members) > 1:
                return '<'+str(self.__members)[1:-1]+'>'  #‹›
            #return self.__members
        def __repr__(self):
            return '<'+str(self.__members)[1:-1]+'>'

        def __setattr__(self,_attr,value):
            if self._init:
                raise AttributeError(f"'Constant' object does not support item assignment")
            else:
                super(_Lang.Constant,self).__setattr__(_attr,value)

        def __getitem__(self,index):
            return self.__members[index]
        def __contains__(self,obj):
            return obj in self.__members
        def __bool__(self):
            return bool(len(self.__members))
        #'''
        def __hash__(self):
            return hash(tuple(['Constant',len(self)]+list(self.__members)))
        #'''
        def __len__(self):
            #if type(self.__members) == tuple:
                return len(self.__members)

        def _dict_getter(self):
            raise AttributeError("Conatant object has no attribute '__dict__'")
            #return {}
        __dict__ = property(_dict_getter)

        def __dir__(self):
            ret = list(super().__dir__())#[:-2]
            ret.remove('_init')
            ret.remove('_dict_getter')
            return ret
    const = Const = constant = Constant

"""
"""
        #] Save Cache
        elif regex:=re.match(r'Save-?Cache\s*:\s*(?P<flag>.+)', rstrip, re.IGNORECASE):
            raise NotImplementedError
            flag = regex.group("flag").capitalize()
            if flag in ("True","False")  and  flag=='False':
                ABSPATH = os.path.dirname(rx.files.abspath(FILE))
                SOURCE.insert(-1,f'std.files.remove("{ABSPATH}/__RX_LC__",force=True)')
            else:
                raise ERRORS.ValueError(FILE, 'SaveCache', flag, line,
                                       SOURCE.index(line), "[True,False]")
"""