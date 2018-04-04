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
