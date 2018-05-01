import os


class DynoflexOptionFile():

    def __init__(self, number):
        self.number = number


class Pile3DOptionFile():

    def __init__(self, p_delta=False, plasticity=False, tol=0.005,
                 max_iter=100, load_steps=5, soln_opt=1, conv_criteria=1,
                 soft_springs=1e-6):
        self.p_delta = p_delta
        self.plasticity = plasticity
        self.tol = tol
        self.max_iter = max_iter
        self.load_steps = load_steps
        self.soln_opt = soln_opt
        self.conv_criteria = conv_criteria
        self.soft_springs = soft_springs

    def write(self, path, name):
        with open(os.path.join(path, name, '.upi'), 'w') as o:
            o.write(f'{int(self.p_delta)}\n{int(self.plasticity)}\n{self.tol}' +
                    f'\n{self.max_iter}\n{self.load_steps}\n{self.soln_opt}\n' +
                    f'{self.conv_criteria}\n{self.soft_springs}')
