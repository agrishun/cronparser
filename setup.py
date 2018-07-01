from setuptools import setup

setup(
    name = 'cronparser',
    version = '0.1.0',
    packages = ['cronparser'],
    entry_points = {
        'console_scripts': [
            'cronparser = cronparser.__main__:main'
        ]
    })