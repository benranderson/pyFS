class Geometry:

    def __init__(self, code, type, name, designation, graphics_type,
                 graphics_offset_y, graphics_offset_z, pipe_OD, pipe_WT, area,
                 I_zz, I_yy, J, A_y, A_z, P_yy, G, S_1_y, S_1_z, S_2_y, S_2_z,
                 S_3_y, S_3_z, S_4_y, S_4_z, G_2, corrosion_allowance,
                 mill_tolerance, contents_density, insultation_thickness,
                 insulation_density, lining_thickness, lining_density):

        self.code = code
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
