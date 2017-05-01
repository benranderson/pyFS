import datetime
import os
from winreg import *
import subprocess


class Model:

    def __init__(self, path, name):
        self.path = path
        self.name = name
        self.date_created = datetime.datetime.now()
        self.nodes = []
        self.beam_elements = []
        self._initialise_model()

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

    def _initialise_model(self):
        self._get_FS2000_install_directory()
        self._update_model_nam()
        self._update_batch_nam()
        self._create_model_files()

    def _create_model_files(self):
        self.write_MDL_file()
        winfram_path = os.path.join(self._install_directory,
                                    'system\winfram.exe')
        subprocess.call([winfram_path, 'I'])

    def write_MDL_file(self):
        path = os.path.join(self.path, self.name + '.mdl')
        with open(path, 'w') as MDL:
            MDL.writelines('N,' + n.number + ',' + n.x + ',' + n.y + ',' +
                           n.z + ',' + n.CSYS for n in self.nodes)
            MDL.writelines('E,' + e.number + ',' + e.N1 + ',' + e.N2 + ',' +
                           e.N3 + ',' + e.rotation + ',' + e.geometry + ',' +
                           e.material + ',' + e.relZ + ',' + e.relY + ',' +
                           e.taper + ',' + e.type + ',' + e.CO + ',' +
                           e.bend_radius for e in self.beam_elements)

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


class Node:

    def __init__(self, number, x_coord, y_coord, z_coord, CSYS=0):
        self.number = number
        self.x = x_coord
        self.y = y_coord
        self.z = z_coord
        self.CSYS = CSYS

    def __repr__(self):
        return 'Node {0} <{1}, {2}, {3}> CSYS={4}'.format(self.number, self.x,
                                                          self.y, self.z,
                                                          self.CSYS)


class BeamElement:

    def __init__(self, number, N1, N2, N3, rotation, geometry, material,
                 relZ, relY, taper, type, CO, bend_radius):
        self.number = number
        self.N1 = N1
        self.N2 = N2
        self.N3 = N3
        self.rotation = rotation
        self.geometry = geometry
        self.material = material
        self.relZ = relZ
        self.relY = relY
        self.taper = taper
        self.type = type
        self.CO = CO
        self.bend_radius = bend_radius

    def __repr__(self):
        return 'Beam Element {0} <N1 = {1}, N2 = {2}>'.format(self.number,
                                                              self.N1, self.N2)

if __name__ == "__main__":
    m = Model('C:\Dev\pyFS\Model', 'test model')
    for node in range(1, 12):
        m.create_node(node, node - 1, 0, 0, 0)
    for element in range(1, 11):
        m.create_beam_element(N1=element, N2=element + 1)

    print(m.nodes)
    print(m.beam_elements)
