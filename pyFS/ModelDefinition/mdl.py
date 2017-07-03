class Component:

    def __init__(self, number):
        self.number = number

    def __repr__(self):
        return '{0}: {1}'.format(self.__class__.__name__, self.number)

    def MDLFormat(self):
        return ''


class Node(Component):

    def __init__(self, number, x_coord, y_coord, z_coord, CSYS=0):
        Component.__init__(self, number)
        self.x = x_coord
        self.y = y_coord
        self.z = z_coord
        self.CSYS = CSYS

    def MDLFormat(self):
        return ('N,' + str(self.number) + ',' + str(self.x) + ',' +
                str(self.y) + ',' + str(self.z) + ',' + str(self.CSYS) + '\n')


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

    def MDLFormat(self):
        return ('E,' + str(self.number) + ',' + str(self.N1) + ',' +
                str(self.N2) + ',' + str(self.N3) + ',' + str(self.rotation) +
                ',' + str(self.geometry) + ',' + str(self.material) + ',' +
                str(self.relZ) + ',' + str(self.relY) + ',' + str(self.taper) +
                ',' + str(self.type) + ',' + str(self.CO) + ',' +
                str(self.bend_radius) + '\n')


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

    def MDLFormat(self):
        return ('SC,' + str(self.number) + ',' + str(self.N1) + ',' +
                str(self.N2) + ',' + str(self.rotation) + ',' +
                str(self.reference_element) + ',' +
                str(self.spring_constant_table) + ',' + str(self.CSYS) + '\n')


class Restraint(Component):

    def __init__(self, number, Tx, Ty, Tz, Rx, Ry, Rz):
        Component.__init__(self, number)
        self.Tx = Tx
        self.Ty = Ty
        self.Tz = Tz
        self.Rx = Rx
        self.Ry = Ry
        self.Rz = Rz

    def MDLFormat(self):
        return ('REST,' + str(self.number) + ',' + str(int(self.Tx)) + ',' +
                str(int(self.Ty)) + ',' + str(int(self.Tz)) + ',' +
                str(int(self.Rx)) + ',' + str(int(self.Ry)) + ',' +
                str(int(self.Rz)) + '\n')


class Geometry(Component):

    def __init__(self, number, type, name, designation, graphics_type,
                 graphics_offset_y, graphics_offset_z, pipe_OD, pipe_WT, area,
                 I_zz, I_yy, J, A_y, A_z, P_yy, P_zz, G, S_1_y, S_1_z, S_2_y,
                 S_2_z, S_3_y, S_3_z, S_4_y, S_4_z, G_2, corrosion_allowance,
                 mill_tolerance, contents_density, insulation_thickness,
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
        self.P_zz = P_zz
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
        self.insulation_thickness = insulation_thickness
        self.insulation_density = insulation_density
        self.lining_thickness = lining_thickness
        self.lining_density = lining_density

    def MDLFormat(self):
        return ('GTAB1,' + str(self.number) + ',' + str(self.type) + ',' +
                self.name + ',' + str(self.designation) + ',' +
                str(self.graphics_type) + ',' + str(self.graphics_offset_y) +
                ',' + str(self.graphics_offset_z) + '\n' +
                'GTAB2,' + str(self.number) + ',' + str(self.pipe_OD) + ',' +
                str(self.pipe_WT) + ',' + str(self.area) + ',' +
                str(self.I_yy) + ',' + str(self.I_zz) + ',' + str(self.J) +
                '\n' +
                'GTAB3,' + str(self.number) + ',' + str(self.A_y) + ',' +
                str(self.A_z) + ',' + str(self.P_yy) + ',' + str(self.P_zz) +
                ',' + str(self.G) + '\n' +
                'GTAB4,' + str(self.number) + ',' + str(self.S_1_y) + ',' +
                str(self.S_1_z) + ',' + str(self.S_2_y) + ',' +
                str(self.S_2_z) + '\n' +
                'GTAB5,' + str(self.number) + ',' + str(self.S_3_y) + ',' +
                str(self.S_3_z) + ',' + str(self.S_4_y) + ',' +
                str(self.S_4_z) + ',' + str(self.G_2) + '\n' +
                'GTABP,' + str(self.number) + ',' +
                str(self.corrosion_allowance) + ',' +
                str(self.mill_tolerance) + ',' + str(self.contents_density) +
                ',' + str(self.insulation_thickness) + ',' +
                str(self.insulation_density) + ',' +
                str(self.lining_thickness) + ',' + str(self.lining_density) +
                '\n')


class Material(Component):

    def __init__(self, number, E, G, mu, rho, alpha, yield_strength, name, UTS,
                 pipework_UTS, cold_allowable_stress, quality_factor,
                 pressure_coefficient, temperature_table):
        Component.__init__(self, number)
        self.E = E
        Self.G = G
        self.mu = mu
        self.rho = rho
        self.alpha = alpha
        self.yield_strength = yield_strength
        self.name = name
        self.UTS = UTS
        self.pipework_UTS = pipework_UTS
        self.cold_allowable_stress = cold_allowable_stress
        self.quality_factor = quality_factor
        self.pressure_coefficient = pressure_coefficient
        self.temperature_table = temperature_table

    def MDLFormat(self):
        pass

    def add_temperature_point(self, temperature, alpha, E, allowable_stress):

        self.temperature_table.append([temperature, alpha, E,
                                       allowable_stress])


class SpringTable(Component):

    def __init__(self, number, K1, K2, K3, K4, K5, K6, type, CO):
        Component.__init__(self, number)
        self.K1 = K1
        self.K2 = K2
        self.K3 = K3
        self.K4 = K4
        self.K5 = K5
        self.K6 = K6
        self.type = type
        self.CO = CO


class RCTable(Component):

    def __init__(number, rc_points):
        Component.__init__(self, number)
        self.rc_points = rc_points


class ICTable(Component):

    def __init__(self, number, IC0, IC1, IC2, IC3, IC4, IC5, IC6):
        Component.__init__(self, number)
        self.IC0 = IC0
        self.IC1 = IC1
        self.IC2 = IC2
        self.IC3 = IC3
        self.IC4 = IC4
        self.IC5 = IC5
        self.IC6 = IC6


class MDLList(list):

    def __init__(self, data=[]):
        list.__init__(self, data)

    def __getslice__(self, i, j):
        return MDLList(list.__getslice__(self, i, j))

    def __add__(self, other):
        return MDLList(list.__add__(self, other))

    def __mul__(self, other):
        return MDLList(list.__mul__(self, other))

    def __getitem__(self, item):
        result = list.__getitem__(self, item)
        try:
            return MDLList(result)
        except TypeError:
            return result

    def add_item(self, new_item):
        index = next((i for i, item in enumerate(self)
                      if item.number == new_item.number), None)
        if index is not None:
            self[index] = new_item
        else:
            self.append(new_item)

class Point:

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
