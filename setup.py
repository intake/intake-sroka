#!/usr/bin/env python

from setuptools import setup, find_packages
import versioneer


requires = open('requirements.txt').read().strip().split('\n')

setup(
    name='intake-sroka',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description='Cloud API drivers for Intake',
    url='https://github.com/intake/intake-sroka',
    maintainer='Martin Durant',
    maintainer_email='mdurant@anaconda.com',
    license='BSD',
    py_modules=['intake_sroka'],
    packages=find_packages(),
    package_data={'': ['*.csv', '*.yml', '*.html']},
    entry_points={
        'intake.drivers': ['athena = intake_sroka.sources:AthenaSource',
                           'google_analytics = intake_sroka.sources:GASource']},
    include_package_data=True,
    install_requires=requires,
    long_description=open('README.md').read(),
    zip_safe=False,
)
