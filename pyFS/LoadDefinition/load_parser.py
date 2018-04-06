from pyFS.LoadDefinition.l import (NL, ND, EP, UDL, ED, FP, TEPR, PUDL, PPRESS,
                                   PTEMP, Grv, AMBT, LList)
import os


class LoadParser:

    def __init__(self, path, name, extension):
        self.load = os.path.join(path, name + extension)
        self._create_empty_lists()
        self._read_load_file()
