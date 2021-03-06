from re import match

class CronConfigParserValueError(Exception):
    def __init__(self, field_name, errors=[]):
        super(CronConfigParserValueError, self).__init__('Incorrect value for {} argument'.format(field_name))

class CronConfigParser():
    fields = [
        'minutes',
        'hours',
        'day of month',
        'month',
        'day of week',
        'command'
    ]
    constrains = {
        'minutes' : [0, 59],
        'hours': [0, 23],
        'day of month': [1, 31],
        'month': [1, 12],
        'day of week': [1, 7],
    }
    expression_regex = {
        'RAW': r'^\d{1,2}|\w{3}$',
        'EVERY': r'^\*$',
        'ON_EVERY': r'^\*\/\d{1,2}$',
        'RANGE': r'^\d{1,2}\-\d{1,2}$',
        'SEQUENCE': r'^(\d{1,2})(,\s*\d{1,2})*$',
        'CONTAINS_CHARS': r'[a-zA-Z]'
    }
    days_of_the_week = {
        'mon': '1',
        'tue': '2',
        'wed': '3',
        'thu': '4',
        'fri': '5',
        'sat': '6',
        'sun': '7'
    }

    def __init__(self, arguments):
        if len(arguments) < 6:
            raise Exception('Invalid arguments')

        self.arguments = self.parse_arguments(arguments)
        self.expressions = []
        self.parse()

    def _validateRange(self, range_start, range_end, constraint_start, constraint_end, field_type):
        if int(range_start) < constraint_start or int(range_end) > constraint_end:
            raise CronConfigParserValueError(field_type)
    
    def _create_range(self, range_start, range_end, min_value, max_value):
        if int(range_start) > int(range_end):
            arr = []
            i = int(range_start)
            while i is not range_end:
                if i > max_value:
                    i = min_value
                arr.append(str(i))
                i = i + 1
            return arr
        
        return [str(i) for i in range(int(range_start), int(range_end))]

    def _convert_chars(self, value, field_type):
        try:
            if match(self.expression_regex['CONTAINS_CHARS'], value):
                return self.days_of_the_week[value]
            return value
        except:
            raise CronConfigParserValueError(field_type)

    def parse_arguments(self, arguments):
        commands = arguments[:5]
        commands.append(' '.join(arguments[5:]))
        return commands

    def parse(self):
        for key, field_type in enumerate(self.fields):
            field_constrains = self.constrains.get(field_type)
            if (field_constrains):
                result = self.parse_field(self.arguments[key], field_type, field_constrains)
            else:
                result = self.arguments[key]
            self.expressions.append(result)

    def parse_field(self, value, field_type, field_constrains):
        start, end = field_constrains

        if match(self.expression_regex['RAW'], value):
            value = self._convert_chars(value, field_type)
            self._validateRange(value, value, start, end, field_type)
            return [value]

        if match(self.expression_regex['EVERY'], value):
            return self._create_range(int(start), int(end) + 1, start, end)

        if match(self.expression_regex['RANGE'], value):
            range_start, range_end = value.split('-')
            self._validateRange(range_start, range_end, start, end, field_type)
            return self._create_range(int(range_start), int(range_end) + 1, start, end)

        if match(self.expression_regex['SEQUENCE'], value):
            sequence = value.split(',')
            for n in sequence:
                self._validateRange(n, n, start, end, field_type)
            return sequence
        
        if match(self.expression_regex['ON_EVERY'], value):
            _, divider = value.split('/')
            all_values = range(int(start), int(end) + 1)
            return [str(n) for n in all_values if int(n) % int(divider) == 0]

        raise CronConfigParserValueError(field_type)

    def print_expressions(self):
        for key, field_type in enumerate(self.fields):
            if self.expressions[key]:
                expression = self.expressions[key]
                if (self.constrains.get(field_type)):
                    expression = ' '.join(self.expressions[key])
                string = '{0: <14}'.format(field_type) + expression
                print(string)
