from importlib.metadata import entry_points
import setuptools
import os

def readfile(filename):
    with open(filename, 'r+') as f:
        return f.read()

this_folder = os.path.dirname(os.path.abspath(__file__))
readme = os.path.join(this_folder, 'README.md')
license = os.path.join(this_folder, 'LICENSE')

setuptools.setup(
    name="PSV",
    version="0.1",
    description="Password manager vault",
    author="Keith Neo",
    author_email="keithneo00@gmail.com",
    long_description=readfile(readme),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    url="https://github.com/Cyrof/Password-manager",
    py_modules=["main"],
    install_requires=["cryptography==37.0.4", "prettytable==3.4.1", "pyfiglet==0.8.post1", "python-dotenv==0.20.0", "termcolor==1.1.0"],
    python_requires=">=3.10",
    entry_points={
        'console_scripts' : [
            'psv = main:cmd'
        ]
    },
)