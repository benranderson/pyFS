from node import *
from beam_element import *
from model_parser import *
from spring_couple import *


import datetime
import os
from winreg import *
import subprocess


class Model:

    def __init__(self, path, name, initialise_model=False):
        self.path = path
        self.name = name
        self._initialise_app()
        if initialise_model:
            self._initialise_model()
            self.initialise_model()
        else:
            self._read_model()

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
            number == len(self.couples) + 1
        if N1 == 0:
            N1 = len(self.nodes) + 1
        if N2 == 0:
            N2 = N1 + 1
        self.couples.append(SpringCouple(number, N1, N2, rotation,
                                         reference_element,
                                         spring_constant_table, CSYS))

    def _initialise_model(self):
        self.date_created = datetime.datetime.now()
        self._create_empty_lists()

    def _read_model(self):
        mp = ModelParser(self.path, self.name)
        self.nodes = mp.nodes
        self.beam_elements = mp.beam_elements
        self.couples = []
        self.geometries = []
        self.couple_properties = []
        self.materials = []
        self.rc_tables = []
        self.restraints = []

    def _create_empty_lists(self):
        self.nodes = []
        self.beam_elements = []
        self.couples = []
        self.geometries = []
        self.couple_properties = []
        self.materials = []
        self.rc_tables = []
        self.restraints = []

    def _initialise_app(self):
        self._get_FS2000_install_directory()
        self._update_model_nam()
        self._update_batch_nam()

    def _create_model_files(self):
        self.write_MDL_file()
        self.initialise_model()

    def initialise_model(self):
        winfram_path = os.path.join(self._install_directory,
                                    'system\winfram.exe')
        subprocess.call([winfram_path, 'I'])

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
            MDL.writelines('SC' + str(sc.number) + ',' + str(sc.N1) + ',' +
                           str(sc.N2) + ',' + str(sc.rotation) + ',' +
                           str(sc.reference_element) + ',' +
                           str(sc.spring_constant_table) + ',' str(sc.CSYS)
                           for sc in self.couples)

    def _get_FS2000_install_directory(self):
        reg = ConnectRegistry(None, HKEY_LOCAL_MACHINE)
        key = OpenKey(reg, 'SOFTWARE\Wow6432Node\FS2000\Setup')
        self._install_directory = EnumValue(key, 0)[1]

    def _generate_nam_data(self):
        return '{0}\{1}\n{1}\n{0}'.format(self.path, self.name)

    def _update_model_nam(self):
        path = os.path.join(self._install_directory, 'model.nam')
        with open(path, 'w') as nam:
            nam.write(self._generate_nam_data())

    def _update_batch_nam(self):
        path = os.path.join(self._install_directory, 'batch.nam')
        with open(path, 'w') as nam:
            nam.write(self._generate_nam_data())

    def __repr__(self):
        return 'Model: {0}'.format(self.name)
