from pyFS.node import *
from pyFS.beam_element import *
from pyFS.model_parser import *
from pyFS.spring_couple import *

import os


class ModelParser:

    def __init__(self, path, name):
        self.mdl = os.path.join(path, name + '.mdl')
        self._create_empty_lists()
        self._read_input_file()

    def _create_empty_lists(self):
        self.nodes = []
        self.beam_elements = []
        self.couples = []
        self.geometries = []
        self.couple_properties = []
        self.materials = []
        self.rc_tables = []
        self.restraints = []

    def _read_input_file(self):
        with open(self.mdl, 'r') as mdl:

            for line in mdl:
                split_line = line.split(',')

                if split_line[0].lower() == 'n':
                    self.nodes.append(Node(int(split_line[1]),
                                           float(split_line[2]),
                                           float(split_line[3]),
                                           float(split_line[4]),
                                           int(split_line[5])))

                elif split_line[0].lower() == 'e':
                    self.beam_elements.append(BeamElement(int(split_line[1]),
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
                    self.couples.append(SpringCouple(int(split_line[1]),
                                                     int(split_line[2]),
                                                     int(split_line[3]),
                                                     int(split_line[4]),
                                                     int(split_line[5]),
                                                     int(split_line[6]),
                                                     int(split_line[7])))
