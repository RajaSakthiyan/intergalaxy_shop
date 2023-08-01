'''
Created on 11-Nov-2019

@version: Python3.5
@author: Rajasakthiyan
@contact: rajasakthiyan.g@gmail.com
'''

import unittest


class NotForSale(Exception):

    def __str__(self, item):
        return "Item you chosen - { } is not for sale".format(item)


class Units(object):

    class Goods(object):

        def __init__(self, name, cost_value):
            self.name = name
            self.__cost = cost_value

        @property
        def unit_cost(self):
            return self.__cost

        def __mul__(self, value):
            return self.unit_cost * value

    def __init__(self, **kwargs):
        for goods_name, cost in kwargs.items():
            super().__setattr__(goods_name, self.Goods(goods_name.capitalize(), cost))

    def __getitem__(self, goods):
        if hasattr(self, goods):
            return getattr(self, goods)
        raise NotForSale(goods)

    def __str__(self):
        return str({self[item].name: '{0} credits'.format(self[item].unit_cost) for item in self.__dict__})


class TestUnits(unittest.TestCase):

    def setUp(self):
        self.units = Units(Gold=16, Silver=22, BigBallofMud=90)

    def test_item(self):
        self.assertEqual(self.units['Gold'], self.units.Gold)

    def test_unitcost(self):
        self.assertEqual(self.units['Gold'] * 10, 160)

    def test_noitem(self):
        with self.assertRaises(NotForSale):
            self.units["Soap"]


if __name__ == '__main__':

    unittest.main()
