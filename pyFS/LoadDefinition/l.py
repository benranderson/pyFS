class Load:

    def __init__(self, number):
        self.number = number

    def __repr__(self):
        return '{0}: {1}'.format(self.__class__.__name__, self.number)

    def LFormat(self):
        return ''
