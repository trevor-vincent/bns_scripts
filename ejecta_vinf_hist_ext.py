#!/usr/bin/python

import matplotlib
import matplotlib as mpl
import matplotlib.pyplot as plt
import csv
import numpy as np
import io
from math import *
import math
import sys

pgf_with_rc_fonts = {"pgf.texsystem": "pdflatex"}
matplotlib.rcParams.update(pgf_with_rc_fonts)

#plt.rc('text', usetex=False)
#plt.rc('font', family='serif')
plt.rcParams["figure.facecolor"] = "white"
plt.rcParams["axes.facecolor"] = "white"
plt.rcParams["savefig.facecolor"] = "white"
file = 'ParticlesFromOutFlowCat.dat'
log_elems = []
mgfcg_iter = []
fcg_iter = []

# [1] Time 
# [2] Particle mass 
# [3-5] Coords
# [6] Rho0Phys
# [7] Ye
# [8] Temp
# [9] Minusu_t
# [10] Minusu_tH
# [11-13] vInertial
Rho = []
Ye = []
Minusu_tH = []
unb_E = []
v_inf = []

ejecta_type = sys.argv[1]
theta_type = sys.argv[2]
theta_max = float(sys.argv[3])


with io.open(file, mode='r',encoding='utf-8') as f:
    reader = csv.reader(f, delimiter=' ')
    for row in reader:
        Minusu_tH.append(float(row[9]))
        if Minusu_tH[-1] > 1.:
            Rho.append(float(row[5]))
            unb_E.append(Rho[-1]*(Minusu_tH[-1] - 1))
            A = unb_E[-1]
            B = Rho[-1]
            if theta_max >= 0:
                if ejecta_type != "left_grid_only":
                    print("if theta_max >= 0, ejecta must be on_grid_only and not " + str(ejecta_type))
                    sys.exit()
                x = float(row[2])
                y = float(row[3])
                z = float(row[4])
                r = sqrt(x**2 + y**2 + z**2)
                theta = acos(z/r)
                if theta_type == "polar" and (theta < math.radians(theta_max) or theta > math.radians(180 - theta_max)):
                    v_inf.append(sqrt(1-1/(1+A/B)/(1+A/B)))
                elif theta_type == "equatorial" and (theta > math.radians(theta_max) and theta < math.radians(180 - theta_max)):
                    v_inf.append(sqrt(1-1/(1+A/B)/(1+A/B)))
            else:
                v_inf.append(sqrt(1-1/(1+A/B)/(1+A/B)))
        
# [2] = A[B lt   0.050000000]
# [3] = A[B lt    0.10000000]
# [4] = A[B lt    0.15000000]
# [5] = A[B lt    0.20000000]
# [6] = A[B lt    0.25000000]
# [7] = A[B lt    0.30000000]
# [8] = A[B lt    0.35000000]
# [9] = A[B lt    0.40000000]
# [10] = A[B lt    0.45000000]
# [11] = A[B lt    0.50000000]
# [12] = A[B lt    0.55000000]
# [13] = A[B lt    0.60000000]
# [14] = A[B lt    0.65000000]
# [15] = A[B lt    0.70000000]
# [16] = A[B lt    0.75000000]
# [17] = A[B lt    0.80000000]
# [18] = A[B lt    0.85000000]
# [19] = A[B lt    0.90000000]
# [20] = A[B lt    0.95000000]
# [21] = A[B gt   9.4999999999999996e-01]

vinf_bins = np.arange(0.05,1.05,0.05)
vinf_bin_values = np.zeros(len(vinf_bins))
print(vinf_bin_values)

for i in range(0,len(v_inf)):
    for j in range(0,len(vinf_bins)):
        if v_inf[i] <= vinf_bins[j]:
            vinf_bin_values[j] += 1
            break

rows = []
with io.open("VinfBin.agr", mode='r', encoding='utf-8') as f:
    reader = csv.reader(f, delimiter=' ')
    for row in reader:
        #print(row)
        rows.append(row)
        #time.append(float(row[0]))

y = []
for i in rows[-1]:
    if str(i) != "":
        y.append(float(i))

y.pop(0)
#print(y)

if ejecta_type == "left_grid_only":
    print("ejecta_type = left_grid_only")
elif ejecta_type == "on_grid_only":
    print("ejecta_type = on_grid_only")
else:
    print("ejecta_type = combined")

for j in range(0,len(vinf_bins)):
    if ejecta_type == "left_grid_only":
        vinf_bin_values[j] *= 1e-8
    elif ejecta_type == "on_grid_only":
        vinf_bin_values[j] = y[j]
    else:
        vinf_bin_values[j] *= 1e-8                   
        vinf_bin_values[j] += y[j]

fig, ax = plt.subplots()
index = np.arange(20)
print(index)
plt.bar(index, vinf_bin_values)

vinf_bin_strings = []

for i in range(0,len(vinf_bins)):
    vinf_bin_strings.append('{:.2f}'.format(vinf_bins[i]))

print(vinf_bin_strings)
ax.set_xticks(index)
ax.set_xticklabels(vinf_bin_strings)

for label in  ax.xaxis.get_ticklabels()[::2]:
    label.set_visible(False)

ax.set_yscale('log')

plt.xlabel(r"$v_\infty$",fontsize=15)
plt.ylabel(r'Unbound Mass $(M_\odot)$',fontsize=15)
plt.savefig("vinf_hist_" + str(ejecta_type) + "_" + str(theta_max) + "_" + sys.argv[2] + ".pdf",rasterized=False)

total_mass = 0.
f = open("vinf_hist_" + str(ejecta_type) + "_" + str(theta_max) + "_" + sys.argv[2] + ".dat","w+")
for j in range(0,len(vinf_bin_values)):
    f.write(str(vinf_bins[j]) + " " + str(vinf_bin_values[j]) + "\n")
    total_mass = total_mass + vinf_bin_values[j]
f1 = open("vinf_hist_" + str(ejecta_type) + "_" + str(theta_max) + "_" + sys.argv[2] + " " + str(total_mass) + ".dat","w+")
f1.write("\n")
