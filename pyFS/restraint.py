class Restraint:

    def __init__(self, Node, Tx, Ty, Tz, Rx, Ry, Rz):
        self.Node = Node
        self.Tx = Tx
        self.Ty = Ty
        self.Tz = Tz
        self.Rx = Rx
        self.Ry = Ry
        self.Rz = Rz

    def __repr__(self):
        return 'Restraint {0}'.format(self.Node)
