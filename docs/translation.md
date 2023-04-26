# Translating to python documentation

Translation part consist of 2 sections:

- Defining Structure: Setting the apps main options
- Syntax: Translating new syntax from RXL to python

<br>

# Define Structure

*`Grammar.define_structure()`*

There are few options that should be defined in first lines of the file which will define few options for translation and runtime.

## Options

**`Lib-Name`:** with this option you can set the name of the `std` module. (Also called Lib-Shortcut)

Syntax:

```python
Lib-Name: MyLib_123
# Accpetable names regex: \w+
```

Python translation:

```python
MyLib_123 = std
```

**`Print`:** determines wether print function should be stylized or normal (default: stylized).

Syntax:

```python
Print: Stylized
# Accpetable values regex: ((stylized)|(normal))
```

Python translation:

```python
print = std.Style.print
```

**`Func-Type-Checker`:** This option will automatically put the `@std.Check_Type` before every function definition. (default:False)

Syntax:

```python
func-type-checker : True
# Accpetable values regex: ((True)|(False))
```

**`End-Exit`:** Determines wether there should be a prompt that waits for the user to press enter to exit. (Default:True)

Syntax:

```python
End-Exit : True
# Accpetable values regex: ((True)|(False))
```

Python translation:

```python
# if False add this to the end of the file
rx.IO.getpass("Press [Enter] to Exit")
```

---

<br>


# Syntax

*`Grammar.syntax()`*

Syntax is the main part of the program where python-like syntax can be used. When structures are defined, you will reach this part of the translation.

New grammars added to python:

- `include`: importing std functions/classes directly
- `load`: loading RXL modules
- `foreach`: iterate through items of an iterable
- `until`: opposite of `while` loop (only executes if condition is false)
- `unless`: opposite of `if` (only executes if condition is false)
- `func`: used to define a function indicating it is not pure
- `do while`: a while loop with promise of executing the code at least once (like other programming languages)
- `array`: a list of objects with same type and with a pre-defined size
- `$`
  - `$check`: tries to execute the code, if it raises error it will be ignored (try-except block in one line)(read the docs)
  - `$checkwait`: tries to execute code, retries if fails until it does not fail.
  - `$cmd`: run a command on terminal
  - `$call`: call a function after the given delay
  - `$clear`: clears the terminal
