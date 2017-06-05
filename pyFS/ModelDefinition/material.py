class Material():

    def __init__(self, code, E, G, mu, rho, alpha, yield_strength, name, UTS,
                 pipework_UTS, cold_allowable_stress, quality_factor,
                 pressure_coefficient, temperature_table):

        self.code = code
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

    def add_temperature_point(self, temperature, alpha, E, allowable_stress):

        self.temperature_table.append([temperature, alpha, E,
                                       allowable_stress])
