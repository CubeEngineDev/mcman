""" Setup file for PlugMan. """
from setuptools import setup
import mcman

setup(
    name='mc-man',
    version=mcman.__version__,
    author=mcman.__author__,
    author_email='mail@totokaka.io',
    description='A Minecraft server jar and plugins manager',
    url='https://github.com/CubeEngineDev/mc-man',
    packages=['mcman', 'mcman.frontend', 'mcman.backend'],
    scripts=["bin/mcman"],
    install_requires=['PyYAML>=3.10',
                      'pyBukGet>=2.3',
                      'pySpaceGDN>=0.2'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: System :: Systems Administration',
        'Topic :: Utilities',
    ],
)
