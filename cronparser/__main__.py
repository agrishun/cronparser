import sys
from .parser import CronExpressionParser

def main():
    try:
        args = sys.argv[1].split(' ')
        expression = CronExpressionParser(args)
        expression.print_expression()
    except IndexError:
        raise Exception('Missing arguments')

if __name__ == '__main__':
    main()