#!/usr/bin/env python-sirius
"""Package installer."""

from setuptools import setup

with open('VERSION', 'r') as _f:
    __version__ = _f.read().strip()

setup(
    name='ps-ramp-tests',
    version=__version__,
    author='lnls-sirius',
    description='PS Ramp Tests.',
    url='https://github.com/lnls-sirius/ps-tests',
    download_url='https://github.com/lnls-sirius/ps-tests',
    license='GNU GPLv3',
    classifiers=[
        'Intended Audience :: Science/Research',
        'Programming Language :: Python',
        'Topic :: Scientific/Engineering'
    ],
    packages=['ps_ramp_tests'],
    package_data={'ps_ramp_tests': ['VERSION']},
    scripts=['scripts/sirius-ramp-analysis.py',
             'scripts/sirius-ramp-test.py',
             'scripts/pulse_evt01.py',
             ],
    zip_safe=False
)
