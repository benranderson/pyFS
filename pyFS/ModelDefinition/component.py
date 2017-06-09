class Component:

    def __init__(self, number):
        self.number = number

    def __repr__(self):
        return '{0}: {1}'.format(self.__str__, self.number)


class Node(Component):

    def __init__(self, number, x_coord, y_coord, z_coord, CSYS=0):
        Component.__init__(self, number)
        self.x = x_coord
        self.y = y_coord
        self.z = z_coord
        self.CSYS = CSYS


class BeamElement(Component):

    def __init__(self, number, N1, N2, N3, rotation, geometry, material,
                 relZ, relY, taper, type, CO, bend_radius):
        Component.__init__(self, number)
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


class SpringCouple:

    def __init__(self, number, N1, N2, rotation, reference_element,
                 spring_constant_table, CSYS):
        Component.__init__(self, number)
        self.N1 = N1
        self.N2 = N2
        self.rotation = rotation
        self.reference_element = reference_element
        self.spring_constant_table = spring_constant_table
        self.CSYS = CSYS


