"""
This module represents the Model Definintion task in the FS2000 GUI. The aim is
that this module provides equivalent functionality to the Model Definition task
through an instance of the ModelDefinition class.

Designing the object heirarchy this way allows multiple ModelDefinitions to be
defined in a pyFS list and these can be used  with single or multiple Load,
Analysis of Post-Processing objects in a single pyFS model.
"""
from .mdl import (Node, BeamElement, SpringCouple, Restraint, MDLList,
                  Point, Geometry, Material, SpringTable, RCTable, ICTable)
from .model_parser import ModelParser
from ..BatchController.batch_controller import BatchController
#from ..BatchController.commands import *
from .. import SystemUtils as util

import datetime
import os
import shutil
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
            1.  Create a new model, uninitialised
                (overwrite_model=True, initialise_model=False)
                This creates a model structure within pyFS containing the
                model definition data for a new model. The model does not
                (yet) exist as an FS2000 model. This model could not be opened
                within the GUI and would not exist persistently unless it
                initialised explictly or written to MDL. Any existing model of
                the same name in the same directory will be overwritten.

            2.  Create a new model, initialised
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

        if not os.path.exists(self.path):
            os.makedirs(self.path)

        if (not overwrite_model and
                os.path.exists(os.path.join(self.path, self.name + '.mdl'))):
            self._read_model_definition()
        else:
            self._initialise_model_definition()

        if initialise_model:
            self.interpret_model_definition()

    def create_node(self, number=0, x=0, y=0, z=0, CSYS=0):
        if number == 0:
            number = len(self.nodes) + 1
        self.nodes.add_item(Node(number, x, y, z))

    def create_point(self, x=0, y=0, z=0):
        return Point(x, y, z)

    def select_nodes_by_points(self, point_1, point_2):

        def is_in_range(node):
            return ((node.x > min(point_1.x, point_2.x)) and
                    (node.x < max(point_1.x, point_2.x)) and
                    (node.y > min(point_1.y, point_2.y)) and
                    (node.y < max(point_1.y, point_2.y)) and
                    (node.z > min(point_1.z, point_2.z)) and
                    (node.z < max(point_1.z, point_2.z)))

        nodes = [node for node in self.nodes if is_in_range(node)]

        return nodes

    def create_beam_element(self, number=0, N1=0, N2=0, N3=0, rotation=0,
                            geometry=0, material=0, relZ=0,
                            relzY=0, taper=0, type=0, CO=0,
                            bend_radius=0):
        if number == 0:
            number = len(self.beam_elements) + 1
        if N1 == 0:
            N1 = len(self.beam_elements) + 1
        if N2 == 0:
            N2 = N1 + 1
        self.beam_elements.add_item(BeamElement(number, N1, N2, N3, rotation,
                                                geometry, material, relZ,
                                                relzY, taper, type, CO,
                                                bend_radius))

    def create_couple(self, number=0, N1=0, N2=0, rotation=0,
                      reference_element=0, spring_constant_table=0, CSYS=0):
        if number == 0:
            number = len(self.couples) + 1
        if N1 == 0:
            N1 = len(self.nodes) + 1
        if N2 == 0:
            N2 = N1 + 1
        self.couples.add_item(SpringCouple(number, N1, N2, rotation,
                                           reference_element,
                                           spring_constant_table, CSYS))

    def create_restraint(self, number, Tx=False, Ty=False, Tz=False, Rx=False,
                         Ry=False, Rz=False):
        if not (Tx or Ty or Tz or Rx or Ry or Rz):
            raise ValueError("One degree of freedom must be retrained (True)")
        self.restraints.add_item(Restraint(number, Tx, Ty, Tz, Rx, Ry, Rz))

    def create_geometry(self, number=0, type=0, name='', designation='',
                        graphics_type=0, graphics_offset_y=0,
                        graphics_offset_z=0, pipe_OD=0, pipe_WT=0, area=0,
                        I_zz=0, I_yy=0, J=0, A_y=0, A_z=0, P_yy=0, P_zz=0,
                        G=0, S_1_y=0, S_1_z=0, S_2_y=0, S_2_z=0, S_3_y=0,
                        S_3_z=0, S_4_y=0, S_4_z=0, G_2=0,
                        corrosion_allowance=0, mill_tolerance=0,
                        contents_density=0, insultation_thickness=0,
                        insulation_density=0, lining_thickness=0,
                        lining_density=0):
        if pipe_OD == pipe_WT == area == I_yy == I_zz == 0:
            raise ValueError("Must provide pipe sizes or section definition")
        if number == 0:
            number = len(self.geometries) + 1
        self.geometries.add_item(Geometry(number, type, name, designation,
                                          graphics_type, graphics_offset_y,
                                          graphics_offset_z, pipe_OD, pipe_WT,
                                          area, I_zz, I_yy, J, A_y, A_z, P_yy,
                                          P_zz, G, S_1_y, S_1_z, S_2_y, S_2_z,
                                          S_3_y, S_3_z, S_4_y, S_4_z, G_2,
                                          corrosion_allowance, mill_tolerance,
                                          contents_density,
                                          insultation_thickness,
                                          insulation_density, lining_thickness,
                                          lining_density))

    def create_material(self, number=0, E=0, G=0, mu=0, rho=0, alpha=0,
                        yield_strength=0, name='', UTS=0, pipework_UTS=0,
                        cold_allowable_stress=0, quality_factor=0,
                        pressure_coefficient=0, temperature_table=[]):

        if number == 0:
            number = len(self.materials) + 1
        self.geometries.add_item(Material(number, E, G, mu, rho, alpha,
                                          yield_strength, name, UTS,
                                          pipework_UTS, cold_allowable_stress,
                                          quality_factor, pressure_coefficient,
                                          temperature_table))

    def create_couple_property(self, number=0, K1=0, K2=0, K3=0, K4=0, K5=0,
                               K6=0, type=0, CO=0):
        if number == 0:
            number = len(self.couple_properties) + 1
        self.couple_properties.add_item(SpringTable(number, K1, K2, K3, K4, K5,
                                                    K6, type, CO))

    def create_RC_table(self, number, rc_points=[]):
        if number == 0:
            number = len(self.rc_tables) + 1
        self.rc_tables.add_item(RCTable(number, rc_points))

    def create_IC_table(self, number, IC0=0, IC1=0, IC2=0, IC3=0, IC4=0, IC5=0,
                        IC6=0):
        if number == 0:
            number = len(self.ic_tables) + 1
        self.ic_tables.add_item(ICTable(number, IC0, IC1, IC2, IC3, IC4, IC5,
                                        IC6))

    def _model_exists(self):
        file_path = os.path.join(self.path, self.name + '.xyz')
        file = pathlib.Path(file_path)
        return file.is_file()

    def _initialise_model_definition(self):
        self.date_created = datetime.datetime.now()
        self._create_empty_lists()
        self.write_MDL_file()

    def _read_model_definition(self):
        mp = ModelParser(self.path, self.name)
        self.nodes = mp.nodes
        self.beam_elements = mp.beam_elements
        self.couples = mp.couples
        self.restraints = mp.restraints
        self.geometries = mp.geometries
        self.couple_properties = mp.couple_properties
        self.materials = mp.materials
        self.rc_tables = mp.rc_tables
        self.ic_tables = mp.ic_tables

    def _create_empty_lists(self):
        self.nodes = MDLList()
        self.beam_elements = MDLList()
        self.couples = MDLList()
        self.restraints = MDLList()
        self.geometries = MDLList()
        self.couple_properties = MDLList()
        self.materials = MDLList()
        self.rc_tables = MDLList()
        self.ic_tables = MDLList()

    def _create_model_files(self):
        self.write_MDL_file()
        self.interpret_model_definition()

    def interpret_model_definition(self):
        bc = BatchController(self.path, self.name)
        c = Winfram('I')
        bc.run_command(c)

    def write_MDL_file(self):
        path = os.path.join(self.path, self.name + '.mdl')
        with open(path, 'w+') as MDL:
            MDL.writelines(n.MDLFormat() for n in self.nodes)
            MDL.writelines(e.MDLFormat() for e in self.beam_elements)
            MDL.writelines(sc.MDLFormat() for sc in self.couples)
            MDL.writelines(r.MDLFormat() for r in self.restraints)
            MDL.writelines(g.MDLFormat() for g in self.geometries)

    def __repr__(self):
        return 'Model: {0}'.format(self.name)
