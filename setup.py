from setuptools import setup

setup(
    name='lambdalabs-copy',
    version='0.1',
    install_requires=[
        'argparse',
    ],
    entry_points={
        'console_scripts': [
            'lambdalabs-copy=mypackage:main',
        ],
    },
)