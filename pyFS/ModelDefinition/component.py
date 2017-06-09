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


class SpringCouple(Component):

    def __init__(self, number, N1, N2, rotation, reference_element,
                 spring_constant_table, CSYS):
        Component.__init__(self, number)
        self.N1 = N1
        self.N2 = N2
        self.rotation = rotation
        self.reference_element = reference_element
        self.spring_constant_table = spring_constant_table
        self.CSYS = CSYS


class Restraint(Component):

    def __init__(self, number, Tx, Ty, Tz, Rx, Ry, Rz):
        Component.__init__(self, number)
        self.Tx = Tx
        self.Ty = Ty
        self.Tz = Tz
        self.Rx = Rx
        self.Ry = Ry
        self.Rz = Rz

class Geometry(Component):

    def __init__(self, code, type, name, designation, graphics_type,
                 graphics_offset_y, graphics_offset_z, pipe_OD, pipe_WT, area,
                 I_zz, I_yy, J, A_y, A_z, P_yy, G, S_1_y, S_1_z, S_2_y, S_2_z,
                 S_3_y, S_3_z, S_4_y, S_4_z, G_2, corrosion_allowance,
                 mill_tolerance, contents_density, insultation_thickness,
                 insulation_density, lining_thickness, lining_density):
        Component.__init__(self, number)
        self.type = type
        self.name = name
        self.designation = designation
        self.graphics_type = graphics_type
        self.graphics_offset_y = graphics_offset_y
        self.graphics_offset_z = graphics_offset_z
        self.pipe_OD = pipe_OD
        self.pipe_WT = pipe_WT
        self.area = area
        self.I_yy = I_yy
        self.I_zz = I_zz
        self.J = J
        self.A_y = A_y
        self.A_z = A_z
        self.P_yy = P_yy
        self.G = G
        self.S_1_y = S_1_y
        self.S_1_z = S_1_z
        self.S_2_y = S_2_y
        self.S_2_z = S_2_z
        self.S_3_y = S_3_y
        self.S_3_z = S_3_z
        self.S_4_y = S_4_y
        self.S_4_z = S_4_z
        self.G_2 = G_2
        self.corrosion_allowance = corrosion_allowance
        self.mill_tolerance = mill_tolerance
        self.contents_density = contents_density
        self.insultation_thickness = insulation_thickness
        self.insulation_density = insulation_density
        self.lining_thickness = lining_thickness
        self.lining_density = lining_density