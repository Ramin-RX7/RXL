apply = lambda f,iterable: type(iterable)(__import__("builtins").map(f,iterable))



_auto = -1
class array(list):
    def __init__(self,__iterable=...,type_=_auto, max_length=_auto):
        if __iterable is not Ellipsis:
            if type_ == _auto:
                type_ = type(__iterable[0])
                for element in __iterable:
                    if type(element) is not type_:
                        raise TypeError("Given iterable has wrong type (type(element)!=type_)")
                self._type = type_
            else:
                members_types = set(type(t) for t in __iterable)
                if len(members_types) != 1:
                    raise TypeError("All array elements must have the same type")
                if list(members_types)[0] != type_:
                    raise TypeError("Array with wrong element type is given")
                self._type = list(members_types)[0]

            if max_length == _auto:
                max_length = len(__iterable)
            if len(__iterable) > max_length:
                raise MemoryError("Length of given iterable is more that `_max_length`")
            self._max_length = max_length
            final_iterable = [item for item in __iterable] + [None for _ in range(max_length-len(__iterable))]
            return super().__init__(final_iterable)

        else:
            if max_length < 0:
                raise ValueError("In empty array, max_length has to be set")

            self._max_length = max_length
            return super().__init__()


    def __str__(self) -> str:
        return f"<{super().__str__()[1:-1]}>"

    def append(self,__v):
        if type(__v) != self._type:
            raise TypeError("Attempt to add a value with wrong type to array")
        if len(self) >= self._max_length:
            raise MemoryError("Maximum size of the array is reached")
        super().append(__v)


def constant(f):
    def fset(self, value):
        raise PermissionError
    def fget(self):
        return f()
    return property(fget, fset)
class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]