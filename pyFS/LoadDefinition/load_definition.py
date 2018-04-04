"""
This module represents the Load Definintion task in the FS2000 GUI. The aim is
that this module provides equivalent functionality to the Load Definition task
through an instance of the LoadDefinition class.

Designing the object heirarchy this way allows multiple LoadDefinitions to be
defined in a pyFS list and these can be used  with single or multiple Model,
Analysis of Post-Processing objects in a single pyFS model.
"""
from pyFS.LoadDefinition.l import (NL, ND, EP, UDL, LList)
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

    def create_nodal_load(self, number=0, node=0, x_force=0, y_force=0,
                          z_force=0, x_moment=0, y_moment=0, z_moment=0,
                          conc_mass=0):
        if number == 0:
            number = len(self.nodal_loads) + 1
        self.nodal_loads.add_item(NL(number, node, x_force, y_force, z_force,
                                     x_moment, y_moment, z_moment, conc_mass))

    def create_nodal_displacement(self, number=0, node=0, x_disp=0, y_disp=0,
                                  z_disp=0, x_rot=0, y_rot=0, z_rot=0):
        if number == 0:
            number = len(self.nodal_displacements) + 1
        self.nodal_displacements.add_item(ND(number, node, x_disp, y_disp,
                                             z_disp, x_rot, y_rot, z_rot))

    def create_element_point_load(self, number=0, element=0, coord=1, length=0,
                                  x_force=0, y_force=0, z_force=0, x_moment=0,
                                  y_moment=0, z_moment=0):
        if number == 0:
            number = len(self.nodal_displacements) + 1
        self.element_point_loads.add_item(EP(number, element, coord, length,
                                             x_force, y_force, z_force,
                                             x_moment, y_moment, z_moment))

    def create_element_uniformly_distributed_load(self, number=0, element=0,
                                                  x_force=0, y_force=0,
                                                  z_force=0):
        if number == 0:
            number = len(self.nodal_displacements) + 1
        self.element_uniformly_distributed_loads.add_item(UDL(number, element,
                                                              x_force, y_force,
                                                              z_force))

    def _initialise_load_definition(self):
        self.date_created = datetime.datetime.now()
        self._create_empty_lists()
        self.write_L_file()

    def _read_load_definition(self):
        pass

    def _create_empty_lists(self):
        self.nodal_loads = LList()
        self.nodal_displacements = LList()
        self.element_point_loads = LList()
        self.element_uniformly_distributed_loads = LList()

    def write_L_file(self):
        path = os.path.join(self.path, self.name + self.extension)
        with open(path, 'w+') as L:
            L.writelines(nl.LFormat() for nl in self.nodal_loads)
            L.writelines(nd.LFormat() for nd in self.nodal_displacements)
            L.writelines(ep.LFormat() for ep in self.element_point_loads)
            L.writelines(udl.LFormat() for udl
                         in self.element_uniformly_distributed_loads)
