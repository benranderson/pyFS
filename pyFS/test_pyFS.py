from pyFS import pyFS as pyFS
import pytest
import os
import datetime

initialised_folder = 'initialised'
initialised_name = initialised_folder + '_pyFS'
uninitialised_folder = 'uninitialised'
uninitialised_name = uninitialised_folder + '_pyFS'

def test_bad_path_character():
    bad_character_path = 'a?'
    with pytest.raises(ValueError):
        pyFS.pyFS(bad_character_path, 'test')

def test_bad_path_long():
    bad_path_long = 'a' * 40000
    with pytest.raises(ValueError):
        pyFS.pyFS(bad_path_long, 'test')

@pytest.fixture
def uninitialised_pyFS(tmpdir):
    return pyFS.pyFS(str(tmpdir.join(uninitialised_folder)), uninitialised_name)

def test_default_uninitialised_pyFS_path(uninitialised_pyFS, tmpdir):
    assert uninitialised_pyFS.path == str(tmpdir.join(uninitialised_folder))
    
def test_default_uninitialised_pyFS_name(uninitialised_pyFS):
    assert uninitialised_pyFS.name == uninitialised_name

@pytest.fixture
def initialised_pyFS(tmpdir):
    return pyFS.pyFS(str(tmpdir.join(initialised_folder)), initialised_name,
                     initialise_model=True)

def test_default_initialised_pyFS(initialised_pyFS, tmpdir):
    assert initialised_pyFS.path == str(tmpdir.join(initialised_folder))

def test_default_initialised_pyFS_name(initialised_pyFS):
    assert initialised_pyFS.name == initialised_name

def test_default_initialised_pyFS_date(initialised_pyFS):
    assert (initialised_pyFS.date_created - datetime.datetime.now() < 
            datetime.timedelta(5000))