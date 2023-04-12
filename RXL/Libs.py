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
        # set_title = __import__('win32api').SetConsoleTitle
        # get_title = __import__('win32api').GetConsoleTitle
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
        exists  =  os.path.exists
        abspath =  os.path.abspath
        isfile  =  os.path.isfile
        isdir   =  os.path.isdir
        dirname =  os.path.dirname
        basename = os.path.basename
        mdftime =  os.path.getmtime
        move    =  shutil.move
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
            return rx.IO.selective_input(prompt,['y','yes','n','no'],default,True,error,action)

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

    apply = lambda f,iterable: type(iterable)(__import__("builtins").map(f,iterable))

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
