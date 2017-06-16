from .mdl import (MDLList, Node, BeamElement, SpringCouple, Restraint,
                  Geometry, Material)
import os


class ModelParser:

    def __init__(self, path, name):
        self.mdl = os.path.join(path, name + '.mdl')
        self._create_empty_lists()
        self._read_input_file()

    def _create_empty_lists(self):
        self.nodes = MDLList()
        self.beam_elements = MDLList()
        self.couples = MDLList()
        self.geometries = MDLList()
        self.couple_properties = MDLList()
        self.materials = MDLList()
        self.rc_tables = MDLList()
        self.restraints = MDLList()

    def _read_input_file(self):
        with open(self.mdl, 'r') as mdl:

            for line in mdl:
                split_line = line.rstrip().split(',')

                if split_line[0].lower() == 'n':
                    self.nodes.add_item(Node(int(split_line[1]),
                                             float(split_line[2]),
                                             float(split_line[3]),
                                             float(split_line[4]),
                                             int(split_line[5])))

                elif split_line[0].lower() == 'e':
                    self.beam_elements.add_item(BeamElement(
                                                    int(split_line[1]),
                                                    int(split_line[2]),
                                                    int(split_line[3]),
                                                    int(split_line[4]),
                                                    int(split_line[5]),
                                                    int(split_line[6]),
                                                    int(split_line[7]),
                                                    int(split_line[8]),
                                                    int(split_line[9]),
                                                    int(split_line[10]),
                                                    int(split_line[11]),
                                                    int(split_line[12]),
                                                    int(split_line[13])))

                elif split_line[0].lower() == 'sc':
                    self.couples.add_item(SpringCouple(int(split_line[1]),
                                                       int(split_line[2]),
                                                       int(split_line[3]),
                                                       int(split_line[4]),
                                                       int(split_line[5]),
                                                       int(split_line[6]),
                                                       int(split_line[7])))

                elif split_line[0].lower() == 'rest':
                    self.restraints.add_item(Restraint(
                                                int(split_line[1]),
                                                bool(int(split_line[2])),
                                                bool(int(split_line[3])),
                                                bool(int(split_line[4])),
                                                bool(int(split_line[5])),
                                                bool(int(split_line[6])),
                                                bool(int(split_line[7]))))

                elif (split_line[0].lower()[:-1] == 'gtab'):
                    self.read_GTAB(split_line)

                elif (split_line[0].lower() == 'mtab'):
                    self.materials.add_item(Material(int(split_line[1]),
                                                     float(split_line[1]),
                                                     float(split_line[1]),
                                                     float(split_line[1]),
                                                     float(split_line[1]),
                                                     float(split_line[1]),
                                                     split_line[1],
                                                     float(split_line[1])))

    def read_GTAB(self, split_line):
        attributes = [[['type', int], ['name', str], ['designation', int],
                       ['graphics_type', self.check_q_mark],
                       ['graphics_offset_y', float],
                       ['graphics_offset_z', float]],
                      [['pipe_OD', float], ['pipe_WT', float], ['area', float],
                       ['I_yy', float], ['I_zz', float], ['J', float]],
                      [['A_y', float], ['A_z', float], ['P_yy', float],
                       ['P_zz', float], ['G', float]],
                      [['S_1_y', float], ['S_1_z', float], ['S_2_y', float],
                       ['S_2_z', float]],
                      [['S_3_y', float], ['S_3_z', float], ['S_4_y', float],
                       ['S_4_z', float], ['G_2', float]],
                      [['corrosion_allowance', float],
                       ['mill_tolerance', float], ['contents_density', float],
                       ['insultation_thickness', float],
                       ['insulation_density', float],
                       ['lining_thickness', float], ['lining_density', float]]]
        number = int(split_line[1])
        index = next((i for i, item in enumerate(self.geometries)
                     if item.number == number), None)
        if index is not None:
            g = self.geometries[index]
        else:
            g = Geometry(number, 0, '', 0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                         0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                         0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                         0.0)
        if split_line[0].lower()[-1] == 'p':
            for index, [attribute, method] in enumerate(attributes[-1]):
                setattr(g, attribute, method(split_line[index + 2]))
        else:
            for index, [attribute, method] in enumerate(
                    attributes[int(split_line[0][-1])-1]):
                setattr(g, attribute, method(split_line[index + 2]))
        self.geometries.add_item(g)

    def check_q_mark(self, val):
        if not val.isnumeric():
            return 0
        else:
            return int(val)
