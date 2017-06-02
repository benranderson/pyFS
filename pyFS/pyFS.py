from pyFS.ModelDefinition.model_definition import ModelDefinition

import datetime
import os
from winreg import *

class pyFS:

    def __init__(self, path, name, initialise_model=False):
        self.path = path
        self.name = name
        self._initialise_app()
        if initialise_model:
            self._initialise_model()
        else:
            self._read_model()

    def _initialise_app(self):
        self._get_FS2000_install_directory()

    def _get_FS2000_install_directory(self):
        reg = ConnectRegistry(None, HKEY_LOCAL_MACHINE)
        key = OpenKey(reg, 'SOFTWARE\Wow6432Node\FS2000\Setup')
        self._install_directory = EnumValue(key, 0)[1]

    def _initialise_model(self):
        self.date_created = datetime.datetime.now()
        self._create_empty_model()

    def _create_empty_model(self):
        self.model_definition = ModelDefinition(self.path, self.name,
                                                self._install_directory,
                                                initialise_model=True)
        # Add implementation of Load, Analysis, Results etc.

    def _read_model(self):
        self.model_definition = ModelDefinition(self.path, self.name,
                                           initialise_model=False)
        # Add implementation of Load, Analysis, Results etc.

    def _generate_nam_data(self):
        return '{0}\{1}\n{1}\n{0}'.format(self.path, self.name)

    def _update_model_nam(self):
        path = os.path.join(self._install_directory, 'model.nam')
        with open(path, 'w') as nam:
            nam.write(self._generate_nam_data())

    def _update_batch_nam(self):
        path = os.path.join(self._install_directory, 'batch.nam')
        with open(path, 'w') as nam:
            nam.write(self._generate_nam_data())
