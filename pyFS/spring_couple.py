class SpringCouple:

    def __init__(self, number, N1, N2, rotation, reference_element,
                 spring_constant_table, CSYS):
        self.number = number
        self.N1 = N1
        self.N2 = N2
        self.rotation = rotation
        self.reference_element = reference_element
        self.spring_constant_table = spring_constant_table
        self.CSYS = CSYS

    def __repr__(self):
        return 'Spring/Couple Element {0} <N1 = {1}, N2 = {2}>'.format(
                                                 self.number, self.N1, self.N2)
