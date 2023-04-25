# Runtime documentation

This documentation contains different stages of runtime ordered.
Each phase may contain different parts and use multiple parts of code to achieve what needs to be done.

<br>

## Preparing Environment

### *Setup_Env()*

Sets the environment ready for RXL to run. Does not return anything.

- creates the `CACHE_DIR`


## Parsing Arguments

Everything related to parsing terminal arguments is under a class called `ArgumentParser`. This class has a static method named `parse_args()` which will return terminal arguments as a dict. These arguments are all defined in `ArgumentParser.Parser` which handles setting/getting the args.

After this, `Tasks.detect_task()` will be used to figure out what should be done with given args.

<br>

## Tasks

Tasks are defined as the jobs that are requested by user. User requests should be all given from the terminal and be parsed (to a dict using `ArgumentPrser.parse_args()`). `Tasks.detect_task()` takes this dictionary (dotted-dictionary) and determines what task is requested.
There is a function for each task which covers everything that needs to be done only for that specifiec job. `detect_task()` will return name of the requested task plus the args that need to be passed to the function of task. `Tasks.run_task()` will take the result of `detect_task()` and runs the given task with given args.

### List of tasks

**`runfile`**: Translates thie given file to python code and runs it.

**`translate_only`**: only translates the given file to python

**`compile`**: Open menu to compile given file to bytecode

**`console`**: Opens an interactive RXL console
