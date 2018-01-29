from setuptools import setup, find_packages
import re

version = re.search(
    '^__version__\s*=\s*"(.*)"',
    open('itunizer/itunizer.py').read(),
    re.M
    ).group(1)

setup(
    name='itunizer',
    author='James Campbell',
    author_email='james@jamescampbell.us',
    version=version,
    license='GPLv3',
    description = 'Machine readable data from iTunes store for market research and data analytics',
    packages=['itunizer'],
    py_modules=['itunizer'],
    keywords = ['itunes', 'data-analysis', 'api', 'market-research', 'pricing'],
    classifiers = ["Programming Language :: Python :: 3 :: Only"],
    install_requires=[
        'argparse',
        'pandas',
        'pprint',
        'requests'
    ],
    entry_points={
        'console_scripts': [
            'itunizer = itunizer.itunizer:main',
        ],
        },
    url = 'https://github.com/jamesacampbell/itunizer',
    download_url = 'https://github.com/jamesacampbell/itunizer/archive/{}.tar.gz'.format(version)
)