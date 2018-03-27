from pyFS.ModelDefinition.model_definition import ModelDefinition
import pytest
import os


@pytest.fixture
def new_uninitialised_ModelDefinition(tmpdir):
    return ModelDefinition(str(tmpdir.join('new_unini')), 'new_unini',
                           overwrite_model=True)


def test_new_uninitialised_ModelDefinition_path(
        new_uninitialised_ModelDefinition, tmpdir):
    assert new_uninitialised_ModelDefinition.path == str(tmpdir.join(
        'new_unini'))


def test_new_uninitialised_ModelDefinition_name(
        new_uninitialised_ModelDefinition):
    assert new_uninitialised_ModelDefinition.name == 'new_unini'


def test_new_uninitialised_ModelDefinition_install_directory(
        new_uninitialised_ModelDefinition):
    assert os.path.exists(new_uninitialised_ModelDefinition.install_directory)


@pytest.fixture
def new_initialised_ModelDefinition(tmpdir):
    return ModelDefinition(str(tmpdir.join('new_ini')), 'new_ini',
                           overwrite_model=True,
                           initialise_model=True)


def test_new_initialised_ModelDefinition_path(new_initialised_ModelDefinition,
                                              tmpdir):
    assert new_initialised_ModelDefinition.path == str(tmpdir.join('new_ini'))


def test_new_initialised_ModelDefinition_name(new_initialised_ModelDefinition):
    assert new_initialised_ModelDefinition.name == 'new_ini'


def test_new_initialised_ModelDefinition_install_directory(
        new_initialised_ModelDefinition):
    assert os.path.exists(new_initialised_ModelDefinition.install_directory)
