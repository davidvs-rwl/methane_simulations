from hapi import *
import os
import numpy as np
import pylab

# ==== Inputs ====
T       = 293  # K
P       = 1.0       # atm
xi      = 10000e-6  # mole fraction
L       = 3000      # cm
Species = 6
SpecStr = 'CH4'
Isotope = 1
dw      = 0.001
nu_min  = 4383
nu_max  = 4386

# ==== Extract HITRAN data ====
fetch(SpecStr, Species, Isotope, nu_min, nu_max)

nu, coefLow = absorptionCoefficient_Voigt(
    ((Species, Isotope),),
    SpecStr,
    Environment={'p': P, 'T': T},
    WavenumberStep=dw,
    HITRAN_units=False,
    GammaL='gamma_air'
)

a = coefLow * L * xi

# ==== Build filename per spec ====
T_str = f"{int(round(T)):03d}"

# Pressure: always keep one decimal place, replace '.' with '_'
P_fmt = f"{P:.1f}"
P_str = P_fmt.replace('.', '_')

# Path length: 4 digits, zero-padded
L_str = f"{int(round(L)):04d}"

# Mole fraction: in ppm, 5 digits, zero-padded
X_ppm = int(round(xi * 1e6))
X_str = f"{X_ppm:05d}"

filename = f"{T_str}-{P_str}-{L_str}-{X_str}.csv"

# ==== Save CSV ====
script_dir = os.path.dirname(os.path.abspath(__file__))
save_path = os.path.join(script_dir, filename)

np.savetxt(
    save_path,
    np.column_stack((nu, a)),
    delimiter=",",
    header="nu (cm^-1),absorbance",
    comments=""
)

print(f"Absorbance data saved to: {save_path}")

# ==== Plot (after saving) ====
pylab.figure(1)
pylab.plot(nu, a, 'k', label=f"T={T} K, P={P} atm, xi={X_ppm} ppm, L={L} cm")
pylab.legend(loc='upper left')
pylab.xlabel('Frequency, cm$^{-1}$')
pylab.ylabel('Absorbance')
pylab.tight_layout()
pylab.show()
