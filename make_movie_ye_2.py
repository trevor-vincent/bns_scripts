#!/usr/bin/python

import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import pylab as py
import os
import sys

pgf_with_rc_fonts = {"pgf.texsystem": "pdflatex"}
matplotlib.rcParams.update(pgf_with_rc_fonts)


from pylab import zeros,log10,linspace
from pylab import figure,clf,rcParams,FixedLocator,subplot,contourf,axis

# File options
filedir = "./"
outputdir = filedir
filepath = filedir+str(sys.argv[1])
SkipToStep = 0
FilePrefix = str(sys.argv[1])
Fscale = 1.
F0 = 0
colouraxis = zeros([100])
for i in range(0, 100):
    colouraxis[i] = 0 + i*0.5/99.
LegendTag = [0,0.1,0.2,0.3,0.4,0.5]
LegendName = "Ye"
#LegendName = "$Y_e$"
cmapname = 'inferno'
useLog = 0

# Plotting options
XMin = -180.
XMax = 180
YMin = -180
YMax = 180
bgcolor = 'black'

                                  
# Function calibrated for SliceData in SpEC                                                                                                                                   
def GetSliceDims(filename):
    f = open(filename,'r')
    Nx = 0
    Ny = 0
    ReadHeader = 0
    while True:
        line = f.readline()
        if line[0]=='#':
            if ReadHeader > 0:
                Ny = Ny+1
                break
            ReadHeader = 1
        else:
            str_input = line.split()
            if len(str_input)==4:
                Nx = Nx+1
            else:
                Ny = Ny+1
                Nx = 0
    f.close()
    f = open(filename,'r')
    Nt = 0
    Nc = 0
    for line in f:
        Nc = Nc+1
        if Nc == (Nx+1)*Ny :
            Nc = 0
            Nt = Nt+1
    return [Nt,Nx,Ny]

def GetNextSlice(f,Nx,Ny):
    mOutput = zeros([Ny,Nx,4])
    line = f.readline()
    while line[0]=='#':
        line = f.readline()
    for j in range(0,Ny):
        for i in range(0,Nx):
            str_input = line.split()
            if len(str_input)!=4:
                print("Bad format in GetNextSlice",line,j,i)
                break
            else:
                for k in range(0,4):
                    mOutput[j,i,k] = float(str_input[k])
            line = f.readline()
        # SpEC skips one line when indexing non-leading index
        if j<Ny-1:
            line = f.readline()
    if(len(line)>0):
        str_input = line.split()
        NextTime = float(str_input[1])
    else:
        NextTime = -1.
    return mOutput,NextTime


print("Get file dimensions")
Nt,Nx,Ny = GetSliceDims(filepath)
print(Nt,Nx,Ny)

# Plotting...
figure(figsize=(12,12))
clf()
# Set plot parameters to make beautiful plots
minorLocatorX   = FixedLocator(linspace(XMin,XMax,21))
minorLocatorY   = FixedLocator(linspace(YMin,YMax,21))
majorLocatorX   = FixedLocator(linspace(XMin,XMax,5))
majorLocatorY   = FixedLocator(linspace(XMin,XMax,5))
dX = (XMax-XMin)/4.
Xlab = ["%.0f"%XMin,"%.0f"%(XMin+dX),"%.0f"%(XMin+2*dX),"%.0f"%(XMin+3*dX),"%.0f"%XMax]
dY = (YMax-YMin)/4.
Ylab = ["%.0f"%YMin,"%.0f"%(YMin+dY),"%.0f"%(YMin+2*dY),"%.0f"%(YMin+3*dY),"%.0f"%YMax]

rcParams['figure.figsize']  = 12, 12
rcParams['lines.linewidth'] = 1.5
rcParams['font.family']     = 'serif'
rcParams['font.weight']     = 'bold'
rcParams['font.size']       = 30
rcParams['font.sans-serif'] = 'serif'
#rcParams['text.usetex']     = True
rcParams['axes.linewidth']  = 1.5
rcParams['axes.titlesize']  = 'medium'
rcParams['axes.labelsize']  = 'medium'
rcParams['xtick.major.size'] = 8
rcParams['xtick.minor.size'] = 4
rcParams['xtick.major.pad']  = 8
rcParams['xtick.minor.pad']  = 8
rcParams['xtick.color']      = bgcolor
rcParams['xtick.labelsize']  = 'medium'
rcParams['xtick.direction']  = 'in'
rcParams['ytick.major.size'] = 8
rcParams['ytick.minor.size'] = 4
rcParams['ytick.major.pad']  = 8
rcParams['ytick.minor.pad']  = 8
rcParams['ytick.color']      = bgcolor
rcParams['ytick.labelsize']  = 'medium'
rcParams['ytick.direction']  = 'in'
rcParams['axes.linewidth'] = 3

f = open(filepath,'r')
if SkipToStep>0:
    Nskip = SkipToStep*(Nx+1)*Ny
    Buff = [next(f) for x in range(Nskip)]

line = f.readline()
str_input = line.split()
NextTime = float(str_input[1])
for t in range(SkipToStep,Nt-1):
    LastTime = NextTime
    print("Stamp ",t," at time ",LastTime)
    mData,NextTime = GetNextSlice(f,Nx,Ny)
    while(NextTime <= LastTime):
        print("Skipping stamp ",t," at time ",NextTime)
        mDummy,NextTime = GetNextSlice(f,Nx,Ny)
        t = t+1

    X = mData[:,:,0]*1.475
    Y = mData[:,:,1]*1.475
    Z = mData[:,:,2]*1.475
    F = mData[:,:,3]*Fscale

    if str(sys.argv[3]) == "xz":
        X = mData[:,:,0]*1.475
        Y = mData[:,:,2]*1.475
    elif str(sys.argv[3]) == "xy":    
        X = mData[:,:,0]*1.475
        Y = mData[:,:,1]*1.475
    elif str(sys.argv[3]) == "yz":
        X = mData[:,:,1]*1.475
        Y = mData[:,:,2]*1.475        
    else:
        print("only xz and xy slices supported")
        exit

    
    fig, axes = plt.subplots(nrows=1, ncols=1)
    fig.set_size_inches((12,12))
    sp=subplot(111)
    if useLog == 1:
        im2 = contourf(X, Y, log10(F+F0), colouraxis,cmap=cmapname)
    else:
        im2 = contourf(X, Y, F+F0, colouraxis,cmap=cmapname)
    plt.xlabel("$X [km]$",fontsize=36,color=bgcolor)
    plt.ylabel("$Y [km]$",fontsize=36,color=bgcolor)

    dt = NextTime*0.00496
    titlestring = "t - $t_{\\rm merge}$ = %.02f ms" % (dt)
    plt.title(titlestring,fontsize=36,color=bgcolor)

    ax = plt.gca()
    ax.xaxis.set_major_locator(majorLocatorX)
    ax.xaxis.set_minor_locator(minorLocatorX)
    ax.xaxis.set_ticklabels(Xlab,fontsize=32,color=bgcolor)
    ax.xaxis.set_tick_params(which='minor', length=5, width=2)
    ax.xaxis.set_tick_params(which='major', width=3,length=10)
    ax.yaxis.set_major_locator(majorLocatorY)
    ax.yaxis.set_minor_locator(minorLocatorY)
    ax.yaxis.set_ticklabels(Ylab,fontsize=32,color=bgcolor)
    ax.yaxis.set_tick_params(which='minor', length=5, width=2)
    ax.yaxis.set_tick_params(which='major', width=3,length=10)

    axis([XMin, XMax, YMin, YMax])

    cbar_ax2 = fig.add_axes([0.88, 0.15, 0.03, 0.7])
    cbar2 = fig.colorbar(im2, ticks=LegendTag,cax=cbar_ax2)
    cbar2.set_label(label=LegendName,fontsize=36,color=bgcolor)
    outputname = outputdir+"/"+FilePrefix+"%04d"%t+".jpg"

    plt.subplots_adjust(left=0.15, bottom=0.15, top=0.85, right=0.85)
    plt.savefig(outputname)
    plt.close(fig)

cmd = "ffmpeg -f image2 -i "+outputdir+FilePrefix+"%04d.jpg -vf scale=720:720 -framerate 20 "+outputdir+FilePrefix+".mpg"
os.system(cmd)
