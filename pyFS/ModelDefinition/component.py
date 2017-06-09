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

