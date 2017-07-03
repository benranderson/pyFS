from .model_definition import ModelDefinition
import pytest
import os

# This represents mode 1 in __init__()
@pytest.fixture
def new_uninitialised_ModelDefinition(tmpdir):
    return ModelDefinition(str(tmpdir.join('new_unini')), 'new_unini',
                           overwrite_model=True)

def test_new_uninitialised_ModelDefinition_path(new_uninitialised_ModelDefinition,
                                                tmpdir):
    assert new_uninitialised_ModelDefinition.path == str(tmpdir.join('new_unini'))

def test_new_uninitialised_ModelDefinition_name(new_uninitialised_ModelDefinition):
    assert new_uninitialised_ModelDefinition.name == 'new_unini'
    
def test_new_uninitialised_ModelDefinition_install_directory(
        new_uninitialised_ModelDefinition):
    assert os.path.exists(new_uninitialised_ModelDefinition.install_directory)