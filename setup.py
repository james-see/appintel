import re
from setuptools import setup, Command
import os

class PostInstallCommand(Command):
    """Post-installation for installation mode."""
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        target_path = "/usr/local/bin/itunizer"
        source_path = os.path.join(self.install_scripts, 'itunizer')
        if os.path.islink(target_path):
            os.unlink(target_path)
        os.symlink(source_path, target_path)
        print(f"Created symlink: {target_path} -> {source_path}")

version = re.search(
    '^__version__\s*=\s*"(.*)"', open("appintel/appintel.py").read(), re.M
).group(1)

setup(
    name="appintel",
    author="James Campbell",
    author_email="james@jamescampbell.us",
    version=version,
    license="GPLv3",
    description="Machine readable data from iTunes store for market research and data analytics",
    packages=["appintel"],
    py_modules=["appintel"],
    keywords=["itunes", "data-analysis", "api", "market-research", "pricing"],
    classifiers=["Programming Language :: Python :: 3 :: Only"],
    install_requires=["argparse", "pandas", "pprint", "requests"],
    entry_points={"console_scripts": ["itunizer = itunizer.itunizer:main"]},
    url="https://github.com/jamesacampbell/itunizer",
    download_url="https://github.com/jamesacampbell/itunizer/archive/{}.tar.gz".format(
        version
    ),
    cmdclass={
        'install': PostInstallCommand,
    },
)
