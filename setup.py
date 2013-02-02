from setuptools import setup
import os
import codecs
import re
here = os.path.abspath(os.path.dirname(__file__))


def read(*parts):  # Stolen from pip's setup.py
    try:
        return codecs.open(os.path.join(here, *parts), 'r', 'utf8').read()
    except:
        return ""


def find_version(*file_paths):  # Stolen from pip's setup.py
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


setup(
    name='Flask-OlinAuth',
    version=find_version('flask_olinauth.py'),
    url='https://github.com/wcdolphin/flask-olinauth',
    license='MIT',
    author='Cory Dolphin',
    author_email='wcdolphin@gmail.com',
    description='A simple Flask extension implementing Olin\'s authentication',
    long_description= read("README.txt"),
    py_modules=['flask_olinauth'],
    # if you would be using a package instead use packages instead
    # of py_modules:
    # packages=['flask_sqlite3'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Flask>=0.8',
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