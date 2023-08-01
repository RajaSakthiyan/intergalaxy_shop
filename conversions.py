'''
Created on 11-Nov-2019

@version: Python3.5
@author: Rajasakthiyan
@contact: rajasakthiyan.g@gmail.com
'''
import re
import unittest

from intergalaxy_shop.numerals import RomanNumeral


class InvalidRomanLiterals(Exception):

    def __str__(self, _str):
        return "Invalid Roman literal found - " + _str


class RomanNumerialRules(object):

    __Numeral = RomanNumeral()
    __NEGATIVES = (__Numeral.I.name, __Numeral.X.name,
                   __Numeral.C.name)
    __PRECEDENCE = {__Numeral.I.name:(__Numeral.V.name, __Numeral.X.name),
                    __Numeral.X.name: (__Numeral.C.name, __Numeral.L.name),
                   __Numeral.C.name :(__Numeral.D.name, __Numeral.M.name)}

    __RomanRegex = re.compile("^(?:M*(?:LD|LM|CM|CD|D?C{0,3})(?:VL|VC|XC|XL|L?X{0,3})(?:IX|IV|V?I{0,3}))$")

    def __init__(self, roman_str):
        if not self.__RomanRegex.match(roman_str):
            raise InvalidRomanLiterals(roman_str)
        self.letters = roman_str

    def iter_arabic(self):
        _len = len(self.letters)
        for i, letter in enumerate(self.letters):
            if letter in self.__NEGATIVES and i + 1 < _len and \
                self.letters[i + 1] in self.__PRECEDENCE[letter]:
                yield -1 * getattr(self.__Numeral, letter)()
            else:
                yield getattr(self.__Numeral, letter)()


class InterGalacticConversion(object):

    def __init__(self, galacticNumeral):
        self.galacticNumeral = galacticNumeral

    def to_roman(self, galactic_str):
        return ''.join(map(lambda letter: getattr(self.galacticNumeral, letter).value, galactic_str))

    def to_arabic(self, roman_str):
        romanStr = RomanNumerialRules(roman_str)
        return sum(romanStr.iter_arabic())

    def to_credit(self, galactic_str, arabic_str):
        return arabic_str / self.to_arabic(self.to_roman(galactic_str))


class TestConversion(unittest.TestCase):

    def setUp(self):
        from intergalaxy_shop.numerals import InterGalacticNumeral
        ignumeral = InterGalacticNumeral(
                            glob="I", prok="V",
                            pish="X", tegj="L"
                        )
        self.galactic_conversion = InterGalacticConversion(ignumeral)

    def test_to_roman(self):
        roman_str = self.galactic_conversion.to_roman(['pish', 'tegj', 'glob', 'glob'])
        self.assertEqual("XLII", roman_str)

    def test_to_roman1(self):
        roman_str = self.galactic_conversion.to_roman(['tegj', 'glob', 'pish', 'glob', ])
        self.assertNotEqual("XLII", roman_str)

    def test_to_arabic1(self):
        with self.assertRaises(InvalidRomanLiterals):
            self.galactic_conversion.to_arabic("LIXI")

    def test_to_credit(self):
        credit = self.galactic_conversion.to_credit(['glob', 'glob'], 34)
        self.assertEqual(17, credit)


if __name__ == '__main__':

    unittest.main()
