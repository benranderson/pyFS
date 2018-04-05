class Load:

    def __init__(self, number):
        self.number = number

    def __repr__(self):
        return '{0}: {1}'.format(self.__class__.__name__, self.number)

    def LFormat(self):
        return ''


class NL(Load):

    def __init__(self, number, node, x_force, y_force, z_force, x_moment,
                 y_moment, z_moment, conc_mass):
        Load.__init__(self, number)
        self.node = node
        self.Fx = x_force
        self.Fy = y_force
        self.Fz = z_force
        self.Mx = x_moment
        self.My = y_moment
        self.Mz = z_moment
        self.NMass = conc_mass

    def LFormat(self):
        return ('NF,' + str(self.node) + ',' + str(self.Fx) + ','
                + str(self.Fy) + ',' + str(self.Fz) + ',' + str(self.Mx) + ','
                + str(self.My) + ',' + str(self.Mz) + ',' + str(self.NMass)
                + '\n')


class ND(Load):

    def __init__(self, number, node, x_disp, y_disp, z_disp, x_rot, y_rot,
                 z_rot):
        Load.__init__(self, number)
        self.node = node
        self.Tx = x_disp
        self.Ty = y_disp
        self.Tz = z_disp
        self.Rx = x_rot
        self.Ry = y_rot
        self.Rz = z_rot

    def LFormat(self):
        return ('ND,' + str(self.node) + ',' + str(self.Tx) + ','
                + str(self.Ty) + ',' + str(self.Tz) + ',' + str(self.Rx) + ','
                + str(self.Ry) + ',' + str(self.Rz) + '\n')


class EP(Load):

    def __init__(self, number, element, coord, length, x_force, y_force,
                 z_force, x_moment, y_moment, z_moment):
        Load.__init__(self, number)
        self.element = element
        self.coord = coord
        self.length = length
        self.Fx = x_force
        self.Fy = y_force
        self.Fz = z_force
        self.Mx = x_moment
        self.My = y_moment
        self.Mz = z_moment

    def LFormat(self):
        return ('EP,' + str(self.element) + ',' + str(self.coord) + ','
                + str(self.length) + ',' + str(self.Fx) + ',' + str(self.Fy)
                + ',' + str(self.Fz) + ',' + str(self.Mx) + ',' + str(self.My)
                + ',' + str(self.Mz) + '\n')


class UDL(Load):

    def __init__(self, number, element, x_force, y_force, z_force):
        Load.__init__(self, number)
        self.element = element
        self.UDX = x_force
        self.UDY = y_force
        self.UDZ = z_force

    def LFormat(self):
        return ('UDL,' + str(self.element) + ',' + str(self.UDX) + ','
                + str(self.UDY) + ',' + str(self.UDZ) + '\n')


class ED(Load):

    def __init__(self, number, element, coord, s_length, f_length, s_x_force,
                 f_x_force, s_y_force, f_y_force, s_z_force, f_z_force):
        Load.__init__(self, number)
        self.element = element
        self.coord = coord
        self.SLength = s_length
        self.FLength = f_length
        self.GDX1 = s_x_force
        self.GDX2 = f_x_force
        self.GDY1 = s_y_force
        self.GDY2 = f_y_force
        self.GDZ1 = s_z_force
        self.GDZ2 = f_z_force

    def LFormat(self):
        return ('ED,' + str(self.element) + ',' + str(self.coord) + ','
                + str(self.SLength) + ',' + str(self.FLength) + ','
                + str(self.GDX1) + ',' + str(self.GDX2) + ',' + str(self.GDY1)
                + ',' + str(self.GDY2) + ',' + str(self.GDZ1) + ','
                + str(self.GDZ2) + '\n')


class FP(Load):

    def __init__(self, number, element, face, direction, p1, p2, p3, p4):
        Load.__init__(self, number)
        self.element = element
        self.face = face
        self.dir = direction
        self.P1 = p1
        self.P2 = p2
        self.P3 = p3
        self.P4 = p4

    def LFormat(self):
        return ('FP,' + str(self.element) + ',' + str(self.face) + ','
                + str(self.dir) + ',' + str(self.P1) + ',' + str(self.P2) + ','
                + str(self.P3) + ',' + str(self.P4) + '\n')


class TEPR(Load):

    def __init__(self, number, element, temperature, press_pi, temp_ls,
                 press_po):
        Load.__init__(self, number)
        self.element = element
        self.TEMP1 = temperature
        self.PRESS1 = press_pi
        self.TEMP2 = temp_ls
        self.PRESS2 = press_po

    def LFormat(self):
        return ('TEPR,' + str(self.element) + ',' + str(self.TEMP1) + ','
                + str(self.PRESS1) + ',' + str(self.TEMP2) + ','
                + str(self.PRESS2) + '\n')


class PUDL(Load):

    def __init__(self, number, geometric_code, load_direction, load_magnitude):
        Load.__init__(self, number)
        self.code = geometric_code
        self.dir = load_direction
        self.load = load_magnitude

    def LFormat(self):
        return ('PUDL,' + str(self.code) + ',' + str(self.dir) + ','
                + str(self.load) + '\n')


class PPRESS(Load):

    def __init__(self, number, geometric_code, internal_pressure):
        Load.__init__(self, number)
        self.code = geometric_code
        self.press = internal_pressure

    def LFormat(self):
        return ('PPRESS,' + str(self.code) + ',' + str(self.press) + '\n')


class PTEMP(Load):

    def __init__(self, number, geometric_code, differential_temperature):
        Load.__init__(self, number)
        self.code = geometric_code
        self.temp = differential_temperature

    def LFormat(self):
        return ('PTEMP,' + str(self.code) + ',' + str(self.temp) + '\n')


class AMBT(Load):

    def __init__(self, number, temperature):
        Load.__init__(self, number)
        self.ambient_temperature = temperature

    def LFormat(self):
        return ('AMBT,' + str(self.ambient_temperature) + '\n')


class LList(list):

    def __init__(self, data=[]):
        list.__init__(self, data)

    def __add__(self, other):
        return list.__add__(self, other)

    def __mul__(self, other):
        return list.__mul__(self, other)

    def __getitem__(self, key):
        return list.__getitem__(self, key)

    def __setitem__(self, key, value):
        return list.__setitem__(self, key, value)

    def __delitem__(self, key):
        return list.__delitem__(self, key)

    def add_item(self, new_item):
        index = next((i for i, item in enumerate(self)
                      if item.number == new_item.number), None)
        if index is not None:
            self[index] = new_item
        else:
            self.append(new_item)
