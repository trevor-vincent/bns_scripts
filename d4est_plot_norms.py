#!/scinet/niagara/software/2018a/opt/base/anaconda3/5.1.0/bin/python3
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.ticker import FormatStrFormatter
plt.gca().xaxis.set_major_formatter(FormatStrFormatter('%g'))
import csv
import sys
import numpy as np
from math import *
from scipy import stats

run_labels = []
files = []

if len(sys.argv) <= 3:
    print("d4est_plot_norm.py <norm_type> <num_runs> <file(s)> <run(s)>")
    exit

norm_type = sys.argv[1]
num_runs = int(sys.argv[2])
total_args = num_runs*2 + 2 + 1

if len(sys.argv) != total_args:
    print("len sys = " + str(len(sys.argv)))
    print("total_args = " +  str(total_args))
    print("num_runs = " + str(num_runs))
    print("len(sys.argv) != num_runs*2 + 2 + 1")
    print("d4est_plot_norm.py <norm_type> <num_runs> <file(s)> <run(s)>")
    exit

for i in range(0,num_runs):
    files.append(sys.argv[2 + i + 1])
    run_labels.append(sys.argv[2 + num_runs + i + 1])

for i in range(0,num_runs):

    dof = []
    dof_1o3 = []
    avg_deg = []
    linfty = []
    l2 = []
    energy = []
    estimator = []
    quad = []
    j = 0 
    print(files[i])
    with open(files[i], 'r',encoding='ascii') as f:
        reader = csv.reader(f, delimiter=' ')
        for row in reader:
            if j != 0 and j != 1:
                dof.append(float(row[1]))
                quad.append(float(row[0]))
                avg_deg.append((pow(dof[-1]/quad[-1],1./3.) - 1))
                l2.append(float(row[3]))
                dof_1o3.append(pow(dof[-1], 1./3.))
                linfty.append(float(row[4]))
                if norm_type != 'linfty_uniform':
                    energy.append(float(row[5]))
                    estimator.append(float(row[6]))
            j = j + 1
    if norm_type == 'l2':
        plt.plot(dof_1o3,l2,label=run_labels[i],linestyle=':', marker='o', markersize =5)
        plt.ylabel(r"$||u-u_h||_2$")
    elif norm_type == 'linfty' or norm_type == 'linfty_uniform':
        plt.plot(dof_1o3,linfty,label=run_labels[i],linestyle=':', marker='o', markersize =5)
        plt.ylabel(r"$||u-u_h||_\infty$")
    elif norm_type == 'estimator':
        plt.plot(dof_1o3,estimator,label=run_labels[i],linestyle=':', marker='o', markersize =5)
        plt.ylabel(r"$\eta$")
    else:
        print("not supported yet")
    

plt.tick_params(axis='both', which='both', labelsize=8)
plt.xlabel(r"DOF$^{1/3}$",fontsize=8)
plt.grid()
plt.legend(loc=0)
plt.yscale('log')
plt.savefig("figs.pdf",rasterizes=False)

