#!usr/local/bin/python

# -*- coding:utf-8 -*-


import os
import sys

import numpy as np
import matplotlib.pyplot as plt


band = 1, 2, 3, 4, 5, 6
sensor = "TM5"
spectra = "0095uuu"
bwlen = []


def bandpass(sensor, band):
    bandorta = np.array([[0.4825, 0.5650, 0.6600, 0.8250, 1.6500, 2.2150],
                         [0.4850, 0.5600, 0.6600, 0.8300, 1.6500, 2.2150]])
    platforms = {'TM5': 3, 'TM4': 2, 'TM7': 1}
    bands = ('spectral_b1.txt', 'spectral_b2.txt', 'spectral_b3.txt',
             'spectral_b4.txt', 'spectral_b5.txt', 'spectral_b7.txt')
    wlens, refl = np.loadtxt(os.path.join("spectra/manmade", '%s.txt' % spectra),
                             unpack=True, skiprows=26)
    refl /= 100  # Yansitimlari normalize ettik
    if sensor in platforms:
        for i in band:
            wlenr, resp = np.loadtxt((os.path.join("filtfunc", bands[i - 1])),
                                     unpack=True, usecols=(0, platforms[sensor]), skiprows=1)
            wlenr /= 1000
            indis = (wlens >= np.min(wlenr)) & (wlens <= np.max(wlenr))
            x = wlens[indis]  
            y = refl[indis]  
            refson = np.interp(wlenr, x, y)  
            pay = np.multiply(resp, refson)
            pay = np.sum(pay)
            payda = np.sum(resp)
            deger = pay / payda
            bwlen.append(deger)
        print "Degerler: \n %r" % bwlen
        if platforms[sensor] == 3:
            plt.xlim(min(bandorta[platforms[sensor] - 3] - 0.01),
                     max(bandorta[platforms[sensor] - 3] + 0.01))
            plt.title("Spektral Konvolusyon " + spectra + sensor)
            plt.plot(bandorta[platforms[sensor] - 3], bwlen)
            print "Bant Orta Degerleri: \n %r" % (bandorta[platforms[sensor] - 3])
        elif platforms[sensor] == 2 or platforms[sensor] == 1:
            plt.title("Spektral Konvolusyon " + spectra + sensor)
            plt.xlim(min(bandorta[platforms[sensor] - 2] - 0.01), max(bandorta[platforms[sensor] - 2] + 0.01))
            plt.plot(bandorta[platforms[sensor] - 2], bwlen)
            print "Bant Orta Degerleri: %r" % (bandorta[platforms[sensor] - 2])
        plt.ylabel("Yansitim")
        plt.xlabel("Dalga Boyu(mikrometre)")
        plt.show()
    else:
        sys.exit("Hatali Platform Secimi!")


bandpass(sensor, band)