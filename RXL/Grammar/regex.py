import re

from .. import Errors as ERRORS



#< List of all regex patterns >#
class REGEX:

    include = re.compile(r'(?P<Indent>\s*)include \s*(?P<objects>.+)\s*')

    load = re.compile(r'(?P<indent>\s*)load \s*(?P<packages>\w+,?)?')

    _memory_loc = re.compile(r'[,\(\[\{\+=: ]&(?P<var>\w+)')

    until = re.compile(r'(?P<Indent>\s*)until \s*(?P<Expression>.+):(?P<Rest>.*)')

    unless = re.compile(r'(?P<Indent>\s*)unless \s*(?P<Expression>.+):(?P<Rest>.*)')

    foreach = re.compile(r'(?P<indent>\s*)foreach \s*(?P<iterable>.+)\[(?P<forvar>(?:\w|,)+)\]:\s*')

    func = re.compile(r'func \s*(?P<Expression>.+)')

    array = re.compile(r'(?P<Indent>\s*)array \s*(?P<VarName>\w+)\s*\[\s*((?P<Length>\w+)?\s*(:?\s*(?P<Type>\w+))?\s*)?\]\s*=\s*{(?P<Content>.*)}\s*')

    class DoWhile:
        do = re.compile(r'(?P<Indent>\s*)do\s*:\s*')
        _while = re.compile(r'while\s*\(.+\)')

    class Commands:
        class Check:
            ignore_pattern = r'(?P<Indent>\s*)\$check \s*(?P<Test>.+)'
            then_pattern = r'\s* then (?P<Then>.+)'
            anyway_pattern = r'\s* anyway(s)? (?P<Anyway>.+)'
            ignore =  re.compile(ignore_pattern)
            then   =  re.compile(ignore_pattern + then_pattern)
            anyway =  re.compile(ignore_pattern + anyway_pattern)
            thenanyway = re.compile(ignore_pattern + then_pattern + anyway_pattern)

        _checkwait = re.compile(r'')

        cmd = re.compile(r'(?P<Indent>\s*)\$cmd \s*(?P<Command>.+)')

        call = re.compile(r'(?P<Indent>\s*)\$call (?P<Function>.+) \s*in \s*(?P<Time>.+)')

        _clear = NotImplemented



def get_regex(
        pattern_name:str,
        text:str,
        file:str,
        line_nom:int,
        msg:str=None):
    if pattern_name.startswith("$"):
        pattern = REGEX.Commands.__dict__[pattern_name[1:]]
    else:
        pattern = REGEX.__dict__[pattern_name]
    if regex := pattern.match(text):
        return regex
    if msg is None:
        msg = f"Wrong usage of {pattern_name}"
    raise ERRORS.SyntaxError(
        file,line_nom,text.strip(),msg
    )