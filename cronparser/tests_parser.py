import unittest
from parser import CronExpressionParser, CronExpressionParserValueError


class TestCronExpressionParser(unittest.TestCase):
    def test_valid_input(self):
        parser = CronExpressionParser(['*/15', '0', '1,15', '*', '1-5', 'command'])
        self.assertEqual(parser.expressions[0], ['0', '15', '30', '45'])
        self.assertEqual(parser.expressions[1], ['0'])
        self.assertEqual(parser.expressions[2], ['1', '15'])
        self.assertEqual(parser.expressions[3], ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12'])
        self.assertEqual(parser.expressions[4], ['1', '2', '3', '4', '5'])
        self.assertEqual(parser.expressions[5], 'command')

    def test_invalid_input(self):
        with self.assertRaises(CronExpressionParserValueError):
            parser = CronExpressionParser(['*/', '0', '1,15', '*', '1-5', 'command'])
        with self.assertRaises(CronExpressionParserValueError):
            parser = CronExpressionParser(['*/', '_', '1,15', '*', '1-5', 'command'])
        with self.assertRaises(CronExpressionParserValueError):
            parser = CronExpressionParser(['*/', 'd', '1,15', '*', '1-5', 'command'])
        with self.assertRaises(CronExpressionParserValueError):
            parser = CronExpressionParser(['*/', '0', '1,,15', '*', '1-5', 'command'])
        with self.assertRaises(CronExpressionParserValueError):
            parser = CronExpressionParser(['*/', '0', '1,15', '*', '1-51', 'command'])
        with self.assertRaises(CronExpressionParserValueError):
            parser = CronExpressionParser(['*/', '0', '1,15', '*', '1--5', 'command'])
        with self.assertRaises(Exception):
            parser = CronExpressionParser(['*/', '0', '1,15', '*', '1-5'])

if __name__ == '__main__':
    unittest.main()