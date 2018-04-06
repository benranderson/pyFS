from pyFS.LoadDefinition.l import (NF, ND, EP, UDL, ED, FP, TEPR, PUDL, PPRESS,
                                   PTEMP, Grv, AMBT, LList)
import os


class LoadParser:

    def __init__(self, path, name, extension):
        self.load = os.path.join(path, name + extension)
        self._create_empty_lists()
        self._read_load_file()

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

    def _read_load_file(self):
        with open(self.load, 'r') as load:

            for line in load:
                split_line = line.rstrip().split(',')

                if split_line[0].lower() == 'nf':
                    self.nodal_loads.add_item(NF(int(split_line[1]),
                                                 float(split_line[2]),
                                                 float(split_line[3]),
                                                 float(split_line[4]),
                                                 float(split_line[5]),
                                                 float(split_line[6]),
                                                 float(split_line[7]),
                                                 float(split_line[8])))

                elif split_line[0].lower() == 'nd':
                    self.nodal_displacements.add_item(ND(int(split_line[1]),
                                                         float(split_line[2]),
                                                         float(split_line[3]),
                                                         float(split_line[4]),
                                                         float(split_line[5]),
                                                         float(split_line[6]),
                                                         float(split_line[7])))

                elif split_line[0].lower() == 'ep':
                    self.element_point_loads.add_item(EP(int(split_line[1]),
                                                         int(split_line[2]),
                                                         float(split_line[3]),
                                                         float(split_line[4]),
                                                         float(split_line[5]),
                                                         float(split_line[6]),
                                                         float(split_line[7]),
                                                         float(split_line[8]),
                                                         float(split_line[9])))

                elif split_line[0].lower() == 'udl':
                    self.element_uniformly_distributed_loads.add_item(UDL(
                        int(split_line[1]),
                        float(split_line[2]),
                        float(split_line[3]),
                        float(split_line[4])))

                elif split_line[0].lower() == 'ed':
                    self.element_distributed_loads.add_item(ED(
                        int(split_line[1]),
                        int(split_line[2]),
                        float(split_line[3]),
                        float(split_line[4]),
                        float(split_line[5]),
                        float(split_line[6]),
                        float(split_line[7]),
                        float(split_line[8]),
                        float(split_line[9]),
                        float(split_line[10])))

                elif split_line[0].lower() == 'fp':
                    self.face_and_edge_loads.add_item(FP(int(split_line[1]),
                                                         int(split_line[2]),
                                                         int(split_line[3]),
                                                         float(split_line[4]),
                                                         float(split_line[5]),
                                                         float(split_line[6]),
                                                         float(split_line[7])))

                elif split_line[0].lower() == 'tepr':
                    self.thermal_and_pressure_loads.add_item(TEPR(
                        int(split_line[1]),
                        float(split_line[2]),
                        float(split_line[3]),
                        float(split_line[4]),
                        float(split_line[5])))

                elif split_line[0].lower() == 'pudl':
                    self.geometric_property_code_UDLs.add_item(PUDL(
                        int(split_line[1]),
                        int(split_line[2]),
                        float(split_line[3])
                    ))

                elif split_line[0].lower() == 'ppress':
                    self.geometric_property_code_press.add_item(PPRESS(
                        int(split_line[1]),
                        float(split_line[2])))

                elif split_line[0].lower() == 'ptemp':
                    self.geometric_property_code_temps.add_item(PTEMP(
                        int(split_line[1]),
                        float(split_line[2])))

                elif split_line[0].lower() == 'accel':
                    self.gravitational_constants.add_item(Grv(
                        float(split_line[1]),
                        float(split_line[2]),
                        float(split_line[3])))

                elif split_line[0].lower == 'ambt':
                    self.ambient_temperature_loads.add_item(AMBT(
                        float(split_line[1])))
