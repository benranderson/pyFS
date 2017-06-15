from .mdl import Node, BeamElement, SpringCouple, Restraint, MDLList
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

                elif split_line[0].lower() == 'gtab1':
                    number = split_line[1]
                    index = next((i for i, item in enumerate(self.geometries)
                                 if item.number == number), None)
                    if index is not None:
                        g = self.geometries[index]
                        g.type = int(split_line[2])
                        g.name = split_line[3]
                        g.designation = split_line[4]
                        g.graphics_type = split_line[5]
                        g.graphics_offset_y = split_line[6]
                        g.graphics_offset_z = split_line[7]
                    else:
                        self.geometries.add_item(
                            Geometry(number=number, type=int(split_line[2]),
                                     name=split_line[3],
                                     designation=split_line[4],
                                     graphics_type=split_line[5],
                                     graphics_offset_y=split_line[6],
                                     graphics_offset_z=split_line[7]))
