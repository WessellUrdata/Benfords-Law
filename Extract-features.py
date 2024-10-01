import cv2
import numpy as np
import numpy.matlib
import os
import radialProfile
import glob
from matplotlib import pyplot as plt
import pickle
from scipy.interpolate import griddata
import pylab as py
import rp
import sys

if(len(sys.argv) != 5):
        print("Not enough arguments")
        print("insert <dir> <features> <max_files> <output filename>")
        exit()

dir=sys.argv[1]

if os.path.isdir(dir) is False:
        print("this directory does not exist")
        exit(0)

N=int(sys.argv[2])
number_iter=int(sys.argv[3])
output_filename=str(sys.argv[4])+".pkl"

data= {}

y = []

psd1D_total = np.zeros([number_iter, N])
label_total = np.zeros([number_iter])
psd1D_org_mean = np.zeros(N)

cont = 0

#fake data
rootdir = dir+"/fake"

for subdir, dirs, files in os.walk(rootdir):

    for file in files:        
        filename = os.path.join(subdir, file)

        if filename==dir+"/fake"+"\desktop.ini":
            continue
       
        img = cv2.imread(filename,0)
        
        # we crop the center
        h = int(img.shape[0]/3)
        w = int(img.shape[1]/3)
        img = img[h:-h,w:-w] 


        f = np.fft.fft2(img)
        fshift = np.fft.fftshift(f)


        magnitude_spectrum = np.abs(fshift)
        psd1D = rp.radial_profile(magnitude_spectrum)
        
        points = np.linspace(0,N,num=psd1D.size) # coordinates of a
        xi = np.linspace(0,N,num=N) # coordinates for interpolation

        interpolated = griddata(points,psd1D,xi,method='cubic')
 
        psd1D_total[cont,:] = interpolated             
        label_total[cont] = 0
        cont+=1

        if cont == number_iter:
                break
    if cont == number_iter:
        break
            
for x in range(N):
    psd1D_org_mean[x] = np.mean(psd1D_total[:,x])

## real data
psd1D_total2 = np.zeros([number_iter, N])
label_total2 = np.zeros([number_iter])
psd1D_org_mean2 = np.zeros(N)

cont = 0

rootdir2=dir+"/real"

for subdir, dirs, files in os.walk(rootdir2):
    for file in files:        
 
        filename = os.path.join(subdir, file)
        parts = filename.split("/")

        if filename==dir+"/real"+"\desktop.ini":
            break
        
        img = cv2.imread(filename,0)
    
        # we crop the center
        h = int(img.shape[0]/3)
        w = int(img.shape[1]/3)
        img = img[h:-h,w:-w]

        f = np.fft.fft2(img)
        fshift = np.fft.fftshift(f)
        #fshift += epsilon
       

        magnitude_spectrum = np.abs(fshift)

        # Calculate the azimuthally averaged 1D power spectrum
        psd1D = rp.radial_profile(magnitude_spectrum)

        points = np.linspace(0,N,num=psd1D.size) # coordinates of a
        xi = np.linspace(0,N,num=N) # coordinates for interpolation

        interpolated = griddata(points,psd1D,xi,method='cubic')
        #interpolated /= interpolated[0]

        psd1D_total2[cont,:] = interpolated             
        label_total2[cont] = 1
        cont+=1
        

        #print(interpolated)

        if cont == number_iter:
            break
    if cont == number_iter:
        break



for x in range(N):
    psd1D_org_mean2[x] = np.mean(psd1D_total2[:,x])
 
y.append(psd1D_org_mean)
y.append(psd1D_org_mean2)


psd1D_total_final = np.concatenate((psd1D_total,psd1D_total2), axis=0)
label_total_final = np.concatenate((label_total,label_total2), axis=0)

data["data"] = psd1D_total_final
data["label"] = label_total_final


output = open(output_filename, 'wb')
pickle.dump(data, output)
output.close()

print("DATA Saved")

