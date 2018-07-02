# cronparser

### Installation
```
pip install -e .
```

### Usage
```
cronparser 'MINUTE HOUR DAY_OF_THE_MONTH MONTH DAY_OF_THE_WEEK COMMAND_TO_RUN'
```

### Example

```
> cronparser '*/15 0 1,15 * 1-5 /usr/bin/find'
```

The following output will be printed in your console

```
minutes       0 15 30 45
hours         0
day of month  1 15
month         1 2 3 4 5 6 7 8 9 10 11 12
day of week   1 2 3 4 5
command       /usr/bin/find
```

### Running tests
```
python cronparser/tests_parser.py
```