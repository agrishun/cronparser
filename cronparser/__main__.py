import sys
from .parser import CronConfigParser

def main():
    try:
        args = sys.argv[1].split(' ')
        expression = CronConfigParser(args)
        expression.print_expressions()
    except IndexError:
        raise Exception('Missing arguments')

if __name__ == '__main__':
    main()