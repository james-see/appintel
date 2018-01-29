from setuptools import setup, find_packages

setup(
    name='itunizer',
    author='James Campbell',
    author_email='james@jamescampbell.us',
    version='0.5.2',
    license='GPLv3',
    description = 'Machine readable data from iTunes store for market research and data analytics',
    packages=find_packages(),
    py_modules=['itunizer'],
    keywords = ['itunes', 'data-analysis', 'api'], # arbitrary keywords
    classifiers = ["Programming Language :: Python :: 3 :: Only"],
    install_requires=[
        'argparse',
        'pandas',
        'pprint',
        'requests'
    ],
    entry_points={
        'console_scripts': [
            'itunizer = itunizer.__main__:main',
        ],
        },
    url = 'https://github.com/jamesacampbell/itunizer', # use the URL to the github repo
    download_url = 'https://github.com/jamesacampbell/itunizer/archive/0.2.tar.gz', # I'll explain this in a second
)