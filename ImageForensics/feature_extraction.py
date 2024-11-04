from functools import partial
from multiprocessing import Pool, cpu_count
import cv2
import numpy as np
import scipy as sp


# from radialProfile.py
def azimuthalAverage(image, center=None):
    """
    Calculate the azimuthally averaged radial profile.

    image - The 2D image
    center - The [x,y] pixel coordinates used as the center. The default is
             None, which then uses the center of the image (including
             fracitonal pixels).

    """
    # Calculate the indices from the image
    y, x = np.indices(image.shape)

    if not center:
        center = np.array([(x.max() - x.min()) / 2.0, (y.max() - y.min()) / 2.0])

    r = np.hypot(x - center[0], y - center[1])

    # Get sorted radii
    ind = np.argsort(r.flat)
    r_sorted = r.flat[ind]
    i_sorted = image.flat[ind]

    # Get the integer part of the radii (bin size = 1)
    r_int = r_sorted.astype(int)

    # Find all pixels that fall within each radial bin.
    deltar = r_int[1:] - r_int[:-1]  # Assumes all radii represented
    rind = np.where(deltar)[0]  # location of changed radius
    nr = rind[1:] - rind[:-1]  # number of radius bin

    # Cumulative sum to figure out sums for each radius bin
    csim = np.cumsum(i_sorted, dtype=float)
    tbin = csim[rind[1:]] - csim[rind[:-1]]

    radial_prof = tbin / nr

    return radial_prof


class FeatureExtraction:
    def __init__(self, features=100):
        self.features = features

    def fft_original(filename, N):
        img = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)

        # get the center 1/3 of the image
        height = int(img.shape[0] / 3)
        width = int(img.shape[1] / 3)
        img = img[height:-height, width:-width]

        # do FFT and shift zero frequency component to center
        frequencies = np.fft.fft2(img)
        frequencies_shifted = np.fft.fftshift(frequencies)

        # calculate magnitude spectrum
        magnitude_spectrum = np.abs(frequencies_shifted)

        # Calculate the azimuthally averaged 1D power spectrum
        psd1D = azimuthalAverage(magnitude_spectrum)

        points = np.linspace(0, N, num=psd1D.size)  # coordinates of points in psd1D
        xi = np.linspace(0, N, num=N)  # coordinates for interpolation

        interpolated = sp.griddata(points, psd1D, xi, method="cubic")

        return interpolated

    def fft_modified(self, filename):
        with Pool(processes=cpu_count()) as pool:
            return pool.map(partial(self.fft_modified_singlethread), filename)

    def fft_modified_singlethread(self, filename):
        img = cv2.imread(filename, 0)

        # we crop the center
        # height = int(img.shape[0] / 3)
        # width = int(img.shape[1] / 3)
        # img = img[height:-height, width:-width]

        # do FFT and shift zero frequency component to center
        frequencies = np.fft.fft2(img)
        # frequencies_shifted = np.fft.fftshift(frequencies)

        # calculate magnitude spectrum
        magnitude_spectrum = np.abs(frequencies)

        # Calculate the azimuthally averaged 1D power spectrum
        psd1D = azimuthalAverage(magnitude_spectrum)

        points = np.linspace(
            0, self.features, num=psd1D.size
        )  # coordinates of points in psd1D
        xi = np.linspace(
            0, self.features, num=self.features
        )  # coordinates for interpolation

        return np.interp(xi, points, psd1D)
