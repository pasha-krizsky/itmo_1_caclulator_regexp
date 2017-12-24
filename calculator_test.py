import unittest

from calculator import *
import timeit
from random import random


class CalculatorTest(unittest.TestCase):

    def test_remove_whitespaces(self):
        expression, result = "  3  +  2  ", "3+2"
        self.assertEqual(result, remove_whitespaces(expression))

    def test_find_subexpression(self):
        expression, result = "1+2+3*(4+3*(3+2)*19)*(2+3)", "(3+2)"
        self.assertEqual(result, find_subexpression(expression))
        expression, result = "3+2", "3+2"
        self.assertEqual(result, find_subexpression(expression))

    def test_add(self):
        expression, result = "3+2", 5.0
        self.assertEqual(result, add(expression))

    def test_subtract(self):
        expression, result = "3-2", 1.0
        self.assertEqual(result, subtract(expression))

    def test_multiply(self):
        expression, result = "3*2", 6.0
        self.assertEqual(result, multiply(expression))

    def test_divide(self):
        expression, result = "3/2", 1.5
        self.assertEqual(result, divide(expression))

    def test_calculate_subexpression(self):
        expression, result = "1+2/2-1*10", '-8.0'
        self.assertEqual(result, calculate_subexpression(expression))

    def test_calculate(self):
        e = 0.0001
        expression_and_result = {
            "2.+2.": 4,
            "2-.2": 1.8,
            "2*2": 4,
            "2/2.2": 0.9091,
            "-2/2": -1.0000,
            "-2/-2": 1.0000,
            "  2   /    2  ": 1.0000,
            "1.5+1.4": 2.9,
            "2.2*3.3": 7.26,
            "2.285566655*3.42432423": 7.82652127599655065,
            "1111111111111111111111111111111111111111+222222222222222": 1111111111111111111111111333333333333333,
            "(2+2)": 4,
            "(2+2*(3-1+5))": 16,
        }

        self.assertAlmostEqual(calculate("2.285566655*3.42432423"), 7.82652127599655065, delta=e)

        for key, value in expression_and_result.items():
            print(key)
            print(key + ' = ' + str(calculate(key)) + ' = ' + str(value))
            self.assertAlmostEqual(calculate(key), value, delta=e)

        expression = "1/0"
        calculate(expression)


    def testPerformance(self):

        ops = ["+", "-", "*", "/"]
        res = ""
        for i in range(0, 500):
            res += str(random() * 1000 + 1)
            res += ops[int(random() * 3)]
        res += "1"

        print("Start calc...")
        a = timeit.default_timer()

        calculate(res)
        print(timeit.default_timer() - a)

if __name__ == '__main__':
    unittest.main()
