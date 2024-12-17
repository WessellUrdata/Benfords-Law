import numpy as np
import os
import pickle
from icecream import ic

from ImageForensics import FeatureExtraction


def main(args):
    dir_fake = args.fake_dir
    dir_real = args.real_dir
    N = args.features
    output_filename = args.output_filename + ".pkl"

    data = {}

    if not (os.path.isdir(dir_fake) and os.path.isdir(dir_real)):
        print("the specified directories do not exist")
        exit(0)

    # Collect all file paths
    fake_files = [
        os.path.join(subdir, file)
        for subdir, dirs, files in os.walk(dir_fake)
        for file in files
    ]
    real_files = [
        os.path.join(subdir, file)
        for subdir, dirs, files in os.walk(dir_real)
        for file in files
    ]

    extract = FeatureExtraction(features=N)

    psd1D_total_fake = extract.fft(fake_files)
    psd1D_total_real = extract.fft(real_files)

    # Remove None results if any files failed to process
    psd1D_total_fake = [result for result in psd1D_total_fake if result is not None]
    psd1D_total_real = [result for result in psd1D_total_real if result is not None]

    label_total_fake = np.zeros(len(psd1D_total_fake))
    label_total_real = np.ones(len(psd1D_total_real))

    psd1D_total_final = np.concatenate((psd1D_total_fake, psd1D_total_real), axis=0)
    label_total_final = np.concatenate((label_total_fake, label_total_real), axis=0)

    data["data"] = psd1D_total_final
    data["label"] = label_total_final
    data["N"] = N

    output = open(output_filename, "wb")
    pickle.dump(data, output)
    output.close()

    print("DATA Saved")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument("fake_dir", help="Directory where the fake images are stored")
    parser.add_argument("real_dir", help="Directory where the real images are stored")
    parser.add_argument("features", type=int, help="Number of features to extract")
    parser.add_argument("output_filename", help="Name of the output file")

    args = parser.parse_args()

    main(args)
