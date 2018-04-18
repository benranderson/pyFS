from math import pi, sin, tan, exp, sqrt
import numpy as np
from scipy.interpolate import interp1d

def Tu(D, H, c, f, psi, gamma):
    psi = psi * 2 * pi / 360    
    alpha = 0.608-0.123*c-0.274/(c**2+1)+0.695/(c**3+1)
    K0 = 1 - sin(psi)    
    return (pi * D * alpha * c + pi * D * H * gamma * (1 + K0) / 2 * tan(f * psi))

def Delta_t(soil):
    delta_ts = {
        'dense sand': 0.003,
        'loose sand': 0.005,
        'stiff clay': 0.008,
        'soft clay': 0.01,
    }
    return delta_ts.get(soil, ValueError('Unknown soil type.'))

def Nch(c, H, D):

    if c > 0:
        x = H / D
        return min(6.752 + 0.065 * x - 11.063 / (x + 1)**2 + 7.119 /
                   (x + 1)**3, 9)
    else:
        return 0

def Nqh(psi, H, D):

    if psi > 0:
        if psi < 20:
            psi = 20
        elif psi > 45:
            psi = 45
        psi_range = [20, 25, 30, 35, 40, 45]
        a = [2.399, 3.332, 4.565, 6.816, 10.959, 17.658]
        b = [0.439, 0.839, 1.234, 2.019, 1.783, 3.309]
        c = [-0.03, -0.09, -0.089, -0.146, 0.045, 0.048]
        d = [1.059*10**-3, 5.606*10**-3, 4.275*10**-3,
             7.651*10**-3, -5.425*10**-3, -6.443*10**-3]
        e = [-1.754*10**-5, -1.319*10**-4, -9.159*10**-5,
             -1.683*10**-4, -1.153*10**-4, -1.299*10**-4]
        x = H / D
        def par(case):
            return interp1d(psi_range, case)(psi)

        return (par(a) + par(b) * x + par(c) * x**2 + par(d) * x**3 +
                par(e) * x**4)
    else:
        return 0

def Pu(c, H, D, psi, gamma):    
    return Nch(c, H, D) * c * D + Nqh(psi, H, D) * gamma * H * D
    
def Delta_p(H, D):    
    return min(0.04 * (H + D / 2), 0.15 * D)

def Ncv(c, H, D):
    
    if c > 0:
        return min(2 * H / D, 10)
    else:
        return 0

def Nq(psi):

    psi = psi * 2 * pi / 360
    return exp(pi * tan(psi)) * tan(pi / 4 + psi / 2)**2

def Nqv(psi, H, D):
    
    if psi > 0:
        return min(psi * H / 44 / D, Nq(psi))
    else:
        return 0

def Qu(psi, c, D, gamma, H):
    
    return Ncv(c, H, D) * c * D + Nqv(psi, H, D) * gamma * H * D

def Delta_qu(soil, H, D):
    if 'sand' in soil:
        return min(0.02 * H, 0.1 * D)
    elif 'clay' in soil:
        return min(0.2 * H, 0.2 * D)
    else:
        raise ValueError('Unknown soil type.')
        
def cot(a):
    
    return 1 / tan(a)

def Nc(psi):

    psi = psi * 2 * pi / 360
    return (cot(psi + 0.001) * (exp(pi * tan(psi + 0.001)) * tan(pi / 4 + (psi + 0.001) / 2)**2 - 1))

def Ngamma(psi):
    return exp(0.18 * psi - 2.5)

def Qd(psi, c, D, gamma, H):
    
    return (Nc(psi) * c * D + Nq(psi) * gamma * H * D + Ngamma(psi) * (gamma + (1000 * 9.81)) * D**2 / 2)

def Delta_qd(soil):
    if 'sand' in soil:
        return 0.1 * D
    elif 'clay' in soil:
        return 0.2 * D
    else:
        raise ValueError('Unknown soil type.')

def DepthEquilibrium(psi, c, D, gamma, soil):
    R = D / 2
    widths = [w for w in np.arange(D / 6, D + 0.1 * D / 6, D / 6)]
    penetrations = [R - sqrt(R**2 - (w / 2)**2) for w in widths]
    Qds = [Qd(psi, c, w, gamma, 0) for w in widths]
    p_max = 5 * D
    F_max = p_max / Delta_qd(soil) * Qds[-1]
    penetrations.append(p_max)
    Qds.append(F_max)
    Fd = np.stack((penetrations, Qds), axis=-1)
    return Fd
        
    
if __name__ == '__main__':
    D = 0.4572
    c = 0
    f = 0.6
    psi = 45
    gamma = 11000
    
    print(DepthEquilibrium(psi, c, D, gamma, 'dense sand'))
    
    with open('soil_stiffnesses.out', 'w') as o:
    
        for b in np.arange(0.5, 4.5, 0.5):
            _H = b + D / 2
            _Tu = Tu(D, _H, c, f, psi, gamma)
            _Delta_t = Delta_t('dense sand')
            o.write('Burial: ' + str(b) + 'm' +
                    '\tTu: ' + str(round(_Tu, 0)) + ' N/m' +
                    '\t\tDelta_t: ' + str(round(_Delta_t,3)) + ' m' +
                    '\tKt: ' + str(round(_Tu / _Delta_t,0)) + ' N/m/m\n')

        o.write('\n\n')
        for b in np.arange(0.5, 4.5, 0.5):
            _H = b + D / 2
            _Pu = Pu(c, _H, D, psi, gamma)
            _Delta_p = Delta_p(_H, D)
            o.write('Burial: ' + str(b) + 'm' +
                    '\tPu: ' + str(round(_Pu, 0)) + ' N/m' +
                    '\t\tDelta_p: ' + str(round(_Delta_p,3)) + ' m' +
                    '\tKp: ' + str(round(_Pu / _Delta_p,0)) + ' N/m/m\n')

        o.write('\n\n')
        for b in np.arange(0.5, 4.5, 0.5):
            _H = b + D / 2
            _Qu = Qu(psi, c, D, gamma, _H)
            _Delta_qu = Delta_qu('dense sand', _H, D)
            o.write('Burial: ' + str(b) + 'm' +
                    '\tQu: ' + str(round(_Qu, 0)) + ' N/m' +
                    '\t\tDelta_qu: ' + str(round(_Delta_qu,3)) + ' m' +
                    '\tKqu: ' + str(round(_Qu / _Delta_qu,0)) + ' N/m/m\n')

        o.write('\n\n')
        for b in np.arange(0.5, 4.5, 0.5):
            _H = b + D / 2
            _Qd = Qd(psi, c, D, gamma, _H)
            _Delta_qd = Delta_qd('dense sand')
            o.write('Burial: ' + str(b) + 'm' +
                    '\tQd: ' + str(round(_Qd, 0)) + ' N/m' +
                    '\t\tDelta_qd: ' + str(round(_Delta_qd,3)) + ' m' +
                    '\tKqd: ' + str(round(_Qd / _Delta_qd,0)) + ' N/m/\n')

        o.write('\n\n')
        psi = 33
        gamma = 9000    
        for b in np.arange(0.5, 4.5, 0.5):
            _H = b + D / 2
            _Qd = Qd(psi, c, D, gamma, _H)
            _Delta_qd = Delta_qd('dense sand')
            o.write('Burial: ' + str(b) + 'm' +
                    '\tQd: ' + str(round(_Qd, 0)) + ' N/m' +
                    '\t\tDelta_qd: ' + str(round(_Delta_qd,3)) + ' m' +
                    '\tKqd: ' + str(round(_Qd / _Delta_qd,0)) + ' N/m/m\n')

        o.write('\n\n')
        psi = 30
        c = 210
        gamma = 9000
        for b in np.arange(0.5, 4.5, 0.5):
            _H = b + D / 2
            _Qd = Qd(psi, c, D, gamma, _H)
            _Delta_qd = Delta_qd('soft clay')
            o.write('Burial: ' + str(b) + 'm' +
                    '\tQd: ' + str(round(_Qd, 0)) + ' N/m' +
                    '\t\tDelta_qd: ' + str(round(_Delta_qd,3)) + ' m' +
                    '\tKqd: ' + str(round(_Qd / _Delta_qd,0)) + ' N/m/m\n')

        o.write('\n\n')
        psi = 25
        c = 3000
        gamma = 8000
        for b in np.arange(0.5, 4.5, 0.5):
            _H = b + D / 2
            _Qd = Qd(psi, c, D, gamma, _H)
            _Delta_qd = Delta_qd('soft clay')
            o.write('Burial: ' + str(b) + 'm' +
                    '\tQd: ' + str(round(_Qd, 0)) + ' N/m' +
                    '\t\tDelta_qd: ' + str(round(_Delta_qd,3)) + ' m' +
                    '\tKqd: ' + str(round(_Qd / _Delta_qd,0)) + ' N/m/m\n')