import typing as _typing
import os



def convert_file_name(file):
    basename = '_'+os.path.basename(file)+'_'
    return os.path.join(os.path.dirname(file), basename)
    #'‎'+FILE+'‎' THERE IS INVISIBLE CHAR IN QUOTES




class _Lang:

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
