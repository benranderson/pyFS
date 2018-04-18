import matplotlib.pyplot as plt
import numpy as np

def natural_wavelength(E, I, delta_f, W_sub):
    return (72*E*I*delta_f/W_sub)**(1/4)

def foundation_profile(x, delta_f, L_o):
    return delta_f*(x/L_o)**3*(4-3*x/L_o)

if __name__ == "__main__":
    E = 2.07e11
    I = 1.689e-05
    delta_f = 0.5
    W_sub = 19.7084

    L_o = natural_wavelength(E, I, delta_f, W_sub)
    print(L_o)

    xs = np.arange(L_o)
    w_fs = [foundation_profile(x, delta_f, L_o) for x in xs]
    
    fig, ax = plt.subplots(figsize=(5, 3))
    ax.scatter(x=xs, y=w_fs, marker='.')
    ax.set_title(f'Foundation Profile, L_o = {L_o:.2f} m')
    ax.set_xlabel('x [m]')
    ax.set_ylabel('Foundation Profile [m]')
    fig.tight_layout()

    plt.show()

