import pytest
from important.parse import Import
import stat


@pytest.fixture
def python_imports():
    return [
        ('collections', 2, 0),
        ('math', 3, 0),
        ('os', 4, 0),
        ('copy', 5, 0),
        ('re', 6, 0),
        ('time', 6, 0),
        ('sys', 6, 0),
        ('os.path', 7, 0),
        ('dns', 8, 0),
        ('os.path', 9, 0),
        ('IPy', 10, 0),
        ('numpy', 11, 0),
        ('parser', 16, 4),
        ('enum', 19, 4),
        ('csv', 22, 8),
    ]


@pytest.fixture
def python_file_imports(python_imports):
    def create_results(filepath):
        return list(map(
            lambda x: Import(x[0], filepath, x[1], x[2]),
            python_imports
        ))
    items = create_results('scriptfile')
    items.extend(create_results('test1.py'))
    items.extend(create_results('subdir/test3.py'))
    return items


@pytest.fixture
def python_source():
    return '''
#!/usr/bin/env python
from collections import defaultdict
from math import abs as absolute
import os
import copy as duplicate
import re, time, sys
import os.path
import dns
from os.path import exists, join
import IPy
import numpy as np

print("test")

def func():
    import parser

class A(object):
    import enum

    def method(self):
        import csv
'''.strip()


@pytest.fixture
def python_source_file(tmpdir, python_source):
    python_source_file = tmpdir.join('test.py')
    python_source_file.write(python_source)
    return str(python_source_file)


@pytest.fixture
def __python_source_dir__(tmpdir, python_source):
    executable_file_mode = stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH \
        | stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH

    # Create a set of python files and a script file within
    # the base or other subdirectories that should be parsed
    python_source_dir = tmpdir.mkdir('dir')
    python_source_dir.join('test1.py').write(python_source)
    python_scriptfile = python_source_dir.join('scriptfile')
    python_scriptfile.write(python_source)
    python_scriptfile.chmod(executable_file_mode)
    python_source_subdir = python_source_dir.mkdir('subdir')
    python_source_subdir.join('test3.py').write(python_source)

    # Add file without shebang, but the correct permissions, that shouldn't be
    # parsed
    randomfile = python_source_dir.join('randomfile')
    randomfile.write('\n'.join(python_source.split('\n')[1:]))
    randomfile.chmod(executable_file_mode)

    # Add file with shebang but wrong permissions that shouldn't be parsed
    python_source_dir.join('otherrandomfile').write(python_source)

    return python_source_dir


@pytest.fixture
def python_source_dir(__python_source_dir__):
    return str(__python_source_dir__)


@pytest.fixture
def python_excluded_dir(__python_source_dir__):
    # Create a directory intended to be excluded
    python_excluded_dir = __python_source_dir__.mkdir('excluded')
    python_excluded_dir.join('test4.py').write(python_source)
    return str(python_excluded_dir)


@pytest.fixture
def python_excluded_file(__python_source_dir__):
    python_excluded_file = __python_source_dir__.join('excluded.py')
    python_excluded_file.write(python_source)
    return str(python_excluded_file)


@pytest.fixture
def exclusions(python_excluded_file, python_excluded_dir):
    return [python_excluded_file, python_excluded_dir]


@pytest.fixture
def requirements_file(tmpdir):
    requirements_file = tmpdir.join('requirements.txt')
    requirements_file.write('''
pyyaml
os
csv
parser
dnspython
IPy
numpy'''.strip())
    return str(requirements_file)


@pytest.fixture
def ok_requirements_file(tmpdir):
    requirements_file = tmpdir.join('requirements.txt')
    requirements_file.write('''
os
csv
parser
dnspython
IPy
numpy'''.strip())
    return str(requirements_file)


@pytest.fixture
def constraints_file(tmpdir):
    constraints_file = tmpdir.join('constraints.txt')
    constraints_file.write('''
unused==0
other_unused==0
os<6
os.path<6
dnspython==0
enum<10
csv>1
re>1,<=3'''.strip())
    return str(constraints_file)


@pytest.fixture
def ok_constraints_file(tmpdir):
    constraints_file = tmpdir.join('constraints.txt')
    constraints_file.write('''
unused==0
other_unused==0
os<=9
os.path<=6
dnspython<=6
enum<10
csv>1
re>1,<=3'''.strip())
    return str(constraints_file)
