class Command():

    def __init__(self, args, has_trailing_slash=True):
        self.name = self.__class__.__name__
        self.arg = self._create_arg(args, has_trailing_slash)

    def _create_arg(self, args, has_trailing_slash):
        arg = '/'.join(map(str, args))
        if has_trailing_slash:
            arg += '/'
        return arg

    def __str__(self):
        return self.__class__.__name__

    def __repr__(self):
        return self.__str__()


class Winfram(Command):

    def __init__(self, *commands):
        Command.__init__(self, list(commands), has_trailing_slash=False)


class Modmerge(Command):

    def __init__(self, *commands):
        Command.__init__(self, list(commands))
