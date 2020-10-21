import os,subprocess,shutil,time

def cls():
    '''
    You can use this function if you want to clear the environment.
    '''
    if __import__('platform').system() == "Windows":
        os.system('cls')
    else:
        os.system('clear')

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
    getoutput = subprocess.getoutput
    set_title = __import__('win32api').SetConsoleTitle
terminal = Terminal

class style:
    def __init__(self,text,color='default',BG='black'):
        from colored import fg,bg,attr
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
        if type(other)!=style:
            return self.content+other
        else:
            return self.content+other.content

    @staticmethod
    def print(text='', color='default', BG='default', style=0, end='\n'):

        if color=='default' and BG!='default':  # bg & !clr
            print(f'{attr(style)}{bg(BG)}{text}{attr(0)}', end=end)

        elif color!='default' and BG=='default':  # !bg & clr
            print(f'{attr(style)}{fg(color)}{text}{attr(0)}', end=end)

        elif color=='default' and BG=='default':  # !bg & !clr
            print(f'{attr(style)}{text}{attr(0)}', end=end)

        elif color!='default' and BG!='default':  # bg & clr
            print(f'{attr(style)}{bg(BG)}{fg(color)}{text}{attr(0)}', end=end)

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
        globals()['style'].print(text, color, BG, style=style)

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
    def write(file, text='',mode='replace',start=''):
        if not text:
            text = ''
        if not start:
            start = ''
        pass
        if mode in ('replace', 'w', 'continue', 'a'):
            if mode in ('replace', 'w'):
                mode = 'w'
            elif mode in ('continue', 'a'):
                mode = 'a'

            with open(file, mode=mode) as f:
                f.write(str(start)+str(text))

        else:   
            raise ValueError(f'mode should be in [(replace,w),(continue,a)] Not "{mode}"') 
    @staticmethod
    def mkdir(path):
        path = os.path.normpath(path)
        NEW= ''
        for FILE in path.split('\\'):
            NEW+= FILE+'\\'
            try: os.mkdir(NEW)
            except (FileExistsError,FileNotFoundError): pass
Files = files
read  = files.read
write = files.write


class system:
    chdir = os.chdir
System = system
