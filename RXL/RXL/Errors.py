import sys
from . import *

Error = rx.style.log_error



#< List of all errors >#
class RaiseError(Exception):
    def __init__(self, title, msg, line_text, line_nom, File, Lines_Added):
        print( 'Traceback (most recent call last):')
        print(f'  File "{File}", line {line_nom-Lines_Added}, in <module>')
        print( '    '+line_text)
        Error(str(title)+': '+str(msg))
        # Clean_Up(File)
        sys.exit()

class BaseDefinedError(Exception):
    def __init__(self, attribute, line_text, line_nom, File):
        RaiseError(
            'BaseDefinedError',
            f"BaseDefinedError: '{attribute}' can not be defined after setting module [OPTIONS]",
            line_text,line_nom,File
        )

class ValueError(Exception):
    def __init__(self,
            File,       attribute=None , value=None, Line_Text='',
            Line_Nom=0, correct_list=[], msg=None):
        MSG = msg if msg else f"'{attribute}' can not be '{value}'. Valid Choices: {correct_list}"
        raise RaiseError(
              'ValueError', MSG,
              Line_Text,Line_Nom,File
              )

class ConstantError(Exception):
    def __init__(self,
      Line_Nom=0  , Line_Def=0, Line_Text='',
      Attribute='', File=''   , msg=None):
        MSG = msg if msg else f"Redefinition of '{Attribute}' (Already Defined At Line {Line_Def})"
        raise RaiseError(
              'ConstantError', MSG,
              Line_Text,Line_Nom,File
              )

class IndentationError(Exception):
    def __init__(self,
      Line_Nom=0, Line_Text='', File=''):
        raise RaiseError(
              'IndentationError', 'expected an indented block',
              Line_Text,Line_Nom,File
              )

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
        # Clean_Up(File)
        sys.exit()

class ModuleNotFoundError(Exception):
    def __init__(self, File, Name=None, Line_Text='', Line_Nom=0):
        raise RaiseError(
              'ModuleNotFoundError', f"No module named '{Name}'",
              Line_Text,Line_Nom,File
              )

class AttributeError(Exception):
    def __init__(self,File, Line_Nom, Line_Text, Module_Version, Attribute, Type='module'):
        raise RaiseError(
              'AttributeError', f"{Type} '{Module_Version}' has no attribute '{Attribute}'",
              Line_Text,Line_Nom,File
              )

class LoadError(Exception):
    def __init__(self, Module, File, error=False):
        print( 'Traceback (most recent call last):')
        print(f'  Loading Module "{Module}" Resulted in an Error', 'red' if error else 'default')
        if error:
            print(error)
        else:
            print(f'    Module {Module} Returned Output When Loading')
            Error(f'LoadError: Make Sure There is No Print/Output in Module "{Module}"')
        # Clean_Up(File)
        sys.exit()

class SyntaxError(Exception):
    def __init__(self,File, Line_Nom, Line_Text, msg):
        raise RaiseError(
              'SyntaxError', msg,
              Line_Text,Line_Nom,File
              )
