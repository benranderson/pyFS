"""
This module represents the Load Definintion task in the FS2000 GUI. The aim is
that this module provides equivalent functionality to the Load Definition task
through an instance of the LoadDefinition class.

Designing the object heirarchy this way allows multiple LoadDefinitions to be
defined in a pyFS list and these can be used  with single or multiple Model,
Analysis of Post-Processing objects in a single pyFS model.
"""

import datetime
import os


class LoadDefinition:
    """
    Represents all the functionality found in the Load Definition Task and
    ultimately provides functionality to define loads in FS2000 or to write
    .L files for use in an analysis.
    """

    def __init__(self, path, name, extension='.L', overwrite_load=False):
        """
        A load definition can be created in one of two manners:
            1.  Create a new load
                (overwrite_load=True)
                This creates a load structure within pyFS containing the load
                definition data for a new load. The load does not (yet) exist
                in the FS2000 model. Any existing load of the same name in the
                same directory will be overwritten.

            2.  Open an existing load
                (overwrite_load=False)
                If the named load exists on the specified path the L file will
                be read into the pyFS structure. If the load does not exist
                then a new load will be created and this acts like option 1.
        """
        self.path = path
        self.name = name
        self.extension = extension

        if not os.path.exists(self.path):
            os.makedirs(self.path)

        if (not overwrite_load and
                os.path.exists(os.path.join(self.path, self.name + '.L'))):
            self._read_load_definition()
        else:
            self._initialise_load_definition()

    def _initialise_load_definition(self):
        self.date_created = datetime.datetime.now()
        self._create_empty_lists()
        self.write_L_file()

    def _read_load_definition(self):
        pass

    def _create_empty_lists(self):
        pass

    def write_L_file(self):
        path = os.path.join(self.path, self.name + self.extension)
        with open(path, 'w+') as L:
            L.writelines('Test')
