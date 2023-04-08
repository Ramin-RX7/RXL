import typing as _typing
import os
import sys
import time
import shutil
import tokenize

from colored import  fg,bg,attr
_auto = -1


def convert_file_name(file):
    return '_'+os.path.basename(file)+'_'
    #'‎'+FILE+'‎' THERE IS INVISIBLE CHAR IN QUOTES


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

        def _get_now():
            return time.strftime('%H:%M:%S',time.localtime())
        def _log(pre, text, color='', BG='default', style=None, add_time=True):
            #globals()['style'].print(text, color, BG, style=style)
            if add_time:
                NOW = f"[{rx.Style._get_now()}]  "
            else:
                NOW = ""
            rx.Style.print(f"{NOW}{text}", color=color, BG=BG, style=style)
        @staticmethod
        def log_error(text, color='red', BG='default', style=0, add_time=True):
            rx.Style._log("[!]",text,color,BG,style,add_time)
    Style = style


    class files:
        rename  =  os.rename
        abspath =  os.path.abspath
        exists  =  os.path.exists
        mdftime =  os.path.getmtime
        move    =  shutil.move
        isfile  =  os.path.isfile
        isdir   =  os.path.isdir
        dirname =  os.path.dirname
        @staticmethod
        def copy(src,dest,preserve_metadata= True):
            if rx.files.isdir(src):
                shutil.copytree(src,dest)
            else:
                if preserve_metadata: shutil.copy2(src,dest)
                else: shutil.copy(src,dest)
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
                        raise OSError(
                            f"[WinError 145] The directory is not empty: '{path}'" + '\n' + ' '*23 +
                            '(Use force=True as an argument of remove function to' +
                            ' remove non-empty directories.)')
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
        cwd = os.getcwd
    System = system


    class IO:
        @staticmethod
        def wait_for_input(prompt):
            answer= ''
            while not answer:
                answer = input(prompt).strip()
            return answer

        @staticmethod
        def selective_input(prompt, choices, default=None,
                            ignore_case:bool=False, invalid_message='Invalid input',
                            action=None):

            assert (callable(action) or action==None)

            if not callable(choices):
                Choices = choices
                if type(choices) == dict:
                    Choices = list(choices.keys())+list(choices.values())
                if ignore_case:
                    Choices = [item.lower() for item in Choices if isinstance(item,str)]

            while True:
                inp = input(prompt)
                inp = inp.lower() if ignore_case else inp
                if callable(choices):
                    if choices(inp):
                        break
                    elif invalid_message:
                        rx.style.print(invalid_message, color='red')
                elif not inp:
                    if default:
                        inp = default
                        break
                    else:
                        if invalid_message:
                            rx.style.print(invalid_message, color='red')
                elif inp in Choices:
                    break
                else:
                    if invalid_message:
                        rx.style.print(invalid_message, color='red')

            if type(choices) == dict:
                try:
                    inp = choices[inp]
                except KeyError:
                    pass

            if action:
                inp = action(inp)

            return inp

        @staticmethod
        def yesno_input(prompt,default=None):
            error= "Invalid Input" if bool(default) else ""
            def action(inp):
                if inp.lower() in ("yes","y"):
                    return True
                elif inp.lower() in ("no","n"):
                    return False
            return IO.selective_input(prompt,['y','yes','n','no'],default,True,error,action)

        @staticmethod
        def Input(prompt:str ='', default_value:str =''):
            import win32console
            _stdin = win32console.GetStdHandle(win32console.STD_INPUT_HANDLE)
            keys = []
            for c in str(default_value):
                evt = win32console.PyINPUT_RECORDType(win32console.KEY_EVENT)
                evt.Char = c
                evt.RepeatCount = 1
                evt.KeyDown = True
                keys.append(evt)
            _stdin.WriteConsoleInput(keys)
            return input(str(prompt))

        @staticmethod
        def getpass(prompt):
            import getpass as Getpass
            return Getpass.getpass(prompt=prompt)
    io = IO


class IndentCheck:
    """
    This Class is a copy of tabnanny module in standard library
    About half of the methods that are not used are deleted from the code
    SOURCE: https://github.com/python/cpython/blob/3.10/Lib/tabnanny.py
    """
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
        S, T = ' ','\t'

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



class array(list):
    def __init__(self,__iterable=...,type_=_auto, max_length=_auto):
        if __iterable is not Ellipsis:
            if type_ == _auto:
                type_ = type(__iterable[0])
                for element in __iterable:
                    if type(element) is not type_:
                        raise TypeError("Given iterable has wrong type (type(element)!=type_)")
                self._type = type_
            else:
                members_types = set(type(t) for t in __iterable)
                if len(members_types) != 1:
                    raise TypeError("All array elements must have the same type")
                if list(members_types)[0] != type_:
                    raise TypeError("Array with wrong element type is given")
                self._type = list(members_types)[0]

            if max_length == _auto:
                max_length = len(__iterable)
            if len(__iterable) > max_length:
                raise MemoryError("Length of given iterable is more that `_max_length`")
            self._max_length = max_length

            return super().__init__(__iterable)

        else:
            if max_length < 0:
                raise ValueError("In empty array, max_length has to be set")

            self._max_length = max_length
            return super().__init__()


    def __str__(self) -> str:
        return f"<{super().__str__()[1:-1]}>"

    def append(self,__v):
        if type(__v) != self._type:
            raise TypeError("Attempt to add a value with wrong type to array")
        if len(self) >= self._max_length:
            raise MemoryError("Maximum size of the array is reached")
        super().append(__v)







class _Lang:

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


    class Types:
        Str         =  str
        Int         =  int
        Float       =  float
        Set         =  set
        Tuple       =  tuple
        Dict        =  dict
        List        =  list
        Bool        =  bool
        Bytes       =  bytes

        Class       =  type
        Type        =  type
        Object      =  object

        Lambda      =  type(lambda: None)
        Function    =  Lambda #type(lambda: None)

        #Constant   =  type(_Lang.Constant(1))
        #Array      =  type(_Lang.Array(1,1))

        Any         =   type#_typing.Any
        Callable    =  _typing.Callable
        Container   =  _typing.Container
        Generator   =   Lambda #type(_f) #Not Built-in(s)   #_types.GeneratorType || _typing.Generator
        Iterable    =  _typing.Iterable
        Iterator    =  _typing.Iterator
        NoReturn    =  _typing.NoReturn
        Optional    =  _typing.Optional
        BuiltinFunction = type(len)
        BuiltinMethod   = type([].append)
        Module = type(_typing)
        # Method = type(globals()['Record']().lap)
        #Mapping     =  _typing.Mapping
        #OrderedDict =  _typing.OrderedDict
        #Text        =  str
        #Union  = _typing.Union
        #_types.AsyncGeneratorType
    types = Types
#setattr(_Lang,'Const',type(_Lang.Constant(1)))
#setattr(_Lang,'Array',type(_Lang.Array(1,1)))
