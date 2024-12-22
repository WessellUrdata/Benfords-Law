from functools import partial
from multiprocessing import Pool, cpu_count

import cv2
import numpy as np
import scipy.interpolate
from tqdm import tqdm


def azimuthalAverage(magnitude_spectrum: np.ndarray) -> np.ndarray:
    # Calculate the indices from the image
    y, x = np.indices(magnitude_spectrum.shape)

    center_y, center_x = ((i - 1) / 2 for i in magnitude_spectrum.shape)

    r = np.hypot(y - center_y, x - center_x)

    # Get the integer part of the radii (bin size = 1)
    r_int = r.astype(int)

    # Calculate the mean for each radius bin
    tbin = np.bincount(r_int.ravel(), magnitude_spectrum.ravel())
    nr = np.bincount(r_int.ravel())

    radial_prof = tbin / nr

    return radial_prof


class FeatureExtraction:
    @staticmethod
    def fft(
        filename: str,
        features: int = 300,
        crop: bool = True,
    ) -> list[float]:
        img = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)
        height, width = img.shape

        if crop:
            # we crop the center
            height = height // 3
            width = width // 3
            img = img[height:-height, width:-width]

        # do FFT
        frequencies = np.fft.fft2(img)
        # shift zero frequency component to center
        # not doing frequency shift will slightly negatively impact accuracy
        frequencies = np.fft.fftshift(frequencies)

        # calculate magnitude spectrum
        magnitude_spectrum = np.abs(frequencies)

        # Calculate the azimuthally averaged 1D power spectrum
        psd1D = azimuthalAverage(magnitude_spectrum)

        # if the extracted features isn't enough, interpolate them
        if psd1D.size < features:
            points = np.linspace(
                0, features, num=psd1D.size
            )  # coordinates of points in psd1D
            xi = np.linspace(0, features, num=features)  # coordinates for interpolation

            interpolated = scipy.interpolate.griddata(points, psd1D, xi, method="cubic")

            return interpolated

        else:
            return psd1D

    @staticmethod
    def multithread_fft(filenames: list[str], **kwargs) -> list[list[float]]:
        with Pool(processes=cpu_count()) as pool:
            results = list(
                tqdm(
                    pool.imap(partial(FeatureExtraction.fft, **kwargs), filenames),
                    total=len(filenames),
                    desc="Performing Feature Extraction",
                )
            )
        return results
