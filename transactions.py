'''
Created on 12-Nov-2019

@author: sakthi-mahesh
'''
import unittest

from intergalaxy_shop.conversions import InterGalacticConversion
from intergalaxy_shop.numerals import InterGalacticNumeral
from intergalaxy_shop.units import Units


class Translation(object):

    UnitConversion = 'credit'

    IgnoreWords = (
                    'is',
                    'credits'
                    )

    def __init__(self, *args):
        self.__units = None
        self.galacticNumerals = InterGalacticNumeral(
                                    **dict(list(self._numerals(*args)))
                                )
        self.galacticConversion = InterGalacticConversion(self.galacticNumerals)
        self.units = self._units(*args)

    def _numerals(self, *args):
        for sentense in args:
            sentense = sentense.strip()
            if sentense and sentense.lower().find(self.UnitConversion) == -1:
                words = map(lambda word: word.strip(), sentense.split())
                yield [word for word in words if word.lower() not in self.IgnoreWords]

    def _credits(self, *args):
        for sentense in args:
            sentense = sentense.strip()
            if sentense and sentense.lower().find(self.UnitConversion) != -1:
                words = map(lambda word: word.strip(), sentense.split())
                yield [word for word in words if word.lower() not in self.IgnoreWords]

    def _units(self, *args):
        for credit_trans in self._credits(*args):
            galactic_num = credit_trans[:2]
            item_name, arabic_num = credit_trans[-2:]
            yield item_name, self.galacticConversion.to_credit(galactic_num, int(arabic_num))

    @property
    def units(self):
        return self.__units

    @units.setter
    def units(self, iterable):
        self.__units = Units(**dict(iterable))


class TransactionalQuery(object):

    UnitConversion = 'credit'

    def __init__(self, translator, *args):
        self.__conversion_queries = None
        self.__credit_queries = None
        self.translator = translator
        self.conversion_queries = self._conversion_query(*args)
        self.credit_queries = self._credit_query(*args)

    def _conversion_query(self, *args):
        for sentense in args:
            sentense = sentense.strip()
            if sentense and sentense.lower().find(self.UnitConversion.lower()) == -1:
                words = map(lambda word: word.strip(), sentense.split())
                yield sentense, [ word for word in  words if hasattr(self.translator.galacticNumerals, word)]

    def _credit_query(self, *args):
        for sentense in args:
            sentense = sentense.strip()
            if sentense and sentense.lower().find(self.UnitConversion.lower()) != -1:
                words = map(lambda word: word.strip(), sentense.split())
                words = [word for word in words if hasattr(self.translator.units, word) \
                                                or hasattr(self.translator.galacticNumerals, word)]
                galactic_num = words[:-1]
                item_name = words[-1]
                yield  sentense, item_name, galactic_num

    @property
    def conversion_queries(self):
        return self.__conversion_queries

    @conversion_queries.setter
    def conversion_queries(self, iterable):

        def answers():
            for question, galactic_num in iterable:
                if not galactic_num:
                    yield question, "I have no idea what you are talking about"
                else:
                    value = self.translator.galacticConversion.to_arabic(
                                self.translator.galacticConversion.to_roman(galactic_num))
                    yield question, ' '.join(galactic_num) + ' is ' + str(value)

        self.__conversion_queries = answers()

    @property
    def credit_queries(self):
        return self.__credit_queries

    @credit_queries.setter
    def credit_queries(self, iterable):

        def answers():
            for question, item_name, galactic_num in iterable:
                if not galactic_num:
                    yield question, "I have no idea what you are talking about"
                else:
                    arabic_num = self.translator.galacticConversion.to_arabic(
                                    self.translator.galacticConversion.to_roman(galactic_num))
                    value = self.translator.units[item_name] * arabic_num
                    yield question, ' '.join(galactic_num) + ' ' + item_name + ' is ' + str(value) + ' Credits'

        self.__credit_queries = answers()


def transaction(inputs, queries):
    translator = Translation(*inputs.split('\n'))
    transactions = TransactionalQuery(translator, *queries.split('\n'))
    for question, answer in transactions.conversion_queries:
        print(question)
        print('\t', answer)
    for question, answer in transactions.credit_queries:
        print(question)
        print('\t', answer)


class TestTransaction(unittest.TestCase):

    def setUp(self):
        translator = Translation(*[
                        "glob is I",
                        "prok is V",
                        "pish is X",
                        "tegj is L",
                        "glob glob Silver is 34 Credits",
                        "glob prok Gold is 57800 Credits",
                        "pish pish Iron is 3910 Credits",
                    ])
        transactions = TransactionalQuery(translator, *[
                        "how much is pish tegj glob glob ?",
                        "how many Credits is glob prok Silver ?",
                        "how many Credits is glob prok Gold ?",
                        "how many Credits is glob prok Iron ?",
                        "how do you do?"
                    ])
        for _, conversion_answer in transactions.conversion_queries:break
        for _, credit_answer in transactions.credit_queries:break
        self.conversion_answer = conversion_answer
        self.credit_answer = credit_answer

    def test_query(self):
        self.assertEqual(self.conversion_answer, "pish tegj glob glob is 42")

    def test_credit(self):
        self.assertEqual(self.credit_answer, "glob prok Silver is 68.0 Credits")


if __name__ == "__main__":
    unittest.main()
