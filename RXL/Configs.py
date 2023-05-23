import sys
import tomllib

import rx7 as rx



DEFAULT_CONFIG_PATH = "RXLconfig.toml"



def default_config():
    configs = {
        "info" : {
            "version": "None",
            "author" : None,
            "title"  : None,
        },
        "structure": {
            "lib_name" : "std",
            "print" : "stylized",
            "func_type_checker" : False,
            "end_exit" : True,
            # "lib_version" : "rx7",
            # "allow_reload": True,
            #? Consts : NotImplemented,
        },
        # "runtime" : {
            # "verbose" :  False,
            # "debug"   :  False,
            # "cache"   :  True,
            # "python_path" :  sys.executable
        # },
        # "pre_run_command"  :  None,
        # "post_run_command" :  None,
    }
    return configs



def get_configs(dir_path):

    if not rx.files.exists(dir_path+"/"+DEFAULT_CONFIG_PATH):
        return default_config()

    with open(dir_path+"/RXLconfig.toml", 'rb') as f:
        user_configs = tomllib.load(f)
    default_configs = default_config()

    configs = {}
    for table in ['info', 'structure']:
        configs[table] = {**default_configs[table], **user_configs.get(table,{})}




    return configs
