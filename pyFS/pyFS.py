from .ModelDefinition import ModelDefinition
from . import SystemUtils as util

import datetime
import os
import sys
if 'win' in sys.platform:
    from winreg import ConnectRegistry, HKEY_LOCAL_MACHINE, OpenKey, EnumValue


class pyFS:

    def __init__(self, path, name, initialise_model=False):
        self.path = path
        self.name = name
        if initialise_model:
            self._initialise_model()
        else:
            self._read_model()

    def _initialise_model(self):
        self.date_created = datetime.datetime.now()
        if 'win' in sys.platform:
            self._create_empty_model()

    def _create_empty_model(self):
        self.model_definition = ModelDefinition(self.path, self.name,
                                                initialise_model=True)
        # Add implementation of Load, Analysis, Results etc.

    def _read_model(self):
        self.model_definition = ModelDefinition(self.path, self.name,
                                                initialise_model=False)
        # Add implementation of Load, Analysis, Results etc.
