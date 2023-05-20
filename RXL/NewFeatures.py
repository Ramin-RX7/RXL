_auto = None
class array(list):
    def __init__(self,__iterable=...,type_=_auto, max_length:int=_auto):
        if __iterable is not Ellipsis:
            if type_ == _auto:
                type_ = type(__iterable[0])
                for item in __iterable:
                    if (not isinstance(item, type_)) and (item is not None):
                        raise TypeError(f"Given iterable has wrong type ({type(item)}!={type_})")
                self._type = type_
            else:
                members_types = set(type(t) for t in __iterable)
                if (len(members_types) >= 3):
                    raise TypeError("All array elements must have the same type")
                if (len(members_types) == 2) and (type(None) not in members_types):
                    raise TypeError("All array elements must have the same type")
                self._type = list(members_types-{type(None)})[0]

            if max_length == _auto:
                max_length = len(__iterable)
            elif len(__iterable) > max_length:
                raise MemoryError("Length of given iterable is more that `_max_length`")
            self._max_length = max_length
            final_iterable = ([item for item in __iterable] +
                              [None for _ in range(max_length-len(__iterable))])
        else:
            if type_ is _auto:
                raise ValueError("In empty array, type must be set")
            if max_length < 0:
                raise ValueError("In empty array, max_length has to be set")
            final_iterable = []
            self._type = type_
            self._max_length = max_length

        super().__init__(final_iterable)


    def __str__(self) -> str:
        return f"<{super().__str__()[1:-1]}>"

    def append(self, __v, *, shift=False):
        if shift:
            self.shift()
        if (type(__v) != self._type) and (__v is not None):
            raise TypeError("Attempt to add a value with wrong type to array")
        for i in range(len(self)):
            if self[i] is None:
                self[i] = __v
                break
        else:
            raise MemoryError("Maximum size of the array is reached")

    def shift(self):
        for i,item in enumerate(self):
            if item is None:
                if self[i:] == [None]*(len(self)-i):
                    break
                self.pop(i)
                super().append(None)
