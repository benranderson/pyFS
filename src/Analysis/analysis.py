from pyFS.Analysis.solution import Pile3DOptionFile
import os


class Analysis:

    def __init__(self, path, name, overwrite=False):
        self.path = path
        self.name = name
        self.options = {}

        if overwrite:
            self._reset_option_files()
        else:
            self._read_analysis_otions()

    def _reset_option_files(self):
        self._reset_pile_3d_options()

    def _reset_pile_3d_options(self):
        try:
            os.remove(os.path.join(self.path, self.name, 'upi'))
        except OSError:
            pass
        self.options['pile3d'] = Pile3DOptionFile()
        self.options['pile3d'].write()

    def _read_analysis_otions(self):
        self._read_pile_3d_options()

    def _read_pile_3d_options(self):
        try:
            with open(os.path.join(self.path, self.name, '.upi'), 'r') as o:
                opts = o.readlines()
                p3dof = Pile3DOptionFile(bool(opts[0]), bool(opts[1]),
                                         float(opts[2]), int(opts[3]),
                                         int(opts[4]), int(opts[5]),
                                         int(opts[6]), int(opts[7]),
                                         float(opts[8]))
        except FileNotFoundError:
            pass
