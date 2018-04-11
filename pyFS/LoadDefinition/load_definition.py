"""
This module represents the Load Definintion task in the FS2000 GUI. The aim is
that this module provides equivalent functionality to the Load Definition task
through an instance of the LoadDefinition class.

Designing the object heirarchy this way allows multiple LoadDefinitions to be
defined in a pyFS list and these can be used  with single or multiple Model,
Analysis of Post-Processing objects in a single pyFS model.
"""
from pyFS.LoadDefinition.l import (NF, ND, EP, UDL, ED, FP, TEPR, PUDL, PPRESS,
                                   PTEMP, Grv, AMBT, LList, LDict)
from pyFS.LoadDefinition.load_parser import LoadParser
import datetime
import os


class LoadDefinition:
    """
    Defines a list of all load cases associated with the FS2000 model.
    """

    def __init__(self, path, name, number, description='Description',
                 overwrite_load=False):
        """
        On initiation, either needs to

        1.  Insert a new load into the list / dictionary.
            (Number > 0 doesn't exist)

        2.  Overwrite an existing load in the list / dictionary.
            (Number > 0 already exists, overwrite_load=True)

        3.  Update an existing load in the list / dictionary.
            (Number > 0 already exists, overwrite_load=False)
        """
        self.path = path
        self.name = name
        self.number = number
        self.load_description = description
        self.overwrite_load = overwrite_load

        self._create_dict_of_loads()

    def _create_dict_of_loads(self):
        try:
            dict_of_loads
        except NameError:
            dict_of_loads = LDict()

        key = self.number
        if key not in dict_of_loads:
            dict_of_loads[key] = slef.load_description
        elif key in dict_of_loads and self.overwrite_load:
            dict_of_loads[key] = slef.load_description
        elif (key in dict_of_loads and not self.overwrite_load and
              not dict_of_loads[key] == slef.load_description):
            dict_of_loads[key] = slef.load_description
        return dict_of_loads


class LoadCase:
    """
    Represents all the functionality required to write a load case file and to
    write .L files for use in an analysis.
    """

    def __init__(self, path, name, number, description='Description',
                 overwrite_load=False):
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
        self.number = number
        self.extension = '.L' + str(self.number)
        self.load_description = description

        self.loads = LoadDefinition(self.path, self.name, self.number,
                                    self.load_description, overwrite_load)

        if not os.path.exists(self.path):
            os.makedirs(self.path)

        if (not overwrite_load and
                os.path.exists(os.path.join(self.path, self.name + '.L'))):
            self._read_load_definition()
        else:
            self._initialise_load_definition()

    def create_nodal_load(self, number=0, x_force=0, y_force=0,
                          z_force=0, x_moment=0, y_moment=0, z_moment=0,
                          conc_mass=0):
        if number == 0:
            number = len(self.nodal_loads) + 1
        self.nodal_loads.add_item(NF(number, x_force, y_force, z_force,
                                     x_moment, y_moment, z_moment, conc_mass))

    def create_nodal_displacement(self, number=0, x_disp=0, y_disp=0,
                                  z_disp=0, x_rot=0, y_rot=0, z_rot=0):
        if number == 0:
            number = len(self.nodal_displacements) + 1
        self.nodal_displacements.add_item(ND(number, x_disp, y_disp, z_disp,
                                             x_rot, y_rot, z_rot))

    def create_element_point_load(self, number=0, coord=1, length=0,
                                  x_force=0, y_force=0, z_force=0, x_moment=0,
                                  y_moment=0, z_moment=0):
        if number == 0:
            number = len(self.element_point_loads) + 1
        self.element_point_loads.add_item(EP(number, coord, length, x_force,
                                             y_force, z_force, x_moment,
                                             y_moment, z_moment))

    def create_element_uniformly_distributed_load(self, number=0, x_force=0,
                                                  y_force=0, z_force=0):
        if number == 0:
            number = len(self.element_uniformly_distributed_loads) + 1
        self.element_uniformly_distributed_loads.add_item(UDL(number, x_force,
                                                              y_force,
                                                              z_force))

    def create_element_distributed_load(self, number=0, coord=1, s_length=0,
                                        f_length=0, s_x_force=0,
                                        f_x_force=None, s_y_force=0,
                                        f_y_force=None, s_z_force=0,
                                        f_z_force=None):
        if number == 0:
            number = len(self.element_distributed_loads) + 1
        if f_x_force is None:
            f_x_force = s_x_force
        if f_y_force is None:
            f_y_force = s_y_force
        if f_z_force is None:
            f_z_force = s_z_force
        self.element_distributed_loads.add_item(ED(number, coord, s_length,
                                                   f_length, s_x_force,
                                                   f_x_force, s_y_force,
                                                   f_y_force, s_z_force,
                                                   f_z_force))

    def create_face_and_edge_load(self, number=0, face=0, direction=1, p1=0,
                                  p2=0, p3=0, p4=0):
        if number == 0:
            number = len(self.face_and_edge_loads) + 1
        self.face_and_edge_loads.add_item(FP(number, face, direction, p1, p2,
                                             p3, p4))

    def create_thermal_and_pressure_load(self, number=0, temperature=0,
                                         press_pi=0, temp_ls=None, press_po=0):
        if number == 0:
            number = len(self.thermal_and_pressure_loads) + 1
        if temp_ls is None:
            temp_ls = temperature
        self.thermal_and_pressure_loads.add_item(TEPR(number, temperature,
                                                      press_pi, temp_ls,
                                                      press_po))
        # self.create_ambient_temperature_load()

    def create_geometric_property_code_load(self, number=0, x_udl=None,
                                            y_udl=None, z_udl=None,
                                            internal_pressure=None,
                                            differential_temperature=None):
        self.create_geometric_property_code_UDL(number, x_udl, y_udl, z_udl)
        self.create_geometric_property_code_press(number, internal_pressure)
        self.create_geometric_property_code_temp(number,
                                                 differential_temperature)

    def create_geometric_property_code_UDL(self, number=0, x_udl=None,
                                           y_udl=None, z_udl=None):
        if x_udl is not None:
            if number == 0:
                number = len(self.geometric_property_code_UDLs) + 1
            self.geometric_property_code_UDLs.add_item(PUDL(number, 1,
                                                            x_udl))
        if y_udl is not None:
            if number == 0 or x_udl is not None:
                number = len(self.geometric_property_code_UDLs) + 1
            self.geometric_property_code_UDLs.add_item(PUDL(number, 2, y_udl))
        if z_udl is not None:
            if number == 0 or x_udl is not None or y_udl is not None:
                number = len(self.geometric_property_code_UDLs) + 1
            self.geometric_property_code_UDLs.add_item(PUDL(number, 3, z_udl))
        pass

    def create_geometric_property_code_press(self, number=0,
                                             internal_pressure=None):
        if internal_pressure is None:
            pass
        else:
            if number == 0:
                number = len(self.geometric_property_code_press) + 1
            self.geometric_property_code_press.add_item(
                PPRESS(number, internal_pressure))

    def create_geometric_property_code_temp(self, number=0,
                                            differential_temperature=None):
        if differential_temperature is None:
            pass
        else:
            if number == 0:
                number = len(self.geometric_property_code_temps) + 1
            self.geometric_property_code_temps.add_item(
                PTEMP(number, differential_temperature))

    def create_gravitational_constants(self, number=0, x_acceleration=0,
                                       y_acceleration=0, z_acceleration=0):
        if number == 0:
            number = len(self.gravitational_constants) + 1
        self.gravitational_constants.add_item(Grv(number, x_acceleration,
                                                  y_acceleration,
                                                  z_acceleration))

    def create_ambient_temperature_load(self, number=0, temperature=0):
        if number == 0:
            number = len(self.ambient_temperature_loads) + 1
        self.ambient_temperature_loads.add_item(AMBT(number, temperature))

    def _initialise_load_definition(self):
        self.date_created = datetime.datetime.now()
        self._create_empty_lists()
        self.write_L_file()

    def _read_load_definition(self):
        lp = LoadParser(self.path, self.name, self.extension)
        self.nodal_loads = lp.nodal_loads
        self.nodal_displacements = lp.nodal_displacements
        self.element_point_loads = lp.element_point_loads
        self.element_uniformly_distributed_loads = lp.element_uniformly_distributed_loads
        self.element_distributed_loads = lp.element_distributed_loads
        self.face_and_edge_loads = lp.face_and_edge_loads
        self.thermal_and_pressure_loads = lp.thermal_and_pressure_loads
        self.geometric_property_code_UDLs = lp.geometric_property_code_UDLs
        self.geometric_property_code_press = lp.geometric_property_code_press
        self.geometric_property_code_temps = lp.geometric_property_code_temps
        self.gravitational_constants = lp.gravitational_constants
        self.ambient_temperature_loads = lp.ambient_temperature_loads

    def _create_empty_lists(self):
        self.nodal_loads = LList()
        self.nodal_displacements = LList()
        self.element_point_loads = LList()
        self.element_uniformly_distributed_loads = LList()
        self.element_distributed_loads = LList()
        self.face_and_edge_loads = LList()
        self.thermal_and_pressure_loads = LList()
        self.geometric_property_code_UDLs = LList()
        self.geometric_property_code_press = LList()
        self.geometric_property_code_temps = LList()
        self.gravitational_constants = LList()
        self.ambient_temperature_loads = LList()

    def write_L_file(self):
        path = os.path.join(self.path, self.name + self.extension)
        with open(path, 'w+') as L:
            L.write('REFORMAT\n')
            L.writelines(nf.LFormat() for nf in self.nodal_loads)
            L.writelines(nd.LFormat() for nd in self.nodal_displacements)
            L.writelines(ep.LFormat() for ep in self.element_point_loads)
            L.writelines(udl.LFormat() for udl
                         in self.element_uniformly_distributed_loads)
            L.writelines(ed.LFormat() for ed in self.element_distributed_loads)
            L.writelines(fp.LFormat() for fp in self.face_and_edge_loads)
            L.writelines(tepr.LFormat() for tepr
                         in self.thermal_and_pressure_loads)
            L.writelines(pudl.LFormat() for pudl
                         in self.geometric_property_code_UDLs)
            L.writelines(ppress.LFormat() for ppress
                         in self.geometric_property_code_press)
            L.writelines(ptemp.LFormat() for ptemp
                         in self.geometric_property_code_temps)
            L.writelines(grv.LFormat() for grv in self.gravitational_constants)
            L.writelines(ambt.LFormat() for ambt
                         in self.ambient_temperature_loads)
