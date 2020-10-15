import os
import subprocess
import shutil
import time

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
terminal = Terminal

class style:
    def __init__(self,text,color='default',BG='black'):
        from colored import fg,bg,attr
        try: color= color.lower();BG=BG.lower()#;style=style.lower()
        except:pass        
        if color=='default':
            color=7 #188
        self.text= text     
        self.content= f"{fg(color)}{bg(BG)}{text}{attr(0)}"
    def __str__(self):
        return self.content
    def __repr__(self):
        return self.content
    def __add__(self,other):
        #print(type(other))
        if type(other)!=style:
            return self.content+other
        else:
            return self.content+other.content
    def __mul__(self,nom):
        return self.content*nom
    def __getitem__(self,index):
        return self.text[index]


    @staticmethod
    def print(text='',color='default',BG='default',style='None',end='\n'):
        from colored import fg,bg,attr
        try: color= color.lower();BG=BG.lower();style=style.lower()
        except:pass
        if color=='default': color=7 #188
        if style=='none': style=0

        if color=='default' and BG!='default':
            print('%s%s%s%s' % (attr(style),bg(BG),text,attr(0)),end=end)
        if color!='default' and BG=='default':
            print('%s%s%s%s' % (attr(style),fg(color),text,attr(0)),end=end)
        if color=='default' and BG=='default':
            print('%s%s%s%s%s' % (attr(style),bg(BG),fg(color),text,attr(0)),end=end)
    @staticmethod
    def switch(color='default',BG='black',style='None'):
        try: color= color.lower();BG=BG.lower();style=style.lower()
        except:pass        
        if style=='none': style=0
        if color=='default': color=7
        from colored import fg,bg,attr
        print('%s%s%s' % (attr(style),bg(BG),fg(color)),end='')
    @staticmethod
    def switch_default():
        from colored import attr
        print('%s' % (attr(0)),end='')
    reset = switch_default
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
