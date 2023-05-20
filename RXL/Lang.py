import threading





apply = lambda f,iterable: type(iterable)(__import__("builtins").map(f,iterable))



def constant(f):
    def fset(self, value):
        raise PermissionError
    def fget(self):
        return f()
    return property(fget, fset)



class modified_thread(threading.Thread):
    def get_result(self):
        return {k:v for i,(k,v) in enumerate(self.__dict__.items()) if i >= 13}

    @property
    def result(self):
        return self.get_result()



class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
