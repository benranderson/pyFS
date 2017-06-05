"""
This module represents the Model Definintion task in the FS2000 GUI. The aim is
that this module provides equivalent functionality to the Model Definition task
through an instance of the ModelDefinition class.

Designing the object heirarchy this way allows multiple ModelDefinitions to be
defined in a pyFS list and these can be used  with single or multiple Load,
Analysis of Post-Processing objects in a single pyFS model.
"""

from pyFS.ModelDefinition.node import Node
from pyFS.ModelDefinition.beam_element import BeamElement
from pyFS.ModelDefinition.model_parser import ModelParser
from pyFS.ModelDefinition.spring_couple import SpringCouple
from pyFS.ModelDefinition.restraint import Restraint
from pyFS.BatchController.batch_controller import BatchController
from pyFS.BatchController.commands import *
import pyFS.SystemUtils as util

import datetime
import os
import subprocess
import pathlib


class ModelDefinition:
    """
    Represents all the functionality found in the Model Definition Task and
    ultimately provides functionality to initialise a model in FS2000 or to
    write .MDL files for use in an analysis.
    """

    def __init__(self, path, name,
                 overwrite_model=False, initialise_model=False):
        """
        A model definition can be created in one of four manners:
            1.  Create a new model, unitialised
                (overwrite_model=True, initialise_model=False)
                This essentially creates a model structure within pyFS
                containing the model definition data for a new model. The model
                does not (yet) exist as an FS2000 model. This model could
                not be opened within the GUI and would not exist persistently
                unless it initialised explictly or written to MDL. Any existing
                model of the same name in the same directory will be
                overwritten.

            2.  Create a new model, itialised
                (overwrite_model=True, initialise_model=True)
                As 1. but with a blank .MDL file created and initialised
                using "WINFRAM I". This will create FS2000 model files and a
                model which may be opened in the FS2000 GUI.

            3.  Open an existing model, uninitialised
                (overwrite_model=False, initialise_model=False)
                If the named model exists on the specified path the MDL file
                will be read into the pyFS structure. pyFS will not check if
                the read in model has also been initialised in FS2000. If the
                model does not exist then a new model will be created and this
                acts like option 1.

            4.  Open an existing model, initialised
                (overwrite_model=False, initialise_model=True)
                As 3. except the model  will be initialised using "WINFRAM I".
                This will ensure that the FS2000 model files match the model
                listed in the MDL file.
        """
        self.path = path
        self.name = name
        self.install_directory = util.get_FS2000_install_directory()
        if (not overwrite_model) and self._model_exists():
            self._read_model_definition()
        else:
            self._initialise_model_definition()
        if initialise_model:
            self.initialise_model_definition()

    def create_node(self, number=0, x=0, y=0, z=0, CSYS=0):
        if number == 0:
            number = len(self.nodes) + 1
        self.nodes.append(Node(number, x, y, z))

    def create_beam_element(self, number=0, N1=0, N2=0, N3=0, rotation=0,
                            geometry=0, material=0, relZ=0,
                            relzY=0, taper=0, type=0, CO=0,
                            bend_radius=0):
        if number == 0:
            number = len(self.beam_elements) + 1
        if N1 == 0:
            N1 = len(self.nodes) + 1
        if N2 == 0:
            N2 = N1 + 1
        self.beam_elements.append(BeamElement(number, N1, N2, N3, rotation,
                                              geometry, material, relZ, relzY,
                                              taper, type, CO, bend_radius))

    def create_couple(self, number=0, N1=0, N2=0, rotation=0,
                      reference_element=0, spring_constant_table=0, CSYS=0):
        if number == 0:
            number = len(self.couples) + 1
        if N1 == 0:
            N1 = len(self.nodes) + 1
        if N2 == 0:
            N2 = N1 + 1
        self.couples.append(SpringCouple(number, N1, N2, rotation,
                                         reference_element,
                                         spring_constant_table, CSYS))

    def create_restraint(self, node, Tx=False, Ty=False, Tz=False, Rx=False,
                         Ry=False, Rz=False):
        if not (Tx or Ty or Tz or Rx or Ry or Rz):
            raise ValueError("One degree of freedom must be retrained (True)")
        self.restraints.append(Restraint(node, Tx, Ty, Tz, Rx, Ry, Rz))

    def _model_exists(self):
        file_path = os.path.join(self.path, self.name + '.xyz')
        file = pathlib.Path(file_path)
        return file.is_file()

    def _initialise_model_definition(self):
        self.date_created = datetime.datetime.now()
        self._create_empty_lists()

    def _read_model_definition(self):
        mp = ModelParser(self.path, self.name)
        self.nodes = mp.nodes
        self.beam_elements = mp.beam_elements
        self.couples = mp.couples
        self.restraints = mp.restraints
        self.geometries = []
        self.couple_properties = []
        self.materials = []
        self.rc_tables = []
        self.ic_tables = []

    def _create_empty_lists(self):
        self.nodes = []
        self.beam_elements = []
        self.couples = []
        self.restraints = []
        self.geometries = []
        self.couple_properties = []
        self.materials = []
        self.rc_tables = []
        self.ic_tables = []

    def _create_model_files(self):
        self.write_MDL_file()
        self.initialise_model()

    def initialise_model_definition(self):
        bc = BatchController(self.path, self.name)
        c = Winfram('I')
        bc.run_command(c)

    def write_MDL_file(self):
        path = os.path.join(self.path, self.name + '.mdl')
        with open(path, 'w') as MDL:
            MDL.writelines('N,' + str(n.number) + ',' + str(n.x) + ',' +
                           str(n.y) + ',' + str(n.z) + ',' + str(n.CSYS) +
                           '\n' for n in self.nodes)
            MDL.writelines('E,' + str(e.number) + ',' + str(e.N1) + ',' +
                           str(e.N2) + ',' + str(e.N3) + ',' +
                           str(e.rotation) + ',' + str(e.geometry) + ',' +
                           str(e.material) + ',' + str(e.relZ) + ',' +
                           str(e.relY) + ',' + str(e.taper) + ',' +
                           str(e.type) + ',' + str(e.CO) + ',' +
                           str(e.bend_radius) + '\n'
                           for e in self.beam_elements)
            MDL.writelines('SC,' + str(sc.number) + ',' + str(sc.N1) + ',' +
                           str(sc.N2) + ',' + str(sc.rotation) + ',' +
                           str(sc.reference_element) + ',' +
                           str(sc.spring_constant_table) + ',' +
                           str(sc.CSYS) + '\n'
                           for sc in self.couples)
            MDL.writelines('REST,' + str(r.Node) + ',' + str(int(r.Tx)) +
                           ',' + str(int(r.Ty)) + ',' + str(int(r.Tz)) +
                           ',' + str(int(r.Rx)) + ',' + str(int(r.Ry)) +
                           ',' + str(int(r.Rz)) + '\n'
                           for r in self.restraints)

    def __repr__(self):
        return 'Model: {0}'.format(self.name)
