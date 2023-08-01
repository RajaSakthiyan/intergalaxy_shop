'''
Created on 11-Nov-2019

@version: Python3.5
@author: Rajasakthiyan
@contact: rajasakthiyan.g@gmail.com
'''

from abc import ABCMeta
import unittest


class ReadOnlySymbol(Exception):

    def __str__(self):
        return "Symbol is ready only,"\
                " assignment operation not supported"


class SymbolNotFound(Exception):

    def __str__(self, symbol):
        return "Symbol '{0}' not found".format(symbol)


class Symbol(object):

    def __init__(self, symbol_name, symbol_value, symbol_type,
                 weight_type, weight_value):
        self.name = symbol_name
        self.type = symbol_type
        self.value = symbol_value
        self.weight_type = weight_type
        self.weight_value = weight_value

    def __call__(self):
        return self.weight_value() if isinstance(self.weight_value, Symbol) else self.weight_value

    def __str__(self):
        return "{0}: {1}({2}) as {3}: {4}".format(
                            self.type,
                            self.name, self.value,
                            self.weight_type, self.weight_value
                            )


class SymbolProperty(object):

    def __init__(self, symbol_name, symbol_value, symbol_type,
                 weight_type, weight_value):
        self.symbol = Symbol(
                        symbol_name,
                        symbol_value,
                        symbol_type,
                        weight_type,
                        weight_value
                    )

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return self.symbol


class Numeral(metaclass=ABCMeta):

    def __init__(self, **kwargs):
        self.__map = kwargs
        for name, value in kwargs.items():
            object.__setattr__(self, name,
                    type('SymbolTable', (object,),
                         dict(
                             symbol=SymbolProperty(
                                name, value,
                                symbol_type=str(self),
                                weight_type=str(self.WeightAs),
                                weight_value=self.WeightAs.get_symbol(value))
                             ))().symbol
                    )

    def __iter__(self):
        for name in self.__map:
            yield getattr(self, name)

    def get_symbol(self, name):
        if hasattr(self, name):
            return getattr(self, name)
        raise SymbolNotFound(name)


class Integer(Numeral):

    def __init__(self):
        self.WeightAs = None

    def get_symbol(self, value):
        return int(value)

    def __str__(self):
        return self.__class__.__name__


class ArabicNumeral(Numeral):

    def __init__(self):
        self.WeightAs = Integer()
        super().__init__(
                **{
                    "1":"1",
                    "5":"5",
                    "10":"10",
                    "50":"50",
                    "100":"100",
                    "500":"500",
                    "1000":"1000"
                }
            )

    def __str__(self):
        return self.__class__.__name__


class RomanNumeral(Numeral):

    def __init__(self):
        self.WeightAs = ArabicNumeral()
        super().__init__(
                I="1",
                V="5",
                X="10",
                L="50",
                C="100",
                D="500",
                M="1000"
            )

    def __str__(self):
        return self.__class__.__name__


class InterGalacticNumeral(Numeral):

    def __init__(self, weight_as=None, **kwargs):
        self.WeightAs = weight_as or RomanNumeral()
        super().__init__(**kwargs)

    def __str__(self):
        return self.__class__.__name__


class TestNumerals(unittest.TestCase):

    def setUp(self):
        self.numeral1 = InterGalacticNumeral(
            glob="I",
            prok="V",
            pish="X",
            tegj="L"
            )

        self.numeral2 = RomanNumeral()

    def test_symbol(self):
        num = self.numeral1.glob
        self.assertEqual("glob", num.name)
        num = self.numeral2.V
        self.assertEqual("V", num.name)

    def test_symbol_value(self):
        num = self.numeral1.glob
        self.assertEqual("I", num.value)
        num = self.numeral2.V
        self.assertEqual("5", num.value)

    def test_final_value(self):
        num = self.numeral1.glob
        self.assertEqual(1, num())
        num = self.numeral2.V
        self.assertEqual(5, num())

    def test_attr(self):
        with self.assertRaises(AttributeError):
            self.numeral1.blob


if __name__ == '__main__':

    unittest.main()
    #===========================================================================
    # numeral1 = InterGalacticNumeral(
    #             glob="I",
    #             prok="V",
    #             pish="X",
    #             tegj="L"
    #             )
    # for num in numeral1:
    #     print('***'.center(10, '_'))
    #     print(num.name)
    #     print(num.type)
    #     print(num.value)
    #     print(num())
    #===========================================================================

