import sys

def test_python_version_not_3_6():
    '''
    Testing main.py code to fail if version is < 3.6
    '''
    sys.version_info = (3,5,1)
    assert not sys.version_info >= (3,6)

def test_python_version_3_6():
    '''
    Testing main.py code will pass if version is < 3.6
    '''
    sys.version_info = (3,6)
    assert sys.version_info >= (3,6)

def test_current_python_version():
    '''
    Testing main.py code will pass if version is < 3.6
    '''
    assert sys.version_info >= (3,6)