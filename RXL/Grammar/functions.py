class Source(list):

    def call_syntax_f(self, name, line_nom, regex):
        if name.startswith("$"):
            name = name[1:]
        print(name)
        eval(f"self.{name}")(line_nom,regex)


    def include():
        ...


    def load():
        ...


    def until(self, line_nom, regex):
        self[line_nom-1] = f"{regex.group('Indent')}while not ({regex.group('Expression')}):{regex.group('Rest')}"


    def unless(self, line_nom, regex):
        self[line_nom-1] = f"{regex.group('Indent')}if not ({regex.group('Expression')}):{regex.group('Rest')}"


    def func(self, line_nom, regex):
        self[line_nom-1].replace('func', 'def', 1)


    def foreach(self, line_nom, regex):
        indent, iterable, forvar = regex.groups()
        modified = f"{indent}for {forvar} in {iterable}:"
        self[line_nom-1] = modified


    def array(self, line_nom, regex):
        Indent  = regex.group('Indent')
        VarName = regex.group('VarName')
        Length  = regex.group('Length')
        Type    = regex.group('Type')
        Content = regex.group('Content')
        Length  =  '' if not Length  else ', max_length='+Length
        Type    =  '' if not Type    else ', type_='+Type
        # if not any([Length, Type]):
            # raise ERRORS.SyntaxError("length and type of the array elements should be set")
        self[line_nom-1] = f'{Indent}{VarName} = std.array(({Content},){Type}{Length})'


    def cmd(self, line_nom, regex):
        self[line_nom-1] = f'{regex.group("Indent")}std.terminal.run("{regex.group("Command") if regex else "cmd"}")'


    def call(self, line_nom, regex):
        print("in call")
        Indent = regex.group('Indent'  )
        Delay  = regex.group('Time'    )
        Func   = regex.group('Function')
        self[line_nom-1] = f"{Indent}std.call({Func},delay={Delay})"
