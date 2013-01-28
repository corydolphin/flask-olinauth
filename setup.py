from setuptools import setup
from flask_olinauth import __version__
import os
here = os.path.abspath(os.path.dirname(__file__))

setup(
    name='Flask-OlinAuth',
    version=__version__,
    url='https://github.com/wcdolphin/flask-olinauth',
    license='MIT',
    author='Cory Dolphin',
    author_email='wcdolphin@gmail.com',
    description='A simple Flask extension implementing Olin\'s authentication',
    long_description= open(os.path.join(here, "README.md")).read(),
    py_modules=['flask_olinauth'],
    # if you would be using a package instead use packages instead
    # of py_modules:
    # packages=['flask_sqlite3'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Flask',
        'requests>=1.1.0'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)