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

file1 = sys.argv[1]
file2 = sys.argv[2]
num_points = 4
point_rows = []

for i in range(0,num_points):
    point_rows.append([])

p = 0
with open(file1, 'r',encoding='ascii') as f:
    reader = csv.reader(f, delimiter=' ')
    for row in reader:
        point_rows[p % num_points].append(row)
        p += 1
                
row_x = 0
row_y = 3

labels = ["(0,0,0)", "(3,0,0)", "(10,0,0)", "(100,0,0)"]
linestyles = ["-", ":", "--", "-."]
axes_labels = [r'\textbf{DOF}$^{1/3}$',"",r'$|u_i-u_{i+1}|$',r'$|u_i-u_{SpEC}|$']

m = -1
b = -1
low_err = -1
high_dof = -1
for p in range(0,num_points):
    x= []
    y = []
    z = []
    for i in range(0,len(point_rows[2])):
        xi = point_rows[p][i][row_x]
        yi = point_rows[p][i][row_y]
        print(xi,yi)
        x.append(float(xi)**(1./3.))
        y.append(float(yi))
        z.append(float(log(y[-1])))
        if p == 1:
            m,b = np.polyfit(x,z,1)
            low_err = y[-1]
            high_dof = x[-1]
    plt.plot(x,y,label=labels[p],color='black',linestyle=linestyles[p])


m = -1
b = -1
low_err = -1
high_dof = -1
for p in range(0,num_points):
    x= []
    y = []
    z = []
    for i in range(0,len(point_rows[2])):
        xi = point_rows[p][i][row_x]
        yi = point_rows[p][i][row_y]
        print(xi,yi)
        x.append(float(xi)**(1./3.))
        y.append(float(yi))
        z.append(float(log(y[-1])))
        if p == 1:
            m,b = np.polyfit(x,z,1)
            low_err = y[-1]
            high_dof = x[-1]
    plt.plot(x,y,label=labels[p],color='red',linestyle=linestyles[p],marker='o')



l = plt.legend(loc=0, prop={'size':13})
l.get_frame().set_edgecolor('black')
plt.yscale('log')
plt.tick_params(axis='both', which='major', labelsize=15)
plt.tick_params(axis='both', which='minor', labelsize=8)


plt.ylabel(axes_labels[row_y],fontsize=15)
plt.xlabel(axes_labels[row_x],fontsize=15)
plt.grid()
plt.tight_layout()
plt.savefig("points_compare" + str(high_dof) + "_" + str(m) + "_" + str(low_err) + ".pdf",rasterized=False)
