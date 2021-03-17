#!/usr/bin/env python
# -*- coding: UTF-8 -*-


class forat_negre_sonat(object):
    def __init__(self, mostrar):
        self.mostrar = mostrar

    def __call__(self, f):
        def none(*args, **kw_args):
            print(self.mostrar)
            return f(*args, **kw_args)

        return none


@forat_negre_sonat(mostrar=True)
def suma(a, b):
    "Suma dos elements que li passam com a paràmetre"
    return a + b


if __name__ == "__main__":
    print(suma(2, 3))
    print(suma(5, 6))
    print(suma(9, 5))
