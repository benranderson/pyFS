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
